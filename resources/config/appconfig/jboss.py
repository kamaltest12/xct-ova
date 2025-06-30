import logging
import json
import requests
from requests.auth import HTTPDigestAuth
import hiyapyco
import yaml
import copy
import time
import common_func
import os
import shutil
import subprocess

logger = logging.getLogger('app_config_tool.jboss')
# logger.propagate = False

def send_json(jboss_mgmt_url, json_payload,restart=None):
    response = requests.post(jboss_mgmt_url, json=json_payload, auth=HTTPDigestAuth(app_user, app_user_password))
    if response.status_code != 200:
        # print response.json()['failure-description']
        if "Duplicate resource" in response.json()['failure-description']:
            print response.json()['failure-description']
            logger.debug("Duplicate resource found")
            return "duplicate"
        elif "not found" in response.json()['failure-description']:
            logger.debug("Specified resource not found")
            return "n/a"
        else:
            logger.error("JSON response returned an %s error" % response.status_code)
            logger.error("Failure details: %s " % response.json()['failure-description'])     
            logger.error("Detailed response %s" % response.json())
            exit(1)      
    else:
        try:
            if response.json()['result'] is not None:
                return response.json()['result']
        except:
            return response.json()['outcome']

def config_jdbc(yaml_jdbc_config,config_prefix,jboss_mgmt_url):

    # Add jdbc-driver, remove if exists
    for drivers in yaml_jdbc_config['oracle']:
        for jdbc_driver in drivers:
            for driver_details in drivers[jdbc_driver]:
                if 'driver_module' in driver_details:
                    driver_module_name = driver_details['driver_module']
                    logger.debug("Driver name: %s" % driver_module_name)
                if 'driver_xa_class' in driver_details:
                    driver_module_xa_class = driver_details['driver_xa_class']  
                    logger.debug("XA class name: %s" % driver_module_xa_class)
                if 'datasources' in driver_details:
                    for datasource in driver_details['datasources']:
                        for datasource_details in datasource:
                            # print datasource[datasource_details]
                            datasource_name = datasource_details
                            for datasource_conn_param in datasource[datasource_details]:                            
                                if 'xa_enabled' in datasource_conn_param:
                                    ds_xa_enabled = datasource_conn_param['xa_enabled']
                            if ds_xa_enabled:
                                ds_config_path = "xa-data-source"
                            else:
                                ds_config_path = "data-source"
                            address = []             
                            if config_prefix is not None:
                                address = copy.deepcopy(config_prefix)
                            address.extend(("subsystem","datasources",ds_config_path, datasource_name))
                            if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address}):
                                logger.info("resource %s already exists, removing data-source first before removing linked jdbc driver %s" % (datasource_name,jdbc_driver))                                                       
                                send_json(jboss_mgmt_url,{"operation":"remove","address":address})                                
        # Set correct prefix path(domain/standalone)
        address = []
        if config_prefix is not None:
            address = copy.deepcopy(config_prefix)
        address.extend(("subsystem","datasources","jdbc-driver", jdbc_driver))
        # (Re)Create the jdbc-driver
        if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address}):
            logger.info("resource %s already exists, removing jdbc-driver first" % jdbc_driver)
            send_json(jboss_mgmt_url,{"operation":"remove","address":address})
        logger.info("Creating jdbc driver: %s" % jdbc_driver)
        send_json(jboss_mgmt_url,{"operation":"add", "driver-name":jdbc_driver,"driver-module-name":driver_module_name,"driver-xa-datasource-class-name":driver_module_xa_class, "address":address})

    # Creating datasources
    for drivers in yaml_jdbc_config['oracle']:
        for jdbc_driver in drivers:
            for driver_details in drivers[jdbc_driver]:
                if 'driver_module' in driver_details:
                    driver_module_name = driver_details['driver_module']
                    logger.debug("Driver name: %s" % driver_module_name)
                if 'driver_xa_class' in driver_details:
                    driver_module_xa_class = driver_details['driver_xa_class']  
                    logger.debug("XA class name: %s" % driver_module_xa_class)
                if 'datasources' in driver_details:
                    for datasource in driver_details['datasources']:
                        for datasource_details in datasource:
                            # print datasource[datasource_details]
                            datasource_name = datasource_details
                            for datasource_conn_param in datasource[datasource_details]:
                                if 'xa_enabled' in datasource_conn_param:
                                    ds_xa_enabled = datasource_conn_param['xa_enabled']
                                    logger.debug(ds_xa_enabled)
                                if 'jdbc_url' in datasource_conn_param:
                                    ds_jdbc_url = datasource_conn_param['jdbc_url']
                                    logger.debug(ds_jdbc_url)
                                if 'db_hostname' in datasource_conn_param:
                                    ds_db_hostname = datasource_conn_param['db_hostname']
                                    logger.debug(ds_db_hostname)
                                if 'db_port' in datasource_conn_param:
                                    ds_db_port = datasource_conn_param['db_port']
                                    logger.debug(ds_db_port)
                                if 'db_sid' in datasource_conn_param:
                                    ds_db_sid = datasource_conn_param['db_sid']
                                    logger.debug(ds_db_sid)
                                if 'db_user' in datasource_conn_param:
                                    ds_db_user = datasource_conn_param['db_user']
                                    logger.debug(ds_db_user)
                                if 'db_password' in datasource_conn_param:
                                    ds_db_password = datasource_conn_param['db_password']
                                    logger.debug(ds_db_password)  
                                if 'jndi_name' in datasource_conn_param:
                                    ds_jndi_name = datasource_conn_param['jndi_name']
                                    logger.debug(ds_jndi_name)
                         
                            # Set correct prefix path(domain/standalone)                                
                            address = []
                            if config_prefix is not None:
                                address = copy.deepcopy(config_prefix)
                            address.extend(("subsystem","datasources"))
                            logger.info("Creating datasource : %s" % datasource_name)   
                            if ds_xa_enabled:
                                address.extend(("xa-data-source", datasource_name))
                                send_json(jboss_mgmt_url,{"operation":"add", "driver-name":jdbc_driver, "jndi-name":"java:/jdbc/"+ds_jndi_name, "user-name":ds_db_user, "password":ds_db_password,"enabled": "true", "address":address})
                                address.extend(("xa-datasource-properties",  "ServerName"))
                                send_json(jboss_mgmt_url,{"operation":"add", "value":ds_db_hostname,"address":address})  
                                address.pop()
                                address.append("PortNumber")
                                send_json(jboss_mgmt_url,{"operation":"add", "value":ds_db_port,"address":address})
                                address.pop()
                                address.append("DatabaseName")
                                send_json(jboss_mgmt_url,{"operation":"add", "value":ds_db_sid,"address":address})
                                address.pop()
                                address.append("URL")
                                send_json(jboss_mgmt_url,{"operation":"add", "value":ds_jdbc_url+ds_db_hostname+":"+ds_db_port+":"+ds_db_sid,"address":address})
                            else:
                                address.extend(("data-source", datasource_name))
                                send_json(jboss_mgmt_url,{"operation":"add", "connection-url": ds_jdbc_url+ds_db_hostname+":"+ds_db_port+":"+ds_db_sid, "driver-name":jdbc_driver, "jndi-name":"java:/jdbc/"+ds_jndi_name, "user-name":ds_db_user, "password":ds_db_password,"enabled": "true", "address":address})                                

