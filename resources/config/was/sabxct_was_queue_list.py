# Definition of queues for sabxct
sabxctQueueList = [
     [
         'testQ', 'HK.OPY.MX2MT.01.REQUEST',
         [
             ['description', ''],
             ['persistence', 'PERSISTENT'],
             ['priority', 'APPLICATION_DEFINED'],
             ['expiry', 'APPLICATION_DEFINED,'],
             ['mqmdReadEnabled', 'TRUE'],
             ['mqmdWriteEnabled', 'TRUE']
         ], [
             ['maxSessions', '20'],
             ['maxRetries', '5'],
             ['maxMessages', '1']
         ],
         ['actSpecEnable', 'true'],
         'SenderQCFQMGR'  # qmgr reference
     ]
]
