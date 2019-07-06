# Ansible playbooks for launching and deploying Spring-boot apps

The playbooks are designed to dynamically work with almost any spring app, the infrastructure is also built to be scalable, fault-tolerant and highly available for a basic production environment.

The whole setup is bound to the `AWS_DEFAULT_PROFILE`. Theory, we have a profile which could be an environment, an app within an environment, a region, or a combination of the three. As boto and awscli are coupled with `aws_profile` it made it more flexible to do it in this fashion. more on requirements.


--- 

#### An overview of the infrastructure design:

![alt text](aws-springapp-infrastructure.png)

---

#### Requirements:

- packages that we need installed: `python3, ansible > 2.4 , boto, boto3, botocore, awscli`
- Define our ansible variables and profiles in ~/.aws/config and ~/.aws/credentials.

---
##### Required ansible variables:
``` Sample group_vars/all
app_instances: 2
app_port: 8080
haproxy_springapps_port: 8888
aws_profile: "{{ lookup('env', 'AWS_DEFAULT_PROFILE') | default('test', true) }}"
aws_region: "{{ lookup('env', 'AWS_DEFAULT_REGION') | default('us-east-1', true) }}"
aws_key_name: waheed
ansible_ssh_private_key_file: "~/.ssh/{{ aws_key_name }}"
git_key: ec2-new
app_git_url: "git@gitlab.com:waheedi/spring-time-app.git"
branch: master
create_ec2_instances: yes
instances_count: 1
az_count: 2
aws_instance_type: t2.micro
rsyslog_server: localhost
route53_zone: "saascoin.network"
hello_dns: "hello.example.com"
git_api: "https://gitlab.com/api"
git_access_token: "{{ lookup('env', 'GITLAB_TOKEN') }}"
aws_distro_ami: "ubuntu/images/*/ubuntu-*-18.04-*"


```
---
##### Optional ansible variables:

```
aws_profile_2: "{{ lookup('env', 'AWS_SECOND_PROFILE') | default('false') }}"
topic_alerts_email: "waheed.barghouthi@gmail.com"
#app_version: "123-prod-west-1" # leave undefined for auto versioning
#aws_instance_ami: 

```
---
##### Profiles configurations:


```Sample ~/.aws/config 

[profile test-time-app]
region = us-west-1

[profile test-hello-app]
region = us-west-2

[profile prod-time-app-east]
region = us-east-1

[profile prod-time-app-west]
region = us-west-1

```

```Sample ~/.aws/credentials
[test-time-app]
aws_access_key_id = 
aws_secret_access_key = 

```

---

##### Deploy the infrastructure and the spring app:
- Configure the IAM policies for the user running the deployment, `ec2,route53,sts,elasticloadbalancing,apigateway,autoscaling,iam` with the desired arn resources
- We need to specify a git url for the app to clone, configure the number of app instances for each ec2 instance in the groups_vars/all file, which has all the default values for our playbooks
- Run the full deploy: `AWS_DEFAULT_PROFILE=prod-time-app-east ansible-playbook -i hosts full_deploy.yml`, note the env variable, you can surely specify it in different ways
- During the play you will have to copy the public keys of the new instances to the git service, it will pause for two minutes, we can automate this for github, its already automated for gitlab
- deploy to another region by changing the `AWS_DEFAULT_PROFILE` to the desired profile/region. `AWS_DEFAULT_PROFILE=prod-time-app-west ansible-playbook -i hosts full_deploy.yml`
- now as we have two regions running we can use route53 to load balance/health check on two elbs that have been created, just run deploy_to_route53.yml with two env variables `AWS_DEFAULT_PROFILE=prod-time-app-west and AWS_SECOND_PROFILE=prod-time-app-east`
- Please note, the name of aws_profile cannot contain characters that are not letters, or digits or dash (-)

---
##### The full deploy:
- The full deploy is the starting point to run the infrastructure and the app we select for the deployment, by executing the below:
1. Create the aws needed services and servers, add to our route53 zone with the desired dns name for the load balancer(s) that has been created
2. Install python on the target machines (in a raw fashion)
3. Install common packages as well as nginx, haproxy to load balance app instances inside the ec2 instance
4. Deploy the App, clone it, package it, run it and test it
- For Single region multi-az: `./auto_deploy create profile` or `AWS_DEFAULT_PROFILE=profile ansible-playbook -i hosts full_deploy.yml`

---
##### Extras:
- An auto_deploy python script that takes multiple profiles as arguments and create a full deploy for them, (multi-region fault-tolerant) which can be run using `./auto_deploy create prod prod-west` it will automatically create a failover dns aliases for the first two regions
- aws-autoscale role can be used when there is a custom ami to boot from, for autoscaling and faster deploy time (a custom ami for us-west-1 and us-east-1 is already created for demo purposes)
- aws-cleanup role, to cleanup any related service or file that has been generated for a profile
- auto_deploy support extra arguments like `-e aws_profile=time-app-west --start-at-task="\"minimal_python : Install python for Ansible use (Facts gathering)"\"` but they need to be the last arguments provided, like `./auto-deploy create profile -e ...`
- auto_deploy support takes the first argument as action, available actions are create: to make a full deployment, delete: will delete all generated aws services and files, route: will route two regions with aliases to the same DNS name (failover scenario)
- For multi-region multi-az: `./auto_deploy create profile-east profile-west`
