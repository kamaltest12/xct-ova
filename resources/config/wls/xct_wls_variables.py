maxHeapSize = '9g'
maxPermSize = '2048m'

authenticationProviders = [
    {
        'name': 'OPF Person Registry',
        'class': 'com.clear2pay.bph.security.registry.login.OPFPersonRegistry',
        'attrs': { 'ControlFlag': 'OPTIONAL', 'bvaRegEx': '/BankVisibility/.*|/opfrest/.*|/xctrest/.*|/ova/.*' }
    },
    {
        'name': 'OPF Identity Trust',
        'class': 'com.clear2pay.bph.security.identification.login.OPFIdentityTrust',
        'attrs': { 'ControlFlag': 'OPTIONAL', 'bvaRegEx': '/BankVisibility/.*|/opfrest/.*|/xctrest/.*|/ova/.*' }
    },
    {
        'name': 'OPF Subject Credentials Propagation',
        'class': 'com.clear2pay.bph.security.identification.login.OPFSubjectCredentialsPropagation',
        'attrs': { 'ControlFlag': 'OPTIONAL' }
    },
    {
        'name': 'OPF Post-Authentication',
        'class': 'com.clear2pay.bph.security.session.OPFPostAuthentication',
        'attrs': { 'ControlFlag': 'OPTIONAL' }
    }
]

users.extend([
    { 'name': 'client', 'password': 'password', 'description': 'FSIS user', 'groups': ['Administrators'] }
])