def config_jaas(yaml_jdbc_config,config_prefix,jboss_mgmt_url):
    

    for domains in yaml_jdbc_config['jboss']:
        for sec_domain in domains:
            for login_modules in domains[sec_domain]:
                for login_module in login_modules:
                    address = []             
                    if config_prefix is not None:
                        address = copy.deepcopy(config_prefix)
                    address.extend(("subsystem","security","security-domain", sec_domain, "authentication","classic","login-module"))
                    for login_module_details in login_modules[login_module]:
                        address.append(login_module)
                        if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address}):
                            logger.info("resource %s already exists, removing login-module first" % login_module)
                            send_json(jboss_mgmt_url,{"operation":"remove","address":address})
                        address.pop()
            address = []
            if config_prefix is not None:
                address = copy.deepcopy(config_prefix)
            address.extend(("subsystem","security","security-domain", sec_domain))
            if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address}):
                logger.info("resource %s already exists, removing securirty domain first" % sec_domain)
                send_json(jboss_mgmt_url,{"operation":"remove","address":address})    
            logger.info("Adding security domain %s" % sec_domain)
            send_json(jboss_mgmt_url,{"operation":"add","cache-type":"default", "address":address})
            address.extend(("authentication", "classic"))  
            send_json(jboss_mgmt_url,{"operation":"add","cache-type":"default", "address":address})

    for domains in yaml_jdbc_config['jboss']:
        for sec_domain in domains:
            for login_modules in domains[sec_domain]:
                for login_module in login_modules:
                    address = []
                    login_module_options = {}          
                    if config_prefix is not None:
                        address = copy.deepcopy(config_prefix)
                    address.extend(("subsystem","security","security-domain", sec_domain, "authentication","classic","login-module"))
                    login_module_details = login_modules[login_module]
                    # address.append(login_module)
                    # logger.info("Creating login-module %s" % login_module)
                    # send_json(jboss_mgmt_url,{"operation":"add","code":login_module_details['code'],"flag":"required","module-options" "address":address})
                    # print login_module_details[]['code']
                    for login_module_details in login_modules[login_module]:
                        # print login_module_details
                        if 'code' in login_module_details:
                            login_class = login_module_details['code']
                        if 'module_options' in login_module_details:
                            for options in login_module_details['module_options']:
                                for key,value in options.iteritems():
                                    login_module_options[key]=value
                    address.append(login_module)
                    logger.info("Creating login-module %s" % login_module)
                    send_json(jboss_mgmt_url,{"operation":"add","code":login_class,"flag":"required","address":address})
                    send_json(jboss_mgmt_url,{"operation":"write-attribute","name":"module-options","value":login_module_options,"address":address})
                    

