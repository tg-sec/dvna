# Secrets Management

## Objective

The aim of this section is to set up a _secrets management_ service on the cloud to segregate the app and the associated secrets required for it to function and provide a solution to the 2nd point of the [problem statement](/problem_statement) under `Task 4`.

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

* Here's the AWS Secrets Manager web console after I added all the secrets:
![AWS Secrets Manager](/img/secrets_manager.PNG)

* Below is an image depicting where to retrieve the Secret's ARN on the web console:
![Secret ARN](/img/secret_value.PNG)

* Now, instead of creating a _revision_ to the existing task definition, I created a new task definition following the [steps](/moving_setup_to_aws/#deploying-dvna-on-aws) I used earlier (skipping the first nine steps as they did not need to be redone) with the new task definition's name as `deployDvnaSecretsManager`. This time, however, instead of directly passing the values for the database configurations, I chose the `ValueFrom` option and passed the respective `Secret ARN` that I took note of in the first step as the value for each secret under the environment variables section while providing the container details.
![Fetching Secret with ARN](/img/secrets_fromvalue_arn.PNG)

* Next, I created a new service (`dvnaSSMDeployService`) under the previously created cluster named `deploymentCluster` and created a task from the task definition created in the previous step. This launched DVNA on a new ECS instance with the secrets retrieved from the Secrets Manager.

* I did not have to change anything in the pipeline or the script I wrote earlier to manage deployments through the pipeline as the script was programmed to stop all running tasks under the designated cluster and then display all new tasks that were spun by the services to fetch the public IPs of the DVNA instances deployed.

## HashiCorp Vault

HashiCorp Vault is another secrets manager which is more generic in terms of a solution as it addresses the general problem of managing secrets and is not specific to a particular cloud vendor. It also more configurable than AWS Secrets Manager as it comes along with various secrets engines built-in that can be used as per the project requirements.

### Configuring HashiCorp Vault

Since Vault is an application itself, it was needed to be installed to be used as a Secrets Manager. I used the Jenkins Agent EC2 instance to install and configure Vault with the steps mentioned below:

* I followed along with this [article](https://phoenixnap.com/kb/how-to-install-vault-ubuntu) exactly as it also explained how to set up [Consul](https://www.consul.io/) which is a storage backend, also built by HashiCorp, which can be used in conjunction with Vault to store secrets. The tutorial also helped set up both Vault and Consul as system services which I felt was a better way to use them than explicitly running them manually.

* After completing all the steps mentioned in the article above, I took note of the `root initialization token` used to initialize Vault and the **5** keys required to _unseal_ Vault to retrieve secrets.

* I added all the 5 keys and the root initialization token as `Secret Text` type credentials in Jenkins to use them in the pipeline as and when required.

### Integrating Vault with Pipeline

After Vault was configured and was ready to be used, I went through the steps, mentioned below, to add the secrets and figure out how to retrieve them so I could use them to launch a new ECS task on AWS with the required parameters:

* I _unsealed_ Vault with 3 (out of the 5) keys that were given during the installation of Vault with the command - `vault operator unseal <KEY VALUE>`.
* After Vault was unsealed, I used `vault kv put dvna/db <NAME>=<VALUE>` to add secrets to vault. Here, `dvna/db` path was chosen by me to represent the relevance of the secrets being stored in that particular path.

**Note**: Initially `put` command was not working and I received an error saying - `preflight capability check returned 403, please ensure client's policies grant access to path "kv/dvna/"`. It turned out to be because of the path `dvna/db` not being initialized with the `kv` secrets engine. To solve this I used the command `vault secrets enable -path=dvna kv` according to the official [documentation](https://learn.hashicorp.com/vault/getting-started/secrets-engines).

* To retrieve secrets I used the command - `vault kv get dvna/db` which printed all the secrets in that path (Database name, host, port, username, and password) in a tabular format. Now, I had to fetch just the secret out of the output, instead of formatting the output to suit my needs, Vault came with a utility to only print the value of the secret by specifying the name of the field I need. The command I used to retrieve the secrets' values was `vault kv get -field=<SECRET NAME> dvna/db` where `SECRET NAME` was one the values from - database, username, password, port, and host.

* Now, for the secrets to be retrieved in the pipeline, the vault needs to be unsealed first and then it should also be resealed after the secrets are fetched. To achieve this, firstly, I made use of the `withCredentials` section in the pipeline syntax to fetch secrets from Jenkins' credential manager to retrieve Vault Keys that we stored there earlier and used them with the unseal command in the pipeline stage. I then amended the script I used to stop the currently running ECS tasks and fetch new deployed ECS instances running the latest container images of DVNA and lastly, I sealed the vault again.

* Unsealing (and resealing) Vault with keys from Jenkins Secret Manager in the pipeline script:

```jenkins

stage ('Build and Deploy DVNA') {
    agent {
        label 'jenkins-agent-ec2'
    }

    steps {
        withCredentials([string(credentialsId: 'vault-key-1', variable: 'key1'), string(credentialsId: 'vault-key-2', variable: 'key2'), string(credentialsId: 'vault-key-3', variable: 'key3')]) {
            sh '''
                export VAULT_ADDR=http://127.0.0.1:8200
                vault operator unseal $key1
                vault operator unseal $key2
                vault operator unseal $key3
                /home/ubuntu/task-manager.sh
                vault operator seal
                '''
        }
        sh 'rm -rf ./*'
        sh 'docker rmi $(docker images | grep none | awk \'{print $3}\')'
    }
}
```

* Amendments made to the previous deployment script, in the [previous section](/moving_setup_to_aws/#deploying-dvna-on-aws), to launch ECS tasks with the updated DVNA docker image:

```bash
#!/bin/bash

# Cloning the project repository to build the image
git clone https://github.com/ayushpriya10/dvna.git
cd dvna

# Login to the ECR Registry to push docker images
$(aws ecr get-login --no-include-email --region us-east-2)

# Building the docker image, tagging it as 'latest' and pushing it to the registry
docker build -t dvna_app .
docker tag dvna_app:latest <ID>.dkr.ecr.us-east-2.amazonaws.com/dvna-aws-registry:latest
docker push <ID>.dkr.ecr.us-east-2.amazonaws.com/dvna-aws-registry:latest

# Fetching all active tasks running under the 'deploymentCluster'
task_arns=`aws ecs list-tasks --cluster deploymentCluster | jq '.taskArns' | jq -c '.[]'`

# Stopping all tasks which are running the older docker image of DVNA
for task in $task_arns
do
    echo "Stopping Task: $task"
    task_id=`echo $task | cut -d '/' -f 2 | cut -d '"' -f 1`
    aws ecs stop-task --cluster deploymentCluster --task $task_id > /dev/null
done

# Retrieving secrets from Vault
MYSQL_DATABASE=$(vault kv get -field=database dvna/db)
MYSQL_HOST=$(vault kv get -field=host dvna/db)
MYSQL_PORT=$(vault kv get -field=port dvna/db)
MYSQL_USER=$(vault kv get -field=username dvna/db)
MYSQL_PASSWORD=$(vault kv get -field=password dvna/db)

# Creating JSON with container parameters to override for ECS Task
OVERRIDES="{
    \"containerOverrides\": [{
        \"name\": \"dvna-latest-ssm\",
        \"environment\": [{
            \"name\": \"MYSQL_DATABASE\",
            \"value\": \"$MYSQL_DATABASE\"
        }, {
            \"name\": \"MYSQL_HOST\",
            \"value\": \"$MYSQL_HOST\"
        }, {
            \"name\": \"MYSQL_PORT\",
            \"value\": \"$MYSQL_PORT\"
        }, {
            \"name\": \"MYSQL_PASSWORD\",
            \"value\": \"$MYSQL_PASSWORD\"
        }, {
            \"name\": \"MYSQL_USER\",
            \"value\": \"$MYSQL_USER\"
        }]
    }]
}"

# Creating JSON with Network Configuration for the ECS Task
NETWORK_CONFIG='{
    "awsvpcConfiguration": {
        "subnets": ["subnet-fb41fdb7"],
        "securityGroups": ["sg-0b3be5dc4044f6f52"],
        "assignPublicIp": "ENABLED"
    }
}'

# Launching a new ECS Task, independent of existing services in the cluster, to run a Task with overriden parameters
aws ecs run-task --overrides "$OVERRIDES"  --cluster deploymentCluster --task-definition deployDvnaSecretsManager:6 --count 1 --launch-type FARGATE --network-configuration "$NETWORK_CONFIG" > /dev/null

# Waiting for 'dvnaDeployService' to automatically run a new task
echo "Waiting for 1 minute for AWS to bring up new ECS Tasks..."
sleep 1m

# Fetching all active tasks under 'deploymentCluster'
task_arns=`aws ecs list-tasks --cluster deploymentCluster | jq '.taskArns' | jq -c '.[]'`

# Printing the URL where DVNA instance(s) were deployed
for task in $task_arns
do
    echo "New Task ARN: $task"

    task_id=`echo $task | cut -d '/' -f 2 | cut -d '"' -f 1`
    task_attachments=`aws ecs describe-tasks --cluster deploymentCluster --tasks $task_id | jq '.tasks[0].attachments[0].details' | jq -c '.[]'`
    for attachment in $task_attachments
    do
        name=`echo $attachment | jq '.name'`

        if [ "$name" == "\"networkInterfaceId\"" ]; then
            interface_id=`echo $attachment | jq '.value'`
            interface_id=`echo $interface_id | tr -d "\""`
        fi
    done
    public_ip=`aws ec2 describe-network-interfaces --network-interface-ids $interface_id | jq '.NetworkInterfaces[0].Association.PublicIp' | tr -d "\""`
    echo "DVNA is deployed at: http://$public_ip:9090"
done
```

## Comparing AWS Secrets Manager and HashiCorp Vault

The tools I used for Secrets Management are a bit difficult to compare, unlike the other comparative observations I wrote as part of this report previously as both of these tools solve the same problem but have different use-cases.

AWS Secrets Manager required minimal effort in terms of storing secrets, unlike HashiCorp Vault which required extensive setup and configuration. It also had the added ease of fetching secrets from it directly by using the `ARN` for the required in the container details while defining a new task. The biggest downside for AWS Secrets Manager was that it was an AWS-specific solution and that is exactly one of the strongest benefits of HashiCorp's Vault that it is independent of platform or cloud providers. Vault also is more customizable as compared to AWS Secret Manager. Some of these customizable features are - allowing the user to decide what path to store secrets on, what secrets engine to use to encrypt the secrets and which set of keys to use to unseal Vault.

In the context of the problem statement that I had, AWS Secrets Manager is a better solution to use as I was specifically supposed to use AWS as the cloud provider and hence, it makes sense to use the tool/system which requires the least effort to operate. However, if a more general solution was needed or a scenario where the secrets are to be shared with services that do not integrate with AWS Secrets Manager, HashiCorp Vault would be the optimal choice because of its portability in terms on integration with external systems.
