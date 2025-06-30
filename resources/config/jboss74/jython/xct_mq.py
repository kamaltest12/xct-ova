from jboss_utils import CLIHelper, OverridableConfigParser
from xct_jboss_queue_list import xct_queues

environment = OverridableConfigParser('environment.ini')
cli = CLIHelper()

qcf_props = {
    'port': environment.get('Messaging', 'port'),
    'hostName': environment.get('Messaging', 'host'),
    'username': environment.get('Messaging', 'username'),
    'password': environment.get('Messaging', 'password'),
    'channel': environment.get('Messaging', 'channel'),
    'transportType': 'CLIENT',
    'queueManager': environment.get('Messaging', 'qmgr')
}

# Add queues
for queue in xct_queues:
    cli.cd('/subsystem=resource-adapters/resource-adapter=wmq.jmsra.rar')
    cli.add('./admin-objects=%s' % queue['name'], {'jndi-name': 'java\\:\\/jms\\/%s' % queue['name'], 'class-name': 'com.ibm.mq.connector.outbound.MQQueueProxy'})
    cli.cd('./admin-objects=%s' % queue['name'])
    cli.add('./config-properties=baseQueueName', {'value': queue['name']})
    cli.add('./config-properties=baseQueueManagerName', {'value': qcf_props['queueManager']})
    cli.cd('/subsystem=naming')
    cli.add('./binding=java\\:jboss\\/exported\\/jms\\/%s' % queue['name'], {'binding-type': 'lookup', 'lookup': 'java\\:\\/jms\\/%s' % queue['name']})

cli.disconnect()