def config_properties(yaml_jdbc_config,config_prefix,jboss_mgmt_url):

    address = []
    address.append("system-property")  

    for prop in yaml_jdbc_config['jboss']:
            for prop_key in prop:
                logger.info("Adding system property %s with value %s" % (prop_key, prop[prop_key]))
                address.append(prop_key)
                if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address}):
                    logger.info("System property already exists, removing first")
                    send_json(jboss_mgmt_url,{"operation":"remove","address":address})
                send_json(jboss_mgmt_url,{"operation":"add","value":prop[prop_key], "address":address})
                address.pop()

def config_mq(yaml_jdbc_config,config_prefix,jboss_mgmt_url):

    address_prefix = []
    address = []
    if config_prefix is not None:
        address_prefix = copy.deepcopy(config_prefix)
    address = copy.deepcopy(address_prefix)
    # Create path for-adapter subsystem
    address.extend(("subsystem","resource-adapters"))
    # Create path for naming subsystem
    address_naming = copy.deepcopy(address_prefix)
    address_naming.extend(("subsystem","naming","binding"))
    # Create apth for ejb subsystem 
    address_ejb = copy.deepcopy(address_prefix)
    address_ejb.extend(("subsystem","ejb3"))

    enabled_queues = yaml_jdbc_config['queues']['enabled']
    enabled_queue_list = list()

    for queue in enabled_queues:
        enabled_queue_list.append(queue)
    
    try:
        excluded_queues = yaml_jdbc_config['queues']['excluded']
    except KeyError, e:
        excluded_queues = []
    merged_queues = sorted(set(enabled_queue_list) - set(excluded_queues))
    for resource_adapters in yaml_jdbc_config['provider']['mq']:
        for resource_adapter in resource_adapters:
            rar_prop = dict()

            for resource_adapter_details in resource_adapters[resource_adapter]:
                # print resource_adapter_details
                if 'default_rar' in resource_adapter_details:
                    rar_default = resource_adapter_details['default_rar']
                    # print rar_default
                    # print rar_jndi_name
                if 'jndi-name' in resource_adapter_details:
                    rar_jndi_name = resource_adapter_details['jndi-name']
                    # print rar_jndi_name
                if 'class-name' in resource_adapter_details:
                    rar_class_name = resource_adapter_details['class-name']
                    # print rar_class_name
                if 'use-java-context' in resource_adapter_details:
                    rar_java_context = resource_adapter_details['use-java-context']
                    # print rar_java_context
                if 'use-ccm' in resource_adapter_details:
                    rar_ccm = resource_adapter_details['use-ccm']
                    # print rar_ccm
                if 'config-properties' in resource_adapter_details:
                    rar_config_props = resource_adapter_details['config-properties']  
                    # print rar_config_props
                    for properties in rar_config_props:
                        for prop in properties:
                            rar_prop[prop]= properties[prop]
            address_rar = copy.deepcopy(address)
            address_rar.extend(("resource-adapter",resource_adapter))
            address_queue = copy.deepcopy(address_rar)
            address_queue.append("admin-objects")
            # Removing queues if exist
            logger.info("Checking if queues exists, if so remove those")
            for queue in merged_queues:
                address_queue.append(queue)
                address_naming.append("java:jboss/exported/jms/"+queue)
                logger.info("Check if queue %s already exists" % queue)
                if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address_naming}):
                    logger.info("Binding for queue %s already exists, removing first" % queue)
                    send_json(jboss_mgmt_url,{"operation":"remove","address":address_naming})   
                logger.info("Check if bindings already exists for queue %s" % queue)
                if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address_queue}):
                    logger.info("Queue %s already exists, removing first" % queue)
                    send_json(jboss_mgmt_url,{"operation":"remove","address":address_queue})
                address_queue.pop()
                address_naming.pop()

            for qcf in [rar_jndi_name,rar_jndi_name.lower()]:
                for binding_path in ["java:jboss/exported/jms/", "java:/jms/"]:
                    address_naming.append(binding_path+qcf)
                    if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address_naming}):
                        logger.info("Binding for QCF %s already exists, removing first" % qcf)
                        send_json(jboss_mgmt_url,{"operation":"remove","address":address_naming}) 
                    address_naming.pop()

            # Remove rar if exists
            if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address_rar}):
                 logger.info("RAR %s already exists, removing first" % resource_adapter)
                 send_json(jboss_mgmt_url,{"operation":"remove","address":address_rar})   

            # Restart the server before creating the rar,queues bindings again
            logger.info("Restarting the jvm to activate the config changes")                  
            if config_prefix is None:
                send_json(jboss_mgmt_url,{"operation":"reload"})
                time.sleep(5)
            else:
                for host in send_json(jboss_mgmt_url,{"operation":"read-children-names","child-type":"host"}):
                    # Check if host is not a DC, if so skip it
                    if not send_json(jboss_mgmt_url,{"operation":"read-attribute","name":"master", "address":["host",host]}):
                        logger.info("Reload config on host %s" % host)
                        send_json(jboss_mgmt_url,{"operation":"reload","address":["host",host]})
                time.sleep(20)

            # Add RAR and properties
            logger.info("Creating resource adapter")
            send_json(jboss_mgmt_url,{"operation":"add","archive":resource_adapter,"transaction-support":"XATransaction","address":address_rar})
            address_rar.extend(("connection-definitions",rar_jndi_name.lower()))
            logger.info("Adding connection definitions resource adapter")
            send_json(jboss_mgmt_url,{"operation":"add","class-name":rar_class_name,"jndi-name":"java:jboss/jms/"+rar_jndi_name,"use-java-context":rar_java_context,"use-ccm":rar_ccm,"address":address_rar})
            logger.info("Adding config properties to connection definitions")
            address_rar.extend(("config-properties","port"))
            send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['port'],"address":address_rar})
            address_rar.pop()
            address_rar.append("hostName")
            send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['hostname'],"address":address_rar})
            address_rar.pop()
            address_rar.append("username")
            send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['username'],"address":address_rar})
            address_rar.pop()          
            address_rar.append("password")
            send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['password'],"address":address_rar})
            address_rar.pop()   
            address_rar.append("channel")
            send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['channel'],"address":address_rar})
            address_rar.pop()   
            address_rar.append("transportType")
            send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['transporttype'],"address":address_rar})
            address_rar.pop()                           
            address_rar.append("queueManager")
            send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['queuemanager'],"address":address_rar})
            address_rar.pop() 

            #Recreating the queues
            logger.info("Creating queues")
            for queue in merged_queues:
                logger.info("Adding queue %s to resource adapter %s" % (queue, resource_adapter))
                address_queue.append(queue)
                send_json(jboss_mgmt_url,{"operation":"add","class-name":"com.ibm.mq.connector.outbound.MQQueueProxy","jndi-name":"java:/jms/"+queue ,"address":address_queue})
                address_queue.extend(("config-properties","baseQueueName"))
                send_json(jboss_mgmt_url,{"operation":"add","value":queue,"address":address_queue})
                address_queue.pop()
                address_queue.append("baseQueueManagerName")
                send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['queuemanager'],"address":address_queue})

                # Add binding for queue
                binding_queue="java:jboss/exported/jms/"+queue
                address_naming.append(binding_queue)
                logger.info("Adding binding for queue %s" % queue)
                send_json(jboss_mgmt_url,{"operation":"add","binding-type":"lookup","lookup":"java:/jms/"+queue, "address":address_naming})
                address_naming.pop()
                del address_queue[-3:]
            # Create the QCF bindings again
            for qcf in [rar_jndi_name,rar_jndi_name.lower()]:
                for binding_path in ["java:jboss/exported/jms/", "java:/jms/"]:
                    address_naming.append(binding_path+qcf)
                    logger.info("Adding QCF binding %s for %s" % (qcf,binding_path))
                    send_json(jboss_mgmt_url,{"operation":"add","binding-type":"lookup","lookup":"java:jboss/jms/"+rar_jndi_name, "address":address_naming})
                    address_naming.pop()  

            # Create the EJB3 properties
            if rar_default:
                logger.info('Setting ejb attribute default-resource-adapter-name to %s' % resource_adapter)
                send_json(jboss_mgmt_url,{"operation":"write-attribute","name":"default-resource-adapter-name","value":resource_adapter, "address":address_ejb})

            del address_rar[-3:]
            # send_json(jboss_mgmt_url,{"operation":"activate","address":address_rar})


        logger.info('Setting ejb attribute default-missing-method-permissions-deny-access to false')
        send_json(jboss_mgmt_url,{"operation":"write-attribute","name":"default-missing-method-permissions-deny-access","value":"false", "address":address_ejb})

