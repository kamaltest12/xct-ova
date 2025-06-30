
# In order to make this file compile in Intellij IDEA,
# add `wsadminlib.py` in the folder and uncomment the line below.
# from opf_was_85 import *

def opf_qmgr(name, host, port, channel):
 return {
         'qmgrName': name,
         'qmgrHostname': host,
         'qmgrPortNumber': port,
         'qmgrSvrconnChannel' : channel
        }

def opf_qcf_param(name, jndi,desc,qmgr,host,port,channel,ttype,clientid,ccsid,model):
 return [
    	 ['name',name],
         ['jndiName',jndi],
    	 ['description',desc],
    	 ['queueManager',qmgr],
    	 ['host',host],
    	 ['port',port],
    	 ['channel',channel],
    	 ['transportType',ttype],
    	 ['clientID',clientid],
    	 ['CCSID',ccsid],
    	 ['tempModel', model]
       ]

def opf_pool_param(minC,maxC,reap,cto,uto,ato,policy):
 return [
    	 ['minConnections', minC],
    	 ['maxConnections', maxC],
    	 ['reapTime', reap],
    	 ['connectionTimeout', cto],
    	 ['unusedTimeout', uto],
    	 ['agedTimeout', ato],
    	 ['purgePolicy', policy]
	]

qmgrMap={}
qmgrMap['WHITEQMGR'] = opf_qmgr('MQ.QUEUE.MANAGER', 'mq', '1414', 'channel1')
qmgrMap['MYQMGR'] =  opf_qmgr('MQ.QUEUE.MANAGER', 'mq', '1414', 'channel1')
qmgrMap['OTHERQMGR'] = opf_qmgr('MQ.QUEUE.MANAGER', 'mq', '1414', 'channel1')
qmgrMap['SenderQCFQMGR'] = opf_qmgr('MQ.QUEUE.MANAGER', 'mq', '1414', 'channel1')

qmgr = qmgrMap['SenderQCFQMGR']
qcfName = 'SenderQCF'
qcfJndiName = 'jms/SenderQCF'
queueAuthAlias = 'bphmqm'
queueMgr = qmgr['qmgrName']
queueMgrPort = qmgr['qmgrPortNumber']
queueMgrHostname = qmgr['qmgrHostname']
srvConChannel = qmgr['qmgrSvrconnChannel']
clientID = 'mqm'

mqQueueConnectionFactoryParam= opf_qcf_param(qcfName,qcfJndiName,'OPF QCF Queue Connection Factory',queueMgr,queueMgrHostname,queueMgrPort,srvConChannel,'CLIENT',clientID,'819','SYSTEM.DEFAULT.MODEL.QUEUE')
mqQCFConnectionPoolParam = opf_pool_param('10','120','180','180','1800','0','EntirePool')
mqQCFSessionPoolParam = opf_pool_param('1','120','180','180','1800','0','EntirePool')

# JMS creation
mqJMSProvider = AdminConfig.getid( '/Cell:' + cellName + '/JMSProvider:WebSphere MQ JMS Provider/')
MQQCF=removeAndCreate('MQQueueConnectionFactory', mqJMSProvider, mqQueueConnectionFactoryParam, ['jndiName'])
connectionPool = AdminConfig.create('ConnectionPool', MQQCF, mqQCFConnectionPoolParam, 'connectionPool')
sessionPool = AdminConfig.create('ConnectionPool', MQQCF, mqQCFSessionPoolParam, 'sessionPool')

def opf_create_queues(queuelist):
    if isCluster:
        serversForCluster = getServerIDsForClusters([clusterName])
    else:
        serversForCluster = getServerIDsForAllAppServers()

    isSingleQMgr = verifyQManagerInstances(qmgrMap)
    if isSingleQMgr:
        print 'Single Q Manager creation instance'
    else:
        print 'Multi Q Manager creation instance'

    for server in serversForCluster:
      serverId = server[0]
      nodeName = server[1]
      serverName = server[2]
      messageListenerService = AdminConfig.list('MessageListenerService', serverId)
     # Populate list of existing Activation Spec(if any)
      existingActSpecs = AdminTask.listWMQActivationSpecs(cellId).splitlines()
     #Create JMS queues and listener ports
      for queueDef in queuelist:
                queueName = queueDef[0]
                print '   (re)creating queue %s' % queueName
                queueNameMQ = queueDef[1]
                queueParam = queueDef[2]
                actSpec = queueDef[4]
                mqmgr=queueDef[5]

                queueParam.append(['name', queueName])
                if (mqmgr == 'OTHERQMGR') :
                    queueParam.append(['jndiName', 'jms/'+'Other/'+queueNameMQ])
                    if isSingleQMgr :
                        queueParam.append(['baseQueueName', 'TestOther'+queueNameMQ])
                    else :
                        queueParam.append(['baseQueueName', queueNameMQ])
                else :
                     if (mqmgr =='SenderQCFQMGR') :
                        queueParam.append(['jndiName', 'jms/'+queueName])
                        queueParam.append(['baseQueueName', queueNameMQ])
                     else :
                        queueParam.append(['jndiName', 'jms/'+queueNameMQ])
                        queueParam.append(['baseQueueName', queueNameMQ])

                theQueue = removeAndCreate('MQQueue', mqJMSProvider, queueParam, ['jndiName'])

                actSpecName = queueName + 'Port'
                actSpecJndiName = 'eis/' + actSpecName
                actSpecDestJndiName = 'jms/' + queueName
                actSpecMaxSessions = queueDef[3][0]
                actSpecsDelCount = queueDef[3][1][1]
                print "   Adding activation spec:" + actSpecName
                actSpecConfigId = ''
                for spec in existingActSpecs:
                    if re.search('^'+actSpecName+'\(', spec):
                       actSpecConfigId = spec

                #Use the qmgr ref of the queueDef
                qmgr = qmgrMap[mqmgr]
                if actSpec[1] == 'true':
                    if AdminTask.listWMQActivationSpecs(cellId).find(actSpecName) >= 0:
                        sop('modifyWMQActivationSpec' , 'Modifying existing activation spec %s' % actSpecName)
                        AdminTask.modifyWMQActivationSpec(actSpecConfigId, ['-name '+actSpecName+' -jndiName '+actSpecJndiName+' -destinationJndiName '+actSpecDestJndiName+' -destinationType javax.jms.Queue -qmgrName '+qmgr['qmgrName']+' -qmgrHostname '+qmgr['qmgrHostname']+' -qmgrPortNumber '+qmgr['qmgrPortNumber']+' -wmqTransportType CLIENT -qmgrSvrconnChannel '+qmgr['qmgrSvrconnChannel']+' -ccsid 819 -stopEndpointIfDeliveryFails false'+' -failureDeliveryCount 6'])
                    else:
                        sop('createWMQActivationSpec' , 'Adding new activation spec %s' % actSpecName)
                        AdminTask.createWMQActivationSpec(cellId, ['-name '+actSpecName+' -jndiName '+actSpecJndiName+' -destinationJndiName '+actSpecDestJndiName+' -destinationType javax.jms.Queue -qmgrName '+qmgr['qmgrName']+' -qmgrHostname '+qmgr['qmgrHostname']+' -qmgrPortNumber '+qmgr['qmgrPortNumber']+' -wmqTransportType CLIENT -qmgrSvrconnChannel '+qmgr['qmgrSvrconnChannel']+' -ccsid 819 -stopEndpointIfDeliveryFails false'+' -failureDeliveryCount 6'])


opf_create_queues(sabxctQueueList)

