import shutil
import os

print('Copy Keystore %s' %os.environ['DIR_OPTS_JKS_DIR'])

# if os.path.exists('%s' %DIR_OPTS_JKS_DIR):
shutil.copytree('%s' %os.environ['DIR_OPTS_JKS_DIR'], '/opt/jboss/jks/')
# else:
#     shutil.copytree('/tmp/delivery/jks/', '/opt/jboss/jks/')