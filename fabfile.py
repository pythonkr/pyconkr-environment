#!/usr/bin/env python


from fabric.api import run, env
from fabric.contrib.files import append, contains, exists


env.use_ssh_config = True

def update_ssh_authorized_keys():
    auth_key_path = "/root/.ssh/authorized_keys"
    installed_ssh_keys = run("cat /root/.ssh/authorized_keys")
    installed_ssh_keys = set(installed_ssh_keys.splitlines())
    desired_ssh_keys = set([ x for x in
        open("admin_ssh_keys").read().splitlines() if len(x.strip()) > 0 ])
    new_keys = desired_ssh_keys - installed_ssh_keys
    if len(new_keys) == 0:
        return
    append(auth_key_path,
            "\n".join( new_keys))

def add_nginx_repo():
    nginx_config_path = "/etc/yum.repos.d/nginx.repo"
    if not exists(nginx_config_path):
        append(nginx_config_path, open("nginx.repo").read() )

def install_nginx():
    run("yum install -y nginx")
