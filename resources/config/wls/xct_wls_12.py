if targetServer == 'AdminServer':
    cd('/Servers/AdminServer')
    cmo.setStuckThreadMaxTime(1500)

if deploy_env == 'CI':
    adminServerMBeanPath = '/Servers/AdminServer'
    adminServerMBean = getMBean(adminServerMBeanPath)
    adminServerMBean.setStuckThreadMaxTime(1500)

if deploy_env == 'DEV':
    cd('/Servers/soa_server1')
    cmo.setStuckThreadMaxTime(1500)
save()
activate(block='true')
startEdit()