from jboss_utils import CLIHelper, OverridableConfigParser
from queue_list import otherqcf_queues
from queue_list import otherqcf_qcf_names

environment = OverridableConfigParser('environment.ini')
cli = CLIHelper()

def verifyQManagerInstances ():
    singleQMgr = False

    queueMyQMgrName = environment.get('Messaging', 'myqcf_qmgr')
    queueMyQMgrHostname = environment.get('Messaging', 'myqcf_host')
    queueMyQMgrPort = environment.get('Messaging', 'myqcf_port')
    srvConChannelMyQMgr = environment.get('Messaging', 'myqcf_channel')

    queueOtherQMgrName = environment.get('Messaging', 'otherqcf_qmgr')
    queueOtherQMgrHostname = environment.get('Messaging', 'otherqcf_host')
    queueOtherQMgrPort = environment.get('Messaging', 'otherqcf_port')
    srvConChannelOtherQMgr = environment.get('Messaging', 'otherqcf_channel')

    queueQMgrName = environment.get('Messaging', 'qmgr')
    queueQMgrHostname = environment.get('Messaging', 'host')
    queueQMgrPort = environment.get('Messaging', 'port')
    srvConChannelQMgr = environment.get('Messaging', 'channel')

    if (queueMyQMgrName==queueOtherQMgrName) and (queueMyQMgrName==queueQMgrName) :
        if (queueMyQMgrHostname==queueOtherQMgrHostname) and (queueMyQMgrHostname==queueQMgrHostname) :
            if (queueMyQMgrPort==queueOtherQMgrPort) and (queueMyQMgrPort==queueQMgrPort) :
                if (srvConChannelMyQMgr==srvConChannelOtherQMgr) and (srvConChannelMyQMgr==srvConChannelQMgr) : singleQMgr = True

    return singleQMgr
#enddef

# Delete queues
deleted_something = False
for queue in otherqcf_queues:
    deleted_something = cli.delete_if_exists('/subsystem=naming/binding=java\\:jboss\\/exported\\/jms\\/%s' % queue['name'])

# Delete QCFs
deleted_qcf = False
for qcf_name in otherqcf_qcf_names:  # TODO: find out why we have this lower-case name
    deleted_export_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:jboss\\/exported\\/jms\\/%s' % qcf_name)
    deleted_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:\\/jms\\/%s' % qcf_name)
    if deleted_export_binding or deleted_binding:
        deleted_something = True

# Reload if necessary
if deleted_something:
    cli.reload()

isSingleQMgr = verifyQManagerInstances()

# Add QCF
qcf_attrs = {
    'use-ccm': 'true',
    'jndi-name': 'java\\:jboss\\/jms\\/OTHERQCF',
    'use-java-context': 'true',
    'class-name': 'com.ibm.mq.connector.outbound.ManagedQueueConnectionFactoryImpl'
}
qcf_props = {
    'port': environment.get('Messaging', 'otherqcf_port'),
    'hostName': environment.get('Messaging', 'otherqcf_host'),
    'username': environment.get('Messaging', 'otherqcf_username'),
    'password': environment.get('Messaging', 'otherqcf_password'),
    'channel': environment.get('Messaging', 'otherqcf_channel'),
    'transportType': environment.get('Messaging', 'otherqcf_transportType'),
    'queueManager': environment.get('Messaging', 'otherqcf_qmgr')

}
cli.cd('/subsystem=resource-adapters')
cli.cd('./resource-adapter=wmq.jmsra.rar')
cli.add('./connection-definitions=otherqcf', qcf_attrs)
cli.cd('./connection-definitions=otherqcf')
for qcf_prop in qcf_props:
    cli.add('./config-properties=%s' % qcf_prop, {'value': qcf_props[qcf_prop]})
# Add queues
for queue in otherqcf_queues:
    cli.cd('/subsystem=resource-adapters/resource-adapter=wmq.jmsra.rar')
    cli.add('./admin-objects=%s' % queue['name'], {'jndi-name': 'java\\:\\/jms\\/Other\\/%s' % queue['baseQname'], 'class-name': 'com.ibm.mq.connector.outbound.MQQueueProxy'})
    cli.cd('./admin-objects=%s' % queue['name'])

    if isSingleQMgr:
        baseQName = 'TestOther'+ queue['baseQname']
    else:
        baseQName = queue['baseQname']

    cli.add('./config-properties=baseQueueName', {'value': baseQName})
    cli.add('./config-properties=baseQueueManagerName', {'value': qcf_props['queueManager']})
    for key in queue.keys():
        if key != 'name' and key != 'baseQname':
            cli.add('./config-properties=%s' % key, {'value': '%s' % queue[key]})
    cli.cd('/subsystem=naming')
    cli.add('./binding=java\\:jboss\\/exported\\/jms\\/Other\\/%s' % queue['baseQname'], {'binding-type': 'lookup', 'lookup': 'java\\:\\/jms\\/Other\\/%s' % queue['baseQname']})
# Add QCF bindings
binding_attrs = {'binding-type': 'lookup', 'lookup': qcf_attrs['jndi-name']}
for qcf_name in otherqcf_qcf_names:
    cli.cd('/subsystem=naming')
    cli.add('./binding=java\\:jboss\\/exported\\/jms\\/%s' % qcf_name, binding_attrs)
    cli.add('./binding=java\\:\\/jms\\/%s' % qcf_name, binding_attrs)

cli.disconnect()