def config_amq(yaml_jdbc_config,config_prefix,jboss_mgmt_url):

    address_prefix = []
    address = []
    if config_prefix is not None:
        address_prefix = copy.deepcopy(config_prefix)
    address = copy.deepcopy(address_prefix)
    # Create path for-adapter subsystem
    address.extend(("subsystem","resource-adapters"))
    # Create path for naming subsystem
    address_naming = copy.deepcopy(address_prefix)
    address_naming.extend(("subsystem","naming","binding"))
    # Create apth for ejb subsystem 
    address_ejb = copy.deepcopy(address_prefix)
    address_ejb.extend(("subsystem","ejb3"))

    enabled_queues = yaml_jdbc_config['queues']['enabled']
    try:
        excluded_queues = yaml_jdbc_config['queues']['excluded']
    except KeyError, e:
        excluded_queues = []
    merged_queues = sorted(set(enabled_queues) - set(excluded_queues))
    for resource_adapters in yaml_jdbc_config['provider']['amq']:
        for resource_adapter in resource_adapters:
            rar_prop = dict()
            rar_ejb_prop = dict()

            for resource_adapter_details in resource_adapters[resource_adapter]:
                # print resource_adapter_details
                if 'jndi-name' in resource_adapter_details:
                    rar_jndi_name = resource_adapter_details['jndi-name']
                if 'class-name' in resource_adapter_details:
                    rar_class_name = resource_adapter_details['class-name']
                if 'min-pool-size' in resource_adapter_details:
                    rar_min_pool = resource_adapter_details['min-pool-size']
                if 'max-pool-size' in resource_adapter_details:
                    rar_max_pool = resource_adapter_details['max-pool-size']
                if 'pool-prefill' in resource_adapter_details:
                    rar_pool_prefill = resource_adapter_details['pool-prefill']
                if 'same-rm-override' in resource_adapter_details:
                    rar_same_rm_override = resource_adapter_details['same-rm-override']
                if 'recovery-username' in resource_adapter_details:
                    rar_recovery_username = resource_adapter_details['recovery-username']
                if 'recovery-password' in resource_adapter_details:
                    rar_recovery_password = resource_adapter_details['recovery-password']
                if 'enabled' in resource_adapter_details:
                    rar_enabled = resource_adapter_details['enabled']
                if 'config-properties' in resource_adapter_details:
                    rar_config_props = resource_adapter_details['config-properties']  
                    for properties in rar_config_props:
                        for prop in properties:
                            rar_prop[prop]= properties[prop]
                if 'ejb' in resource_adapter_details:
                    rar_ejb_props = resource_adapter_details['ejb']  
                    for ejb_properties in rar_ejb_props:
                        for ejb_prop in ejb_properties:
                            rar_ejb_prop[ejb_prop]= ejb_properties[ejb_prop]
            address_rar = copy.deepcopy(address)
            address_rar.extend(("resource-adapter",resource_adapter))
            address_queue = copy.deepcopy(address_rar)
            address_queue.append("admin-objects")
            # Removing queues if exist
            logger.info("Checking if queues exists, if so remove those")
            for queue in merged_queues:
                address_queue.append(queue)
                address_naming.append("java:jboss/exported/jms/"+queue)
                logger.info("Check if queue %s already exists" % queue)
                if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address_naming}):
                    logger.info("Binding for queue %s already exists, removing first" % queue)
                    send_json(jboss_mgmt_url,{"operation":"remove","address":address_naming})   
                logger.info("Check if bindings already exists for queue %s" % queue)
                if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address_queue}):
                    logger.info("Queue %s already exists, removing first" % queue)
                    send_json(jboss_mgmt_url,{"operation":"remove","address":address_queue})
                address_queue.pop()
                address_naming.pop()

            for qcf in [rar_jndi_name,rar_jndi_name.lower()]:
                for binding_path in ["java:jboss/exported/jms/", "java:/jms/"]:
                    address_naming.append(binding_path+qcf)
                    if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address_naming}):
                        logger.info("Binding for QCF %s already exists, removing first" % qcf)
                        send_json(jboss_mgmt_url,{"operation":"remove","address":address_naming}) 
                    address_naming.pop()

            # Remove rar if exists
            if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address_rar}):
                 logger.info("RAR %s already exists, removing first" % resource_adapter)
                 send_json(jboss_mgmt_url,{"operation":"remove","address":address_rar})   

            # Restart the server before creating the rar,queues bindings again
            logger.info("Restarting the jvm to activate the config changes")                  
            if config_prefix is None:
                send_json(jboss_mgmt_url,{"operation":"reload"})
                time.sleep(5)
            else:
                for host in send_json(jboss_mgmt_url,{"operation":"read-children-names","child-type":"host"}):
                    # Check if host is not a DC, if so skip it
                    if not send_json(jboss_mgmt_url,{"operation":"read-attribute","name":"master", "address":["host",host]}):
                        logger.info("Reload config on host %s" % host)
                        send_json(jboss_mgmt_url,{"operation":"reload","address":["host",host]})
                time.sleep(20)

            # Add RAR and properties
            logger.info("Creating resource adapter")
            send_json(jboss_mgmt_url,{"operation":"add","archive":resource_adapter,"transaction-support":"XATransaction","address":address_rar})
            address_rar.extend(("connection-definitions",rar_jndi_name.lower()))
            logger.info("Adding connection definitions resource adapter")
            send_json(jboss_mgmt_url,{"operation":"add","class-name":rar_class_name,"jndi-name":"java:jboss/jms/"+rar_jndi_name,"enabled":rar_enabled,"min-pool-size":rar_min_pool,"max-pool-size":rar_max_pool,"pool-prefill":rar_pool_prefill,"same-rm-override":rar_same_rm_override,"recovery-username":rar_recovery_username,"recovery-password":rar_recovery_password,"address":address_rar})
            logger.info("Adding config properties to connection definitions")
            address_rar.extend(("config-properties","ServerUrl"))
            send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['serverurl'],"address":address_rar})
            address_rar.pop()
            address_rar.append("UserName")
            send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['username'],"address":address_rar})
            address_rar.pop()          
            address_rar.append("Password")
            send_json(jboss_mgmt_url,{"operation":"add","value":rar_prop['password'],"address":address_rar})

            #Recreating the queues
            logger.info("Creating queues")
            for queue in merged_queues:
                logger.info("Adding queue %s to resource adapter %s" % (queue, resource_adapter))
                address_queue.append(queue)
                send_json(jboss_mgmt_url,{"operation":"add","class-name":"org.apache.activemq.command.ActiveMQQueue","jndi-name":"java:/jms/"+queue ,"address":address_queue})
                address_queue.extend(("config-properties","PhysicalName"))
                send_json(jboss_mgmt_url,{"operation":"add","value":queue,"address":address_queue})

                # Add binding for queue
                binding_queue="java:jboss/exported/jms/"+queue
                address_naming.append(binding_queue)
                logger.info("Adding binding for queue %s" % queue)
                send_json(jboss_mgmt_url,{"operation":"add","binding-type":"lookup","lookup":"java:/jms/"+queue, "address":address_naming})
                address_naming.pop()
                del address_queue[-3:]
            # Create the QCF bindings again
            for qcf in [rar_jndi_name,rar_jndi_name.lower()]:
                for binding_path in ["java:jboss/exported/jms/", "java:/jms/"]:
                    address_naming.append(binding_path+qcf)
                    logger.info("Adding QCF binding %s for %s" % (qcf,binding_path))
                    send_json(jboss_mgmt_url,{"operation":"add","binding-type":"lookup","lookup":"java:jboss/jms/"+rar_jndi_name, "address":address_naming})
                    address_naming.pop()  

            # Create the EJB3 properties
            logger.info('Setting ejb attribute default-resource-adapter-name to %s' % resource_adapter)
            send_json(jboss_mgmt_url,{"operation":"write-attribute","name":"default-resource-adapter-name","value":resource_adapter, "address":address_ejb})
            for ejb_prop_key, ejb_prop_value in rar_ejb_prop.iteritems():
                logger.info('Setting ejb attribute %s to %s' % (ejb_prop_key, ejb_prop_value))
                send_json(jboss_mgmt_url,{"operation":"write-attribute","name":ejb_prop,"value":ejb_prop_value, "address":address_ejb})

            del address_rar[-3:]
            # send_json(jboss_mgmt_url,{"operation":"activate","address":address_rar})


