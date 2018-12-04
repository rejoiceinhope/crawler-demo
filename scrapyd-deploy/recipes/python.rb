#
# Cookbook:: scrapyd-deploy
# Recipe:: python
#
# Copyright:: 2018, The Authors, All Rights Reserved.

apt_update 'update' do
  action :update
end

package 'python-pip'
execute 'pip install -U pip' do
  user 'root'
end
execute 'pip install scrapyd' do
  user 'root'
end
execute "pip install #{node['scrapyd']['packages'].join(' ')}" do
  user 'root'
end