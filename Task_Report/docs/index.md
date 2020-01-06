# Report for Task 1

## Problem Statement

* Setup a basic pipeline (use Jenkins <https://jenkins.io/>) for generating a security report for DVNA (<https://github.com/appsecco/dvna>)
* The DVNA code should be downloaded from Github and then undergo static analysis
* As part of the project understand what is the tech stack for DVNA hence what potential static analysis tools can be applied here
* Once a static analysis is done the report should be saved
* Next the DVNA should get deployed in a server
* To do all of the above just consider 2 virtual machines running in your laptop
* One VM contains the Jenkins and related infrastructure
* Second VM is for deploying the DVNA using the pipeline
* Do document extensively in markdown and deploy the documentation in a mkdocs website on the second VM.

## Setting up VMs

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
                    sh 'ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 "rm -rf dvna/ && mkdir dvna"'
                    sh 'scp -r * chaos@10.0.2.20:~/dvna'
                    sh 'ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 "source ./env.sh && ./env.sh && cd dvna && pm2 restart server.js"'
                }
            }
        }
    }
}
```

## Static Analysis

Tools considered:

* SonarQube
* [NPM Audit](https://docs.npmjs.com/cli/audit)
* [NodeJsScan](https://github.com/ajinabraham/NodeJsScan)
* [Retire.js](https://retirejs.github.io/retire.js/)
* [OWASP Dependency Checker](https://www.owasp.org/index.php/OWASP_Dependency_Check)
* [auditjs](https://github.com/sonatype-nexus-community/auditjs)
* [Synk](https://docs.npmjs.com/cli/audit)
* [JSpwn](https://github.com/dvolvox/JSpwn) (JSPrime + ScanJs)
* [JSPrime](https://github.com/dpnishant/jsprime)
* [ScanJS](https://github.com/mozilla/scanjs) (Deprecated)

### Static Analysis with SonarQube

Plugin used for SAST: SonarQube

* Used SonarQube's docker image to run the application
* Configured the jenkins plugin for SonarQube with Access Token

## Configuring Trigger with Webhook

* Configured a Personal Access Token on GitHub
* Added GitHub Server under "Configure System" with Personal Access Token generated as a Credential in Jenkins
* Added Webhook trigger under the repository settings
* Used `ngrok` to handle the event
* Selected the "GitHub hook trigger for GITScm polling" option under "Build triggers" for the Jenkins project

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
