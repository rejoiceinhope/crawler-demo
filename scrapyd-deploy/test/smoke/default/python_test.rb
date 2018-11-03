# # encoding: utf-8

# Inspec test for recipe scrapyd-deploy::python

# The Inspec reference, with examples and extensive documentation, can be
# found at http://inspec.io/docs/reference/resources/

describe command('python -V') do
  its('exit_status') { should eq 0 }
end

describe command('pip -V') do
  its('exit_status') { should eq 0 }
end

describe command('scrapyd --version') do
  its('exit_status') { should eq 0 }
end
