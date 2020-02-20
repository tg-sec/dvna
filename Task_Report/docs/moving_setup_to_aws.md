# Shifting Local Setup to AWS

## Objective

The aim of this section is to shift the entire setup from the local machine to AWS Cloud to provide a solution to the 1st point of the [problem statement](problem_statement.md) under `Task 4`.

## Configuring Jenkins with EC2 Instances

### Starting an EC2 instance

To start shifting the entire setup that I had locally on my machine, firstly I brought up an EC2 instance to install and run Jenkins on. Below mentioned are the steps to spin-up an EC2 instance:

* Firstly, I navigated to the EC2 page under 'Services'.
![Services Page](/img/services.PNG)

* Then I clicked on 'Launch instance' button and selected the 'Launch instance' option from the drop-down menu instead of the 'Launch instance from template' option as I did not have any template configured.
![Launch Instance](/img/launch_instance.PNG)

* Under the 'Choose AMI' menu, I selected 'Ubuntu Server 18.04 LTS (HVM), SSD Volume Type' option as I was using Ubuntu 18.04 as the OS on my local setup.
![Choosing AMI](/img/choose_ami.png)

* Under the 'Choose an Instance Type' menu, I selected 't2.medium' type primarily because of the requirement of at least 4GB memory to run all the tools along with Jenkins on the instance.
![Instance Type](/img/instance_type.PNG)

* I left everything under 'Configure Instance Details' page to their default values as no change was needed here.

* Under 'Add Storage' page, I changed the storage size from 8GB to 10GB, again, to accommodate all the tools that will be installed on the system. I left all the other options to their defaults.
![Add Storage](/img/add_storage.PNG)

* Under the 'Add Tags' page I added a tag with the instance's name ('Jenkins [Master]').
![Add Tags](/img/instance_tags.PNG)

* Under 'Configure Security Group' page:
    - I clicked on the "Add Rule" button to add a new 'Custom TCP Rule', gave '8080' as the 'Port Range' because that is where the Jenkins UI is accessible.
    - Under the 'Source' column, I selected the 'My IP' option to allow access only from the office IP.
    - I gave a brief description for both the rules I added for the instance.
![Security Rules](/img/security_rules.PNG)

* Lastly, I clicked on the 'Launch' button on the 'Review Instance Launch' page.
![Review & Instance Launch](/img/review_launch.PNG)

### Installing Jenkins on EC2 Instance

After successfully starting the instance, I had to install Jenkins on it. I used the steps from the [previous section](/setting_up_vms/#installing-jenkins) that I wrote on the same.

Starting Jenkins after the installation, I encountered an issue that I had not faced when I was running it on my machine locally. The URLs from where Jenkins fetches plugins had a few redirects which it was not able to handle on it own and failed trying to install any plugin. To rectify this issue, I ended up using [Nginx](https://www.nginx.com/), which is a reverse proxy and was able to handle the redirects successfully. To install Nginx, I followed this [documentation](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04). I, however, skipped step 5 on 'Setting Up Server Blocks' as it was not needed in the context of the problem statement. Lastly, as part of configuring Nginx, I wrote a config file, `jenkins-config`, whose contents are mentioned below:

```nginx
server {
    listen 80;
    server_name <EC2 PUBLIC IP>;

    location / {
      proxy_set_header        Host $host:$server_port;
      proxy_set_header        X-Real-IP $remote_addr;
      proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header        X-Forwarded-Proto $scheme;

      # Fix the "It appears that your reverse proxy set up is broken" error.
      proxy_pass          http://127.0.0.1:8080;
      proxy_read_timeout  90;

      # proxy_redirect      http://127.0.0.1:8080;

          # Required for new HTTP-based CLI
      proxy_http_version 1.1;
          proxy_request_buffering off;
      # workaround for https://issues.jenkins-ci.org/browse/JENKINS-45651
      # add_header 'X-SSH-Endpoint' '<EC2 PUBLIC IP>:50022' always;
    }
}
```

After resolving the issue, I installed the plugins that Jenkins recommends.

## Configuring SAST Tools

After Jenkins was setup on an EC2 instance on AWS, the next step was to add all the tools required to perform the various tests on the application. Below, I have mentioned how I went about doing the same on AWS with a note about any additional steps I took when I deviate from the setup instructions mentioned in [Static Analysis](/static_analysis).

I, once again, made a `reports/` directory inside `Jenkins Home Directory` to store all reports generated in a single location. This time, I also added a `tool_scripts/` directory in the same location to house the various scripts I was required to use through the entire pipeline.

### SonarQube

The installation for SonarQube is divided in two halves - setting up SonarQube Server and setting up the SonarQube Scanner. I was using docker previously to run the SonarQube Server on the local setup and hence, I had to use available services on AWS to run the SonarQube server as container. For the second half, I re-used the steps from my [documentation](/static_analysis/#sonarqube) on installing SonarQube.

* To setup a container with SonarQube Server running in it, I followed this [tutorial](https://itnext.io/run-your-containers-on-aws-fargate-c2d4f6a47fda) as it explained things in a simpler language as compared to other available articles. I however skipped steps `1` and `5` as I directly pulled the docker image from docker hub and I did not wanted to use a domain to point to the container. So, in essence, I started off by creating a cluster (which is a collective of services and tasks), created a new task definition (which is the details about the container) and lastly, created a service to run the task (container). There was one other thing where I deviated from the tutorial I used, in the security group configuration, I added rules to allow access to the container only from the Office IP by selecting the 'My IP' option under the 'Source' field and another rule to allow the Jenkins EC2 instance to access the container via it's public IP.

**Note**: I had a doubt initially whether or not I could pull images from Docker hub directly. After searching for a bit, it turned that I could. I just had to specify the repository URL structure as `docker.io/<docker-image-name>:version` while creating the task definition.

* After setting up SonarQube Server, the rest of the setup was identical to the local setup. For configuring SonarQube Scanner, I followed all the steps (except the first one) as mentioned previously in the report [here](/static_analysis/#sonarqube).

### NPM Audit

For NPM Audit, I did not have to do any AWS specific configuration as it was installed on the Jenkins EC2 Instance itself and followed the steps from the [documentation](/static_analysis/#npm-audit) I wrote for the local setup. There were a few things that I did:

* I placed the bash script inside the `tool_scripts/` directory mentioned at the start of this section.
* I amended the `stage` in the pipeline to execute the script from the the new directory mentioned in the previous step.

### NodeJsScan

### Retire.js

For Retire.js, I followed the [documentation](/static_analysis/#retirejs) exactly as I had when I was setting it up on the local VM as there are no scripts or special requirements associated with this tool.

### OWASP Dependency Check

For OWASP Dependency Check, I followed the [documentation](/static_analysis/#owasp-dependency-check) I wrote previously. The segments where I deviated are as follows:

* I placed the unzipped `dependency-check/` directory in `tool_scripts/` instead of Jenkins home directory.
* I amended the `stage` by changing the paths wherever necessary.

### Auditjs

### Snyk

## Configuring DAST Tools

## Configuring Code Analysis Tools

## Configuring Jenkins Pipeline

### Configuring Webhook for Jenkins on AWS
