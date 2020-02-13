# Final Pipeline Structure

## Objective

The aim of this section is to define the final structure achieved for the pipeline after the various testing stages integrated into the pipeline as part of the solutions for all the three tasks in the [problem statement](/problem_statement).

## Final Pipeline

After completing various testing stages (SAST, DAST, Code Quality Analysis) for DVNA, the last task was to combine all the segments together as all three tasks were tested on separate pipelines. Combining them also meant removing redundant steps from the stages to create a lean pipeline. All the scripts used in this pipeline remain the same as what they were when mentioned in the previous sections in the report. Below is a diagrammatic representation of the flow of the entire pipeline:

![Pipeline Diagram](/img/jenkins_pipeline.png)

The final pipeline script that was the result of combining all three segregated pipelines and removing redundancies is mentioned below:

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
                sh 'npm install'
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

        stage ('Building DVNA') {
            steps {
                sh '''
                    source /{PATH TO SCRIPT}/env.sh
                    pm2 start server.js
                '''
            }
        }

        stage ('Run ZAP for DAST') {
            steps {
                sh '/{PATH TO SCRIPT}/baseline-scan.sh'
            }
        }

        stage ('Run W3AF for DAST') {
            agent {
                label 'raf-vm'
            }

            steps {
                sh '/{PATH TO SCRIPT}/w3af/w3af_console -s /{PATH TO SCRIPT}/scripts/w3af_scan_script.w3af'
                sh 'scp -r /{PATH TO OUPUT}/w3af/output-w3af.txt chaos@10.0.2.19:/{HOME DIRECTORY}/'
            }
        }

        stage ('Take DVNA offline') {
            steps {
                sh 'pm2 stop server.js'
                sh 'mv baseline-report.html /{JENKINS HOME DIRECTORY}/reports/zap-report.html'
                sh 'cp /{HOME DIRECTORY}/output-w3af.txt /{JENKINS HOME DIRECTORY}/reports/w3af-report'
            }
        }

        stage ('Lint Analysis with Jshint') {
            steps {
                sh '/{PATH TO SCRIPT}/jshint-script.sh'
            }
        }

        stage ('Lint Analysis with EsLint') {
            steps {
                sh '/{PATH TO SCRIPT}/eslint-script.sh'
            }
        }

        stage ('Deploy to App Server') {
            steps {
                sh 'echo "Deploying App to Server"'
                sh 'ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 "cd dvna && pm2 stop server.js"'
                sh 'ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 "rm -rf dvna/ && mkdir dvna"'
                sh 'scp -r * chaos@10.0.2.20:~/dvna'
                sh 'ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 "source ./env.sh && cd dvna && pm2 start server.js"'
            }
        }

    }

}
```
