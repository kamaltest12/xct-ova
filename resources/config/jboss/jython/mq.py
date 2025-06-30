from jboss_utils import CLIHelper, OverridableConfigParser
from queue_list import queues

environment = OverridableConfigParser('environment.ini')
cli = CLIHelper()

# Delete queues
deleted_something = False
for queue in queues:
    deleted_export_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:jboss\\/exported\\/jms\\/%s' % queue['name'])
    deleted_admin_object = cli.delete_if_exists('/subsystem=resource-adapters/resource-adapter=wmq.jmsra.rar/admin-objects=%s' % queue['name'])
    if deleted_export_binding or deleted_admin_object:
        deleted_something = True
# Delete QCFs
deleted_qcf = False
for qcf_name in ['QCF', 'qcf']:  # TODO: find out why we have this lower-case name
    deleted_export_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:jboss\\/exported\\/jms\\/%s' % qcf_name)
    deleted_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:\\/jms\\/%s' % qcf_name)
    if deleted_export_binding or deleted_binding:
        deleted_something = True
# Delete RAR
deleted_rar = cli.delete_if_exists('/subsystem=resource-adapters/resource-adapter=wmq.jmsra.rar')
if deleted_rar:
    deleted_something = True
# Reload if necessary
if deleted_something:
    cli.reload()
# Add RAR
rar_attrs = {
    'archive': 'wmq.jmsra.rar',
    'transaction-support': 'XATransaction'
}
cli.cd('/subsystem=resource-adapters')
cli.add('./resource-adapter=wmq.jmsra.rar', rar_attrs)

cli.cd('./resource-adapter=wmq.jmsra.rar')
rar_props = {
    'maxConnections': '100'
}
for rar_prop in rar_props:
    cli.add('./config-properties=%s' % rar_prop, {'value': rar_props[rar_prop]})

# Add QCF
qcf_attrs = {
    'use-ccm': 'true',
    'jndi-name': 'java\\:jboss\\/jms\\/QCF',
    'use-java-context': 'true',
    'class-name': 'com.ibm.mq.connector.outbound.ManagedQueueConnectionFactoryImpl',
    'min-pool-size': '10',
    'max-pool-size': '100',
    'pool-prefill': 'true',
    'pool-use-strict-min': 'true'
}


qcf_props = {
    'port': environment.get('Messaging', 'port'),
    'hostName': environment.get('Messaging', 'host'),
    'username': environment.get('Messaging', 'username'),
    'password': environment.get('Messaging', 'password'),
    'channel': environment.get('Messaging', 'channel'),
    'transportType': environment.get('Messaging', 'transportType'),
    'queueManager': environment.get('Messaging', 'qmgr')

}

cli.add('./connection-definitions=qcf', qcf_attrs)
cli.cd('./connection-definitions=qcf')
for qcf_prop in qcf_props:
    cli.add('./config-properties=%s' % qcf_prop, {'value': qcf_props[qcf_prop]})
# Add queues
for queue in queues:
    cli.cd('/subsystem=resource-adapters/resource-adapter=wmq.jmsra.rar')
    cli.add('./admin-objects=%s' % queue['name'], {'jndi-name': 'java\\:\\/jms\\/%s' % queue['name'], 'class-name': 'com.ibm.mq.connector.outbound.MQQueueProxy'})
    cli.cd('./admin-objects=%s' % queue['name'])
    cli.add('./config-properties=baseQueueName', {'value': queue['name']})
    cli.add('./config-properties=baseQueueManagerName', {'value': qcf_props['queueManager']})
    for key in queue.keys():
        if key != 'name':
            cli.add('./config-properties=%s' % key, {'value': '%s' % queue[key]})
    cli.cd('/subsystem=naming')
    cli.add('./binding=java\\:jboss\\/exported\\/jms\\/%s' % queue['name'], {'binding-type': 'lookup', 'lookup': 'java\\:\\/jms\\/%s' % queue['name']})
# Add QCF bindings
binding_attrs = {'binding-type': 'lookup', 'lookup': qcf_attrs['jndi-name']}
for qcf_name in ['QCF', 'qcf']:
    cli.cd('/subsystem=naming')
    cli.add('./binding=java\\:jboss\\/exported\\/jms\\/%s' % qcf_name, binding_attrs)
    cli.add('./binding=java\\:\\/jms\\/%s' % qcf_name, binding_attrs)

cli.disconnect()

