# Configuring Trigger with Webhook

* Configured a Personal Access Token on GitHub
* Added GitHub Server under "Configure System" with Personal Access Token generated as a Credential in Jenkins
* Added Webhook trigger under the repository settings
* Used `ngrok` to handle the event
* Selected the "GitHub hook trigger for GITScm polling" option under "Build triggers" for the Jenkins project