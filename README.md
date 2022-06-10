Data-pipeline-using-python-kafka-and-mongodb-quickstart
This project contains 2 files (before the README.md).

SourceCode.py is a combination of both scraping data code and Kafka procedure code to stream data to Mongodb (data lake).

real_estate_chotot.json: The data file was downloaded from elasticsearch(data lake).

Scrapping data on Jupyter Notebook by python with selenium libs

Real estate properties data is pulled from chotot.vn using python.


My system os ubuntu server 18.04 LST run in virtual machine

Kafka

See web site for details on the project.

You need to have Java installed.

My project use java 8
to install java : 
sudo apt install java-8-jre-headless

Install Kafka:
single kafka:
download Kafka from offcial webside :https://kafka.apache.org/
recommend download kafka with scala 
My project use kafka_2.13-3.2.0

wget https://dlcdn.apache.org/kafka/3.2.0/kafka_2.13-3.2.0.tgz

See more in https://kafka.apache.org/quickstart

Install Mongodb(two option):
    1.  Use quick guide in offical webside:  https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
    version mongodb of my project: MongoDB 4.4 Community Edition
    2.  Use docker:
    docker pull mongo
    docker run -p 27017:27107 -name name_mongodb mongodb

Connect Kafka to Mongodb:
    You can choose many option to connect as confuluen or debezium (read more in offical )
    My project use jar file mongo-connect-kafka to config sink source . Data from crawl streamming to kafka then from kafka to databases;
    Download jar file in git or website of Maven (https://search.maven.org/artifact/org.mongodb.kafka/mongo-kafka-connect)
    Copy the JAR and any dependencies into the Kafka plugins directory which you can specify in your plugin.path
    Create file MongoSinkConnector.properties in config of kafka. Exemple:
        name=mongo-sink
        topics=test
        connector.class=com.mongodb.kafka.connect.MongoSinkConnector
        tasks.max=1
        key.ignore=true
        connection.uri=mongodb://localhost:27017
        database=test_connect
        collection=transaction
        max.num.retries=3
        retries.defer.timeout=5000
        type.name=kafka-connect
        schemas.enable=false
Start kafka: (Open three terminal)
    1. start zookeeper server
    bin/zookeeper-server-start.sh config/zookeeper-server.properties
    2. start kafka server
    bin/kafka-server-start.sh config/server.properties
    3. start connection
    bin/connect-standalone.sh config/connect-standalone.properties config/MongoSinkConnector.properties


Test 
    1.Open terminal
    2.Create topic test:
    bin/kafka-topic.sh --topic test --bootstrap-server localhost:9092
    3.Start kafka producer:
    bin/kafka-producer.sh --topic test --bootstrap-server localhost:9092
    Send message
    {"hello":"world"}

    4. Check in database(Mongo)
    in orther terminal and run
        mongosh # start mongoshell
        show databases #show all database
        use test #change to database test
        show collections #show all collections in database
        db.transaction.find() #show all record in collections
        if dislay the message , the connect is success 
    
Crawl data and stream kafka to mongodb

run file crawl.py on window with cmd 
REQUIRED install python and some lib (kafka-python,beautifulsoup4,selenium)
         download chromedrive (chekversion)
file crawl.py get data in http://chotot.com


















