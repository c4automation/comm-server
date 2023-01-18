#!/usr/bin/env python3

import time
import re


def reset_database(ipaddress):
    try:
        import paramiko
        _reset_database_paramiko(ipaddress)
    except ImportError:
        _reset_database_c4common(ipaddress)


def _reset_database_paramiko(ipaddress):
    print("Using paramiko")
    import paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=ipaddress, username='control4', password='t0talc0ntr0l4!')
    console = client.invoke_shell()

    print("Resetting the database")
    console.send('su\n')
    time.sleep(0.1)
    console.recv(32).decode('utf-8')
    console.send('foo1bar\n')
    console.recv(32).decode('utf-8')
    time.sleep(0.1)

    cmds = ['rm -rf /mnt/userdata/*',
            '/usr/share/communication-server/sanity-check.sh',
            'systemctl restart mysql',
            'systemctl restart nginx',
            'systemctl restart communication-server-api'
            ]

    regex = re.compile('root@comm-server')
    for cmd in cmds:
        print(cmd)
        console.send(cmd + '\n')
        while True:
            out = console.recv(128).decode('utf-8')
            if regex.match(out):
                break

        time.sleep(0.5)

    client.close()
    print('Waiting for systems to restart')
    time.sleep(10)


def _reset_database_c4common(ipaddress):
    """
    Delete the database and start fresh
    :param ipaddress: IP address of the Comm Server
    :return: None
    """
    print("Using c4common")
    from c4common import ssh
    conn = ssh.open(address=ipaddress, username='control4')

    conn.sendline('su')
    conn.expect('Password', timeout=1)
    conn.sendline('foo1bar')
    conn.expect('root@comm-server', timeout=1)

    cmds = ['rm -rf /mnt/userdata/*',
            '/usr/share/communication-server/sanity-check.sh',
            'systemctl restart mysql',
            'systemctl restart nginx',
            'systemctl restart communication-server-api'
            ]
    for cmd in cmds:
        conn.sendline(cmd)
        conn.expect('root@comm-server', timeout=15)

    conn.sendline('exit')
    conn.close()

    time.sleep(10)


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', help='IP address of comm server', required=True)

    args = parser.parse_args()
    reset_database(args.address)
