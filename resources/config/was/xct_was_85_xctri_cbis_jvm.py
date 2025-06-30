# Specific JVM properties for OPF CBIS Integreation test

print 'Setting JVM Parameters'
for server in serversForCluster:
    serverId = server[0]
    nodeName = server[1]
    serverName = server[2]
    print "   Adapting settings for server %s, REAL CBIS Rest URL " % serverName
    createJvmProperty(nodeName, serverName, 'cbis.rest.base.url', 'http://cbis:9080/cbis/api')

print 'Setup complete for REAL CBIS Rest URL'