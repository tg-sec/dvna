
# Static Analysis

## Objective

The aim of this section is to understand the tech stack used for the project (DVNA), identify suitable tools to perform SAST and generate a report to provide a solution to 2nd, 3rd and 4th points of the [problem statement](problem_statement.md).

## SAST

SAST or Static Application Security Testing is a process that analyses a project's source code, dependencies and related files for known security vulnerabilities. SAST could also help identify segments of project's logic which might lead to a security vulnerability.

## DVNA's Tech Stack

SAST is a targeted analysis configured based on the technologies being used in a project. Hence, for any meaningful SAST stage in a pipeline (or in general), the tools utilized should be concerned only with the technologies that the project uses. If need be, one could use multiple tools (as one should, in most cases) to cover different types of vulnerabilities and/or technologies present in the project.

To perform static analysis on DVNA, the first step for me was to identify what all technologies comprise DVNA (which is quite obvious given the name is Damn Vulnerable NodeJs Application). So, I figured that NodeJs is the server side language used, along with a SQL database.

## SAST Tools for Node.js Applications

After figuring out the tech stack used, I focused on finding tools that perform static analysis specifically for Nodejs applications. The following are some tools that I found to perform SAST on Nodejs applications with steps to install it and configure them with Jenkins:

### [SonarQube](https://www.sonarqube.org/)

