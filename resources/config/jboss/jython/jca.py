from jboss_utils import CLIHelper

cli = CLIHelper()

cli.cd('/subsystem=jca/workmanager=default/short-running-threads=default')
cli.cmd(':write-attribute(name=max-threads,value=150)')
cli.cd('/subsystem=jca/workmanager=default/long-running-threads=default')
cli.cmd(':write-attribute(name=max-threads,value=150)')

cli.disconnect()
