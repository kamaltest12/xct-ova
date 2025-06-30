###############################################################################
### file is intended for configuring server running CBIS in OPF-CBIS-CI JOB ###
### this file is part of scripts.list.was.cbis                              ###
### this file is included in delivery.zip                                   ###
###############################################################################

print "Setting JVM Parameters"
opf_create_jvm_variables({
    'com.clear2pay.bph.opf.deepsea.idle': 'true',
    'jet.jmx.dmport': '2809',
    'SERVER_LOG_ROOT':'${SERVER_LOG_ROOT}',
    'com.clear2pay.bph.warmupEnabled': 'true'
    })

print "Creating JAAS"
### JAAS to login to the APIGW or emulator (defined as the alias in the ExternalSystemParameter table)
if getJAAS('Blue Bank Core RealtimeReference'):
    deleteJAAS('Blue Bank Core RealtimeReference')
createJAAS('Blue Bank Core RealtimeReference', 'cbis', 'password')
if getJAAS('Multi-Bank Core RealtimeReference'):
    deleteJAAS('Multi-Bank Core RealtimeReference')
createJAAS('Multi-Bank Core RealtimeReference', 'cbis', 'password')
if getJAAS('Blue Bank Core GLRealtimeReference'):
    deleteJAAS('Blue Bank Core GLRealtimeReference')
createJAAS('Blue Bank Core GLRealtimeReference', 'cbis', 'password')
if getJAAS('Multi-Bank Core GLRealtimeReference'):
    deleteJAAS('Multi-Bank Core GLRealtimeReference')
createJAAS('Multi-Bank Core GLRealtimeReference', 'cbis', 'password')
if getJAAS('Blue Bank Core BatchReference'):
    deleteJAAS('Blue Bank Core BatchReference')
createJAAS('Blue Bank Core BatchReference', 'cbis', 'password')
if getJAAS('Multi-Bank Core BatchReference'):
    deleteJAAS('Multi-Bank Core BatchReference')
createJAAS('Multi-Bank Core BatchReference', 'cbis', 'password')
if getJAAS('Blue Bank Core GLBatchReference'):
    deleteJAAS('Blue Bank Core GLBatchReference')
createJAAS('Blue Bank Core GLBatchReference', 'cbis', 'password')
if getJAAS('Multi-Bank Core GLBatchReference'):
    deleteJAAS('Multi-Bank Core GLBatchReference')
createJAAS('Multi-Bank Core GLBatchReference', 'cbis', 'password')

### JNDI binding to define the APIGW or emulator

# Generic Core System REST API URL binding - realtime
bindingNameSpace1 = 'url/cbis/genericcoresystem/realtime'
bindingParams1 = [
    ['name', 'CBIS_Generic_Core_System_Realtime_REST_API_URL'],
    ['nameInNameSpace', bindingNameSpace1],
    ['stringToBind', "http://was:9080/emulator/apigateway/corebankingsystem"]
]

# Returns the server name
def getServerName(server):
    return AdminConfig.showAttribute(server, 'name')

# Get the server ID to use as the scope for name space bindings
server = AdminConfig.getid("/Server:" + serverName)

# First, remove binding if exists
for binding in AdminConfig.list('NameSpaceBinding').splitlines():
    if bindingNameSpace1 == AdminConfig.showAttribute(binding, 'nameInNameSpace'):
        print "Removing name space binding '%s'" % bindingNameSpace1
        AdminConfig.remove(binding)

# Now, create a new name space binding
print "Creating name space binding '%s' on server %s" % (bindingNameSpace1, getServerName(server))
AdminConfig.create('StringNameSpaceBinding', server, bindingParams1)

cbisTraceLevel = "*=info: " \
                "com.clear2pay.bph.opfpayment.*=finest: " \
                "com.clear2pay.bph.opfcommon.parsing.*=finest: "\
                "com.clear2pay.bph.cbis.*=finest: "\
                "com.clear2pay.bph.cbisri.*=finest: "\
                "com.clear2pay.bph.opfport.bpel.*=finest"
isCluster = True
try:
  if clusterName == 'none':
    isCluster = False
except NameError:
    isCluster = False

if isCluster:
    serversForCluster = getServerIDsForClusters([clusterName])
else:
    serversForCluster = getServerIDsForAllAppServers()

for server in serversForCluster:
    serverId = server[0]
    nodeName = server[1]
    serverName = server[2]
    print "   Adapting settings for server %s" % serverName
    setServerTrace(nodeName, serverName, cbisTraceLevel, outputType="SPECIFIED_FILE", maxBackupFiles=10, rolloverSize=30)
    createJvmProperty(nodeName, serverName, 'testapi.http.url', 'http://localhost:9080')

AdminConfig.create('HostAlias', AdminConfig.getid('/Cell:OPFCell/VirtualHost:admin_host/'), [['hostname', '*'],['port', 9143]])
AdminTask.modifyServerPort('server1', '[-nodeName node1 -endPointName WC_adminhost_secure -host * -port 9143 -modifyShared true]')

# Save configuration changes
AdminConfig.save()
