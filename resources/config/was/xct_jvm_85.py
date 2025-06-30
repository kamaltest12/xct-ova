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
    createJvmProperty(nodeName, serverName, 'xct.fxs.rest.timeout', '120000')
    createJvmProperty(nodeName, serverName, 'xct.fxs.rest.always.trust' , 'true')
    createJvmProperty(nodeName, serverName, 'xct.pcs.rest.base.url', 'https://localhost:9443/opfresttest/pcs/success')
    createJvmProperty(nodeName, serverName, 'xct.pcs.rest.timeout', '120000')
    createJvmProperty(nodeName, serverName, 'xct.pcs.rest.always.trust', 'true')

    createJvmProperty(nodeName, serverName, 'xct.universal.execution.callback.rest.base.url', 'https://localhost:9443/rest/api')
    createJvmProperty(nodeName, serverName, 'xct.universal.execution.rest.base.url', 'https://localhost:9443/rest/api')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.xct.api.client.base.url.CHANNELS', 'https://localhost:9443/rest/api')

    createJvmProperty(nodeName, serverName, 'com.clear2pay.opf.api.client.base.url.POM', 'https://localhost:9443/opfresttest/rest/uecr')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.opfpayment.fsis.riskassessment.rest.callback.url', 'https://localhost:9443/xctrest/webapi/fsis')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.opf.relay.cache.data.change.notification.batch.mode.sync', 'true')

    createJvmProperty(nodeName, serverName, 'xct.pom.rest.always.trust', 'true')
    createJvmProperty(nodeName, serverName, 'xct.cbis.async.rest.always.trust', 'true')
    createJvmProperty(nodeName, serverName, 'xct.cbis.rest.always.trust', 'true')
    createJvmProperty(nodeName, serverName, 'xct.fsis.risk.assessment.rest.always.trust', 'true')
    createJvmProperty(nodeName, serverName, 'xct.nacas.rest.base.url', 'https://localhost:9443/opfresttest/simulator/nacas')
    createJvmProperty(nodeName, serverName, 'xct.nacas.rest.timeout', '120000')
    createJvmProperty(nodeName, serverName, 'xct.nacas.rest.always.trust', 'true')

    # security settings for OVA
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.opf.client.api.basic.authentication', 'false')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.security.profile', 'WAS_SECURITY')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.client.api.url', 'https://localhost:9443/xctrest/webapi')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.ova.cache.service.operation.ttl','5')

    # request logging for OVA
    createJvmProperty(nodeName, serverName, 'http.logging.strategy', 'full')

    # AMH
    createJvmProperty(nodeName, serverName, 'com.clear2pay.bph.xct.lau.validation.enabled', 'true')
    createJvmProperty(nodeName, serverName, 'com.clear2pay.xct.enable.xsd.validations', 'true')


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

if getJAAS('pcs'):
    deleteJAAS('pcs')
createJAAS('pcs', 'pcs', 'password')

print 'Setup complete for PCS Rest J2C Password Store'

if getJAAS('universal'):
    deleteJAAS('universal')
createJAAS('universal', 'universal', 'password')

print 'Setup complete for UNIVERSAL Rest J2C Password Store'

if getJAAS('POM'):
    deleteJAAS('POM')
createJAAS('POM', 'admin', 'password')

if getJAAS('nacas'):
    deleteJAAS('nacas')
createJAAS('nacas', 'nacas', 'password')

print 'Setup complete for POM Rest J2C Password Store'

if getJAAS('swiftamh'):
    deleteJAAS('swiftamh')
createJAAS('swiftamh', 'swiftamh', '1234567890ABCDEF')

print 'Setup complete for swift amh J2C Password Store'

# Modifies the custom property of the given JCA object.
def opf_modify_J2EEResourceProperty(aspec, name, value):
    propsList = AdminConfig.list('J2EEResourceProperty', aspec).splitlines()
    for props in propsList:
        propName = AdminConfig.showAttribute(props, 'name')
        if propName == name:
            AdminConfig.modify(props, [['value', value]])

