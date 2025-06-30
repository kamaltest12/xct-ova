queues = [
    {'name': 'AccountingQ'},
    {'name': 'DataImportQ'},
    {'name': 'DewarehousingQ'},
    {'name': 'InterchangeLoaderQ','arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'InterfacingReplyQ'},
    {'name': 'SOInitiationQ'},
    {'name': 'BillingQ'},
    {'name': 'OutgoingInitiationQ'}
]

myqcf_queues = [
    {'name': 'BPELInvokerQ'},
    {'name': 'TimeoutReceiptQ'},
    {'name': 'NotificationQ'},
    {'name': 'ParserQ'},
    {'name': 'InterfacingHeraldQ'},
    {'name': 'InterfacingRequestQ'},
    {'name': 'RestSubmissionQ'},
    {'name': 'Urgency1BPELInvokerQ'},
    {'name': 'Urgency1ParserQ'},
    {'name': 'TechExceptionRetryQ'},
    {'name': 'ReplyToRestResponseQ'},
    {'name': 'InterfacingNotifyQ'},
    {'name': 'HandoverInterchangeLoaderQ', 'arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'HandoverInterfacingReplyQ'},
    {'name': 'ChannelQ'},
    {'name': 'CISBPELInvokerQ'},
    {'name': 'CISDewarehousingQ'},
    {'name': 'CISNotificationQ'},
    {'name': 'CISParserQ'},
    {'name': 'CISTransportReceiptQ'},
    {'name': 'TestPlatformIntegration1Q'},
    {'name': 'TestPlatformIntegration2Q'},
    {'name': 'CoralBOEQ'},
    {'name': 'SanctionsCheckQ'},
    {'name': 'FraudCheckQ'},
    {'name': 'CoralDummyTechExceptionTesterQ'},
    {'name': 'FromSWIFTAckQ'},
    {'name': 'OPFNotificationQ'},
    {'name': 'OPFOnlineParserQ'},
    {'name': 'SenderFallbackQ'},
    {'name': 'SenderQ', 'arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'TestNotificationQ'},
    {'name': 'TransportReceiptQ', 'arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'Urgency8BPELInvokerQ'},
    {'name': 'Urgency8InterchangeLoaderQ'},
    {'name': 'Urgency8ParserQ'},
    {'name': 'InterchangeLoaderReplyToQ'},
    {'name': 'SenderReplyToQ'},
    {'name': 'LBSender1Q'},
    {'name': 'LBSender2Q'},
    {'name': 'LBSender3Q'},
    {'name': 'LBSender4Q'},
    {'name': 'LBSenderAck1Q'},
    {'name': 'LBSenderAck2Q'},
    {'name': 'LBSenderAck3Q'},
    {'name': 'LBSenderAck4Q'},
    {'name': 'LBInterchangeLoader1Q'},
    {'name': 'LBInterchangeLoader2Q'},
    {'name': 'LBInterchangeLoader3Q'},
    {'name': 'LBInterchangeLoader4Q'},
    {'name': 'LBInterchangeLoaderAck1Q'},
    {'name': 'LBInterchangeLoaderAck2Q'},
    {'name': 'LBInterchangeLoaderAck3Q'},
    {'name': 'LBInterchangeLoaderAck4Q'},
    {'name': 'LBSWIFTAGISender1Q', 'arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'LBSWIFTAGISender2Q', 'arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'LBSWIFTAGIInboundAck1Q', 'arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'LBSWIFTAGIInboundAck2Q', 'arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'LBSWIFTAGIInterchangeLoader1Q', 'arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'LBSWIFTAGIInterchangeLoader2Q', 'arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'LBInterchangeLoaderReplyTo1Q'},
    {'name': 'LBInterchangeLoaderReplyTo2Q'},
    {'name': 'LBInterchangeLoaderReplyTo3Q'},
    {'name': 'LBInterchangeLoaderReplyTo4Q'},
    {'name': 'EventInitiationQ'},
    {'name': 'EventSenderQ'},
    {'name': 'KafkaIntermediateEventSenderQ'},
    {'name': 'KafkaEventSenderQ'},
    {'name': 'HandoverSWIFTSAAInterchangeLoaderQ'},
    {'name': 'SAFRestPaymentUploadQ'},
    {'name': 'SAFPriority0Q'},
    {'name': 'SAFPriority1Q'},
    {'name': 'SAFPriority2Q'},
    {'name': 'SAFPriority3Q'},
    {'name': 'SAFPriority4Q'},
    {'name': 'SAFPriority5Q'},
    {'name': 'SAFPriority6Q'},
    {'name': 'SAFPriority7Q'},
    {'name': 'SAFPriority8Q'},
    {'name': 'SAFPriority9Q'}
]

myqcf_qcf_names = ['MYQCF', 'myqcf']

otherqcf_queues = [
    {'name': 'OtherHandoverInterchangeLoaderQ','baseQname': 'HandoverInterchangeLoaderQ', 'arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'OtherHandoverInterfacingReplyQ','baseQname': 'HandoverInterfacingReplyQ'},
    {'name': 'OtherHandoverSWIFTSAAInterchangeLoaderQ','baseQname': 'HandoverSWIFTSAAInterchangeLoaderQ'}
]

otherqcf_qcf_names = ['OTHERQCF', 'otherqcf']

lb_qcf_names = ['QCF1', 'qcf1', 'QCF2', 'qcf2', 'QCF3', 'qcf3', 'QCF4', 'qcf4']

swiftagi_qcf_names = ['QCFSWIFTAGI1', 'qcfswiftagi1', 'QCFSWIFTAGI2', 'qcfswiftagi2']

ist_queues = [
    {'name': 'ISTInterchangeLoaderQ'},
    {'name': 'ISTSenderQ'}
]

ist_qcf_names = ['ISTQCF']

swiftsaa_queues = [
    {'name': 'SWIFTSAAInterchangeLoaderQ','messageBodyStyle': 'MQ','arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'},
    {'name': 'SWIFTSAASenderQ','messageBodyStyle': 'MQ','arbitraryProperties': '"mdReadEnabled=\\"true\\",mdWriteEnabled=\\"true\\""'}
]

swiftsaa_qcf_names = ['SWIFTSAAQCF']
