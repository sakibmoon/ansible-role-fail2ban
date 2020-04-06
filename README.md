Role Name
=========

[![Ansible Galaxy](https://img.shields.io/ansible/role/47677.svg?style=flat&logo=ansible)](https://galaxy.ansible.com/sakibmoon/fail2ban)   [![Build Status](https://travis-ci.com/sakibmoon/ansible-role-fail2ban.svg?branch=master)](https://travis-ci.com/sakibmoon/ansible-role-fail2ban)    
An ansible role to install and manage Fail2ban

Requirements
------------

Ansible version 2.6 or later


Installation
------------

### Ansible Galaxy

Use `ansible-galaxy install sakibmoon.fail2ban`

### Git

Use `git clone https://github.com/sakibmoon/ansible-role-fail2ban.git`


Basic Usage
-----------

Install and enable fail2ban and configure ssh with fail2ban

``` yaml
    - hosts: servers
      vars:
        fail2ban_services:
          - name: "sshd"
            enabled: "true"
            port: "ssh"
            filter: "sshd"
            logpath: "/var/log/auth.log"
            maxretry: 6       
      roles:
         - sakibmoon.fail2ban
```

See [Role Variables](#role-varialbes) and [Example Playbook](#example-playbook) for more complex Usecase and how you can finetune all the options

Role Variables
--------------

### Service Monitor Options

`fail2ban_services`<br>
A list of Services to monitor by fail2ban. Every list option must contain service name, logpath. Only specify the settings you want to change. The rest of the configuration will come from global jail configuration as seen/set [here](#global-jail-configuration-option).

Service options:

`name`: Name of the Service<br>
`logpath`: Logpath of the service to monitor<br>
`port`: Comma separated ports to monitor<br>
`enabled`: Whether to enable this jail<br>

### Action List

`fail2ban_actionlist`<br>
A list of action to create. The actions are saved in `/etc/fail2ban/action.d/` directory. A single action can contain following options:

`name`: Action name. The name of the file.<br>
`sections`: A list of sections like `Definition`, `Init` etc wchih contains dictionary of entries<br>
`file_ext`: (Optional) The file extionsion. Can be either `local` or `conf`. Default: `local`

Example:

``` yaml
    fail2ban_actionlist:
      - name: toy-action1
        sections:
          - name: Definition
            options:
              - name: actionstart
                value: "ActionStart value"
              - name: actionflush
                value: "Actionflush value"
          - name: Init
            options:
              - name: timeout
                value: "timeout value"
        file_ext: "local"
      - name: toy-action2
        sections:
          - name: INCLUDES
            options:
              - name: before
                value: something-to-include.local
          - name: Definition
            options:
              - name: actionstart
                value: "ActionStart value"
              - name: actionflush
                value: "Actionflush value"
          - name: Init
            options:
              - name: timeout
                value: "timeout value"
```

### Filter List

`fail2ban_filterlist`<br>
A list of filter to create. The filter is saved in `/etc/fail2ban/action.d/` directory. The format is same as `fail2ban_actionlist` as shown above.

### Fail2ban Configuration Options

| Variable Name | Fail2ban Option Name | Option Values | Default Value | Description |
|---------------|----------------------|---------------|---------------|-------------|
| `fail2ban_confpath` |                | `[FILE]`      | `/etc/fail2ban/fail2ban.local` | The path where fail2ban configuration are written. |
| `fail2ban_loglevel` | `loglevel` | `CRITICAL`<br> `ERROR`<br> `WARNING`<br> `INFO`<br> `DEBUG` <br>\ <br>`[0-3]` | `ERROR` for version > `0.8.x` <br> `1` for version `0.8.x` | Set the log level output. |
| `fail2ban_logtarget` | `logtarget` | `[FILE]`<br> `STDOUT`<br> `STDERR` <br> `SYSLOG` | `/var/log/fail2ban.log` | Set the log target. Only one log target can be specified. <br> If you change logtarget from the default value and you are using logrotate -- also adjust or disable rotation in the corresponding configuration file (e.g. /etc/logrotate.d/fail2ban on Debian systems) |
| `fail2ban_syslogsocket` | `syslogsocket` | `auto`<br> `[FILE]` | `auto` | Set the syslog socket file. <br>Only used when logtarget is SYSLOG. auto uses platform.system() to determine predefined paths |
| `fail2ban_socket` | `socket` | `[FILE]` | `/var/run/fail2ban/fail2ban.sock` | Set the socket file. <br> This is used to communicate with the daemon. Do not remove this file when Fail2ban runs. It will not be possible to communicate with the server afterwards.| 
| `fail2ban_pidfile` | `pidfile` | `[FILE]` | `/var/run/fail2ban/fail2ban.pid` | Set the PID file. This is used to store the process ID of the fail2ban server. | 
| `fail2ban_dbfile` | `dbfile` | `None`<br> `:memory:`<br> `[FILE]` | `/var/lib/fail2ban/fail2ban.sqlite3` | Set the file for the fail2ban persistent data to be stored. <br>A value of `:memory:` means database is only stored in memory and data is lost when fail2ban is stopped. <br> A value of `None` disables the database. |
| `fail2ban_dbpurgeage` | `dbpurgeage` | `[ SECONDS ]` | `86400` | Sets age at which bans should be purged from the database | 
| `fail2ban_dbmaxmatches` | `dbmaxmatches` | `[ INT ]` | `20` | Number of matches stored in database per ticket. | 
| `fail2ban_stacksize` | `stacksize` | `[ SIZE ]` | `0` | This specifies the stack size (in KiB) to be used for subsequently created threads, and must be 0 or a positive integer value of at least 32.| 

### Global Jail Configuration Options

| Variable Name | Fail2ban Option Name | Option Values | Default Value | Description |
|---------------|----------------------|---------------|---------------|-------------|
| `fail2ban_jailpath` |                | `[FILE]`      | `/etc/fail2ban/jail.local`  | The file to write Fail2ban jail default configuration | 
| `fail2ban_ignoreself` | `ignoreself` | boolean<br> `true`<br> `false` | `true`  | Indicates the banning of own IP addresses should be prevented. | 
| `fail2ban_ignoreip` | `ignoreip` | List of IP address |   | list of IPs not to ban. They can include a DNS resp. CIDR mask too. The option affects additionally to ignoreself (if true) and don't need to contain own DNS resp. IPs of the running host. | 
| `fail2ban_ignorecommand` | `ignorecommand` | /path/to/command <ip> |    | External command that will take an tagged arguments to ignore, e.g. <ip>, and return true if the IP is to be ignored. False otherwise. |
| `fail2ban_ignorecache` | `ignorecache` |   | `disabled` | provide cache parameters for ignore failure check (caching of the result from `ignoreip`, `ignoreself` and `ignorecommand`) |
| `fail2ban_bantime` | `bantime` | `[ SECONDS ]` | `600` | Effective ban duration (in seconds). | 
| `fail2ban_findtime` | `findtime` | `[ SECONDS ]` | `600` | time interval (in seconds) before the current time where failures will count towards a ban. | 
| `fail2ban_maxretry` | `maxretry` | `[ INT ]` | `5` | The number of failures before a host get banned. | 
| `fail2ban_backend` | `backend` | `pyinotify`<br> `gamin`<br> `polling`<br> `systemd`<br> `auto` | `auto` | Specifies the backend used to get files modification. | 
| `fail2ban_usedns` | `usedns` | `yes`<br> `warn`<br> `no`<br> `raw` | `warn` | Specifies if jails should trust hostnames in logs, warn when DNS lookups are performed, or ignore all hostnames in logs |
| `fail2ban_logencoding` | `logencoding` | `auto`<br> `ascii`<br> `utf-8`<br> etc. | `auto` | Specifies the encoding of the log files handled by the jail. Default value of `auto` uses current system locale. | 
| `fail2ban_mode` | `mode`             | `normal`<br> `ddos`<br> `extra`<br> `aggressive`      | `normal`      | The mode of the filter  | 
| `fail2ban_filter` | `filter` | filter name | `%(__name__)s[mode=%(mode)s]` | The filter to use by the jail. <br>By default jails have names matching their filter name | 
| `fail2ban_logtimezone` | `logtimezone` | `UTC`<br> `UTC+0200`<br>`GMT-0100`<br> etc. |   | Force the time zone for log lines that don't have one.<br> If this option is not specified, log lines from which no explicit time zone has been found are interpreted by fail2ban in its own system time zone. | 
| `fail2ban_banaction` | `banaction` |  `iptables`, `iptables-new`, `iptables-multiport`, `shorewall`, etc | `iptables-multiport` | Default banning action. It is used to define `action_*` variables. Can be overridden globally or per section within jail.local file | 
| `fail2ban_banaction_allports` | `banaction_allports` |  `iptables`, `iptables-new`, `iptables-multiport`, `shorewall`, etc | `iptables-allports` | the same as banaction but for some "allports" jails like "pam-generic" or "recidive" | 
| `fail2ban_action` | `action` |   | `%(action_)s` | Choose default action. To change, just override value of 'action' with the interpolation to the chosen action shortcut (e.g.  action_mw, action_mwl, etc) or chose action(s) from /etc/fail2ban/action.d/ without the .conf/.local extension. |
| `fail2ban_failregex` | `failregex` | `Python Regualr Expression` |   | regex (Python regular expression) to be added to the filter's failregexes (see failregex in section FILTER FILES for details). | 
| `fail2ban_ignoreregex` | `ignoreregex` |   |   | regex which, if the log line matches, would cause Fail2Ban not consider that line. This line will be ignored even if it matches a failregex of the jail or any of its filters. |
| `fail2ban_maxmatches` | `maxmatches` | `[INT]` |   | max number of matched log-lines the jail would hold in memory per ticket. By default it is the same value as `maxretry` of jail (or default) | 

Dependencies
------------

No dependencies

Supported Platforms
-------------------
This role should work on any Redhat or Debian based linux distribution. It's tested on the following platforms

- CentOS 8
- CentOS 7
- Ubuntu 18.04
- Ubuntu 16.04
- Debian 10
- Debian 9

Example Playbook
----------------

The followng playbook install, enable fail2ban and add ssh jail

``` yaml
    - hosts: servers
      vars:
        fail2ban_services:
          - name: "sshd"
            enabled: "true"
            port: "ssh"
            filter: "sshd"
            logpath: "/var/log/auth.log"
            maxretry: 6       
      roles:
         - sakibmoon.fail2ban
```

License
-------

MIT

Author Information
------------------

This role was created by sakibmoon @2020
