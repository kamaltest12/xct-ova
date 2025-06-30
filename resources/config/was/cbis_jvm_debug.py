print "   Adapting settings for server server1"
print "   Adapting settings for nodeName node1"

AdminTask.setJVMProperties('[-nodeName node1 -serverName server1 -debugMode true]')
AdminConfig.save()