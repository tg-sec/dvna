# Dynamic Analysis

## Objective

The aim of this section is to perform DAST for `DVNA` with `OWASP ZAP` and generate a report to provide a solution to the 1st point of the problem statement under `Task 2`.

## DAST

DAST or Dynamic Application Security Testing is a black-box testing technique in which the DAST tool _interacts_ with the application bein tested in its running state to imitate an attacker. Unlike static analysis, in DAST one does not have access to the source code of the application and the tool is completely reliant on the interactivity the application provides. In dyanamic analysis, tools are used to automate attacks on the application ranging from SQL Injection, Input Validation, Cross-Site Scripting, and so forth.

## OWASP ZAP

Docker is a tool designed to provide ease in shipping applications across platforms. It packages the application, along with all it's dependencies and other required libraries into and _image_. Then _containers_ (running instances of the image) be used to run the application on any machine. It is similar to a virtual machine but it differs greatly from them based on the fact that it does not require a full-fledged operating system to run the application. Instead, it runs the application on the system's kernel itself by just bringing along the required libraries with it which could be missing on machines other than the one the application was built on. Further information on docker can be found in the [official documentation](https://docs.docker.com/).

### Configuring OWASP ZAP with Docker
