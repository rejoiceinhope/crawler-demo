#
# Cookbook:: scrapyd-deploy
# Spec:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.

require 'spec_helper'

writable_dirs = [
  '/var/lib/scrapyd/eggs', '/var/lib/scrapyd/dbs', '/var/lib/scrapyd/items',
  '/var/log/scrapyd', '/var/run/scrapyd'
]
run_user = 'scrapy'
run_group = 'scrapy'
conf_dir = '/etc/scrapyd'
scrapyd_config = File.join(conf_dir, 'scrapyd.conf')

describe 'scrapyd-deploy::default' do
  context 'When all attributes are default, on Ubuntu 16.04' do
    let(:chef_run) do
      # for a complete list of available platforms and versions see:
      # https://github.com/customink/fauxhai/blob/master/PLATFORMS.md
      runner = ChefSpec::ServerRunner.new(platform: 'ubuntu', version: '16.04')
      runner.converge(described_recipe)
    end

    it 'converges successfully' do
      expect { chef_run }.to_not raise_error
    end

    writable_dirs.each do |writable_dir|
      it "should create writable directory #{writable_dir}" do
        expect(chef_run).to create_directory(writable_dir).with(
          user: run_user, group: run_group, recursive: true, mode: '0755')
      end
    end

    it "should create configuration directory #{conf_dir}" do
      expect(chef_run).to create_directory(conf_dir).with(
        user: 'root', group: 'root', mode: '0755')
    end

    it "should create configuration #{scrapyd_config}" do
      expect(chef_run).to create_template(scrapyd_config).with(
        user: 'root', group: 'root', mode: '0644')
    end

    it "should create systemd service scrapyd.service" do
      expect(chef_run).to create_systemd_unit('scrapyd.service').with(
        action: [:create, :enable, :start])
    end
  end
end
