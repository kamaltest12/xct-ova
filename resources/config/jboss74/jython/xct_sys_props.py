from jboss_utils import CLIHelper, OverridableConfigParser

cli = CLIHelper()
environment = OverridableConfigParser('environment.ini')
xct_environment = OverridableConfigParser('xct_environment.ini')

xct_sys_props = {
    # XCT MDBS
    'com.clear2pay.opf.mdb.activationSpec.SwiftInterchangeLoaderMDB.qcfuser.name': environment.get('MDBActivationSpecs', 'qcfuser_name'),
    'com.clear2pay.opf.mdb.activationSpec.SwiftInterchangeLoaderMDB.qcfuser.password': environment.get('MDBActivationSpecs', 'qcfuser_password'),
    'com.clear2pay.opf.mdb.activationSpec.SwiftInterchangeLoaderMDB.maxPoolDepth': '5',
    'com.clear2pay.opf.mdb.activationSpec.SwiftInterchangeLoaderMDB.hostName': environment.get('MDBActivationSpecs', 'qcf_hostName'),
    'com.clear2pay.opf.mdb.activationSpec.SwiftInterchangeLoaderMDB.port': environment.get('MDBActivationSpecs', 'qcf_port'),
    'com.clear2pay.opf.mdb.activationSpec.SwiftInterchangeLoaderMDB.channel': environment.get('MDBActivationSpecs', 'qcf_channel'),
    'com.clear2pay.opf.mdb.activationSpec.SwiftInterchangeLoaderMDB.transportType': environment.get('MDBActivationSpecs', 'qcf_transportType'),
    'com.clear2pay.opf.mdb.activationSpec.SwiftInterchangeLoaderMDB.queueManager': environment.get('MDBActivationSpecs', 'qcf_queueManager'),

    'com.clear2pay.opf.mdb.activationSpec.TransportReceiptMDB.qcfuser.name': environment.get('MDBActivationSpecs', 'qcfuser_name'),
    'com.clear2pay.opf.mdb.activationSpec.TransportReceiptMDB.qcfuser.password': environment.get('MDBActivationSpecs', 'qcfuser_password'),
    'com.clear2pay.opf.mdb.activationSpec.TransportReceiptMDB.maxPoolDepth': '5',
    'com.clear2pay.opf.mdb.activationSpec.TransportReceiptMDB.hostName': environment.get('MDBActivationSpecs', 'qcf_hostName'),
    'com.clear2pay.opf.mdb.activationSpec.TransportReceiptMDB.port': environment.get('MDBActivationSpecs', 'qcf_port'),
    'com.clear2pay.opf.mdb.activationSpec.TransportReceiptMDB.channel': environment.get('MDBActivationSpecs', 'qcf_channel'),
    'com.clear2pay.opf.mdb.activationSpec.TransportReceiptMDB.transportType': environment.get('MDBActivationSpecs', 'qcf_transportType'),
    'com.clear2pay.opf.mdb.activationSpec.TransportReceiptMDB.queueManager': environment.get('MDBActivationSpecs', 'qcf_queueManager'),

    'com.clear2pay.opf.mdb.activationSpec.ForexServiceMDB.qcfuser.name': environment.get('MDBActivationSpecs', 'qcfuser_name'),
    'com.clear2pay.opf.mdb.activationSpec.ForexServiceMDB.qcfuser.password': environment.get('MDBActivationSpecs', 'qcfuser_password'),
    'com.clear2pay.opf.mdb.activationSpec.ForexServiceMDB.maxPoolDepth': '5',
    'com.clear2pay.opf.mdb.activationSpec.ForexServiceMDB.hostName': environment.get('MDBActivationSpecs', 'qcf_hostName'),
    'com.clear2pay.opf.mdb.activationSpec.ForexServiceMDB.port': environment.get('MDBActivationSpecs', 'qcf_port'),
    'com.clear2pay.opf.mdb.activationSpec.ForexServiceMDB.channel': environment.get('MDBActivationSpecs', 'qcf_channel'),
    'com.clear2pay.opf.mdb.activationSpec.ForexServiceMDB.transportType': environment.get('MDBActivationSpecs', 'qcf_transportType'),
    'com.clear2pay.opf.mdb.activationSpec.ForexServiceMDB.queueManager': environment.get('MDBActivationSpecs', 'qcf_queueManager'),

    'com.clear2pay.opf.mdb.activationSpec.ReconciliationTimeoutMDB.qcfuser.name': environment.get('MDBActivationSpecs', 'qcfuser_name'),
    'com.clear2pay.opf.mdb.activationSpec.ReconciliationTimeoutMDB.qcfuser.password': environment.get('MDBActivationSpecs', 'qcfuser_password'),
    'com.clear2pay.opf.mdb.activationSpec.ReconciliationTimeoutMDB.maxPoolDepth': '5',
    'com.clear2pay.opf.mdb.activationSpec.ReconciliationTimeoutMDB.hostName': environment.get('MDBActivationSpecs', 'qcf_hostName'),
    'com.clear2pay.opf.mdb.activationSpec.ReconciliationTimeoutMDB.port': environment.get('MDBActivationSpecs', 'qcf_port'),
    'com.clear2pay.opf.mdb.activationSpec.ReconciliationTimeoutMDB.channel': environment.get('MDBActivationSpecs', 'qcf_channel'),
    'com.clear2pay.opf.mdb.activationSpec.ReconciliationTimeoutMDB.transportType': environment.get('MDBActivationSpecs', 'qcf_transportType'),
    'com.clear2pay.opf.mdb.activationSpec.ReconciliationTimeoutMDB.queueManager': environment.get('MDBActivationSpecs', 'qcf_queueManager'),

    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationServiceMDB.qcfuser.name': environment.get('MDBActivationSpecs', 'qcfuser_name'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationServiceMDB.qcfuser.password': environment.get('MDBActivationSpecs', 'qcfuser_password'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationServiceMDB.maxPoolDepth': '5',
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationServiceMDB.hostName': environment.get('MDBActivationSpecs', 'qcf_hostName'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationServiceMDB.port': environment.get('MDBActivationSpecs', 'qcf_port'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationServiceMDB.channel': environment.get('MDBActivationSpecs', 'qcf_channel'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationServiceMDB.transportType': environment.get('MDBActivationSpecs', 'qcf_transportType'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationServiceMDB.queueManager': environment.get('MDBActivationSpecs', 'qcf_queueManager'),

    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationCandidateServiceMDB.qcfuser.name': environment.get('MDBActivationSpecs', 'qcfuser_name'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationCandidateServiceMDB.qcfuser.password': environment.get('MDBActivationSpecs', 'qcfuser_password'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationCandidateServiceMDB.maxPoolDepth': '5',
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationCandidateServiceMDB.hostName': environment.get('MDBActivationSpecs', 'qcf_hostName'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationCandidateServiceMDB.port': environment.get('MDBActivationSpecs', 'qcf_port'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationCandidateServiceMDB.channel': environment.get('MDBActivationSpecs', 'qcf_channel'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationCandidateServiceMDB.transportType': environment.get('MDBActivationSpecs', 'qcf_transportType'),
    'com.clear2pay.opf.mdb.activationSpec.GPIEndOfDayConfirmationCandidateServiceMDB.queueManager': environment.get('MDBActivationSpecs', 'qcf_queueManager'),

    'com.clear2pay.opf.mdb.activationSpec.AMHMTTransportReceiptMDB.qcfuser.name': environment.get('MDBActivationSpecs', 'qcfuser_name'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTTransportReceiptMDB.qcfuser.password': environment.get('MDBActivationSpecs', 'qcfuser_password'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTTransportReceiptMDB.maxPoolDepth': '5',
    'com.clear2pay.opf.mdb.activationSpec.AMHMTTransportReceiptMDB.hostName': environment.get('MDBActivationSpecs', 'qcf_hostName'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTTransportReceiptMDB.port': environment.get('MDBActivationSpecs', 'qcf_port'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTTransportReceiptMDB.channel': environment.get('MDBActivationSpecs', 'qcf_channel'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTTransportReceiptMDB.transportType': environment.get('MDBActivationSpecs', 'qcf_transportType'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTTransportReceiptMDB.queueManager': environment.get('MDBActivationSpecs', 'qcf_queueManager'),


    'com.clear2pay.opf.mdb.activationSpec.AMHMXTransportReceiptMDB.qcfuser.name': environment.get('MDBActivationSpecs', 'qcfuser_name'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXTransportReceiptMDB.qcfuser.password': environment.get('MDBActivationSpecs', 'qcfuser_password'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXTransportReceiptMDB.maxPoolDepth': '5',
    'com.clear2pay.opf.mdb.activationSpec.AMHMXTransportReceiptMDB.hostName': environment.get('MDBActivationSpecs', 'qcf_hostName'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXTransportReceiptMDB.port': environment.get('MDBActivationSpecs', 'qcf_port'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXTransportReceiptMDB.channel': environment.get('MDBActivationSpecs', 'qcf_channel'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXTransportReceiptMDB.transportType': environment.get('MDBActivationSpecs', 'qcf_transportType'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXTransportReceiptMDB.queueManager': environment.get('MDBActivationSpecs', 'qcf_queueManager'),

    'com.clear2pay.opf.mdb.activationSpec.AMHMTBusinessMessageMDB.qcfuser.name': environment.get('MDBActivationSpecs', 'qcfuser_name'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTBusinessMessageMDB.qcfuser.password': environment.get('MDBActivationSpecs', 'qcfuser_password'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTBusinessMessageMDB.maxPoolDepth': '5',
    'com.clear2pay.opf.mdb.activationSpec.AMHMTBusinessMessageMDB.hostName': environment.get('MDBActivationSpecs', 'qcf_hostName'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTBusinessMessageMDB.port': environment.get('MDBActivationSpecs', 'qcf_port'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTBusinessMessageMDB.channel': environment.get('MDBActivationSpecs', 'qcf_channel'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTBusinessMessageMDB.transportType': environment.get('MDBActivationSpecs', 'qcf_transportType'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMTBusinessMessageMDB.queueManager': environment.get('MDBActivationSpecs', 'qcf_queueManager'),

    'com.clear2pay.opf.mdb.activationSpec.AMHMXBusinessMessageMDB.qcfuser.name': environment.get('MDBActivationSpecs', 'qcfuser_name'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXBusinessMessageMDB.qcfuser.password': environment.get('MDBActivationSpecs', 'qcfuser_password'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXBusinessMessageMDB.maxPoolDepth': '5',
    'com.clear2pay.opf.mdb.activationSpec.AMHMXBusinessMessageMDB.hostName': environment.get('MDBActivationSpecs', 'qcf_hostName'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXBusinessMessageMDB.port': environment.get('MDBActivationSpecs', 'qcf_port'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXBusinessMessageMDB.channel': environment.get('MDBActivationSpecs', 'qcf_channel'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXBusinessMessageMDB.transportType': environment.get('MDBActivationSpecs', 'qcf_transportType'),
    'com.clear2pay.opf.mdb.activationSpec.AMHMXBusinessMessageMDB.queueManager': environment.get('MDBActivationSpecs', 'qcf_queueManager'),


    'xct.rest.base.url': xct_environment.get('URLS', 'rest'),
    'com.clear2pay.ova.opf.client.api.url': xct_environment.get('URLS', 'rest'),

    'jboss.as.management.blocking.timeout':  xct_environment.get('DEPLOYMENT', 'timeout'),

    'com.arjuna.ats.arjuna.coordinator.defaultTimeout':  xct_environment.get('TRANSACTION', 'timeout'),
    'com.arjuna.ats.arjuna.coordinator.txReaperTimeout': xct_environment.get('TRANSACTION', 'reaperTimeout'),

    'com.clear2pay.opfpayment.fsis.riskassessment.rest.callback.url': xct_environment.get('URLS', 'fsis_callback'),
    'xct.fxs.rest.base.url': xct_environment.get('URLS', 'fxs'),
    'xct.fxs.rest.timeout': xct_environment.get('URLS', 'fxs_timeout'),
    'xct.pcs.rest.base.url': xct_environment.get('URLS', 'pcs'),
    'xct.pcs.rest.timeout': xct_environment.get('URLS', 'pcs_timeout'),
    'xct.universal.execution.callback.rest.base.url': xct_environment.get('URLS', 'universal_execution_callback'),
    'xct.universal.execution.rest.base.url': xct_environment.get('URLS', 'universal_execution'),
    'com.clear2pay.xct.api.client.base.url.CHANNELS': xct_environment.get('URLS', 'channels'),
    'xct.nacas.rest.base.url': xct_environment.get('URLS', 'nacas'),
    'xct.nacas.rest.timeout': xct_environment.get('URLS', 'nacas_timeout'),

    'xct.fxs.rest.always.trust': xct_environment.get('URLS', 'fxs_rest_always_trust'),
    'xct.pcs.rest.always.trust': xct_environment.get('URLS', 'pcs_rest_always_trust'),
    'xct.pom.rest.always.trust': xct_environment.get('URLS', 'pom_rest_always_trust'),
    'xct.cbis.async.rest.always.trust': xct_environment.get('URLS', 'cbis_async_rest_always_trust'),
    'xct.cbis.rest.always.trust': xct_environment.get('URLS', 'cbis_rest_always_trust'),
    'xct.fsis.risk.assessment.rest.always.trust': xct_environment.get('URLS', 'fsis_risk_assessment_rest_always_trust'),
    'xct.nacas.rest.always.trust': xct_environment.get('URLS', 'xct_nacas_rest_always_trust')
}
cli.cd('/')
for key in xct_sys_props:
    cli.recreate('./system-property=%s' % key, {'value': xct_sys_props[key]})

cli.cd('/subsystem=deployment-scanner/scanner=default')
cli.cmd(':write-attribute(name=deployment-timeout,value=600)')
cli.cd('/subsystem=transactions')
cli.cmd(':write-attribute(name=default-timeout,value=600)')

cli.disconnect()
