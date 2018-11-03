#
# Cookbook:: scrapyd-deploy
# Recipe:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.

include_recipe 'scrapyd-deploy::python'
include_recipe 'scrapyd-deploy::user'


eggs_dir = '/var/lib/scrapyd/eggs'
dbs_dir = '/var/lib/scrapyd/dbs'
items_dir = '/var/lib/scrapyd/items'
logs_dir = '/var/log/scrapyd'
run_dir = '/var/run/scrapyd'

config_dir = '/etc/scrapyd'
scrapyd_config = File.join(config_dir, 'scrapyd.conf')
pidfile = File.join(run_dir, 'scrapyd.pid')

[eggs_dir, dbs_dir, items_dir, logs_dir, run_dir].each do |writable_dir|
  directory writable_dir do
    owner node['scrapyd']['user']
    group node['scrapyd']['group']
    recursive true
    mode '0755'
  end
end

directory config_dir do
  owner 'root'
  group 'root'
  mode '0755'
end

template scrapyd_config do
  source 'scrapyd.conf.erb'
  variables({dirs: {eggs: eggs_dir, dbs: dbs_dir, items: items_dir, logs: logs_dir}})
  owner 'root'
  group 'root'
  mode '0644'
end

systemd_unit 'scrapyd.service' do
  content({
    Unit: {
      Description: 'Scrapyd',
      After: 'network.target'
    },
    Service: {
      User: node['scrapyd']['user'],
      Group: node['scrapyd']['group'],
      ExecStart: "/usr/bin/env scrapyd -l #{logs_dir}/scrapyd.log --pidfile #{pidfile}",
      PIDFile: "#{pidfile}",
      Restart: 'always'
    },
    Install: {
      WantedBy: 'multi-user.target'
    }
  })

  action [:create, :enable, :start]
end
