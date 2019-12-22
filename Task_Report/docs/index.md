# Report for Task 1

## Setting up VMs

* The setup is of two VMs running Ubuntu 18.04 on VirtualBox.
* One VM has the Jenkins setup, the other is used to deploy DVNA via Jenkins.

## Setting up Jenkins VM

* Installed Jenkins via the documentation on the site.

## Setting up Deployment VM

Deployment script:

```bash
#!/bin/bash

cd dvna
git pull origin master
export MYSQL_USER=root
export MYSQL_DATABASE=dvna
export MYSQL_PASSWORD=AyushPriya#10
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
npm install
pm2 restart server.js
```

### Setting up DVNA

* Forked the DVNA repository
* Added a Jenkinsfile to run the pipeline
* Cloned the repository on the Deployment Server
* Installed MySQL for DVNA

## Setting up the Pipeline

Wrote the following Jenkinsfile for the pipeline:

```jenkins
pipeline {
    agent any

    stages {

        stage ('Initialization') {
            steps {
                sh 'echo "Starting the build"'
            }
        }

        stage ('Build') {
            steps {
                sh '''
                    export MYSQL_USER=root
                    export MYSQL_DATABASE=dvna
                    export MYSQL_PASSWORD=ayushpriya10
                    export MYSQL_HOST=127.0.0.1
                    export MYSQL_PORT=3306
                    npm install
                   '''
            }
        }

        stage ('SonarQube Analysis') {
            environment {
                scannerHome = tool 'SonarQube Scanner'
            }
            steps {
                withSonarQubeEnv ('SonarQube') {
                    sh '${scannerHome}/bin/sonar-scanner'
                    sh 'cat .scannerwork/report-task.txt'
                }
            }
        }

        stage ('Deploy to App Server') {
            steps {
                sshagent(['node-app-server']) {
                    sh 'echo "Deploying App to Server"'
                    sh 'ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 "./deploy.sh"'
                }
            }
        }
    }
}

```

## Static Analysis with SonarQube

Plugin used for SAST: SonarQube

* Used SonarQube's docker image to run the application
* Configured the jenkins plugin for SonarQube with Access Token

## Deploying the report in Markdown

* Used `mkdocs` to build the static site
* Copied the static site to web root
* Used Apache as the server

## Resources

* <https://hub.docker.com/_/sonarqube/>
* <https://medium.com/@rosaniline/setup-sonarqube-with-jenkins-declarative-pipeline-75bccdc9075f>
* <https://codebabel.com/sonarqube-with-jenkins/amp/>
* <https://github.com/xseignard/sonar-js>
* <https://discuss.bitrise.io/t/sonarqube-authorization-problem/4229/2>

