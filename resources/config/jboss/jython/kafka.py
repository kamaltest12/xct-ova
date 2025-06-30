from jboss_utils import CLIHelper, OverridableConfigParser
from queue_list import queues

environment = OverridableConfigParser('environment.ini')
cli = CLIHelper()

# Delete topics
deleted_something = False

deleted_export_binding = False
#    deleted_export_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:jboss\\/exported\\/jms\\/%s' % queue['name'])
deleted_admin_object = cli.delete_if_exists('/subsystem=resource-adapters/resource-adapter=kafka-jms-rar.rar/admin-objects=KafkaTopic')
if deleted_admin_object:
    deleted_something = True
deleted_admin_object = cli.delete_if_exists('/subsystem=resource-adapters/resource-adapter=kafka-jms-rar.rar/admin-objects=KafkaDeadLetterQueue')
if deleted_admin_object:
    deleted_something = True
deleted_admin_object = cli.delete_if_exists('/subsystem=resource-adapters/resource-adapter=kafka-jms-rar.rar/admin-objects=KafkaBusinessEventQueue')
if deleted_admin_object:
    deleted_something = True

# Delete CF
deleted_export_binding = False
#    deleted_export_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:jboss\\/exported\\/jms\\/%s' % qcf_name)
deleted_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:\\/jms\\/KafkaCF')
if deleted_export_binding or deleted_binding:
    deleted_something = True

# Delete RAR
deleted_rar = cli.delete_if_exists('/subsystem=resource-adapters/resource-adapter=kafka-jms-rar.rar')
if deleted_rar:
    deleted_something = True
# Reload if necessary
if deleted_something:
    cli.reload()

# Add RAR
rar_attrs = {
    'archive': 'kafka-jms-rar.rar',
    'transaction-support': 'XATransaction'
}
cli.cd('/subsystem=resource-adapters')
cli.add('./resource-adapter=kafka-jms-rar.rar', rar_attrs)

cli.cd('./resource-adapter=kafka-jms-rar.rar')

# Add QCF
kafkacf_attrs = {
    'jndi-name': 'java\\:jboss\\/jms\\/KafkaCF',
    'class-name': 'com.clear2pay.jca.kafka.jms.connection.KafkaManagedConnectionFactory'
}
cli.add('./connection-definitions=KafkaCF', kafkacf_attrs)

kafkacf_props = {
    'bootstrapServers': environment.get('Kafka', 'bootstrapServers'),
    'clientId': 'stet',
    'securityProtocol': 'SSL',
    'sslTruststoreLocation': environment.get('Kafka', 'sslTruststoreLocation'),
    'sslTruststorePassword': environment.get('Kafka', 'sslTruststorePassword'),
    'sslKeystoreLocation': environment.get('Kafka', 'sslKeystoreLocation'),
    'sslKeystorePassword': environment.get('Kafka', 'sslKeystorePassword'),
    'sslKeyPassword': environment.get('Kafka', 'sslKeyPassword'),
    'jmsToKafkaHeaderNames': 'contenttype\\=content-type'
}
cli.cd('./connection-definitions=KafkaCF')
for kafkacf_prop in kafkacf_props:
    cli.add('./config-properties=%s' % kafkacf_prop, {'value': kafkacf_props[kafkacf_prop]})


kafkatopic_attrs = {
    'jndi-name': 'java\\:\\/jms\\/KafkaTopic',
    'class-name': 'com.clear2pay.jca.kafka.jms.connection.KafkaTopicSpec'
}
cli.cd('/subsystem=resource-adapters/resource-adapter=kafka-jms-rar.rar')
cli.add('./admin-objects=KafkaTopic', kafkatopic_attrs)

kafkatopic_props = {
    'connectionFactoryJndiName': 'java\\:jboss\\/jms\\/KafkaCF',
    'groupId': 'stet',
    'topics': 'stet',
    'retryBackoff': '1000',
    'pollInterval': '2000',
    'maxRetryCount': '3',
    'deadLetterTopicJndiName': 'jms\\/KafkaDeadLetterQueue'
}
cli.cd('./admin-objects=KafkaTopic')
for kafkatopic_prop in kafkatopic_props:
    cli.add('./config-properties=%s' % kafkatopic_prop, {'value': kafkatopic_props[kafkatopic_prop]})


deadlettertopic_attrs = {
    'jndi-name': 'java\\:\\/jms\\/KafkaDeadLetterQueue',
    'class-name': 'com.clear2pay.jca.kafka.jms.connection.KafkaTopicSpec'
}
cli.cd('/subsystem=resource-adapters/resource-adapter=kafka-jms-rar.rar')
cli.add('./admin-objects=KafkaDeadLetterQueue', deadlettertopic_attrs)
deadlettertopic_props = {
    'connectionFactoryJndiName': 'java\\:jboss\\/jms\\/KafkaCF',
    'topic': 'stetdeadletter',
    'enableTransactionSupport': 'false',
    'keySerializer': 'org.apache.kafka.common.serialization.StringSerializer',
    'valueSerializer': 'org.apache.kafka.common.serialization.StringSerializer'
}
cli.cd('./admin-objects=KafkaDeadLetterQueue')
for deadlettertopic_prop in deadlettertopic_props:
    cli.add('./config-properties=%s' % deadlettertopic_prop, {'value': deadlettertopic_props[deadlettertopic_prop]})

businesseventtopic_attrs = {
    'jndi-name': 'java\\:\\/jms\\/businessevent',
    'class-name': 'com.clear2pay.jca.kafka.jms.connection.KafkaTopicSpec'
}
cli.cd('/subsystem=resource-adapters/resource-adapter=kafka-jms-rar.rar')
cli.add('./admin-objects=KafkaBusinessEventQueue', businesseventtopic_attrs)
businesseventtopic_props = {
    'connectionFactoryJndiName': 'java\\:jboss\\/jms\\/KafkaCF',
    'topic': 'analytics.execution_coral.business_event',
    'enableTransactionSupport': 'true',
    'transactionalId': 'businessevent',
    'keySerializer': 'org.apache.kafka.common.serialization.StringSerializer',
    'valueSerializer': 'org.apache.kafka.common.serialization.StringSerializer'
}
cli.cd('./admin-objects=KafkaBusinessEventQueue')
for businesseventtopic_prop in businesseventtopic_props:
    cli.add('./config-properties=%s' % businesseventtopic_prop, {'value': businesseventtopic_props[businesseventtopic_prop]})

cli.disconnect()

