# Actual creation of all queues
xctQueueList.extend(xctAMHQueueList)
for queue in xctQueueList:
    queueName = queue[0]
    queueJNDIName = 'jms/%s' % queue[1]
    cd('/JMSSystemResources/%s/JMSResource/%s/UniformDistributedQueues' % (bphJMSModuleName, bphJMSModuleName))
    cmo.createUniformDistributedQueue(queueName)
    cd('/JMSSystemResources/%s/JMSResource/%s/UniformDistributedQueues/%s' % (bphJMSModuleName, bphJMSModuleName, queueName))
    cmo.setDefaultTargetingEnabled(queueDefaultTargetingEnabled)
    cmo.setJNDIName(queueJNDIName)
    cd('/JMSSystemResources/%s/JMSResource/%s/UniformDistributedQueues/%s/DeliveryFailureParams/%s' % (bphJMSModuleName, bphJMSModuleName, queueName, queueName))
    # WAS has redelivery setting on listener ports, WLS just sets it on the queue
    listenerPortParams = queue[3]
    didSetRetries = False
    for param in listenerPortParams:
        if param[0] == 'maxRetries':
            cmo.setRedeliveryLimit(int(param[1]))
            didSetRetries = True
    if not didSetRetries:
        raise "Did not find a retries value for queue '%s'" % queueName