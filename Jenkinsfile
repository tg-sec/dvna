pipeline {
    agent any
   

    environment{
	SAST_REPORTS = '/var/lib/jenkins/reports'
	} 
    stages {
        
        stage ('Initialization') {
            steps {
                sh 'echo "Starting the CI pipeline."'
            }
        }
        
        stage ('Build') {
            steps {
                sh '''
                    export MYSQL_USER=root
                    export MYSQL_DATABASE=dvna
                    export MYSQL_PASSWORD=Admin@123
                    export MYSQL_HOST=127.0.0.1
                    export MYSQL_PORT=3306
                    npm install
                   '''
            }
        }
      /*  
        stage ('SonarQube Analysis') {
            environment {
                scannerHome = tool 'SonarQube Scanner'
            }
            steps {
                withSonarQubeEnv ('SonarQube') {
                    sh '${scannerHome}/bin/sonar-scanner'
        //            sh 'cat .scannerwork/report-task.txt > ${SAST_REPORTS}/sonarqube-report'
                }
            }    
        }
        
        stage ('NPM Audit Analysis') {
            steps {
               sh 'scripts/npm-audit.sh'
            }
        }
       */ 
        stage ('NodeJsScan Analysis') {
            steps {
                sh 'scripts/nodejsscan.sh'
            }
        }
        
        stage ('Retire.js Analysis') {
            steps {
                sh 'retire --path `pwd` --outputformat json --outputpath ${SAST_REPORTS}/retirejs-report --exitwith 0'
            }
        }
        
        stage ('Dependency-Check Analysis') {
            steps {
                sh '/var/lib/jenkins/dependency-check/bin/dependency-check.sh --scan `pwd` --format JSON --out /var/lib/jenkins/reports/dependency-check-report --prettyPrint'
            }
        }
        
        stage ('Audit.js Analysis') {
            steps {
                sh '/home/chaos/auditjs.sh'
            }
        }
              
        stage ('Snyk Analysis') {
            steps {
                sh '/home/chaos/snyk.sh'
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
