# Secrets Management

## Objective

The aim of this section is to set up a _secrets management_ service on the cloud to segregate the app and the associated secrets required for it to function and provide a solution to the 2nd point of the problem statement under `Task 4`.

## Secrets Management

Secrets management refers to the tools and methods for managing digital authentication credentials (secrets), including passwords, keys, APIs, and tokens for use in applications, services, and privileged accounts. Secret Management services also provide additional services associated with managing various credentials such as rotation of secrets.

## AWS Secrets Manager

The secrets in the context of DVNA are the values for database configuration that DVNA requires to access the database. These secrets are the database host, port, username, password, and database name. Up to this point, I was using `bash` scripts to _source_ the required values and export them as environment variables. For the deployment on AWS with ECS, I added these values as environment variables while creating the task definition for DVNA deployment. But these values were in plaintext. To make use of secrets management, I decided to use Amazon's Secrets Manager, a secrets management service that comes along with AWS services.

To utilize Secrets Manager and import secrets through it for the container's database configuration I needed the `SecretsManagerReadWrite` policy to be attached to my IAM role. After the policy was attached, I followed the following steps:

* The first thing I had to do was to create the secrets themselves. I used the AWS CLI to create the secrets with the names `/db/dvna/username`, `/db/dvna/password`, `/db/dvna/host`, `/db/dvna/port` and `/db/dvna/database`, provided a description and the secret values. I also took note of the `Secret ARN` received in the response for each secret created. The command I used is mentioned below:

```bash
aws secretsmanager create-secret --name <SECRET NAME> --secret-string <SECRET VALUE> --description <DESCRIPTION>
```

**Note**: Using the console to create the secrets was a bit confusing initially. Selecting 'Other type of secrets' option prompted for either a `key-value` or a `plaintext` type secret. The field for entering a plaintext secret had a JSON-like template structure present which turned out to be unnecessary. Removing the template JSON with just the required value worked as well to create secrets from the web console.

* Now, instead of creating a _revision_ to the existing task definition, I created a new task definition following the [steps](/moving_setup_to_aws/#deploying-dvna-on-aws) I used earlier (skipping the first nine steps as they did not need to be redone) with the new task definition's name as `deployDvnaSecretsManager`. This time, however, instead of directly passing the values for the database configurations, I chose the `ValueFrom` option and passed the respective `Secret ARN` that I took note of in the first step as the value for each secret under the environment variables section while providing the container details.

* Next, I created a new service (`dvnaSSMDeployService`) under the previously created cluster named `deploymentCluster` and created a task from the task definition created in the previous step. This launched DVNA on a new ECS instance with the secrets retrieved from the Secrets Manager.

* I did not have to change anything in the pipeline or the script I wrote earlier to manage deployments through the pipeline as the script was programmed to stop all running tasks under the designated cluster and then display all new tasks that were spun by the services to fetch the public IPs of the DVNA instances deployed.
