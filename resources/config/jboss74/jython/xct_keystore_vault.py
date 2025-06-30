from jboss_utils import CLIHelper, OverridableConfigParser
import os
import shutil
import subprocess

environment = OverridableConfigParser('xct_environment.ini')
cli = CLIHelper()

ks_attrs = {
    'KEYSTORE_ALIAS': 'OPF',
    'ENC_FILE_DIR': '/opt/jboss/vault/',
    'KEYSTORE_URL': environment.get('Vault', 'keystore_url'),
    'KEYSTORE_PASSWORD': 'password',
    'SALT': environment.get('Vault', 'salt'),
    'ITERATION_COUNT': environment.get('Vault', 'iteration_count'),
    'KEY_SIZE': environment.get('Vault', 'key_size')
}
print('Recreating directory: %s' % ks_attrs['ENC_FILE_DIR'])
if os.path.exists(ks_attrs['ENC_FILE_DIR']):
    shutil.rmtree(ks_attrs['ENC_FILE_DIR'], ignore_errors=True)
os.makedirs(ks_attrs['ENC_FILE_DIR'])
generate_secret_key_command = \
    '$JAVA_HOME/bin/keytool -genseckey -alias %s -storetype jceks -keyalg AES -keysize %s -storepass %s -keypass %s -keystore %s' % \
    (ks_attrs['KEYSTORE_ALIAS'], ks_attrs['KEY_SIZE'], ks_attrs['KEYSTORE_PASSWORD'], ks_attrs['KEYSTORE_PASSWORD'], ks_attrs['KEYSTORE_URL'])
print('About to run: %s' % generate_secret_key_command)
rc = os.system(generate_secret_key_command)
if rc != 0:
    raise RuntimeError('Failed to generate secret key - see output above for details')

# Vault
vault_attrs = {
    'cbis': {'credential': environment.get('Vault', 'cbis_password')},
    'sanctions_check': {'credential': environment.get('Vault', 'sanctions_check_password')},
    'payment_upload_push': {'credential': environment.get('Vault', 'payment_upload_push_password')},
    'fsis': {'credential': environment.get('Vault', 'fsis_password')},
    'fxs': {'credential': environment.get('Vault', 'fxs_password')},
    'nacas': {'credential': environment.get('Vault', 'nacas_password')},
    'pcs': {'credential': environment.get('Vault', 'pcs_password')}
}
for key in vault_attrs:
    for vault_item in vault_attrs[key]:
        vault_command = \
            "$JBOSS_HOME/bin/vault.sh " \
            "--keystore '%s' " \
            "--keystore-password '%s' " \
            "--alias '%s' " \
            "-e '%s' " \
            "--iteration '%s' " \
            "--salt '%s' " \
            "--vault-block '%s' " \
            "--attribute '%s' " \
            "--sec-attr '%s' > /opt/jboss/vault/log" % \
            (ks_attrs['KEYSTORE_URL'], ks_attrs['KEYSTORE_PASSWORD'], ks_attrs['KEYSTORE_ALIAS'], ks_attrs['ENC_FILE_DIR'],
             ks_attrs['ITERATION_COUNT'], ks_attrs['SALT'], key, vault_item, vault_attrs[key][vault_item])
        print('About to run: %s' % vault_command)
        subprocess.check_output(vault_command, shell=True)
mask_password_command = "cat %slog | grep KEYSTORE_PASSWORD | sed 's/.*\"\\(MASK-[^\"]*\\)\".*/\\1/' | head -n 1" % ks_attrs['ENC_FILE_DIR']
print('About to run: %s' % mask_password_command)
masked_password = subprocess.check_output(mask_password_command, shell=True).rstrip()
ks_attrs['KEYSTORE_PASSWORD'] = masked_password
vault_options = '[' + ','.join(['"%s" => "%s"' % (k, v) for k, v in ks_attrs.items()]) + ']'
cli.recreate('/core-service=vault', {'vault-options': vault_options, 'name': 'vault'})

cli.disconnect()
