from jboss_utils import CLIHelper, OverridableConfigParser
from queue_list import ist_qcf_names
from queue_list import ist_queues

environment = OverridableConfigParser('environment.ini')
cli = CLIHelper()

# Delete queues
deleted_something = False
for queue in ist_queues:
    deleted_something = cli.delete_if_exists('/subsystem=naming/binding=java\\:jboss\\/exported\\/jms\\/%s' % queue['name'])

# Delete QCFs
deleted_qcf = False
for qcf_name in ist_qcf_names:
    deleted_export_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:jboss\\/exported\\/jms\\/%s' % qcf_name)
    deleted_binding = cli.delete_if_exists('/subsystem=naming/binding=java\\:\\/jms\\/%s' % qcf_name)
    if deleted_export_binding or deleted_binding:
        deleted_something = True

# Reload if necessary
if deleted_something:
    cli.reload()

# IST data for qcf and queues
ist_qcf_attrs = {
    'jndi-name': 'java\\:jboss\\/jms\\/ISTQCF',
    'class-name': 'com.clear2pay.jca.tcpip.jms.out.TcpIpManagedConnectionFactory'
}
ist_qcf_props = {
}

ist_queue_class = {
    'ISTSenderQ' : 'com.clear2pay.jca.tcpip.jms.out.TcpIpOutQueueImpl',
    'ISTInterchangeLoaderQ' : 'com.clear2pay.jca.tcpip.jms.in.TcpIpInQueueImpl'
}

ist_queue_props_data = {
    'ISTSenderQ' : {
        'hostname': environment.get('IST-TCPIP', 'hostname'),
        'port': environment.get('IST-TCPIP', 'port'),
        'connectionProtocol': 'UNIQUE_CLIENT_SOCKET',
        #'sslTruststoreLocation': '/tmp/security/ist.server.jks',
        #'sslTruststorePassword': 'password',
        #'sslKeystoreLocation': '/tmp/security/ist.client.jks',
        #'sslKeystorePassword': 'password',
        'connectionLengthSize': '2'
    },

    'ISTInterchangeLoaderQ' : {
        'hostname': environment.get('IST-TCPIP', 'hostname'),
        'port': environment.get('IST-TCPIP', 'port'),
        'connectionProtocol': 'UNIQUE_CLIENT_SOCKET',
        #'sslTruststoreLocation': '/tmp/security/ist.server.jks',
        #'sslTruststorePassword': 'password',
        #'sslKeystoreLocation': '/tmp/security/ist.client.jks',
        #'sslKeystorePassword': 'password',
        'messageType': 'bytes',
        'connectionLengthSize': '2',
        'isoEncoding': '"bitmaps=hex"',
        'isoLogonAdditionalData': '0176011001112M003602',
        'channelControllerList': '"com.clear2pay.jca.tcpip.iso8583.IsoLogonLogoffInitiator, com.clear2pay.jca.tcpip.iso8583.IsoEchoResponder, com.clear2pay.jca.tcpip.iso8583.IsoEchoInitiator"'
    }
}

# Add RAR
rar_attrs = {
    'archive': 'tcpip-jms-rar.rar'
}
cli.cd('/subsystem=resource-adapters')
cli.add('./resource-adapter=tcpip-jms-rar.rar', rar_attrs)

# Add ISTQCF
cli.cd('/subsystem=resource-adapters')
cli.cd('./resource-adapter=tcpip-jms-rar.rar')
cli.add('./connection-definitions=ISTQCF', ist_qcf_attrs)
cli.cd('./connection-definitions=ISTQCF')
for ist_qcf_prop in ist_qcf_props:
    cli.add('./config-properties=%s' % ist_qcf_prop, {'value': ist_qcf_props[ist_qcf_prop]})

# Add ISTQCF bindings
binding_attrs = {'binding-type': 'lookup', 'lookup': ist_qcf_attrs['jndi-name']}
for ist_qcf_name in ist_qcf_names:
    cli.cd('/subsystem=naming')
    cli.add('./binding=java\\:jboss\\/exported\\/jms\\/%s' % ist_qcf_name, binding_attrs)
    cli.add('./binding=java\\:\\/jms\\/%s' % ist_qcf_name, binding_attrs)

# Add IST queues
for ist_queue in ist_queues:
    cli.cd('/subsystem=resource-adapters/resource-adapter=tcpip-jms-rar.rar')
    cli.add('./admin-objects=%s' % ist_queue['name'], {'jndi-name': 'java\\:\\/jms\\/%s' % ist_queue['name'], 'class-name': '%s' % ist_queue_class[ist_queue['name']]})
    cli.cd('./admin-objects=%s' % ist_queue['name'])

    ist_queue_props = ist_queue_props_data[ist_queue['name']]
    for ist_queue_prop in ist_queue_props:
        cli.add('./config-properties=%s' % ist_queue_prop, {'value': ist_queue_props[ist_queue_prop]})

    cli.cd('/subsystem=naming')
    cli.add('./binding=java\\:jboss\\/exported\\/jms\\/%s' % ist_queue['name'], {'binding-type': 'lookup', 'lookup': 'java\\:\\/jms\\/%s' % ist_queue['name']})

cli.disconnect()
