# Configuring Trigger with Webhook

To build and deploy the application based on `push` events and new `releases` on the project repository on GitHub automatically, we need a Jenkins Webhook to handle a trigger that GitHub will send when user selected events occur. The following are the steps to create a Jenkins Webhook with GitHub:

## Configuring Jenkins for Webhook

* Firstly, we need a Personal Access Token (PAT) on GitHub to authenticate Jenkins. A PAT can be generated using this [documentation](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line).
* The PAT generated above is then added as a `Secret Text Credential` in Jenkins under `Credentials > Add New Credential`.
* Added GitHub Server under `Manage Jenkins > Configure System` with Personal Access Token generated as a Credential in Jenkins. The `API URL` used is <https://api.github.com> and the `Manage Hooks` option is checked.
* Selected the `GitHub hook trigger for GITScm polling` option under `Build triggers` for the particular Jenkins project.

## Configuring GitHub for Webhook

On GitHub, we need to add the Webhook to the project repository. The following are the steps to add a Webhook for a GitHub Project:

* We go to the project repository, and there we navigate to `Settings > Webhooks` and click on `Add Webhook` option.
* The `Payload URL` is where we put our Jenkins Servers domain/IP appended with `/github-webhook/` at the end. For example, <http://{JENKINS VM IP}/github-webhook/> is a valid Jenkins Webhook.
* The `Content Type` should be `application/json`.
* Then the required events are selected (Pushes & Releases in this case).
* The `Active` option is checked.
* Save the Webhook.

## Using `ngrok` to handle Webhook over Internet

If we do not have a public IP to handle GitHub's webhook triggers over the web, we can use `ngrok` to provide us with a domain that points to our machine. All the steps below are performed on the Jenkins VM.

* `ngrok` runs as an executable which can be downloaded from [here](https://ngrok.com/download) on the Jenkins VM.
* Unzip the downloaded file as follows:

```bash
unzip /path/to/ngrok.zip
```

* Sign up for an account to get an Authentication Token and then authenticate `ngrok` for initialization as follows:

```bash
./ngrok authtoken <AUTH_TOKEN>
```

* To run `ngrok` and start a HTTP Tunnel, we use the following command:

```bash
./ngrok http 8080
```

**Note**: We use port 8080, instead of 80, as our instance of Jenkins is running on 8080.

* Lastly, we take the URL provided by `ngrok`, append `/github-webhook` at the end, and use it as the `PAYLOAD URL` on GitHub for the Webhook.
