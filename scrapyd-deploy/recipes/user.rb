#
# Cookbook:: scrapyd-deploy
# Recipe:: user
#
# Copyright:: 2018, The Authors, All Rights Reserved.

user node['scrapyd']['user'] do
    manage_home false
    system true
    action :create
end

group node['scrapyd']['group'] do
    members [node['scrapyd']['user']]
    system true
    action :create
end
