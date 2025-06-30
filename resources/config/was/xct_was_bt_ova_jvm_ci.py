for server in serversForCluster:
    serverId = server[0]
    nodeName = server[1]
    serverName = server[2]
    print "   Adapting settings for server %s" % serverName

    # searcher to be always visible
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.hideSearchLimitOverride', '-1')
    # OVA deployments
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.osgi.frameworkReadinessRetryLimit', '600')