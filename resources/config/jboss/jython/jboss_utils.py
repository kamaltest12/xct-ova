from org.jboss.as.cli.scriptsupport import CLI
import ConfigParser
import os
import re
import time

class CLIHelper:
    """Wraps Java class org.jboss.as.cli.scriptsupport.CLI and adds convenience methods
    """

    address_prefix = ''
    reload_poll_interval = 5
    reload_timeout = 120

    def __init__(self):
        self.cli = CLI.newInstance()
        self.cli.connect()
        process_type = self.string_value(':read-attribute(name=process-type)')
        if process_type == 'Domain Controller':
            self.address_prefix = '/profile:full/'

    def cmd(self, command, raise_on_failure=True, echo=True):
        prefixed_command = command if not command.startswith('/') else '%s%s' % (self.address_prefix, command)
        if echo: print(prefixed_command)
        result = self.cli.cmd(prefixed_command)
        if not result.isSuccess() and raise_on_failure:
            raise RuntimeError(result.response.toJSONString(False))
        return result.response

    def cd(self, path):
        self.cmd('cd %s%s' % (self.address_prefix, path))

    def string_value(self, command):
        return self.cmd(command).get('result').asString()

    def exists(self, resource):
        response = self.cmd('%s:read-resource' % resource, False)
        if re.search('failed', str(response.get('outcome').asString())) and re.search('not found', str(response.get('failure-description').asString())):
            return False
        else:
            return True

    def delete_if_exists(self, resource):
        did_delete = False
        if self.exists(resource):
            self.cmd('%s:remove' % resource)
            did_delete = True
        else:
            print('[not found]')
        return did_delete

    def recreate(self, resource, attributes=None):
        if attributes is None: attributes = {}
        self.delete_if_exists(resource)
        self.add(resource, attributes)

    def add(self, resource, attributes=None):
        if attributes is None: attributes = {}
        command = '%s:add' % resource
        attr_list = [('%s=%s' % (k, v)) for k, v in attributes.items()]
        attr_string = ','.join(attr_list)
        if attr_string: command += '(%s)' % attr_string
        self.cmd(command)

    def reload(self):
        self.cmd('/:reload')
        start_time = time.time()
        running = False
        while not running:
            time.sleep(self.reload_poll_interval)
            response = self.cmd('/:read-attribute(name=server-state)', False)
            if response and response.has('result'):
                result = str(response.get('result').asString())
                print('[%s]' % result)
                if result == 'running':
                    running = True
            if time.time() - start_time > self.reload_timeout:
                raise RuntimeError('Server did not enter running status within %s seconds' % self.reload_timeout)

    def restart(self):
        self.cmd('/:shutdown(restart=true)')
        start_time = time.time()
        running = False
        while not running:
            time.sleep(self.reload_poll_interval)
            try:
                response = self.cmd('/:read-attribute(name=server-state)', False)
                if response and response.has('result'):
                    result = str(response.get('result').asString())
                    print('[%s]' % result)
                    if result == 'running':
                        running = True
            except:
                try:
                    self.cli.disconnect()
                except:
                    print('Disconnect error')
                try:
                    self.cli.connect()
                except:
                    print('Connect error')

            if time.time() - start_time > self.reload_timeout:
                raise RuntimeError('Server did not enter running status within %s seconds' % self.reload_timeout)

    def disconnect(self):
        self.cli.disconnect()


class OverridableConfigParser(ConfigParser.ConfigParser, object):
    """Overrides ConfigParser to allow settings to be overridden by environment variables e.g.
        parser.get('DB', 'host') will first check for DB_HOST then fall back to ini file
    """

    def __init__(self, ini_file=None):
        super(OverridableConfigParser, self).__init__()
        if ini_file:
            if not(os.path.isabs(ini_file)):
                script_dir = os.path.dirname(os.path.abspath(__file__))
                ini_file = os.path.join(script_dir, ini_file)
            self.read(ini_file)

    def get(self, section, setting):
        env_var_name = ('%s_%s' % (section, setting)).upper()
        if env_var_name in os.environ:
            return os.environ[env_var_name]
        else:
            return super(OverridableConfigParser, self).get(section, setting)
