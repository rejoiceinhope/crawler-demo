#
# Cookbook:: scrapyd-deploy
# Spec:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.

require 'spec_helper'

describe 'scrapyd-deploy::python' do
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

    it 'should update apt' do
      expect(chef_run).to update_apt_update('update')
    end

    it 'should install package python-pip' do
      expect(chef_run).to install_package('python-pip')
    end

    it 'should upgrade pip' do
      expect(chef_run).to run_execute("pip install -U pip").with(user: 'root')
    end

    it 'should install scrapyd' do
      expect(chef_run).to run_execute("pip install scrapyd").with(user: 'root')
    end
  end
end
