# Set JVM properties specific to integration testing
for server in serversForCluster:
    serverId = server[0]
    nodeName = server[1]
    serverName = server[2]
    createJvmProperty(nodeName, serverName, 'bpmn.test.outputDirectory', '/tmp/bpmn')