from jboss_utils import CLIHelper, OverridableConfigParser
from queue_list import swiftagi_qcf_names

environment = OverridableConfigParser('environment.ini')
cli = CLIHelper()

# Delete QCFs
for qcf_name in swiftagi_qcf_names:
    cli.delete_if_exists('/subsystem=naming/binding=java\\:\\/jms\\/%s' % qcf_name)

# Add QCF bindings
binding_attrs = {'binding-type': 'lookup', 'lookup': 'java\\:jboss\\/jms\\/QCF'}
for qcf_name in swiftagi_qcf_names:
    cli.cd('/subsystem=naming')
    cli.add('./binding=java\\:\\/jms\\/%s' % qcf_name, binding_attrs)

cli.disconnect()

