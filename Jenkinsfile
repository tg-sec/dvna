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
                    npm start
                   '''
            }
        }
        
        stage ('Deploy to App Server') {
            steps {
                sshagent(['node-app-server']) {
                    sh '''
                        cd dvna
                        git pull origin master
                        export MYSQL_USER=root
                        export MYSQL_DATABASE=dvna
                        export MYSQL_PASSWORD=AyushPriya#10
                        export MYSQL_HOST=127.0.0.1
                        export MYSQL_PORT=3306
                        npm install
                        npm start
                       '''
                        
    }
}