def config_web(yaml_web_config,config_prefix,jboss_mgmt_url):

    address_prefix = []
    address = []
    if config_prefix is not None:
        address_prefix = copy.deepcopy(config_prefix)
    address = copy.deepcopy(address_prefix)
    # Create path for web subsystem
    address.extend(("subsystem","web"))
    address_config = copy.deepcopy(address)

    for config in yaml_web_config['jboss']:
        if 'configuration' in config:
            for prop in config['configuration']:
                address_config.append('configuration')
                if 'jsp-configuration' in prop:
                    address_config.append('jsp-configuration')
                    logger.info('Configuring jsp-configuration properties for web subsystem')
                    for attributes in prop['jsp-configuration']:
                        for attribute in attributes:
                            logger.info('Setting property %s with value %s' % (attribute,attributes[attribute]))
                            send_json(jboss_mgmt_url,{"operation":"write-attribute","value":attributes[attribute],"name":attribute,"address":address_config})
                    address_config.pop()
            address_config.pop()
        if 'virtual-server' in config:

            for virtualserver in config['virtual-server']:
                address_config.append('virtual-server')
                for virtualservername in virtualserver:
                    address_config.append(virtualservername)
                    for serverconfig in virtualserver[virtualservername]:
                        if 'attributes' in serverconfig:
                            for virtualserverattrs in serverconfig:
                                for virtualserverattr in serverconfig[virtualserverattrs]:
                                    for key, value in virtualserverattr.iteritems():
                                        logger.info('Setting virtual server attribute "%s" with value %s' % (key,value))
                                        if 'alias' in key:
                                            # Convert string of values to list
                                            temp_list = (value.split())
                                            send_json(jboss_mgmt_url,{"operation":"write-attribute","value":temp_list,"name":key,"address":address_config})
                                        else:
                                            send_json(jboss_mgmt_url,{"operation":"write-attribute","value":value,"name":key,"address":address_config})
                        if 'configuration' in serverconfig:
                            # print serverconfig
                            for virtualserverconfigs in serverconfig:
                                for virtualservercfg in serverconfig[virtualserverconfigs]:
                                    for cfg in virtualservercfg:
                                        if 'sso' in cfg:
                                            address_config.append('sso')
                                            address_config.append('configuration')
                                            
                                            # Remove sso if exists
                                            if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address_config}):
                                                logger.info("resource sso already exists, removing first")
                                                send_json(jboss_mgmt_url,{"operation":"remove","address":address_config})
                                            # Add sso config
                                            send_json(jboss_mgmt_url,{"operation":"add","address":address_config})
                                            # Loop over the sso attributes in the config file
                                            for sso_attrs in virtualservercfg[cfg]:
                                                for key, value in sso_attrs.iteritems():
                                                    logger.info('Setting sso attribute attribute "%s" with value %s' % (key,value))
                                                    send_json(jboss_mgmt_url,{"operation":"write-attribute","value":value,"name":key,"address":address_config})

