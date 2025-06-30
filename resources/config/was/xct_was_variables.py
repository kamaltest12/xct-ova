jaasLoginModules = [

    {
        'name': 'jaasLoginModulesWebInbound',
        'alias': 'WEB_INBOUND',
        'modules': [
                        ['com.clear2pay.bph.security.registry.login.PersonRegistryLoginModule ', [['bvaRegEx', '/BankVisibility/.*|/opfrest/.*|/xctrest/.*|/ova/.*']]],
                        ['com.clear2pay.bph.security.identification.login.OPFIdentityTrustLoginModule', [['bvaRegEx', '/BankVisibility/.*|/opfrest/.*|/xctrest/.*|/ova/.*']]],
                        ['com.ibm.ws.security.server.lm.ltpaLoginModule', []],
                        ['com.ibm.ws.security.server.lm.wsMapDefaultInboundLoginModule', []],
                        ['com.clear2pay.bph.security.identification.login.SubjectCredentialsPropagationLoginModule', []],
                        ['com.clear2pay.bph.security.session.PostAuthenticationLoginModule', []]
                    ]
    },
    {
        'name': 'jaasLoginModulesRmiInbound',
        'alias': 'RMI_INBOUND',
        'modules': [
                        ['com.clear2pay.bph.security.registry.login.PersonRegistryLoginModule', []],
                        ['com.clear2pay.bph.security.identification.login.OPFIdentityTrustLoginModule', []],
                        ['com.ibm.ws.security.server.lm.ltpaLoginModule', []],
                        ['com.ibm.ws.security.server.lm.wsMapDefaultInboundLoginModule', []],
                        ['com.ibm.ws.wssecurity.platform.websphere.wssapi.token.impl.wssTokenPropagationInboundLoginModule', []],
                        ['com.clear2pay.bph.security.identification.login.SubjectCredentialsPropagationLoginModule', []]
                    ]
    },
    {
        'name': 'jaasLoginModulesWSLogin',
        'alias': 'WSLogin',
        'modules': [
                        ['com.clear2pay.bph.security.registry.login.PersonRegistryLoginModule', []],
                        ['com.clear2pay.bph.security.identification.login.OPFIdentityTrustLoginModule', []],
                        ['com.ibm.ws.security.server.lm.ltpaLoginModule', []],
                        ['com.ibm.ws.security.server.lm.wsMapDefaultInboundLoginModule', []],
                        ['com.ibm.ws.wssecurity.platform.websphere.wssapi.token.impl.wssTokenPropagationInboundLoginModule', []],
                        ['com.clear2pay.bph.security.identification.login.SubjectCredentialsPropagationLoginModule', []]
                    ]
    },
]

#Log level details
traceSpecsOPF = "com.clear2pay.bph.*=info: "