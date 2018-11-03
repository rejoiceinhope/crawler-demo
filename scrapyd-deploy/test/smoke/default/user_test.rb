# # encoding: utf-8

# Inspec test for recipe scrapyd-deploy::user

# The Inspec reference, with examples and extensive documentation, can be
# found at http://inspec.io/docs/reference/resources/

user_name = 'scrapy'
group_name = 'scrapy'

describe user(user_name) do
    it { should exist }
    its('groups') { should include group_name }
end

describe group(group_name) do
    it { should exist }
end