# Lab02: The Cloud

We will be using AWS as cloud platform for some of your homeworks and
Labs. AWS gives all W251 students a promotional credit of
\$1000/semester. While this will be sufficient to complete your
homeworks and projects, leaving any unused resources like GPU enabled
EC2 instances, large datasets on S3 can consume the funds very quickly.
We strongly encourage you to de-provision unused resources promptly,
watch your spend/billing reports frequently, create Billing alerts to
avoid incurring extra costs.

**Any spend beyond the \$1000 limit will be student's responsibility!**

# Create and Setup your AWS account

-   Navigate to https://aws.amazon.com

-   Click on Create an AWS account (top right)

-   Follow the prompts to create a new account using your Berkeley
    student email id (you have to use your personal credit card)

-   Once complete, Login to your account

-   Click on your account id (top right) and chose \"My Account\" -\"Credits\"

-   Insert the promotion code shared by your instructor and Redeem. You
    should see your available credits (\$1000) at the bottom of the page

# Add an IAM user, group and a key pair

AWS Best practices deletes Access Key and Secret Key credentials for
Root user and recommends creating separate IAM users. These are needed
to enable CLI and API access.

-   Goto Services -- Select IAM

-   Click on Add User

    -   Set the User Name
    -   Select both Access Types (`Programmatic` and `AWS Management Console`)
    -   Accept the defaults for the password settings
    -   Click the "Next" button
    -   Create a Group
    -   Give your group a name
    -   **select `AdministratorAccess` role**)
    -   Ensure that your new group is selected, then click the "Next" button
    -   Do not add any Tags
    -   Click the "Create User" button
    -   Select to have User Access and Secret Key created and download
        the details to xls
    -   On your workstation (Mac or windows), download, install and configure
        AWS CLI-v2 using the new User credentials you just created.
        Follow the instructions from the link below.

        <https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html>
        -aws configure (enter access key, security key and select region such as us-east-1)

-  Go to Services-EC2-Keypairs

-  Create new keypair and download the .pem file
```
# Once downloaded, adjust the permissions of the pem file on your workstation
# Run this command to remove permissions from other users:
chmod 400 *.pem file 
```

-   Add the downloaded key pair to SSH identities on your workstation.
```
ssh-add -K "your_keypair.pem" 
ssh-add -L
```   

# Launch and Test Key AWS Resources

#### Create Default VPC
```
aws ec2 create-default-vpc
aws ec2 describe-vpcs | grep VpcId
# find the vpc-id of the one you just created
```
**NOTE: If you receive an UnauthorizedOperation error when creating the default VPC, ensure that you added the AdministratorAccess role to the Group you created above**

#### Create Public and Private security groups
```
# Use the VpcId from the previous step
aws ec2 create-security-group --group-name PublicSG --description "Bastion Host Security group" --vpc-id vpc-XXXXXXXX

# Extract GroupID of the Public security group created in the previous step
aws ec2 describe-security-groups | grep -A4 PublicSG | grep GroupId 

# If you do not see a GroupID, try this:
aws ec2 describe-security-groups | grep -A20 PublicSG | grep GroupId

# Use the VpcId from the previous step
aws ec2 create-security-group --group-name PrivateSG --description "Private instances Security group" --vpc-id vpc-XXXXXXXX

# Extract GroupID of the Private security group created in the previous step
aws ec2 describe-security-groups | grep -A4 PrivateSG | grep GroupId

# If you do not see a GroupID, try this:
aws ec2 describe-security-groups | grep -A20 PrivateSG | grep GroupId
```

#### Add SSH Ingress rules to Security groups
Using the Public and Private Security Group IDs from the previous step, authorize ssh ingress to the Security Groups:
```
aws ec2 authorize-security-group-ingress --group-id YOUR_PUBLIC_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress --group-id YOUR_PRIVATE_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0
```

#### Launch Bastion EC2 Instance(JumpBox) into the public Security Group
Use Ubuntu AMI on t2.large instance in the default VPC.  
Replace the string `YOUR_KEY_NAME` with the name of your key pair created above. You can find it using the command `aws ec2 describe-key-pairs | grep KeyName`.

```
# Create the instance
aws ec2 run-instances --image-id ami-0bcc094591f354be2 --instance-type t2.large --security-group-ids YOUR_PUBLIC_GROUP_ID --associate-public-ip-address --key-name YOUR_KEY_NAME

# Retrieve the Public DNS name
aws ec2 describe-instances | grep PublicDnsName
```
    
If you get a message that the image is not available - `The image id '[ami-0bcc094591f354be2]' does not exist` - it could be that the image is not available in your conifgured region. 

You can pick an image in your region, by running the below, 

```
aws ec2 describe-images  --filters  Name=name,Values='ubuntu/images/hvm-ssd/ubuntu-bionic-18.04*' Name=architecture,Values=x86_64   | head -100
```

#### Launch Private EC2 instance into Private Security Group using Ubuntu
```
aws ec2 run-instances --image-id ami-0bcc094591f354be2 --instance-type t2.micro --security-group-ids YOUR_PRIVATE_GROUP_ID --key-name YOUR_KEY_NAME

# Retrieve the PublicDnsName of the new instance
aws ec2 describe-instances | grep PublicDnsName

```
#### SSH into Baston Host first and then to the Private instance
```
# From your workstation
ssh -A ubuntu@YOUR_PUBLIC_EC2_NAME.compute-1.amazonaws.com

# Then ssh from the bastion host to the private instance
ssh ubuntu@YOUR_PRIVATE_EC2_NAME.compute-1.amazonaws.com
```

#### Delete Private instance but keep Bastion Host and other resources for other homeworks and labs
   
```
aws ec2 describe-instances | grep InstanceId
```
A list of ids will appear. You can terminate the ID for your private instance with,
```
aws ec2  terminate-instances --instance-ids i-0d0fd239ccae129e4
```


By default, Amazon EC2 deletes all EBS volumes that were attached when the instance launched. Volumes attached after instance launch continue running.


This HW further builds on using public cloud services with a primer on AWS Sagemaker. Sagemaker is a fully managed Machine Learning Service enabling 
to easily build, train and deploy ML models with an integrated Jupyter Notebook instance. 


# Setup and run Sagemaker Example

-   Readup details on Sagemaker. https://docs.aws.amazon.com/sagemaker/latest/dg/ex1-preprocess-data.html
-   
-   Create Sagemaker notebook instance.  https://docs.aws.amazon.com/sagemaker/latest/dg/gs-console.html

-   Create a jupyter notebook and save it. https://docs.aws.amazon.com/sagemaker/latest/dg/ex1-prepare.html

-   Run the end to end Example https://github.com/aws/amazon-sagemaker-examples/blob/master/sagemaker-python-sdk/1P_kmeans_highlevel/kmeans_mnist.ipynb
(This incl. downloading MNIST dataset to your account's default S3 Object storage)

-   Once complete, Login to your account and check the resources the example created

-   Cleanup the environment by deleting the deployed endpoint, Notebook instance and S3 to not incur AWS charges


# Submit answers to the following Questions on ML services 

-   How can Sagemaker help Data Scientists
  
-   Advantages/Disadvantages of Sagemaker

-   Integration of Sagemaker with other AWS services such as Lambda functions, Kubernetes etc.,

-  When to use what algorithms

-  What are other ML services available from other cloud service providers such as Google, Microsoft, IBM?

