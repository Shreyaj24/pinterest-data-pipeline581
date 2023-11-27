# **Pinterest Data Pipeline project**
Pinterest crunches billions of data points every day to decide how to provide more value to their users. In this project, we create a similar system using the AWS Cloud.
## **Milestone2** 
Initial process to sign in to AWS to start building the data pipeline.
-   **Task1:**        
    -   To get hands on on some infrastructure similar to industry standard while working as Data Engineer
    -   In the script *user_posting_emulation.py* which contains three tables with data resembling data received by the pinterest API when a POST request is made by a user uploading data to Pinterest:
        -   *pinterest_data* contains data about posts being updated to Pinterest.
        -   *geolocation_data* contains data about the geolocation of each Pinterest post found in pinterest_data.
        -   *user_data* contains data about the user that has uploaded each post found in pinterest_data
-   **Task2:**
    -   To sign in AWS console with Account_ID, IAM user name. 

## **Milestone3** 
Configuration of Amazon EC2 instance to use an Apache Kafka client machine.
-   **Task1:**
    -  Create *key pair* file (.pem key file) locally
        - Step1:
            -   Create key piar file locally which will ultimately allow to connect to EC2 instance. Navigate to **Parameter store** in AWS account.
            - Using *KeyPairID*, find specific key pair associated with your EC2 instance. Select the *key pair* under the *value* field select *show*. Copy entirely inc;uding BEGIN and END header and paste in the .pem file created in VSCode.
        - Step2:
            -   Navigate to EC2 console and identify the instance with your unique UserId.
-   **Task2:**
    -   Using *Connect* instructions(SSH client) connect to the EC2 instance:
    **ssh -i "0xxnxxxxnnnx-key-pair.pem" root@ec2-nn-nnn-nn-nn.compute-n.amazonaws.com**.
-   **Task3:**
 Here AWS account has been provided with access to an IAM authenticated MSK cluster. In order to connect to IAM authenticated cluster, we need to install the appropriate packages on EC2 client machine.
    -   Step1:
        -  First, install Kafka on client EC2 machine. 
        -   Here we install ***Java***  using  below command:
        *sudo yum install java-1.8.0* 
        - Then we download Apache Kafka using below command:
        **wget https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz**     
        **tar -xzf kafka_2.12-2.8.1.tgz**
        - This creates Kafka directory inside EC2 client.
    - Step2:
        -   To connect to a cluster that uses IAM authentication, we need to follow additional steps before we are ready to create a topic on our client machine.
        -   First, navigate to Kafka installation folder and then in the libs folder. Inside here we will download the IAM MSK authentication package from Github, using the following command:  
        ***wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.5/aws-msk-iam-auth-1.1.5-all.jar***
    - Step3:
        -   Before IAM cluster authentication, it is required to replace ARN with assigned ARN IN IAM.
        -   Navigate IAM console -> Roles section -> select the one with the following format: <your_UserId>-ec2-access-role -> Go to the Trust relationships tab and select Edit trust policy ->   Click on the Add a principal button and select IAM roles as the Principal type ->   Replace ARN with the <your_UserId>-ec2-access-role ARN you have just copied
        -   By above steps, ARN has necessary permissions to authenticate to the MSK cluster.
    - Step4:
        -   To configure Kafka client to use AWS IAM authentication to the cluster, we need to modify the *client.properties* file inside kafka_folder/bin directorey. If not present we can create it. PSB:
        ![client.properties](pinterest_img/Client_properties_file.JPG)

-   **Task4:**
To create Kafka topics.
    - Step1:
        -   To create kafka topic, certain information retrieval is necessary about MSK cluster: 
            -   *Bootstrap servers string*          
            -  *Plaintext Apache Zookeeper connection string*  
            Above information is retreived from the MSK Management console.
        -   Post which we create the following three topics:
            -   <your_UserId>.pin for the Pinterest posts data
            -   <your_UserId>.geo for the post geolocation data
            -   <your_UserId>.user for the post user data
            command as below:
            **./kafka-topics.sh --bootstrap-server BootstrapServerString --command-config client.properties --create --topic <topic_name>**
            e.g.:
            **./kafka-topics.sh --bootstrap-server b-1.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-3.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098,b-2.pinterestmskcluster.w8g8jt.c12.kafka.us-east-1.amazonaws.com:9098 --command-config client.properties --create --topic 0ac1babf620d.user**
            note: Above commands will work, if CLASSPATH variable is set
            To set up the CLASSPATH environment variable, you can use the following command in .bashrc file using nano ~/.bashrc and then source ~/.bashrc:
            **export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/libs/aws-msk-iam-auth-1.1.5-all.jar**

