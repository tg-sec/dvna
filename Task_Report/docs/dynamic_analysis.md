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

**Note**: When I ran the scan initially, it dropped an error from Python saying that the 'Connection was Refused' while sending requests to the target through the ZAP proxy. It turned out to be an issue with the command written in the blog that I was following. It exposed the wrong port and hence rectifying the port options in the command to `-p 8090:8080` and `-port 8080` solved the issue and the scan worked. Another thing is that I chose `8090` for the host port as I already had Jenkins running on `8080`. Lastly, I also appended the `--rm` flag to delete the container when I stop it.

* Now to be able to scan DVNA from the CLI with ZAP-CLI, I required a _context_ which basically was a cofiguration written in XML to define how to perform a scan. This context also had a set of credentials in it that were recorded with a [ZEST](https://github.com/mozilla/zest/wiki) script, which is a JSON-based form used to record interactions between a website and a user specially created for security tools focused on web applications. This context file along with the ZEST script would allow zap-cli to authenticate with DVNA to be able to scan the portion of the application that lies behind the login screen.

## TEMP Stuff

The stuff listed below here is to be formatted and put into it's required place once the proper segment for the information is identified and written.

Adding jenkins user to the docker group (not recommended as it is equivalent of giving jenkins root access. Preferred way is to have dokcer infra on a separate machine to isolate access from jenkins). Command to add jenkins to docker group:

```bash
sudo usermod -aG docker jenkins
```

Zap baseline scan:

```bash
docker run -v /home/chaos/ZAP/:/zap/wrk/:rw --name zapbase -i owasp/zap2docker-stable zap-baseline.py -t http://172.17.0.1:9090 -r baseline_report.html -l INFO
```

* for trouble shooting 'source not found' issue with jenkins shell (`sh`) pointing to `/bin/dash` instead of `/bin/bash` was solved with the help of this [article](https://www.ionutgavrilut.com/2019/jenkins-pipelines-sh-source-not-found/).

The following context file is what is needed by the zap-cli to authenticate with the login screen in DVNA.

```zap-context
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<configuration>
    <context>
        <name>Default Context</name>
        <desc/>
        <inscope>true</inscope>
        <tech>
            <include>Db</include>
            <include>Db.CouchDB</include>
            <include>Db.Firebird</include>
            <include>Db.HypersonicSQL</include>
            <include>Db.IBM DB2</include>
            <include>Db.Microsoft Access</include>
            <include>Db.Microsoft SQL Server</include>
            <include>Db.MongoDB</include>
            <include>Db.MySQL</include>
            <include>Db.Oracle</include>
            <include>Db.PostgreSQL</include>
            <include>Db.SAP MaxDB</include>
            <include>Db.SQLite</include>
            <include>Db.Sybase</include>
            <include>Language</include>
            <include>Language.ASP</include>
            <include>Language.C</include>
            <include>Language.JSP/Servlet</include>
            <include>Language.Java</include>
            <include>Language.JavaScript</include>
            <include>Language.PHP</include>
            <include>Language.Python</include>
            <include>Language.Ruby</include>
            <include>Language.XML</include>
            <include>OS</include>
            <include>OS.Linux</include>
            <include>OS.MacOS</include>
            <include>OS.Windows</include>
            <include>SCM</include>
            <include>SCM.Git</include>
            <include>SCM.SVN</include>
            <include>WS</include>
            <include>WS.Apache</include>
            <include>WS.IIS</include>
            <include>WS.Tomcat</include>
        </tech>
        <urlparser>
            <class>org.zaproxy.zap.model.StandardParameterParser</class>
            <config>{"kvps":"&amp;","kvs":"=","struct":[]}</config>
        </urlparser>
        <postparser>
            <class>org.zaproxy.zap.model.StandardParameterParser</class>
            <config>{"kvps":"&amp;","kvs":"=","struct":[]}</config>
        </postparser>
        <authentication>
            <type>4</type>
            <loggedin>Logout</loggedin>
            <loggedout>Login</loggedout>
            <script>
                <name>Authenticating with Login Form in DVNA</name>
                <params>cGFzc3dvcmQ=:YWRtaW4=&amp;dXNlcm5hbWU=:YWRtaW4=</params>
            </script>
        </authentication>
        <users>
            <user>57;false;VXNlciAx;4;</user>
        </users>
        <forceduser>57</forceduser>
        <session>
            <type>0</type>
        </session>
        <authorization>
            <type>0</type>
            <basic>
                <header/>
                <body/>
                <logic>AND</logic>
                <code>-1</code>
            </basic>
        </authorization>
    </context>
</configuration>
```
