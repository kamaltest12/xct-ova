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

    # Disabling DeepSea on WPS 8.5 for all applications
    createJvmProperty(nodeName, serverName, 'com.clear2pay.bph.opf.deepsea.enabled', 'false')
    createJvmProperty(nodeName, serverName, 'com.ibm.websphere.threadmonitor.threshold', '3600')
    createJvmProperty(nodeName, serverName, 'com.ibm.websphere.threadmonitor.interval', '0')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.bph.opfcommon.bpel.workflow.BPEL', 'false')
    createJvmProperty(nodeName, serverName, 'client.api.support.mode', 'true')
    createJvmProperty(nodeName, serverName, 'xct.rest.base.url', 'https://127.0.0.1:9443/xctrest/webapi')
    createJvmProperty(nodeName, serverName, 'cbis.rest.base.url', 'https://localhost:9443/opfresttest/cbis/success')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.opfpayment.fsis.riskassessment.rest.base.url', 'https://localhost:9443/opfresttest/fsis/success')
    createJvmProperty(nodeName, serverName, 'xct.fxs.rest.base.url', 'https://localhost:9443/opfresttest/fxs/success')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.opfpayment.fsis.riskassessment.rest.callback.url', 'https://localhost:9443/xctrest/webapi/fsis')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.opf.relay.cache.data.change.notification.batch.mode.sync', 'true')
    createJvmProperty(nodeName, serverName, 'bpmn.test.outputDirectory', '/tmp/bpmn')
    # jmx-http-bridge-url
    # createJvmProperty(nodeName, serverName, 'opf.jmx.http.bridge.url', 'https://dockerhost:9443/xctrest/jmx')
    # createJvmProperty(nodeName, serverName, 'opf.jmx.http.bridge.user', 'bva1')
    # createJvmProperty(nodeName, serverName, 'opf.jmx.http.bridge.password', 'password')

    # security settings for OVA
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.opf.client.api.basic.authentication', 'false')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.security.profile', 'WAS_SECURITY')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.client.api.url', 'https://localhost:9443/xctrest/webapi')

    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.ui.slave.mode', 'false')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.opf.client.webtarget.read.timout', '60000')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.opf.client.webtarget.connect.timout', '30000')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.bankingentities.all.enabled', 'true')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.session.timeout', '1800')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.session.timeout.warning', '120')

    # request logging for OVA
    createJvmProperty(nodeName, serverName, 'http.logging.strategy', 'full')

    # Change [Application servers > server1 > ORB service > Pass by reference] to false
    modify(AdminConfig.list('ObjectRequestBroker', serverId), [['noLocalCopies',  'false']])

    setServerTrace(nodeName, serverName, xctTraceLevel, outputType="SPECIFIED_FILE", maxBackupFiles=10, rolloverSize=30)

for (nodeName, serverName) in listServersOfType('APPLICATION_SERVER'):
    print "   Adapting BNYM Specific Transaction settings for server %s" % serverName
    configureTransactionService(nodeName, serverName, 900, 900, 900, 900)


if getJAAS('cbis'):
    deleteJAAS('cbis')
createJAAS('cbis', 'cbis', 'password')

print 'Setup complete for CBIS Rest J2C Password Store'

if getJAAS('payment_upload_push'):
    deleteJAAS('payment_upload_push')
createJAAS('payment_upload_push', 'payment_upload_push', 'password')

print 'Setup complete for Payment Upload Push Rest J2C Password Store'

if getJAAS('fsis'):
    deleteJAAS('fsis')
createJAAS('fsis', 'fsis', 'password')

print 'Setup complete for FSIS Rest J2C Password Store'

if getJAAS('fxs'):
    deleteJAAS('fxs')
createJAAS('fxs', 'fxs', 'password')

print 'Setup complete for FXS Rest J2C Password Store'

# below are instructions to create a secret key for the websphere keystore, to import key you can use java way to load keystore ,add entry and store the keystore
# or use commands like this :   keytool -importkeystore (all the options you can find in java documentation)
# 1st create keystore and add the secret key to be referenced by websphere keystore setup.
if isCluster:
   serverName = "dmgr"
else:
   serverName = "server1"

#os.system("ps -ef | grep java | grep " + serverName + "| awk '{print $8}' | xargs dirname | grep 'java\|jdk' | awk '!seen[$0]++' > /tmp/javaBinPath.txt")
#os.system('echo -n "cd "  > /tmp/cdJavaBinPath.txt')
#os.system('cat /tmp/javaBinPath.txt  >> /tmp/cdJavaBinPath.txt')
#os.system('echo  "./keytool -genseckey -alias interact-2016 -keyalg AES -keysize 256 -storetype jceks -keystore /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -storepass kspassword -keypass kpassword" >> /tmp/cdJavaBinPath.txt')
#os.system('echo  "./keytool -genseckey -alias interact-2019 -keyalg AES -keysize 256 -storetype jceks -keystore /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -storepass kspassword -keypass kpassword" >> /tmp/cdJavaBinPath.txt')
#os.system('echo  "./keytool -genseckey -alias interact-2020 -keyalg AES -keysize 256 -storetype jceks -keystore /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -storepass kspassword -keypass kpassword" >> /tmp/cdJavaBinPath.txt')
#os.system('echo  "./keytool -genseckey -alias swiftnetlink-lau-2020 -keyalg AES -keysize 256 -storetype jceks -keystore /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -storepass kspassword -keypass kpassword" >> /tmp/cdJavaBinPath.txt')
#os.system('echo  "./keytool -genkeypair -alias swiftnetlink-tls-2020 -dname \'cn=john-smith, o=csdpartc,o=swift\' -validity 180 -storetype jceks -keystore /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -storepass kspassword -keypass kpassword" >> /tmp/cdJavaBinPath.txt')
#os.system('echo  "./keytool -exportcert -file /opt/ibm/WebSphere/AppServer/etc/swiftnetlink.pem -alias swiftnetlink-tls-2020 -storetype jceks -keystore /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -storepass kspassword -keypass kpassword" >> /tmp/cdJavaBinPath.txt')
#os.system('chmod +x /tmp/cdJavaBinPath.txt')
#os.system('/tmp/cdJavaBinPath.txt')
# 2nd setup websphere keystore that pointing to the created keystore in the 1st step (which contains the secret key)
#AdminTask.createKeyStore('[-keyStoreName SAAKeyStore  -scopeName (cell):OPFCell -keyStoreDescription "Used to get AES key for SAA message enryption" -keyStoreLocation /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -keyStorePassword kspassword -keyStorePasswordVerify kspassword -keyStoreType JCEKS -keyStoreInitAtStartup true -keyStoreReadOnly false -keyStoreStashFile false]')

