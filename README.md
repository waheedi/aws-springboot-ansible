# Ansible playbooks for launching and deploying a spring app

The playbooks are designed to dynamically work with almost any spring app, the infrastructure is also designed to be scalable, fault-tolerant and highly available.

### Requirements:
 
 packages that we need installed: python3, ansible > 2.4 , boto, boto3, botocore, awscli

 the whole setup is bound to the AWS_DEFAULT_PROFILE

 Theory, we have a profile which could be an enviornment, an app within an environment, a region, or a combination of the three.

 as boto and awscli are coupled with aws_profile it made it more felixable to do it in this fashion.

 let's continue with the requirements we define our profiles in ~/.aws/config and ~/.aws/credentials

#### Configurations:

 Sample ~/.aws/config 

```

[profile test-time-app]
region = us-west-1

[profile test-hello-app]
region = us-west-2

[profile prod-time-app]
region = us-east-1

[profile prod-time-app-west]
region = us-west-1

```
Sample ~/.aws/config
```
[test-time-app]
aws_access_key_id = 
aws_secret_access_key = 

```


#### Deploy the infrastrcture and the spring app
- Configure the AMI for the user running the deployment, ec2,route53,sts,elasticloadbalancing,apigateway
- We need to specify a git url to clone and configure the number of app instaces for each ec2 instance.
  the groups_vars/all file has all the default values
- run the full deploy: AWS_DEFAULT_PROFILE=prod-time-app ansible-playbook -i hosts full_deploy.yml, note the env variable, you can surely specify it in different ways
- deploy to another region by changing the AWS_DEFAULT_PROFILE to the desired profile/region. AWS_DEFAULT_PROFILE=prod-time-app-west ansible-playbook -i hosts full_deploy.yml
- now as we have two regions running we can use route53 to load balance/health check on two elbs that have been created
- Please note, name of aws_profile cannot contain characters that are not letters, or digits or dash (-)


