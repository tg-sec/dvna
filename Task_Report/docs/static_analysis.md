
# Static Analysis

## SAST Tools for Node.js Applications:

* [SonarQube](https://www.sonarqube.org/)
* [NPM Audit](https://docs.npmjs.com/cli/audit)
* [NodeJsScan](https://github.com/ajinabraham/NodeJsScan)
* [Retire.js](https://retirejs.github.io/retire.js/)
* [OWASP Dependency Checker](https://www.owasp.org/index.php/OWASP_Dependency_Check)
* [auditjs](https://github.com/sonatype-nexus-community/auditjs)

```bash
auditjs --username ayushpriya10@gmail.com --token 55716e0a92c8c53ae2db6296b62f68860ef5f1af
```

* [Synk](https://github.com/snyk/snyk#cli)

* [NSP](https://github.com/nodesecurity/nsp) (This is now replaced with `npm audit` starting npm@6)
* [JSpwn](https://github.com/dvolvox/JSpwn) (JSPrime + ScanJs)
* [JSPrime](https://github.com/dpnishant/jsprime)
* [ScanJS](https://github.com/mozilla/scanjs) (Deprecated)

Resource for combined usage of Dependency Check, Retirejs, Snyk (and NSP): <https://blog.developer.bazaarvoice.com/2018/02/27/getting-started-with-dependency-security-and-nodejs/>

### Static Analysis with SonarQube

Plugin used for SAST: SonarQube

* Used SonarQube's docker image to run the application
* Configured the jenkins plugin for SonarQube with Access Token