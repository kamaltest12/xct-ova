from jboss_utils import CLIHelper

cli = CLIHelper()

security_domain = 'opf-domain'
login_modules = {
    'OPFInternalLoginModule': {
        'code': 'com.clear2pay.bph.security.identification.login.OPFInternalLoginModule',
        'flag': 'required',
        'module-options': {}
    },
    'PersonRegistryLoginModule': {
        'code': 'com.clear2pay.bph.security.registry.login.PersonRegistryLoginModule',
        'flag': 'required',
        'module-options': {'bvaRegEx': '/BankVisibility/.*|/opfrest/.*|/xctrest/.*|/ova/.*'}
    },
    'OPFIdentityTrustLoginModule': {
        'code': 'com.clear2pay.bph.security.identification.login.OPFIdentityTrustLoginModule',
        'flag': 'required',
        'module-options': {'bvaRegEx': '/BankVisibility/.*|/opfrest/.*|/xctrest/.*|/ova/.*'}
    },
    'SubjectCredentialsPropagationLoginModule': {
        'code': 'com.clear2pay.bph.security.identification.login.SubjectCredentialsPropagationLoginModule',
        'flag': 'required',
        'module-options': {}
    },
    'PostAuthenticationLoginModule': {
        'code': 'com.clear2pay.bph.security.session.PostAuthenticationLoginModule',
        'flag': 'required',
        'module-options': {}
    }
}
cli.cd('/subsystem=security')
for key in login_modules:
    cli.delete_if_exists('./security-domain=opf-domain/authentication=classic/login-module=%s' % key)
cli.recreate('./security-domain=opf-domain', {'cache-type': 'default'})
cli.cd('./security-domain=opf-domain')
cli.add('./authentication=classic', {'cache-type': 'default'})
cli.cd('./authentication=classic')
for key in login_modules:
    cli.add('./login-module=%s' % key, {'code': login_modules[key]['code'], 'flag': login_modules[key]['flag'], 'module-options': {}})
    module_options = '[' + ','.join(['"%s" => "%s"' % (k, v) for k, v in login_modules[key]['module-options'].items()]) + ']'
    cli.cmd('./login-module=%s:write-attribute(name=module-options,value=%s)' % (key, str(module_options)))

security_domain = 'opf-internal-domain'
login_modules_internal = {
    'OPFInternalLoginModule': {
        'code': 'com.clear2pay.bph.security.identification.login.OPFInternalLoginModule',
        'flag': 'required',
        'module-options': {}
    },
    'OPFIdentityTrustLoginModule': {
        'code': 'com.clear2pay.bph.security.identification.login.OPFIdentityTrustLoginModule',
        'flag': 'required',
        'module-options': {}
    },
    'SubjectCredentialsPropagationLoginModule': {
        'code': 'com.clear2pay.bph.security.identification.login.SubjectCredentialsPropagationLoginModule',
        'flag': 'required',
        'module-options': {}
    },
    'PostAuthenticationLoginModule': {
        'code': 'com.clear2pay.bph.security.session.PostAuthenticationLoginModule',
        'flag': 'required',
        'module-options': {}
    }
}
cli.cd('/subsystem=security')
for key in login_modules_internal:
    cli.delete_if_exists('./security-domain=opf-internal-domain/authentication=classic/login-module=%s' % key)
cli.recreate('./security-domain=opf-internal-domain', {'cache-type': 'default'})
cli.cd('./security-domain=opf-internal-domain')
cli.add('./authentication=classic', {'cache-type': 'default'})
cli.cd('./authentication=classic')
for key in login_modules_internal:
    cli.add('./login-module=%s' % key, {'code': login_modules[key]['code'], 'flag': login_modules[key]['flag'], 'module-options': {}})
    module_options = '[' + ','.join(['"%s" => "%s"' % (k, v) for k, v in login_modules[key]['module-options'].items()]) + ']'
    cli.cmd('./login-module=%s:write-attribute(name=module-options,value=%s)' % (key, str(module_options)))

cli.disconnect()
