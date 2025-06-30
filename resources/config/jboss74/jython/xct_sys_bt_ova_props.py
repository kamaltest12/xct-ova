from jboss_utils import CLIHelper, OverridableConfigParser

cli = CLIHelper()

xct_sys_bt_ova_props = {
    'com.clear2pay.ova.hideSearchLimitOverride': '-1',
    'com.clear2pay.ova.osgi.frameworkReadinessRetryLimit': '600'
}
cli.cd('/')
for key in xct_sys_bt_ova_props:
    cli.recreate('./system-property=%s' % key, {'value': xct_sys_bt_ova_props[key]})

cli.disconnect()