def config_jca(yaml_jca_config,config_prefix,jboss_mgmt_url):

    address_prefix = []
    address = []
    if config_prefix is not None:
        address_prefix = copy.deepcopy(config_prefix)
    address = copy.deepcopy(address_prefix)
    # Create path for web subsystem
    address.extend(("core-service","vault"))
    address_config = copy.deepcopy(address)

    # print y aml_jca_config['jboss']
    vaultdict = {}
    vaultcreddict = {}

    for item in yaml_jca_config['jboss']['vault']:
        for key,value in item.iteritems():
            vaultdict[key] = value
    logger.info('Creating java vault(%s) (will be recreated if exists' % vaultdict['keystore-file'])
    if os.path.exists(vaultdict['keystore-dir']):
        shutil.rmtree(vaultdict['keystore-dir'], ignore_errors=True)
    os.makedirs(vaultdict['keystore-dir'])
    rc = os.system('$JAVA_HOME/bin/keytool -genseckey -alias %s -storetype jceks -keyalg AES -keysize 128 -storepass %s -keypass %s -keystore %s' % (vaultdict['keystore-alias'], vaultdict['keystore-password'], vaultdict['keystore-password'], vaultdict['keystore-dir'] + vaultdict['keystore-file']))
    if rc != 0:
        print "Failed to execute $JAVA_HOME/bin/keytool"
        exit(1)
    
    if "n/a" not in send_json(jboss_mgmt_url,{"operation":"read-resource","address":address}):
        logger.info("Vault configuration is already present, removing vault")                                                       
        send_json(jboss_mgmt_url,{"operation":"remove","address":address})

    for item in yaml_jca_config['jboss']['vault-cred']:
        for cred in yaml_jca_config['jboss']['vault-cred'][item]:
            for key,value in cred.iteritems():
                subprocess.check_output('$JBOSS_HOME/bin/vault.sh --keystore %s --keystore-password %s --alias %s -e %s --iteration %s --salt "%s" --vault-block %s --attribute %s --sec-attr %s > /opt/jboss/vault/log' % (vaultdict['keystore-dir'] + vaultdict['keystore-file'], vaultdict['keystore-password'], vaultdict['keystore-alias'], vaultdict['keystore-dir'], vaultdict['keystore-iteration'], vaultdict['keystore-salt'], item, key, value), shell=True)
    command = "cat /opt/jboss/vault/log | grep KEYSTORE_PASSWORD | sed 's/.*\"\\(MASK-.*\\)\".*/\\1/'"
    masked_pw = subprocess.check_output(command, shell=True).rstrip()
                    
    send_json(jboss_mgmt_url,{"operation":"add","vault-options":{"KEYSTORE_URL":vaultdict['keystore-dir'] + vaultdict['keystore-file'], "KEYSTORE_PASSWORD":masked_pw,"KEYSTORE_ALIAS":vaultdict['keystore-alias'],"SALT":vaultdict['keystore-salt'],"ITERATION_COUNT":vaultdict['keystore-iteration'],"ENC_FILE_DIR":vaultdict['keystore-dir']},"name":"vault","address":address_config})
            


