# Problem Statement

1. Setup a basic pipeline (use [Jenkins](https://jenkins.io/)) for generating a security report for [DVNA](https://github.com/appsecco/dvna).
2. The DVNA code should be downloaded from Github and then undergo static analysis.
3. As part of the project understand what is the tech stack for DVNA hence what potential static analysis tools can be applied here.
4. Once a static analysis is done the report should be saved.
5. Next, the DVNA should get deployed in a server.
6. Setup the infrastructure, required for the task, on 2 virtual machines running locally on a laptop. One VM contains the Jenkins and related infrastructure, and the second VM is for deploying the DVNA using the pipeline.
7. Do document extensively in markdown and deploy the documentation in a MkDocs website on the second VM.
8. Additionally, there was some inferred task to address in the problem statement:
    1. To create a comparative report about how various SAST tools performed.
    2. To create a webhook to trigger the build when a `push` event occurs on the project repository on GitHub.
