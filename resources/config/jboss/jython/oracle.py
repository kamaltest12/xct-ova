from jboss_utils import CLIHelper, OverridableConfigParser

environment = OverridableConfigParser('environment.ini')
cli = CLIHelper()

cli.cd('/subsystem=datasources')
# Need to delete datasources before recreating the driver
non_xa_deleted = cli.delete_if_exists('./data-source=BPHOracleNonXADataSource')
xa_deleted = cli.delete_if_exists('./xa-data-source=BPHOracleXADataSource')
if non_xa_deleted or xa_deleted:
    cli.reload()
driver_attrs = {
    'driver-name': 'BPHOracleJDBCDriver',
    'driver-xa-datasource-class-name': 'oracle.jdbc.xa.client.OracleXADataSource',
    'driver-module-name': 'com.oracle.jdbc'
}
cli.recreate('./jdbc-driver=BPHOracleJDBCDriver', driver_attrs)
bph_ora_non_xa_attrs = {
    'user-name': environment.get('Database', 'username'),
    'connection-url': environment.get('Database', 'url'),
    'password': environment.get('Database', 'password'),
    'enabled': 'true',
    'driver-name': 'BPHOracleJDBCDriver',
    'jndi-name': 'java:/jdbc/bphNonXA'
}
cli.add('./data-source=BPHOracleNonXADataSource', bph_ora_non_xa_attrs)
# Need to create the XA datasource this way otherwise we see 'At least one xa-datasource-property is required for an xa-datasource'
cli.cmd(
    'xa-data-source add '
    '--name=BPHOracleXADataSource --user-name=%s  --enabled=true --driver-name=BPHOracleJDBCDriver '
    '--jndi-name=java:/jdbc/bph --password=%s '
    '--xa-datasource-properties=[DatabaseName=>%s,PortNumber=>%s,ServerName=>%s,URL=>%s]' %
    (environment.get('Database', 'username'), environment.get('Database', 'password'), environment.get('Database', 'sid'),
     environment.get('Database', 'port'), environment.get('Database', 'host'), environment.get('Database', 'url'))
)

cli.cd('/subsystem=datasources/xa-data-source=BPHOracleXADataSource')
cli.cmd(':write-attribute(name=min-pool-size,value=50)')
cli.cmd(':write-attribute(name=max-pool-size,value=200)')
cli.cmd(':write-attribute(name=pool-prefill,value=true)')

cli.disconnect()
