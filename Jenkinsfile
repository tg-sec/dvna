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
        
        stage ('Deploy to App Server') {
            steps {
                sshagent(['node-app-server']) {
                    sh 'echo "Deploying App to Server"'
                    sh '''
                        ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 << EOF
                        cd dvna
                        git pull origin master
                        export MYSQL_USER=root
                        export MYSQL_DATABASE=dvna
                        export MYSQL_PASSWORD=AyushPriya#10
                        export MYSQL_HOST=127.0.0.1
                        export MYSQL_PORT=3306
                        npm install
                        EOF
                       '''
                    sh 'ssh -o StrictHostKeyChecking=no chaos@10.0.2.20 "cd dvna && pm2 start server.js"'
                }                        
            }
        }
    }
}
