# Ansible playbooks for launching and deploy a spring app

### Lets get the requirments ready for the Play to run
 
 packages that we need installed: python3, ansible > 2.4 , boto, boto3, botocore, awscli

 the whole setup is bound to the AWS_DEFAULT_PROFILE, everything we run will be coupled with the aws_profile

 theory, we have a profile which could be an enviornment or an app within an environment, or just an app.

 as boto and awscli are tightely coupled with aws_profile it was reasonable to do the same.

 we define our profiles in ~/.aws/config and ~/.aws/credentials

 Sample ~/.aws/config 

```

[profile test-time-app]
region = us-west-1

[profile test-hello-app]
region = us-west-1

[profile prod-time-app]
region = us-west-1

```
Sample ~/.aws/config
```
[test-time-app]
aws_access_key_id = 
aws_secret_access_key = 

```


## Deploy the infrastrcture and a spring app
#### requirements: 
- We need to specify a git url to clone and configure the number of app instaces for each ec2 instance.
  the groups_vars/all file has all the default values


run the full deploy: AWS_DEFAULT_PROFILE=prod-time-app ansible-playbook -i hosts instance_deploy.yml