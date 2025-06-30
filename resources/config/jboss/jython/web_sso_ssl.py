from jboss_utils import CLIHelper, OverridableConfigParser

environment = OverridableConfigParser('environment.ini')
cli = CLIHelper()

cli.cd('/subsystem=undertow/servlet-container=default/setting=jsp')
cli.cmd(':write-attribute(name=tag-pooling,value=false)')
cli.cd('/subsystem=undertow/server=default-server/host=default-host')
cli.cmd(':write-attribute(name=alias,value=[localhost])')
cli.recreate('./setting=single-sign-on')
#cli.cd('./setting=single-sign-on')
# cmd ':write-attribute(name=reauthenticate,value=false)' TODO: find out if this property still exists somewhere else
# TODO: adding the domain (dockerhost) breaks login if using localhost in URL
#cli.cmd(':write-attribute(name=domain,value=%s)' % environment.get('SSO', 'domain'))
cli.cd('/core-service=management')
cli.recreate('./security-realm=HTTPSRealm')
cli.cd('./security-realm=HTTPSRealm')
ssl_attrs = {
    'keystore-path': environment.get('Keystore', 'path'),
    'keystore-password': environment.get('Keystore', 'password'),
    'alias': 'dockerhost'
}
cli.add('./server-identity=ssl', ssl_attrs)
cli.cd('/subsystem=undertow/server=default-server')
https_attrs = {
    'socket-binding': 'https',
    'security-realm': 'HTTPSRealm'
}
cli.recreate('./https-listener=https', https_attrs)

cli.disconnect()
