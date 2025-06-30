from jboss_utils import CLIHelper

cli = CLIHelper()

cli.cd('/subsystem=ejb3')
cli.cmd(':write-attribute(name=default-resource-adapter-name,value=wmq.jmsra.rar)')
cli.cmd(':write-attribute(name=default-missing-method-permissions-deny-access,value=false)')

cli.cd('/subsystem=ejb3/thread-pool=default')
cli.cmd(':write-attribute(name=max-threads,value=100)')
cli.cd('/subsystem=ejb3/strict-max-bean-instance-pool=slsb-strict-max-pool')
cli.cmd(':write-attribute(name=derive-size,value=none)')
cli.cmd(':write-attribute(name=max-pool-size,value=1000)')
cli.cd('/subsystem=ejb3/strict-max-bean-instance-pool=mdb-strict-max-pool')
cli.cmd(':write-attribute(name=derive-size,value=none)')
cli.cmd(':write-attribute(name=max-pool-size,value=500)')

cli.disconnect()
