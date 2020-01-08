
# Static Analysis

## SAST Tools for Node.js Applications

The following are some tools that I found to perform SAST on Nodejs Applications:

### [SonarQube](https://www.sonarqube.org/)

* Used SonarQube's docker image to run the application with the following command:

```bash
docker run -d -p 9000:9000 -p 9092:9092 --name sonarqube sonarqube
```

* Created a new Access Token for Jenkins in SonarQube under `Account > Security`.
* In Jenkins, under `Credentials >  Add New Credentials` the token is saved as a `Secret Text` type credential.
* The `SonarQube Server` section under `Manage Jenkins > Configure System`, check the `Enable injection of SonarQube server configuration as build environment variables` option.
* Provide the URL for SonarQube Server (in our case, localhost:9000) and add the previously saved SonarQube Credentials.
* Add the following stage in the Jenkinsfile:

```jenkins
stage ('SonarQube Analysis') {
    environment {
                scannerHome = tool 'SonarQube Scanner'
    }

    steps {
        withSonarQubeEnv ('SonarQube') {
            sh '${scannerHome}/bin/sonar-scanner'
            sh 'cat .scannerwork/report-task.txt > /var/lib/jenkins/reports/sonarqube-report'
        }
    }
}
```

### [NPM Audit](https://docs.npmjs.com/cli/audit)

NPM Audit comes along with `npm@6` and is not required to be installed seprately. To upgrade npm, if needed, run the following command:

```bash
npm install -g npm@latest
```

* NPM Audit gives a non-zero status code, if it finds any vulnerable dependencies, hence, I ran it through a script to avoid failure of the pipeline. The script is as follows:

```bash
#!/bin/bash

cd /var/lib/jenkins/workspace/node-app-pipeline
npm audit --json > /var/lib/jenkins/reports/npm-audit-report

echo $? > /dev/null
```

* Add the following stage in the Jenkinsfile:

```jenkins
stage ('NPM Audit Analysis') {
    steps {
        sh '/home/chaos/npm-audit.sh'
    }
}
```

### [NodeJsScan](https://github.com/ajinabraham/NodeJsScan)

* To install `NodeJsScan`, use the following command:

```bash
pip3 install nodejsscan
```

**Note**: If the package is not getting installed globally, as it will be run by the Jenkins User, run the following command: `sudo -H pip3 install nodejsscan`.

* To analyse the Nodejs project, the following command is used:

```bash
nodejsscan --directory `pwd` --output /var/lib/jenkins/reports/nodejsscan-report
```

* Add the following stage in the Jenkinsfile:

```jenkins
stage ('NodeJsScan Analysis') {
    steps {
        sh 'nodejsscan --directory `pwd` --output /var/lib/jenkins/reports/nodejsscan-report'
    }
}
```

### [Retire.js](https://retirejs.github.io/retire.js/)

* To install Retire.js use the following command:

```bash
npm install -g retire
```

* To analyse the project with Retire.js run the following command:

```bash
retire --path `pwd` --outputformat json --outputpath /var/lib/jenkins/reports/retirejs-report --exitwith 0
```

* Add the following stage in the Jenkinsfile:

```jenkins
stage ('Retire.js Analysis') {
    steps {
        sh 'retire --path `pwd` --outputformat json --outputpath /var/lib/jenkins/reports/retirejs-report --exitwith 0'
    }
}
```

### [OWASP Dependency Checker](https://www.owasp.org/index.php/OWASP_Dependency_Check)

* OWASP Dependency Checker comes as an executable for linux. To get the executable, download the [archive](https://dl.bintray.com/jeremy-long/owasp/dependency-check-5.2.4-release.zip).

* Unzip the archive:

```bash
unzip dependency-check-5.2.4-release.zip
```

* To execute the scan, run the following command:

```bash
/var/lib/jenkins/dependency-check/bin/dependency-check.sh --scan /var/lib/jenkins/workspace/node-app-pipeline --format JSON --out /var/lib/jenkins/reports/dependency-check-report --prettyPrint
```

**Note**: Copy the unzipped archive to `/var/lib/jenkins/` before scanning.

* Add the following stage in the Jenkinfile:

```jenkins
stage ('Dependency-Check Analysis') {
    steps {
        sh '/var/lib/jenkins/dependency-check/bin/dependency-check.sh --scan `pwd` --format JSON --out /var/lib/jenkins/reports/dependency-check-report --prettyPrint'
    }
}
```

### [auditjs](https://github.com/sonatype-nexus-community/auditjs)

* To install Audit.js, use the following command:

```bash
npm install auditjs -g
```

* To perform a scan, run the following command while inside the project directory:

```bash
auditjs --username ayushpriya10@gmail.com --token <auth_token> /var/lib/jenkins/reports/auditjs-report 2>&1
```

* Auditjs gives a non-zero status code, if it finds any vulnerable dependencies, hence, I ran it through a script to avoid failure of the pipeline. The script is as follows:

```bash
#!/bin/bash

cd /var/lib/jenkins/workspace/node-app-pipeline
auditjs --username ayushpriya10@gmail.com --token <auth_token> /var/lib/jenkins/reports/auditjs-report 2>&1

echo $? > /dev/null
```

**Note**: We use `2>&1` to redirct STDERR output to STDOUT otherwise the Vulnerabilities found will not be written to the report but instead will be printed to console.

* Add the following stage to the Jenkinsfile:

```jenkins
stage ('Audit.js Analysis') {
    steps {
        sh '/home/chaos/auditjs.sh'
    }
}
```

### [Snyk](https://github.com/snyk/snyk#cli)

* To install Snyk, use the following command:

```bash
npm install -g snyk
```

* Before scanning a project, we need to authenticate Snyk CLI which can be done as follows:

```bash
snyk auth <AUTH TOKEN>
```

* To perform a scan:

```bash
snyk test
```

* Snyk gives a non-zero status code, if it finds any vulnerable dependencies, hence, I ran it through a script to avoid failure of the pipeline. The script is as follows:

```bash
#!/bin/bash

cd /var/lib/jenkins/workspace/node-app-pipeline
snyk auth <auth_token>
snyk test --json > /var/lib/jenkins/reports/snyk-report

echo $? > /dev/null
```

* Add the following stage to the pipeline:

```jenkins
stage ('Snyk Analysis') {
    steps {
        sh '/home/chaos/snyk.sh'
    }
}
```

## Other Tools

* [NSP](https://github.com/nodesecurity/nsp)  
NSP or Node Security Project is now replaced with `npm audit` starting npm@6 and hence, is unavilable to new users.

* [JSPrime](https://github.com/dpnishant/jsprime)  
JSPrime lacks a CLI interface and hence, couldn't be integrated into the CI Pipeline.

* [ScanJS](https://github.com/mozilla/scanjs) (Deprecated)  
ScanJS is depracated and was throwing an exception while being run via the CLI interface.

* [JSpwn](https://github.com/dvolvox/JSpwn) (JSPrime + ScanJs)  
JSpwn combines both JSPrime and JsScan and has a CLI interface as well. The CLI gave garbage output when ran.
