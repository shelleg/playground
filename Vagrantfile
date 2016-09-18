# -*- mode:1
# : ruby -*-
# # vi: set ft=ruby :
vagrant_dir = File.expand_path(File.dirname(__FILE__))
roles_exist = 0
ansible_verbosity = '-vvv'
# Specify minimum Vagrant version and Vagrant API version
Vagrant.require_version ">= 1.6.0"
VAGRANTFILE_API_VERSION = "2"

# Require YAML module
require 'yaml'

# Read YAML file with box details
servers = YAML.load_file('servers.yml')

if Dir["#{vagrant_dir}/galaxy-roles/*"].empty? && Dir["#{vagrant_dir}/site-roles/*"].empty?
  abort('no roles to execute aborting ,,, [ hint: ansible-galaxy install -r requirements.yml should help :) ]')
end

# Create boxes
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Iterate through entries in YAML file
  servers.each do |servers|
    config.vm.define servers["name"] do |srv|
      srv.vm.box = servers["box"]
      srv.vm.network "private_network", ip: servers["ip"]
      srv.vm.provider :virtualbox do |vb|
        vb.name = servers["name"]
        vb.memory = servers["ram"]
      end
      srv.vm.provision :ansible do |ansible|
            ansible.limit = servers[:name]
            ansible.playbook = "./playbooks/default.yml"
            ansible.sudo = "true"
            ansible.sudo_user = "root"
            ansible.host_key_checking = "false"
            ansible.verbose = "#{ansible_verbosity}"
            ansible.extra_vars = {
              some_var: "some_value",
              dict: {
                kay1: "val1",
                kay2: "val2"
              }
            }
      end
    end
  end
end
