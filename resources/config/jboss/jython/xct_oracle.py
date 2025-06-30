from jboss_utils import CLIHelper

cli = CLIHelper()

cli.cd('/subsystem=datasources/xa-data-source=BPHOracleXADataSource')
cli.cmd(':write-attribute(name=max-pool-size,value=120)')
cli.disconnect()