# Returns the AdminObject type matching the given class and interface.
def opf_get_AdminObjectType(className, infName, ra):
    adminObjectsList = AdminConfig.list('AdminObject', ra).splitlines()
    for adminObject in adminObjectsList:
        adminObjectClassName = AdminConfig.showAttribute(adminObject, 'adminObjectClass')
        adminObjectInfName = AdminConfig.showAttribute(adminObject, 'adminObjectInterface')
        if adminObjectClassName == className and adminObjectInfName == infName:
            return adminObject
    return ''

print 'Starting to install Kafka J2C Resource Adapter from %s' % RAR_DIR
rarFile = '%s/kafka-jms-rar.rar' % RAR_DIR
option = '[-rar.name "OPF Kafka J2C Resource Adapter"]'

nodeNames = listNodes()

for nodeName in nodeNames:
    print "Adapting Kafka settings for node name %s" % nodeName
    kafkaRa = AdminConfig.installResourceAdapter(rarFile, nodeName, option)

    print "Defining kafka connection-factory from %s" % JKS_DIR
    name = ['name', 'KafkaCF']
    jname = ['jndiName', 'jms/KafkaCF']
    j2ccfAttrs = [name, jname]
    cf = AdminConfig.create('J2CConnectionFactory', kafkaRa, j2ccfAttrs)
    opf_modify_J2EEResourceProperty(cf, 'bootstrapServers', 'localhost:9991')
    opf_modify_J2EEResourceProperty(cf, 'clientId', 'stet')
    opf_modify_J2EEResourceProperty(cf, 'securityProtocol', 'SSL')
    opf_modify_J2EEResourceProperty(cf, 'sslTruststoreLocation', '%s/kafka/client/kafka.client.truststore.jks' % JKS_DIR)
    opf_modify_J2EEResourceProperty(cf, 'sslTruststorePassword', 'password')
    opf_modify_J2EEResourceProperty(cf, 'sslKeystoreLocation', '%s/kafka/client/kafka.client.keystore.jks' % JKS_DIR)
    opf_modify_J2EEResourceProperty(cf, 'sslKeystorePassword', 'password')
    opf_modify_J2EEResourceProperty(cf, 'sslKeyPassword', 'password')
    opf_modify_J2EEResourceProperty(cf, 'jmsToKafkaHeaderNames', 'contenttype=content-type')

    print "Defining kafka activation-spec"
    aconfig = AdminConfig.list('ActivationSpec', kafkaRa)
    cdattr = ['activationSpec', aconfig]
    name = ['name', 'stet']
    jname = ['jndiName', 'eis/stet']
    j2cacAttrs = [name, jname, cdattr]
    aspec = AdminConfig.create('J2CActivationSpec', kafkaRa, j2cacAttrs)
    opf_modify_J2EEResourceProperty(aspec, 'connectionFactoryJndiName', 'jms/KafkaCF')
    opf_modify_J2EEResourceProperty(aspec, 'groupId', 'stet')
    opf_modify_J2EEResourceProperty(aspec, 'topics', 'stet')
    opf_modify_J2EEResourceProperty(aspec, 'retryBackoff', '1000')
    opf_modify_J2EEResourceProperty(aspec, 'pollInterval', '2000')
    opf_modify_J2EEResourceProperty(aspec, 'maxRetryCount', '3')
    opf_modify_J2EEResourceProperty(aspec, 'deadLetterTopicJndiName', 'jms/KafkaDeadLetterQueue')

    print "Defining kafka business-event-queue"
    name = ['name', 'businessevent']
    jname = ['jndiName', 'jms/businessevent']
    cdattr = ['adminObject', opf_get_AdminObjectType('com.clear2pay.jca.kafka.jms.connection.KafkaTopicSpec', 'com.clear2pay.jca.kafka.jms.internal.KafkaOutboundSpec',kafkaRa)]
    j2caoAttrs = [name, jname, cdattr]
    ao = AdminConfig.create('J2CAdminObject', kafkaRa, j2caoAttrs)
    opf_modify_J2EEResourceProperty(ao, 'connectionFactoryJndiName', 'jms/KafkaCF')
    opf_modify_J2EEResourceProperty(ao, 'topic', 'analytics.execution_opf.business_event')
    opf_modify_J2EEResourceProperty(ao, 'enableTransactionSupport', 'true')
    opf_modify_J2EEResourceProperty(ao, 'transactionalId', 'businessevent')
    opf_modify_J2EEResourceProperty(ao, 'keySerializer', 'org.apache.kafka.common.serialization.StringSerializer')
    opf_modify_J2EEResourceProperty(ao, 'valueSerializer', 'org.apache.kafka.common.serialization.StringSerializer')

    print "Defining kafka dead-letter-queue"
    name = ['name', 'KafkaDeadLetterQueue']
    jname = ['jndiName', 'jms/KafkaDeadLetterQueue']
    cdattr = ['adminObject', opf_get_AdminObjectType('com.clear2pay.jca.kafka.jms.connection.KafkaTopicSpec', 'com.clear2pay.jca.kafka.jms.internal.KafkaOutboundSpec',kafkaRa)]
    j2caoAttrs = [name, jname, cdattr]
    ao = AdminConfig.create('J2CAdminObject', kafkaRa, j2caoAttrs)
    opf_modify_J2EEResourceProperty(ao, 'connectionFactoryJndiName', 'jms/KafkaCF')
    opf_modify_J2EEResourceProperty(ao, 'topic', 'stetdeadletter')
    opf_modify_J2EEResourceProperty(ao, 'enableTransactionSupport', 'false')
    opf_modify_J2EEResourceProperty(ao, 'keySerializer', 'org.apache.kafka.common.serialization.StringSerializer')
    opf_modify_J2EEResourceProperty(ao, 'valueSerializer', 'org.apache.kafka.common.serialization.StringSerializer')