def config(config_file, jboss_host, jboss_port, user, password, target_env,app_messaging):

    # Set default value of jboss mgmt interface if not specified
    if jboss_port is None:
        jboss_port = 9990

    # logger.info('Loading config file %s' % config_file)
    jboss_mgmt_url = 'http://%s:%s/management' % (jboss_host, jboss_port)
    logger.debug('Running config on host: %s' % jboss_host)
    logger.debug('Using mgmt console : %s' % jboss_mgmt_url)

    global app_user
    app_user = user
    global app_user_password
    app_user_password = password
    
    # Set correct config prefix path based on topology
    jboss_topology = send_json(jboss_mgmt_url,{"operation":"read-attribute", "name":"process-type"})
    if "Domain Controller" in jboss_topology:
        logger.info("Detected domain topology for host %s" %jboss_host)
        domain_mode = True
        config_prefix=['profile','full']
    elif "Server" in jboss_topology:
        logger.info("Detected standalone topology for host %s" %jboss_host)
        domain_mode = False
        config_prefix = None
    else:
        logger.error("Unkown topology %s detected" %jboss_topology)
        exit(1)

    # Load parsed yaml config
    yaml_config = common_func.load_config(config_file, target_env, domain_mode)
    for subsystem in yaml_config['subsystems']:
        if subsystem in 'jdbc':
            logger.info('Configuring JDBC subsystem ')
            config_jdbc(copy.deepcopy(yaml_config['subsystems']['jdbc']),config_prefix, jboss_mgmt_url)
        if subsystem in 'jaas':
            logger.info('Configuring Security subsystem ')
            config_jaas(copy.deepcopy(yaml_config['subsystems']['jaas']),config_prefix, jboss_mgmt_url)
        if subsystem in 'properties':
            logger.info('Configuring system properties')
            config_properties(copy.deepcopy(yaml_config['subsystems']['properties']),config_prefix, jboss_mgmt_url)
        if subsystem in 'messaging':
            if 'amq' in app_messaging:
                logger.info('Configuring AMQ subsystem')
                config_amq(copy.deepcopy(yaml_config['subsystems']['messaging']),config_prefix, jboss_mgmt_url)
            elif 'mq' in app_messaging:
                logger.info('Configuring MQ subsystem')
                config_mq(copy.deepcopy(yaml_config['subsystems']['messaging']),config_prefix, jboss_mgmt_url)
            elif 'hornet' in app_messaging:
                logger.info('Configuring Hornet subsystem')
        if subsystem in 'web':
            logger.info('Configuring web properties')
            config_web(copy.deepcopy(yaml_config['subsystems']['web']),config_prefix, jboss_mgmt_url)
        if subsystem in 'jca':
            logger.info('Configuring Security subsystem ')
            config_jca(copy.deepcopy(yaml_config['subsystems']['jca']),config_prefix, jboss_mgmt_url)

    # Restart the after config
    logger.info("Config script finished succesfully, performing final reload to activate the new config ")                  
    if config_prefix is None:
        send_json(jboss_mgmt_url,{"operation":"reload"})
        time.sleep(5)
    else:
        # send_json(jboss_mgmt_url,{"operation":"reload","address":["host","master"]})
        for host in send_json(jboss_mgmt_url,{"operation":"read-children-names","child-type":"host"}):
            # Check if host is not a DC, if so skip it
            if not send_json(jboss_mgmt_url,{"operation":"read-attribute","name":"master", "address":["host",host]}):
                logger.info("Reload config on host %s" % host)
                send_json(jboss_mgmt_url,{"operation":"reload","address":["host",host]})
        time.sleep(20)
    logger.info("Config script finished succesfully, performing final reload to activate the new config ")  




