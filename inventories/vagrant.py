#!/usr/bin/env python # Adapted from Mark Mandel's implementation https://github.com/ansible/ansible/blob/devel/plugins/inventory/vagrant.py import argparse import json import paramiko
import subprocess
import sys
import os
import argparse
import paramiko
import json
import yaml

def parse_args():
    parser = argparse.ArgumentParser(description="Vagrant inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()

def list_running_hosts():
    cmd = "vagrant status --machine-readable"
    status = subprocess.check_output(cmd.split(), cwd=os.environ["VAGRANT_DIR"]).rstrip()
    hosts = {}
    for line in status.split('\n'):
        info = line.split(',')
        (_, host, key, value, extra) = info[0], info[1], info[2], info[3], info[4:]
        if key == 'state' and value == 'running':
            hosts.update({host: {}})
    return hosts

def get_host_details(host):
    host_details = _get_host_details(host)
    if os.path.isfile(os.environ["VAGRANT_DIR"]+"/servers.yml"):
        servers = None
        with open(os.environ["VAGRANT_DIR"]+"/servers.yml", "r") as stream:
            try:
                servers = yaml.load(stream)
            except yaml.YAMLError as err:
                raise err
        server = [s for s in servers if s['name'] == host].pop()
        host_details['ansible_host'] = server['ip'] #replace localhost ip with public available confgured one
        del host_details['ansible_port'] #remove the localhost port binding used when sshing from localhost
    return host_details

def _get_host_details(host):
    cmd = "vagrant ssh-config {}".format(host)
    p = subprocess.Popen(cmd.split(), cwd=os.environ["VAGRANT_DIR"], stdout=subprocess.PIPE)
    config = paramiko.SSHConfig()
    config.parse(p.stdout)
    c = config.lookup(host)
    return {'ansible_host': c['hostname'],
            'ansible_port': c['port'],
            'ansible_user': c['user'],
            'ansible_ssh_private_key_file': c['identityfile'][0]}

def main():
    args = parse_args()
    if args.list:
        hosts = list_running_hosts()
        json.dump(hosts, sys.stdout)
    else:
        details = get_host_details(args.host)
        json.dump(details, sys.stdout)

if __name__ == '__main__':
    main()
