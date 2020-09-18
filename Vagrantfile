# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.hostname = "SAROGN"

  config.vm.network "forwarded_port", guest: 80, host: 8383

  config.vm.network "public_network", ip: "192.168.1.212", bridge: "eth0"

  config.vm.synced_folder "./public", "/var/www/public"
  config.vm.synced_folder "./html",   "/var/www/html"
  config.vm.synced_folder "/nfs",   "/nfs"
end

