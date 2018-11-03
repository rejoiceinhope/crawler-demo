# # encoding: utf-8

# Inspec test for recipe scrapyd-deploy::default

# The Inspec reference, with examples and extensive documentation, can be
# found at http://inspec.io/docs/reference/resources/

eggs_dir = '/var/lib/scrapyd/eggs'
dbs_dir = '/var/lib/scrapyd/dbs'
items_dir = '/var/lib/scrapyd/items'
logs_dir = '/var/log/scrapyd'
run_dir = '/var/run/scrapyd'

writable_dirs = [eggs_dir, dbs_dir, items_dir, logs_dir, run_dir]
run_user = 'scrapy'
run_group = 'scrapy'
conf_dir = '/etc/scrapyd'
scrapyd_config = File.join(conf_dir, 'scrapyd.conf')

writable_dirs.each do |writable_dir|
  describe directory(writable_dir) do
    it { should exist }
    its('owner') { should eq run_user }
    its('group') { should eq run_group }
    its('mode') { should eq 493 }
  end
end

describe directory(conf_dir) do
  it { should exist }
  its('owner') { should eq 'root' }
  its('group') { should eq 'root' }
  its('mode') { should eq 493 }
end

describe file(scrapyd_config) do
  it { should exist }
  its('owner') { should eq 'root' }
  its('group') { should eq 'root' }
  its('mode') { should eq 420 }
end

describe ini(scrapyd_config) do
  its('scrapyd.eggs_dir') { should eq eggs_dir }
  its('scrapyd.logs_dir') { should eq logs_dir }
  its('scrapyd.items_dir') { should eq items_dir }
  its('scrapyd.jobs_to_keep') { should eq '5' }
  its('scrapyd.dbs_dir') { should eq dbs_dir }
  its('scrapyd.bind_address') { should eq '0.0.0.0' }
  its('scrapyd.http_port') { should eq '6800' }
end

describe systemd_service('scrapyd.service') do
  it { should be_enabled }
  it { should be_installed }
  it { should be_running }
end