#
# Cookbook:: scrapyd-deploy
# Spec:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.

require 'spec_helper'

describe 'scrapyd-deploy::python' do
  context 'When all attributes are default, on Ubuntu 16.04' do
    let(:runner) { ChefSpec::ServerRunner.new(platform: 'ubuntu', version: '16.04') }
    let(:chef_run) { runner.converge(described_recipe) }
    let(:node) { runner.node }

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

    it 'should install pip dependencies' do
      expect(chef_run).to run_execute(
        "pip install #{node.default['scrapyd']['packages'].join(' ')}")
    end
  end
end
