# Setting up VMs

* The setup is of two VMs running Ubuntu 18.04 on VirtualBox.
* One VM has the Jenkins setup, the other is used to deploy DVNA via Jenkins.

## Setting up Jenkins VM

* Installed Jenkins via the documentation on the site.

## Setting up Deployment VM

Script to setup Environment Variables:

```bash
#!/bin/bash

export MYSQL_USER=root
export MYSQL_DATABASE=dvna
export MYSQL_PASSWORD=AyushPriya#10
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
```

### Setting up DVNA

* Forked the DVNA repository
* Added a Jenkinsfile to run the pipeline
* Cloned the repository on the Deployment Server
* Installed MySQL for DVNA