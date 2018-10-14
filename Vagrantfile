# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "bento/ubuntu-18.04"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 6650, host: 6650
  config.vm.network "forwarded_port", guest: 8080, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 6651, host: 6650, host_ip: "127.0.0.1"
  # config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Copy the pulsar standalone startup script to vagrant box
  config.vm.provision "file", source: "./setup/pulsar_start", destination: "~/setup/pulsar_start"
  config.vm.provision "file", source: "./setup/pulsar.service", destination: "~/setup/pulsar.service"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
    vb.memory = "2048"
    vb.cpus = 1
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get upgrade
    apt-get install -y openjdk-8-jdk

    mkdir /home/vagrant/pulsar
    chown vagrant:vagrant /home/vagrant/pulsar

    # cp /home/vagrant/setup/pulsar_start /etc/init.d/pulsar
    cp /home/vagrant/setup/pulsar.service /etc/systemd/system/pulsar.service
    systemctl daemon-reload
    systemctl enable pulsar
    # chmod 755 /etc/init.d/pulsar
    # update-rc.d pulsar defaults

    cd /opt
    wget https://mirrors.ocf.berkeley.edu/apache/pulsar/pulsar-2.1.1-incubating/apache-pulsar-2.1.1-incubating-bin.tar.gz
    mkdir /opt/pulsar
    tar xvfz apache-pulsar-2.1.1-incubating-bin.tar.gz -C /opt/pulsar --strip-components=1
    chown -R vagrant:vagrant /opt

    cd /opt/pulsar/bin
    ./pulsar-admin tenants create sensor_mon
    ./pulsar-admin namespaces create sensor_mon/etl

    systemctl start pulsar
  SHELL
end