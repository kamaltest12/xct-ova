# Definition of queues for AMH
xctAMHQueueList=[]
for queue in ['AMHSenderMTQ','AMHReceiverAckMTQ', 'AMHReceiverMTQ', 'AMHSenderAckMTQ', 'AMHSenderMXQ', 'AMHReceiverAckMXQ','AMHReceiverMXQ','AMHSenderAckMXQ']:
    xctAMHQueueList.append([
        queue, queue,
        [
            ['description', ''],
            ['persistence', 'PERSISTENT'],
            ['priority', 'APPLICATION_DEFINED'],
            ['expiry', 'APPLICATION_DEFINED']
        ],
        [
            ['maxSessions', '20'],
            ['maxRetries', '5'],
            ['maxMessages', '1']
        ],
        ['actSpecEnable', 'true'],
        'WHITEQMGR'  # qmgr reference
    ])