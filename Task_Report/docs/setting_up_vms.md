# Setting up VMs

## Objective

The aim of this section is to set up the required infrastructure to perform the task and solve the 6th point of the [problem statement](problem_statement.md).

## System Configuration

The lab setup is of two VMs running Ubuntu 18.04 on VirtualBox as it is an LTS (Long Term Support) version which is a desirable feature for a CI pipeline. The release notes for Ubuntu 18.04 can be found [here](https://wiki.ubuntu.com/BionicBeaver/ReleaseNotes?_ga=2.263578572.1702646424.1578630197-858707961.1578630197) for additional details. One VM has the Jenkins Infrastructure and the other is used as a Production Server to deploy the application (DVNA) on the server via the Jenkins Pipeline.

* I installed Ubuntu on both VirtualBox VMs following this [documentation](https://linuxhint.com/install_ubuntu_18-04_virtualbox/).

    * I decided to go with this documentation as it was concise.
    * I, however, chose the 'Normal Installation' under the "Minimal Install Option and Third Party Software" segment instead of the ones specified in the instructions as otherwise only the essential Ubuntu core components would be installed.
    * Additionally, I left out the optional third step "Managing installation media" as I did not need the boot media after the installation was complete.

## Installing Jenkins

Jenkins is a Continous Integration (CI) Tool used to automate actions for CI operations for building and deploying applications. Jenkins was used as the tool to build the application deployment pipeline as it was a requisite of the problem statement given.

* Installed Jenkins following Digital Ocean's [documentation](https://www.digitalocean.com/community/tutorials/how-to-install-jenkins-on-ubuntu-18-04). I went along with this particular documentation as it seemed the easiest to follow with clear steps, and I like the style of Digital Ocean's documentation. For this documentation, I didn't skip any step.

## Choosing the Application

The application that was to be analyzed and deployed, as required by the problem statement, was DVNA (or Damn Vulnerable Node Application). It is an intentionally vulnerable application written with Node.js and has various security issues designed to illustrate different security concepts.

## Configuring Production VM

To serve [DVNA](https://github.com/ayushpriya10/dvna), there were some prerequisites. The following steps conclude how to set up the prerequisites for Jenkins to be able to deploy the application through the pipeline.

### Setting up DVNA

* I forked the DVNA repository onto my GitHub account to be able to add files and edit project structure.
* Then I added a Jenkinsfile to the project repository to configure pipeline stages and execute it.
* DVNA's documentation specifies MySQL as the database needed so, to install MySQL for DVNA I again used Digital Ocean's [documentation](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04).
    - Under step 3, I skipped the section about provisionally MySQL access for a dedicated user. I created the 'root' user as mentioned in the documentation previously and then went straight to step 4 so as there was no need for an additional user after `root`.
* MySQL was installed on the Production VM for a successful deployment of the application. The Jenkins VM need not have MySQL installed as DVNA was only getting built on this machine and not deployed.

To not leak the MySQL Server configuration details for the production server, I used a shell script, named `env.sh`, and placed it in the Production VM in the user's home directory (`/home/<username>`). The script gets executed from the pipeline to export the Environment Variables for the application to deploy.

The contents of the script (env.sh) to setup environment variables on Production VM are:

```bash
#!/bin/bash

export MYSQL_USER=root
export MYSQL_DATABASE=dvna
export MYSQL_PASSWORD=<mysql_password>
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
```

This script is executed through the pipeline in the 'Deploy to App Server' stage.

### Configuring SSH Access

For Jenkins to be able to perform operations and copy application files onto the on the Production VM, `ssh` configuration was required to allow the _Jenkins User_ to log on to the Production VM. For the same, I switched to the _Jenkins User_, created a pair of SSH keys (an extensive article about how user authentication works in SSH with public keys can be found [here](https://www.digitalocean.com/community/tutorials/understanding-the-ssh-encryption-and-connection-process)) and placed the public key in the Production VM:

* Switching to Jenkins User

```bash
sudo su - jenkins
```

* Generating new SSH Keys for the Jenkins User

```bash
ssh-keygen -t ed25519 -C "<email>"
```

* The public key generated above was added to  `~/.ssh/authorized_keys` on the Production VM.

**Note**: One could also use the `ssh-agent` plugin in Jenkins to use a different user to ssh into the production VM. The credentials for that user will have to be added under Jenkins Credentials Section.

**Note**: `ed25519` is used instead of the `rsa` option as it provides a smaller key while providing the equivalent security of an RSA key.
