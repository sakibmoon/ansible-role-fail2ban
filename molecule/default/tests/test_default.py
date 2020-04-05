import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_fail2ban_package(host):
    fail2ban = host.package('fail2ban')
    assert fail2ban.is_installed


def test_fail2ban_service(host):
    fail2ban = host.service('fail2ban')

    assert fail2ban.is_running
    assert fail2ban.is_enabled


def test_filterfile(host):
    filterone = host.file('/etc/fail2ban/filter.d/filterone.local')
    assert filterone.exists
    assert filterone.is_file
    assert b'actionstart = never start' in filterone.content


def test_actionfile(host):
    actionone = host.file('/etc/fail2ban/action.d/actionone.conf')
    content = actionone.content

    assert actionone.exists
    assert actionone.is_file
    assert b'[Init]\n\ntimestart = 0' in content


def test_fail2ban_jailed(host):
    cmd = host.run('fail2ban-client status sshd')
    assert cmd.rc == 0
    assert cmd.succeeded
