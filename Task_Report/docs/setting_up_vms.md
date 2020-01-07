# Setting up VMs

The lab setup is of two VMs running Ubuntu 18.04 on VirtualBox. One VM has the Jenkins Infrastructure and the other is used as a Production Server to deploy the application (DVNA) on the server via the Jenkins Pipeline.

* Ubuntu was installed on both VMs following this [documentation](https://linuxhint.com/install_ubuntu_18-04_virtualbox/).

## Installing Jenkins

* Installed Jenkins following Digital Ocean's [documentation](https://www.digitalocean.com/community/tutorials/how-to-install-jenkins-on-ubuntu-18-04).

## Configuring Production VM

To serve [DVNA](https://github.com/ayushpriya10/dvna), there were some prerequisites. The following steps conclude how to setup the prerequisites for Jenkins to be able to deploy the application through the pipeline.

### Setting up DVNA

* Forked the DVNA repository onto my GitHub account
* Added a Jenkinsfile to the project repository to execute the pipeline
* Installed MySQL for DVNA on both VMs with this [documentation](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04)

Script (env.sh) to setup environment variables on Production VM:

```bash
#!/bin/bash

export MYSQL_USER=root
export MYSQL_DATABASE=dvna
export MYSQL_PASSWORD=<mysql_password>
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
```

### Configuring SSH Access

For Jenkins to be able to perform operations and copy application files onto the on the Production VM, `ssh` configuration was required to allow the _Jenkins User_ to log on to the Production VM. For the same, the following commands can be run on the Jenkins VM:

* Switching to Jenkins User

```bash
sudo su - jenkins
```

* Generating new SSH Keys for the Jenkins User

```bash
ssh-keygen -t rsa -b 4096 -C "<email>"
```

* The public key generated above was added to  `~/.ssh/authorized_keys` on the Production VM

**Note**: One could also use the `ssh-agent` plugin in Jenkins to use a different user to ssh in to the production VM. The credentails for that user will have to be added under Jenkins Credentials Section.