SonarQube is a commercial static analysis tool with a community version with restricted features. I used this [Medium article](https://medium.com/@rosaniline/setup-sonarqube-with-jenkins-declarative-pipeline-75bccdc9075f) to utilise SonarQube with Jenkins and Docker:

* To start the SonarQube server for analysis I used SonarQube's docker image, as it seemed more convenient than an installed setup unlike all the other tools I used which had a very simple installation procedure, and ran it with the following command:

```bash
docker run -d -p 9000:9000 -p 9092:9092 --name sonarqube sonarqube
```

* Then for Jenkins to authenticate with the SonarQube server I created a new Access Token for Jenkins in SonarQube under `Account > Security`.
* I saved the above generated token in Jenkins, under `Credentials >  Add New Credentials` as a `Secret Text` type credential so I could use it later with the credential identity created.
* I added the SonarQube plugin for Jenkins and then navigated to the `SonarQube Server` section under `Manage Jenkins > Configure System`. Here, I checked the `Enable injection of SonarQube server configuration as build environment variables` option to allow SonarQube to inject environment variables at pipeline's runtime and be used in the Jenkinsfile.
* I provided the URL for SonarQube Server (in my case) `localhost:9000` and added the previously saved SonarQube Credentials for authentication.
* Lastly, I added the following stage in the Jenkinsfile for DVNA's analysis by SonarQube, which injects the path to the SonarQube scanner, performs the scan and then saves the report locally:

```jenkins
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
```

**Note**: There are two segments where I drifted away from the article I referred to:

* First is that in the article there is no mention of generating/storing a report.
* Secondly, I left out the `timeout` block in the pipeline stage given in the article.

### [NPM Audit](https://docs.npmjs.com/cli/audit)

NPM Audit is a built-in utlitiy that comes along with `npm@6` which allows for _auditing_ the dependencies being used in the project i.e. it analyses the dependencies against a database for known vulnerabilities. Since, NPM Audit comes along with `npm` itself, is not required to be installed seprately. However, if one has an older version of `npm` on the system, the following command can be used to upgrade:

```bash
npm install -g npm@latest
```

* Now, NPM Audit has a characteristic that gives a non-zero status code, if it finds any vulnerable dependencies. This is so if ran through a pipeline, the build can fail thus, stopping the deployment of vulnerable code. Since, DVNA, quite obviously, has a lot of vulnerabilities, I had to run it through a script to avoid failure of the pipeline after analysis so the stages can still be executed. The script that I wrote, which runs `npm-audit`, formats the output in a JSON format, saves it to a file and finally just echoes the status code, is as follows:

```bash
#!/bin/bash

cd /{JENKINS HOME DIRECTORY}/workspace/node-app-pipeline
npm audit --json > /{JENKINS HOME DIRECTORY}/reports/npm-audit-report

echo $? > /dev/null
```

* Lastly, I added the following stage in the Jenkinsfile to execute the script I wrote:

```jenkins
stage ('NPM Audit Analysis') {
    steps {
        sh '/home/chaos/npm-audit.sh'
    }
}
```

### [NodeJsScan](https://github.com/ajinabraham/NodeJsScan)

NodeJsScan is a static security code scanner for NodeJs applications written in python. It comes with a web-based interface, docker image, Python API as well as a CLI.

* Unlike SonarQube, installing NodeJsScan was just a single command so I went ahead and installed it. To install `NodeJsScan`, I used the following command:

```bash
pip3 install nodejsscan
```

**Note**: I noticed that the package was not available to all users, even though I installed it globally. So, to rectify this issue, I ran the following command: `sudo -H pip3 install nodejsscan`.

* Once NodeJsScan was installed, I ran the below command (taken from the [official documentation](https://github.com/ajinabraham/NodeJsScan)) to test the tool and observe its operation before I added it to the pipeline script:

```bash
nodejsscan --directory `pwd` --output /{JENKINS HOME DIRECTORY}/reports/nodejsscan-report
```

* After observing that NodeJsScan did not exit with a non-zero status code, even if vulnerabilities were found, I realised that the command to execute the scan can be directly added to the pipeline. So, I added the following stage in the Jenkinsfile to perform the scan, and store the report in JSON format on the Jenkins machine:

```jenkins
stage ('NodeJsScan Analysis') {
    steps {
        sh 'nodejsscan --directory `pwd` --output /{JENKINS HOME DIRECTORY}/reports/nodejsscan-report'
    }
}
```

### [Retire.js](https://retirejs.github.io/retire.js/)

Retire.js is a tool that scans the project's dependencies to identify dependencies with versions that have known vulnerabilities. It comes as a plugin for various applications and as a CLI.

* Retire.js was also available to be installed as a package without too much hassle, so I installed it with the following command:

```bash
npm install -g retire
```

**Note**: The `-g` flag specifies that the package needs to be insalled globally.

* Then to look at how Retire.js functions, I ran it with the following command as mentioned in the [official documentation](https://github.com/RetireJS/retire.js) to run the scan on DVNA, output the report in JSON format, save it locally on a file and then exit with a zero status-code even if vulnerabilities are found:

```bash
retire --path `pwd` --outputformat json --outputpath /{JENKINS HOME DIRECTORY}/reports/retirejs-report --exitwith 0
```

* After observing the output and since, I had the ability to alter the status code the program gave on exit, I used the command directly and added the following stage in the Jenkinsfile:

```jenkins
stage ('Retire.js Analysis') {
    steps {
        sh 'retire --path `pwd` --outputformat json --outputpath /{JENKINS HOME DIRECTORY}/reports/retirejs-report --exitwith 0'
    }
}
```

### [OWASP Dependency Check](https://www.owasp.org/index.php/OWASP_Dependency_Check)

As mentioned on OWASP Dependency Check's official site, it is a software composition analysis tool, used to identify if the project has any known security vulnerabilities as part of it's dependencies.

* OWASP Dependency Check comes as an executable for linux and does not require any installation, so I decided to use the binary. I downloaded the executable from this [archive](https://dl.bintray.com/jeremy-long/owasp/dependency-check-5.2.4-release.zip).

* Next, I unzipped the archive and then placed its contents in `/{JENKINS HOME DIRECTORY}/`:

```bash
unzip dependency-check-5.2.4-release.zip
```

* As written in the [official documentation](https://jeremylong.github.io/DependencyCheck/dependency-check-cli/index.html), I ran the following command to start the scan with the executable and save the output to a file in JSON format:

```bash
/{JENKINS HOME DIRECTORY}/dependency-check/bin/dependency-check.sh --scan /{JENKINS HOME DIRECTORY}/workspace/node-app-pipeline --format JSON --out /{JENKINS HOME DIRECTORY}/reports/dependency-check-report --prettyPrint
```

* Since, Dependency-Check doesn't change the status code to a non-zero one, I added the command directly as a stage in the Jenkinfile:

```jenkins
stage ('Dependency-Check Analysis') {
    steps {
        sh '/{JENKINS HOME DIRECTORY}/dependency-check/bin/dependency-check.sh --scan `pwd` --format JSON --out /{JENKINS HOME DIRECTORY}/reports/dependency-check-report --prettyPrint'
    }
}
```

**Note**: By using OWASP's Dependency Check, I happened to introduce a redundant use of a few tools, namely Retire.js and NPM Audit, as they are already a part of Dependency Check's scan methodology.

### [Auditjs](https://github.com/sonatype-nexus-community/auditjs)

Auditjs is a SAST tool which uses [OSS Index](https://ossindex.sonatype.org/), which is a service used to determine if a dependency being used has a known vulnerability, to analyse NodeJs applications.

* Like Retire.js, Auditjs is also available as a npm-package. So, I installed it with the following command:

```bash
npm install -g auditjs
```

* Next, I ran a scan to observe the output provided by Auditjs by running the following command, as mentioned in the [documentation](https://github.com/sonatype-nexus-community/auditjs), while being inside the project directory:

```bash
auditjs --username ayushpriya10@gmail.com --token <auth_token> /{JENKINS HOME DIRECTORY}/reports/auditjs-report 2>&1
```

**Note**: As it appears, Auditjs prints the vulnerabilities found to STDERR and everything else to STDOUT. Hence, I couldn't write the vulnerabilities found to a file directly. So, I used `2>&1` to redirct STDERR output to STDOUT to be able to write everything to a file.

* Like some previous tools, Auditjs gives a non-zero status code, if it finds any vulnerable dependencies, hence, I ran it through a script to avoid build failures with the pipeline. I wrote a script to overcome this issue, as done previously as well, to run the scan and save the report locally. The contents of the script I wrote are as follows:

```bash
#!/bin/bash

cd /{JENKINS HOME DIRECTORY}/workspace/node-app-pipeline
auditjs --username ayushpriya10@gmail.com --token <auth_token> /{JENKINS HOME DIRECTORY}/reports/auditjs-report 2>&1

echo $? > /dev/null
```

* Lastly, I added the following stage to the Jenkinsfile to execute the script I wrote:

```jenkins
stage ('Audit.js Analysis') {
    steps {
        sh '/home/chaos/auditjs.sh'
    }
}
```

### [Snyk](https://github.com/snyk/snyk#cli)

Snyk is a platform that helps monitor (open source) projects present on GitHub, Bitbucket, etc. or locally to identify dependencies with known vulnerabilities. It is available as a CLI and as a docker image.

* Snyk can be installed with `npm` so, I used the following command to do so:

```bash
npm install -g snyk
```

* Snyk required that I authenticated Snyk CLI with an Authentication Token, that can be found on one's profile after signing up for Snyk, before scanning a project, which I did as follows:

```bash
snyk auth <AUTH TOKEN>
```

* Then to perform a scan I ran the following command as mentioned in the [official documentation](https://github.com/snyk/snyk#cli):

```bash
snyk test
```

* Snyk also gives a non-zero status code, if it finds any vulnerable dependencies, hence, I ran it through a script,which performs a scan and stores the report in a JSON format, to avoid build-failure with the pipeline. The contents of the script I wrote are as follows:

```bash
#!/bin/bash

cd /{JENKINS HOME DIRECTORY}/workspace/node-app-pipeline
snyk auth <auth_token>
snyk test --json > /{JENKINS HOME DIRECTORY}/reports/snyk-report

echo $? > /dev/null
```

* Finally, I added a stage to the pipeline which executes the script:

```jenkins
stage ('Snyk Analysis') {
    steps {
        sh '/home/chaos/snyk.sh'
    }
}
```

## SAST Analysis Reports

I stored the reports generated by the various tools in `/reports/` directory inside Jenkins' home directory. Most of these reports were in JSON format, except for SonarQube and Auditjs. SonarQube's report was available on in the web interface and Auditjs' report was normal textual output being printed to console or, in my case, being redirected to a file.

## Other Tools

There were a few other tools avaible to perform SAST on NodeJs applications. They are listed below along with the reason why I chose not to use them for this task:

* [NSP](https://github.com/nodesecurity/nsp)  
According to what NSP's (Node Security Project) official site said, it is now replaced with `npm audit` starting npm@6 and hence, is unavilable to new users but without any loss as it's functionality is available with NPM Audit.

* [JSPrime](https://github.com/dpnishant/jsprime)  
JSPrime appeared to be a really nice tool from its documentation and a demonstration video from a talk in a security conference, but it lacked a CLI interface and hence, I couldn't integrate it into the CI Pipeline.

* [ScanJS](https://github.com/mozilla/scanjs)  
As stated by the official site, ScanJS is now depracated and was throwing an exception when I tried running an available version via the CLI interface. So, I ended up excluding it from my implementation for the task.

* [JSpwn](https://github.com/dvolvox/JSpwn) (JSPrime + ScanJs)  
JSpwn is an SAST tool which combined both JSPrime and ScanJs and had a CLI interface as well but when I executed it in accordance with the official documentation, the CLI gave garbage output without throwing any error and ran without ever terminating. Hence, I chose not to use it in my solution for the task.
