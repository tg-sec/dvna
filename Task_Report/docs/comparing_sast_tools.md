# Comparing SAST Tools

A comparitive look at the various findings the various tools had.

## Vulnerability Reports Generated

The following are the various vulnerabilities found by the tools used to perform SAST on DVNA:

### SonarQube

* SonarQube didn't find any security vulnerabilities. It, instead, found linting and syntax based bugs.

### NPM Audit

* NPM Audit found 5 security vulnerabilities:
    * 3 Critical
    * 1 High
    * 1 Low

* Vulnereble modules identified:
    * mathjs (2 Critical Vulnerabilities)
    * node-serialize (1 Critical Vulnerability)
    * typed-function (1 High Vulnerability)
    * express-fileupload (1 Low Vulnerability)

### NodeJsScan

* NodeJsScan found a 34 dependency-based vulnerabilities:
    * Deserialization with Remote Code Execution (8 Vulnerabilities)
    * Open Redirect (1 Vulnerabilities)
    * SQL Injection (1 Vulnerabilities)
    * Secrete Hardcoded (1 Vulnerabilities)
    * Server Side Injection (1 Vulnerabilities)
    * Unescaped Variables (12 Vulnerabilities)
    * Weak Hash Used (11 Vulnerabilities)

* Additionally, NodeJsScan found 5 web-based vulnerabilities:
    * Missing Header
        * Strict-Transport-Security (HSTS)
        * Public-Key-Pin (HPKP)
        * X-XSS-Protection
        * X-Download-Options
    * Information Disclosure
        * X-Powered-By

### Retire.js

* Retire.js found 3 security vulnerabilities:
    * 1 High
    * 1 Medium
    * 1 Low

* Vulnerable modules identified:
    * node-serialize 0.0.4 (High)
    * jquery 2.1.1 (Medium)
    * jquery 3.2.1 (Low)

### OWASP Dependency Check

* Dependency-Check identified 7 security vulnerabilities:
    * 3 Critical
    * 1 High
    * 2 Medium
    * 1 Low

* Vulnerable modules identified:
    * mathjs 3.10.1 (Critical)
    * node-serialize 0.0.4 (Critical)
    * sequelize 4.44.3 (Critical)
    * typed-function 0.10.5 (High)
    * jquery-2.1.1.min.js (Medium)
    * jquery-3.2.1.min.js (Medium)
    * express-fileupload 0.4.0 (Low)

### Auditjs

* Auditjs found 22 security vulnerabilities in the 5 vulnerable modules identified:
    * Nodejs 8.10.0 (14 Vulnerabilities)
    * mathjs 3.10.1 (3 Vulnerabilities)
    * typed-function 0.10.5 (2 Vulnerabilities)
    * sequelize 4.44.3 (2 Vulnerabilities)
    * express-fileupload 0.4.0 (1 Vulnerability)

### Snyk

* Snyk indentifeid 8 security vulnerabilities:
    * 6 High:
        * express-fileupload (Denial of Service; 1 Vulnerability)
        * typed-function (Arbitary Code Execution; 1 Vulnerability)
        * mathjs (Arbitary Code Execution; 3 Vulnerabilities)
        * node-serialize (Arbitary Code Execution; 1 Vulnerability)
    * 2 Medium:
        * mathjs (Arbitary Code Execution; 2 Vulnerabilities)

## Conclusion

Based on the reports generated and the vulnerabilities found by the various scanner used to analyse DVNA, the ranking of these tools from best to worse (in my opinion) is as follows:

* NodeJsScan (34 dependency-based + 5 web-based)
* Auditjs (22)
* Snyk (8)
* OWASP Dependency Check (7)
* NPM Audit (5)
* Retire.js (3)
* SonarQube (0)
