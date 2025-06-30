# Specific TLS properties
def createSecurityProperty(propertyName, propertyValue) :
    security = AdminConfig.getid('/Security:/')
    prop = AdminConfig.getid('/Security:/Property:'+propertyName+'/')
    if prop:
        AdminConfig.modify(prop, [['value', propertyValue]])
    else:
        AdminConfig.create('Property', security, [['name',propertyName], ['value',propertyValue]])

def modifySSLConfiguration(alias, scope, protocol, provider, securityLevel, ciphersSSLList )  :
    fullAlias = '-alias ' + alias
    if scope:
        fullAlias = fullAlias + ' -scopeName '+ scope
    try:
        config =  AdminTask.getSSLConfig(fullAlias)
        if config:
            commandLine = fullAlias + ' -jsseProvider ' +  provider + ' -sslProtocol ' + protocol + ' -securityLevel ' + securityLevel + ' -enabledCiphers ' + ciphersSSLList
            AdminTask.modifySSLConfig(commandLine)
    except:
        print 'The SSL config ' + fullAlias + " is  not found"


print 'Setting TLS Parameters==============================='
#List of Kafka file server SSL configuration
kafkaAlias = ['OPFClientSSLSSLSettings']
#List of alias to ignore during the update process
ignoreAlias = ['']
print 'Setting ==============================='
#cellName = AdminControl.getCell()
ciphersList = 'SSL_RSA_WITH_AES_256_GCM_SHA384,SSL_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, SSL_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, SSL_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256, SSL_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, SSL_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, SSL_ECDHE_RSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256'
ciphersIBMListFull = 'SSL_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 SSL_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 SSL_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256 SSL_ECDHE_RSA_WITH_AES_128_GCM_SHA256 SSL_ECDHE_RSA_WITH_AES_256_GCM_SHA384 SSL_ECDHE_RSA_WITH_AES_128_CBC_SHA256'
ciphersIBMListKafka = 'SSL_ECDHE_RSA_WITH_AES_128_CBC_SHA256'
# disabledAlgo = 'SSLv3, RC4, DES, MD5withRSA, DH, DESede, 3DES_EDE_CBC, anon, NULL, TLSv1, TLSv1.1, SHA1, DSA, SHA224withRSA, ECDH, SSL_RSA_WITH_AES_128_CBC_SHA256, SSL_RSA_WITH_AES_256_CBC_SHA256, SSL_RSA_WITH_AES_256_GCM_SHA384, SSL_RSA_WITH_AES_128_GCM_SHA256, SSL_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, SSL_ECDHE_RSA_WITH_AES_256_CBC_SHA384'
# Kafka test server does not work when the following is disabled (TODO check with Coastguard the reason for bulk disablement of a large amount of algo but not all, eg SHA1 disabled but not other variants of SHA1) - DH, DESede, DSA
disabledAlgo = 'SSLv3, RC4, DES, MD5withRSA, DH, DESede, 3DES_EDE_CBC, anon, NULL, TLSv1, TLSv1.1, SHA1, DSA, SHA224withRSA, ECDH, SSL_RSA_WITH_AES_128_CBC_SHA256, SSL_RSA_WITH_AES_256_CBC_SHA256, SSL_RSA_WITH_AES_128_GCM_SHA256, SSL_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, SSL_ECDHE_RSA_WITH_AES_256_CBC_SHA384'

print 'Setting TLS Parameters in JVM properties'
for server in serversForCluster:
    serverId = server[0]
    nodeName = server[1]
    serverName = server[2]

    ##TLS
    createJvmProperty(nodeName, serverName, 'jdk.tls.client.protocols', 'TLSv1.2')
    createJvmProperty(nodeName, serverName, 'https.protocols', 'TLSv1.2')
    createJvmProperty(nodeName, serverName, 'https.cipherSuites', ciphersList)

print 'Setting TLS Parameters in Security properties'
createSecurityProperty('com.ibm.jsse2.overrideDefaultTLS', 'true')
createSecurityProperty('com.ibm.jsse2.overrideDefaultProtocol', 'TLSv12')
createSecurityProperty('com.ibm.websphere.tls.disabledAlgorithms', disabledAlgo)
createSecurityProperty('com.ibm.websphere.ssl.include.ECCiphers', 'true')

print 'Changes TLS parameters in all SSL configuration'
allConfigs = AdminTask.listSSLConfigs('[-all true]')
for sslConfig in allConfigs.splitlines():
    alias = sslConfig.split(' managementScope: ')[0].strip()
    alias = alias.split('alias: ')[1].strip()


    needToBeUpdated = True
    for aliasName in ignoreAlias:
        if alias == aliasName:
            needToBeUpdated = False

    if needToBeUpdated:
        scope = sslConfig.split(' managementScope: ')[1].strip()
        ciphers = ciphersIBMListFull
        for aliasName in kafkaAlias:
            if alias == aliasName:
                ciphers = ciphersIBMListKafka
        print 'Modification SSL config: ' + alias + ' in scope: ' + scope + ' with ciphers: ' + ciphers
        AdminTask.modifySSLConfig('[-alias '+alias+' -scopeName '+scope+' -sslProtocol TLSv1.2 -jsseProvider IBMJSSE2 -securityLevel CUSTOM -enabledCiphers "'+ciphers+'"]')
        #modifySSLConfiguration(alias, scope,'TLSv1.2', 'IBMJSSE2', 'CUSTOM', ciphers)
