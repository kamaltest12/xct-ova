# Definition of queues for XCT

xctQueueList = [
    [
        'FromSWIFTQ', 'FromSWIFTQ',
        [
            ['description', ''],
            ['persistence', 'PERSISTENT'],
            ['priority', 'APPLICATION_DEFINED'],
            ['expiry', 'APPLICATION_DEFINED,']
        ], [
            ['maxSessions', '20'],
            ['maxRetries', '5'],
            ['maxMessages', '1']
        ],
        ['actSpecEnable', 'true'],
        'WHITEQMGR'  # qmgr reference
    ],
    [
        'ManualReconciliationQ', 'ManualReconciliationQ',
        [
            ['description', ''],
            ['persistence', 'PERSISTENT'],
            ['priority', 'APPLICATION_DEFINED'],
            ['expiry', 'APPLICATION_DEFINED,']
        ], [
            ['maxSessions', '20'],
            ['maxRetries', '5'],
            ['maxMessages', '1']
        ],
        ['actSpecEnable', 'true'],
        'WHITEQMGR'  # qmgr reference
    ],
    [
        'PublishRateQ', 'PublishRateQ',
        [
            ['description', ''],
            ['persistence', 'PERSISTENT'],
            ['priority', 'APPLICATION_DEFINED'],
            ['expiry', 'APPLICATION_DEFINED,']
        ], [
            ['maxSessions', '20'],
            ['maxRetries', '5'],
            ['maxMessages', '1']
        ],
        ['actSpecEnable', 'true'],
        'WHITEQMGR'  # qmgr reference
    ],
    [
        'GPIEndOfDayConfirmationQ', 'GPIEndOfDayConfirmationQ',
        [
            ['description', ''],
            ['persistence', 'PERSISTENT'],
            ['priority', 'APPLICATION_DEFINED'],
            ['expiry', 'APPLICATION_DEFINED,']
        ], [
            ['maxSessions', '20'],
            ['maxRetries', '5'],
            ['maxMessages', '1']
        ],
        ['actSpecEnable', 'true'],
        'WHITEQMGR'  # qmgr reference
    ],
    [
        'GPIEndOfDayConfirmationCandidateQ', 'GPIEndOfDayConfirmationCandidateQ',
        [
            ['description', ''],
            ['persistence', 'PERSISTENT'],
            ['priority', 'APPLICATION_DEFINED'],
            ['expiry', 'APPLICATION_DEFINED,']
        ], [
            ['maxSessions', '20'],
            ['maxRetries', '5'],
            ['maxMessages', '1']
        ],
        ['actSpecEnable', 'true'],
        'WHITEQMGR'  # qmgr reference
    ]
]
