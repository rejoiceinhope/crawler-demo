#
# Cookbook:: scrapyd-deploy
# Spec:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.

require 'spec_helper'

describe 'scrapyd-deploy::user' do
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

    it 'creates a system user scrapy' do
      expect(chef_run).to create_user('scrapy').with(
        manage_home: false, system: true)
    end

    it 'creates a group scrapy with user scrapy' do
      expect(chef_run).to create_group('scrapy').with(members: ['scrapy'])
    end
  end
end
