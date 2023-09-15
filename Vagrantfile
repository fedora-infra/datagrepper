# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true

  config.vm.define "datagrepper" do |datagrepper|
    datagrepper.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/38/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-38-1.6.x86_64.vagrant-libvirt.box"
    datagrepper.vm.box = "f38-cloud-libvirt"
    datagrepper.vm.hostname = "datagrepper.test"

    datagrepper.vm.synced_folder '.', '/vagrant', disabled: true
    datagrepper.vm.synced_folder ".", "/home/vagrant/datagrepper", type: "sshfs"
    datagrepper.vm.synced_folder "../datanommer", "/home/vagrant/datanommer", type: "sshfs"


    datagrepper.vm.provider :libvirt do |libvirt|
      libvirt.cpus = 2
      libvirt.memory = 2048
    end

    datagrepper.vm.provision "ansible" do |ansible|
      ansible.playbook = "devel/ansible/datagrepper.yml"
      ansible.config_file = "devel/ansible/ansible.cfg"
      ansible.verbose = true
    end
  end

end
