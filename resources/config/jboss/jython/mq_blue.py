from jboss_utils import CLIHelper, OverridableConfigParser
from queue_list import blue_queues
from queue_list import blue_qcf_names

environment = OverridableConfigParser('environment.ini')
cli = CLIHelper()

# Delete queues
deleted_something = False
for queue in blue_queues:
    deleted_something = cli.delete_if_exists('/subsystem=naming/binding=java\\:jboss\\/exported\\/jms\\/%s' % queue['name'])

# Delete QCFs
deleted_qcf = False
for qcf_name in blue_qcf_names:  # TODO: find out why we have this lower-case name
    deleted_export_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:jboss\\/exported\\/jms\\/%s' % qcf_name)
    deleted_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:\\/jms\\/%s' % qcf_name)
    if deleted_export_binding or deleted_binding:
        deleted_something = True

# Reload if necessary
if deleted_something:
    cli.reload()

# Add QCF
qcf_attrs = {
    'use-ccm': 'true',
    'jndi-name': 'java\\:jboss\\/jms\\/BLUEQCF',
    'use-java-context': 'true',
    'class-name': 'com.ibm.mq.connector.outbound.ManagedQueueConnectionFactoryImpl'
}
qcf_props = {
    'port': environment.get('Messaging', 'port'),
    'hostName': environment.get('Messaging', 'host'),
    'username': environment.get('Messaging', 'username'),
    'password': environment.get('Messaging', 'password'),
    'channel': environment.get('Messaging', 'channel'),
    'transportType': 'CLIENT',
    'queueManager': environment.get('Messaging', 'qmgr')

}

cli.cd('/subsystem=resource-adapters')
cli.cd('./resource-adapter=wmq.jmsra.rar')
cli.add('./connection-definitions=blueqcf', qcf_attrs)
cli.cd('./connection-definitions=blueqcf')
for qcf_prop in qcf_props:
    cli.add('./config-properties=%s' % qcf_prop, {'value': qcf_props[qcf_prop]})

# Add queues
for queue in blue_queues:
    cli.cd('/subsystem=resource-adapters/resource-adapter=wmq.jmsra.rar')
    cli.add('./admin-objects=%s' % queue['name'], {'jndi-name': 'java\\:\\/jms\\/%s' % queue['name'], 'class-name': 'com.ibm.mq.connector.outbound.MQQueueProxy'})
    cli.cd('./admin-objects=%s' % queue['name'])
    cli.add('./config-properties=baseQueueName', {'value': queue['name']})
    cli.add('./config-properties=baseQueueManagerName', {'value': qcf_props['queueManager']})
    cli.cd('/subsystem=naming')
    cli.add('./binding=java\\:jboss\\/exported\\/jms\\/%s' % queue['name'], {'binding-type': 'lookup', 'lookup': 'java\\:\\/jms\\/%s' % queue['name']})
# Add QCF bindings
binding_attrs = {'binding-type': 'lookup', 'lookup': qcf_attrs['jndi-name']}
for qcf_name in blue_qcf_names:
    cli.cd('/subsystem=naming')
    cli.add('./binding=java\\:jboss\\/exported\\/jms\\/%s' % qcf_name, binding_attrs)
    cli.add('./binding=java\\:\\/jms\\/%s' % qcf_name, binding_attrs)

cli.disconnect()

