def opf_create_jvm_variables(params):
    for name, value in params.items():
        createJvmProperty(nodeName, serverName, name, value)

opf_create_jvm_variables({
    # Disabling Deepsea by default
    'com.clear2pay.bph.opf.deepsea.enabled': 'false',
})
