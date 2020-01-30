# Setting Up Pipeline

## Objective

The aim of this section is to set up a basic pipeline in Jenkins to provide a solution to the 1st, 2nd, 4th and 5th points of the [problem statement](problem_statement.md) under `Task 1`.

## Pipeline

A Continuous Integration (CI) pipeline is a set of automated actions defined to be performed for delivering software applications. The pipeline helps in automating building the application, testing it and deploying it to production thus, reducing the time it requires for a software update to reach the production stage. A more detailed explanation can be found in this [article](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment) by Atlassian. I liked this article's explanation because it was written in an easy-to-understand language.

## Jenkins Pipeline Project

To start off with the task of building a pipeline, I setup Jenkins as mentioned in the previous section, logged on to the Jenkins Web Interface and then followed these steps to create a new pipeline under Jenkins for DVNA:

* I clicked on `New Item` from the main dashboard which leads me to a different page. I gave `node-app-pipeline` as the project's name and chose `Pipeline` as the project type amongst all the options present. Few articles on the web also demonstrated the usage of `Freestyle Project` but I liked the syntactical format and hence, went with `Pipeline`.
* Next came the project configurations page. Here:
    * Under `General` section:
        * I gave a brief description of the application being deployed and the purpose of this pipeline.
        * I checked the `Discard Old Builds` option as I felt there was no need of keeping artifacts from previous builds.
        * I also checked the `GitHub Project` option and provided the GitHub URL for the project's repository. This option allowed Jenkins to know where to fetch the project from.
    * Under `Build Triggers` section:
        * I checked the `GitHub hook trigger for GITScm Polling` option to allow automated builds based on webhook triggers on GitHub for selected events. The need for this option is explained in more detail in the upcoming section, [Configuring Webhook](configuring_webhook.md).
    * Under `Pipeline` section:
        * For `Definition`, I chose `Pipeline Script from SCM` option as I planned on adding the Jenkinsfile directly to the project repository.
        * For `Script Path`, I just provided `Jenkinsfile` as it was situated at the project's root directory.
* Lastly, I clicked on save to save the configurations.

## The Jenkinsfile

Jenkins has a utility where the actions that are to be performed on the build can be written in a syntactical format in a file called `Jenkinsfile`. I used this format to define the pipeline as I found it programmatically intuitive and easy to understand. I followed this [article](https://jenkins.io/doc/pipeline/tour/running-multiple-steps/) because it was the official documentation from Jenkins and it was very thoroughly written in a simple format with examples.

I wrote and added a Jenkinsfile to the root folder of the project repository. The following are the contents of the Jenkinsfile which executes the CI pipeline:

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
                    export MYSQL_PASSWORD=<MYSQL PASSWORD>
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
                    sh 'cat .scannerwork/report-task.txt > /{JENKINS HOME DIRECTORY}/reports/sonarqube-report'
                }
            }
        }

        stage ('NPM Audit Analysis') {
            steps {
                sh '/{PATH TO SCRIPT}/npm-audit.sh'
            }
        }

        stage ('NodeJsScan Analysis') {
            steps {
                sh 'nodejsscan --directory `pwd` --output /{JENKINS HOME DIRECTORY}/reports/nodejsscan-report'
            }
        }

        stage ('Retire.js Analysis') {
            steps {
                sh 'retire --path `pwd` --outputformat json --outputpath /{JENKINS HOME DIRECTORY}/reports/retirejs-report --exitwith 0'
            }
        }

        stage ('Dependency-Check Analysis') {
            steps {
                sh '/{JENKINS HOME DIRECTORY}/dependency-check/bin/dependency-check.sh --scan `pwd` --format JSON --out /{JENKINS HOME DIRECTORY}/reports/dependency-check-report --prettyPrint'
            }
        }

        stage ('Audit.js Analysis') {
            steps {
                sh '/{PATH TO SCRIPT}/auditjs.sh'
            }
        }

        stage ('Snyk Analysis') {
            steps {
                sh '/{PATH TO SCRIPT}/snyk.sh'
            }
        }

        stage ('Deploy to App Server') {
            steps {
                sh 'echo "Deploying App to Server"'
                sh 'ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 "cd dvna && pm2 stop server.js"'
                sh 'ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 "rm -rf dvna/ && mkdir dvna"'
                sh 'scp -r * chaos@10.0.2.20:~/dvna'
                sh 'ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 "source ./env.sh && ./env.sh && cd dvna && pm2 start server.js"'
            }
        }

    }

}

```

* The `pipeline` block constitutes the entire definition of the pipeline.
* The `agent` keyword is used to choose the way the Jenkins instance(s) are used to run the pipeline. The `any` keyword defines that Jenkins should allocate any available agent (an instance of Jenkins/a slave/the master instance) to execute the pipeline. A more thorough explanation can be found [here](https://jenkins.io/doc/book/pipeline/syntax/).
* The `stages` block houses all the stages that will comprise the various operations to be performed during the execution of the pipeline.
* The `stage` block defines a set of steps to be executed as part of that particular stage.
* The `steps` block defines the actions that are to be performed within a particular stage.
* Lastly, `sh` keyword is used to execute shell commands through Jenkins.

## Stages

I divided the pipeline into various stages based on the operations being performed. The following are the stages I chose:

### Initialization

This is just a dummy stage, nothing happens here. I wrote this to test out and practice the syntax for writing the pipeline.

### Build

In the build stage, I built the app with `npm install` on the Jenkins VM. This loads all the dependencies that the app (DVNA) requires so static analysis can be performed on the app in later stages.

**Note**: The app gets built with all of its dependencies only on the Jenkins VM.

### Static Analysis

All the stages that follow the Build Stage, except for the last (deployment) stage, consist of performing static analysis on DVNA with various tools. These stages are used to generate a report of their analysis and are stored locally on the Jenkins VM. The individual stages under Static Analysis are explained in detail in the upcoming sections [Static Analysis](static_analysis.md) and [Comparing SAST Tools](comparing_sast_tools.md).

### Deployment

Finally, in the stage titled 'Deploy to App Server', operations are performed on the App VM over SSH which I configured previously as mentioned in [Setting up VMs](setting_up_vms.md).

* Firstly, I stop the instance of the app running on the App VM.
* Then I purge all project associated files present on the App VM.
* All files from the Jenkins machine, including the dependencies built earlier, are copied over to the production VM.
* Finally, I restart the application with the updates reflecting changes made to the project.

**Note**: The app is not _built_ on the Production VM to avoid breaking the functioning of the instance of the application running on the production machine. All the dependencies are always built on the Jenkins machine and then copied over to the production server.