print 'Finished installing Kafka J2C Resource Adapter'

# below are instructions to create a secret key for the websphere keystore, to import key you can use java way to load keystore ,add entry and store the keystore
# or use commands like this :   keytool -importkeystore (all the options you can find in java documentation)
# 1st create keystore and add the secret key to be referenced by websphere keystore setup.
if isCluster:
   serverName = "dmgr"
else:
   serverName = "server1"

os.system("ps -ef | grep java | grep " + serverName + "| awk '{print $8}' | xargs dirname | grep 'java\|jdk' | awk '!seen[$0]++' > /tmp/javaBinPath.txt")
os.system('echo -n "cd "  > /tmp/cdJavaBinPath.txt')
os.system('cat /tmp/javaBinPath.txt  >> /tmp/cdJavaBinPath.txt')
os.system('echo  "./keytool -genseckey -alias interact-2016 -keyalg AES -keysize 256 -storetype jceks -keystore /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -storepass kspassword -keypass kpassword" >> /tmp/cdJavaBinPath.txt')
os.system('echo  "./keytool -genseckey -alias interact-2019 -keyalg AES -keysize 256 -storetype jceks -keystore /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -storepass kspassword -keypass kpassword" >> /tmp/cdJavaBinPath.txt')
os.system('echo  "./keytool -genseckey -alias interact-2020 -keyalg AES -keysize 256 -storetype jceks -keystore /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -storepass kspassword -keypass kpassword" >> /tmp/cdJavaBinPath.txt')
os.system('echo  "./keytool -genseckey -alias amhhmac-lau-2023 -keyalg AES -keysize 256 -storetype jceks -keystore /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -storepass kspassword -keypass kpassword" >> /tmp/cdJavaBinPath.txt')
os.system('chmod +x /tmp/cdJavaBinPath.txt')
os.system('/tmp/cdJavaBinPath.txt')
# 2nd setup websphere keystore that pointing to the created keystore in the 1st step (which contains the secret key)
AdminTask.createKeyStore('[-keyStoreName SAAKeyStore  -scopeName (cell):OPFCell -keyStoreDescription "Used to get AES key for SAA message enryption" -keyStoreLocation /opt/ibm/WebSphere/AppServer/etc/saa.keystore.jceks -keyStorePassword kspassword -keyStorePasswordVerify kspassword -keyStoreType JCEKS -keyStoreInitAtStartup true -keyStoreReadOnly false -keyStoreStashFile false]')
