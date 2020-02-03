# Dynamic Analysis

## Objective

The aim of this section is to perform DAST for `DVNA` with `OWASP ZAP` and generate a report to provide a solution to the 1st point of the [problem statement](/problem_statement) under `Task 2`.

## DAST

DAST or Dynamic Application Security Testing is a black-box testing technique in which the DAST tool _interacts_ with the application bein tested in its running state to imitate an attacker. Unlike static analysis, in DAST one does not have access to the source code of the application and the tool is completely reliant on the interactivity the application provides. In dyanamic analysis, tools are used to automate attacks on the application ranging from SQL Injection, Input Validation, Cross-Site Scripting, and so forth.

## OWASP ZAP

ZAP or Zed Attack Proxy is an open-source tool used to perform dynamic application security testing designed specifically for web applications. ZAP has a desktop interface, APIs for it to be used in an automated fashion and also a CLI. It imitates an actual user where it interacts with the application to perform various attacks. ZAP comes with a plethora of options to use, for which further details can be found [here](https://www.zaproxy.org/getting-started/). ZAP also comes as a [Docker](https://docs.docker.com/) image which is more convenient to use specially if one is using the CLI interface.

Docker is a tool designed to provide ease in shipping applications across platforms. It packages the application, along with all it's dependencies and other required libraries into an _image_. Then _containers_ (running instances of the image) can be used to run the application on any machine. It is similar to a virtual machine but it differs greatly from them based on the fact that it does not require a full-fledged operating system to run the application. Instead, it runs the application on the system's kernel itself by just bringing along the required libraries with it which could be missing on machines other than the one the application was built on. Further information on docker can be found in the [official documentation](https://docs.docker.com/).

## Configuring OWASP ZAP with Docker

There's not really any configuration required to run ZAP with Docker other than pulling the image from [Docker Hub](https://hub.docker.com). I used this [documentation](https://blog.mozilla.org/fxtesteng/2016/05/11/docker-owasp-zap-part-one/) from Mozilla as it had a lot of errors demonstrated along with their rectification steps for starting out with ZAP. This was missing from all other sources I found.

* To start off with ZAP, I needed to pull its docker image which I did by running:

```docker
docker pull owasp/zap2docker-stable
```

* Then I tried to run the tool with its CLI interface as such:

```docker
docker run -e LC_ALL=C.UTF-8 -e LANG=C.UTF-8 -i owasp/zap2docker-stable zap-cli --help
```

**Note**: Due to an encoding inconsistency between Python2 and Python3, I had to set some environment variables, which can be seen in the above command, to explicitly mention the encoding to be used as ZAP failed to start otherwise.

* Next I ran a `quick-scan` to have a look at how ZAP outputs information:

```docker
docker run -e LC_ALL=C.UTF-8 -e LANG=C.UTF-8 -i owasp/zap2docker-stable zap-cli quick-scan --start-options '-config api.disablekey=true' --self-contained --spider -l Low http://172.17.0.1:9090
```

**Note**: Since ZAP is running inside a Docker container, we can not use `localhost` or `127.0.0.1` as then the container would take it to be it's own host. So, to overcome this issue we use the IP assigned to `docker0`, the network interface created for Docker. This IP can be found with this one-liner: `$(ip -f inet -o addr show docker0 | awk '{print $4}' | cut -d '/' -f 1)`.

**Note**: As ZAP also has an API that can be used to interact with it programmatically, I had to use `--start-options '-config api.disablekey=true'` as otherwise ZAP tried (and failed) to connect to the proxy as the API key was not specified. Also, the `-l` option specifies the severity level at which ZAP should log a vulnerability to console (or to a report).

* Now, I tried the `active-scan` option. For this I first needed to start the _daemon_ for zap to be accessed by the CLI and then run the scan against DVNA. This step was not required previously as while running a `quick-scan`, the daemon is automatically started to run the scan and stopped after the scan is finished. To do run the daemon with Docker, I ran the following command (with the `-u zap` segment to execute things with the `zap` user instead of Docker's default `root` user):

```docker
docker run --rm -e LC_ALL=C.UTF-8 -e LANG=C.UTF-8 --name zap -u zap -p 8090:8080 -d owasp/zap2docker-stable zap.sh -daemon -port 8080 -host 0.0.0.0 -config api.disablekey=true
docker exec <CONTAINER NAME/ID> zap-cli open-url <TARGET URL>
docker exec <CONTAINER NAME/ID> zap-cli active-scan <TARGET URL>
```

**Note**: Before a scan be be run, I had to run `open-url` to add the target URL to the configuration in ZAP-CLI, without this, `active-scan` option will not start a scan on the target.

**Note**: When I ran the scan initially, it dropped an error from Python saying that the 'Connection was Refused' while sending requests to the target through the ZAP proxy. It turned out to be an issue with the command written in the blog that I was following. It exposed the wrong port and hence rectifying the port options in the command to `-p 8090:8080` and `-port 8080` solved the issue and the scan worked. Another thing is that I chose `8090` for the host port as I already had Jenkins running on `8080`. Lastly, I also appended the `--rm` flag to delete the container, automatically, when I stop it.

* Now to be able to scan DVNA from the CLI with ZAP-CLI, I required a _context_ which basically was a cofiguration written in XML to define how to perform a scan. This context also had a set of credentials in it that were recorded with a [ZEST](https://github.com/mozilla/zest/wiki) script, which is a JSON-based form used to record interactions between a website and a user specially created for security tools focused on web applications. This context file along with the ZEST script would allow zap-cli to authenticate with DVNA to be able to scan the portion of the application that lies behind the login screen. I used the browser-based GUI to generate the context and the Zest script and exported them to the machine. But importing them created various complications as zap-cli was unable to identify the embedded Zest script in the context provided to it.

* Due to the above complications, I decided to use Zap's baseline scan instead. To start off ZAP baseline scan with the docker image, I ran the following command, by following this [documentation](https://github.com/zaproxy/zaproxy/wiki/ZAP-Baseline-Scan):

```bash
docker run -i owasp/zap2docker zap-baseline.py -t "http://172.17.0.1:9090" -l INFO
```

* Now, to save the report on the Jenkins machine, I needed to mount a volume with Docker. To mount the current working directory, I used the `-v` flag, as mentioned in the docker [documentation](https://docs.docker.com/storage/volumes/), save the scan output to a HTML report on the Jenkins machine:

```bash
docker run -v $(pwd):/zap/wrk/ -i owasp/zap2docker zap-baseline.py -t "http://172.17.0.1:9090" -r baseline-report.html -l PASS
```

**Note**: While running ZAP scans above, I explicitly ran DVNA, without Jenkins, for it to be tested.

## Integrating ZAP with Jenkins

* After figuring out how to use the baseline-scan and it's various options, I started integrating the scan as part of DAST in the Jenkins pipeline. But before I could scan DVNA with ZAP Baseline, I needed to build the dependencies and start and instance of DVNA. To do the same, I also had to fetch code from the repository on GitHub (explicitly, because I didn't use a Jenkinsfile for this task).

**Note**: I chose to build a new pipeline just for DAST, as combining SAST and DAST in a single pipeline would have taken too much time during each execution which felt unnecessary at this point.

* To start off, I added a stage to fetch the code from the GitHub repository as follows:

```jenkins
stage ('Fetching Code') {
    steps {
        git url: 'https://github.com/ayushpriya10/dvna.git'
    }
}
```

* Next, I built the dependencies for DVNA, as I did while performing SAST, and started an instance of DVNA, as mentioned in the stage mentioned below:

```jenkins
stage ('Building DVNA') {
    steps {
        sh '''
            npm install
            source /{PATH TO SCRIPT}/dast/env.sh
            pm2 start server.js
        '''
    }
}
```

**Note**: I kept all the required environment variables in the `env.sh` file which can seen in the above stage, and used it to export those variables for DVNA to be able to connect with the database. While trying to export the variables, the `shell` that comes along with Jenkins kept throwing an error saying it didn't recognise the comand `source`. This turned out to be because that by default the `sh` shell in Jenkins point to `/bin/dash` which doesn't have the command `source`. To rectify this, I changed the Jenkins shell to point to `/bin/bash` instead with this command - `sudo ln -sf /bin/bash /bin/sh`, which I found in this [blog](https://www.ionutgavrilut.com/2019/jenkins-pipelines-sh-source-not-found/).

* Now, that DVNA was up and running, ran the baseline scan on it with docker and Zap. But I had to wrap the command in a shell script to evade the non-zero status code that ZAP gives on finding issues. So, I wrote the script, `baseline-scan.sh`, mentioned below and made it executable with `chmod +x`:

```bash
cd /{JENKINS HOME DIRECTORY}/workspace/node-dast-pipeline

docker run -v $(pwd):/zap/wrk/ -i owasp/zap2docker zap-baseline.py -t "http://172.17.0.1:9090" -r baseline-report.html -l PASS

echo $? > /dev/null
```

**Note**: One thing to take note of is that Jenkins would require to use `sudo` when running docker commands as it's not part of the `docker` user group on the system. This is the preferred way, that required docker setup is on another VM and Jenkins SSHs into the other VM with access to run docker commands as a sudo user. But for the purpose of this task, I did not setup another VM, instead I added the `jenkins` user to the docker user group with - `sudo usermod -aG docker jenkins`, for it to be able to perform operation without using `sudo`. This, however, is not recommended.

* I added a stage in the Jenkins Pipeline, to execute the shell script and generate the DAST report. The stage's content is mentioned below:

```jenkins
stage ('Run ZAP for DAST') {
    steps {
        sh '/{PATH TO SCRIPT}/baseline-scan.sh'
    }
}
```

**Note**: Running the pipeline threw an access error, saying the report could not be written in the directory. This was because the `zap` user in the docker container did not have write permission for Jenkins' workspace. So, for the sake of the task, I modified the permissions of the `node-dast-pipelin/` directoy with `chmod 777 node-dast-pipeline/`. This is also not recommended. If the permissions need to be changed, they should be specific an exact in terms of the access they grant which should not be more than that is required.

* Lastly, I added a stage to stop the instance of DVNA that was running as it was no longer needed and moved the report generated from the workspace directory to the reports directory that I've been using for the tasks:

```jenkins
stage ('Take DVNA offline') {
    steps {
        sh 'pm2 stop server.js'
        sh 'mv baseline-report.html /{JENKINS HOME DIRECTORY}/reports/zap-report.html'
    }
}
```

The complete pipeline script is as follows:

```jenkins
pipeline {

    agent any

    stages {
        stage ('Fetching Code') {
            steps {
                git url: 'https://github.com/ayushpriya10/dvna.git'
            }
        }

        stage ('Building DVNA') {
            steps {
                sh '''
                    npm install
                    source /{PATH TO SCRIPT}/dast/env.sh
                    pm2 start server.js
                '''
            }
        }

        stage ('Run ZAP for DAST') {
            steps {
                sh '/{PATH TO SCRIPT}/baseline-scan.sh'
            }
        }

        stage ('Take DVNA offline') {
            steps {
                sh 'pm2 stop server.js'
                sh 'mv baseline-report.html /{JENKINS HOME DIRECTORY}/reports/zap-report.html'
            }
        }
    }
}
```

**Note**: I also tried running a `docker` agent in the Jenkins pipeline to execute zap-baseline scan but it kept throwing an access error (different than the one mentioned above). This issue was not recitified yet. The stage that I wrote (but was not working) is as follows:

```jenkins
stage ('Run ZAP for DAST') {
    agent {
        docker {
            image 'owasp/zap2docker-stable'
            // args '-dir /zap/wrk/.ZAP/'
            // args '-v $(pwd):/zap/wrk/'
            args '-v /var/lib/jenkins/workspace/node-dast-pipeline/:/zap/wrk/'
        }
    }
    steps {
        sh 'zap-baseline.py -t http://172.17.0.1:9090 -r zap_baseline_report.html -l PASS'
    }
}
```

## DAST Report generated by ZAP

The complete report generated by the ZAP baseline scan can be found [here]().