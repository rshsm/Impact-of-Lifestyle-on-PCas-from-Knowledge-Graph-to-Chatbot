### 一.Set up Knowledge Graph

##### 1. Install Java  
- [Download Java version:1.8](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html)  
- Configure environment variables  

- Verify installation of Java,Open a command prompt,and enter the following:
    ```
    java -version
    ```

##### 2. Install Node.js
 - [Download Node.js](https://nodejs.org/en/download/)

 - Verify installation of Node,Open a command prompt,and enter the following:
    ```
    node -v
    npm -v
    ```
##### 3. Install Neo4j
- [Download Neo4j  version:3.5](https://neo4j.com/download-center/#enterprise)

- Configure environment variables
- Verify installation of Neo4j,Open a command prompt,and enter the following:
    ```
    neo4j.bat console
    ```
##### 4. Run Knowledge Graph
- Open a command prompt
- Enter the bin directory under the neo4j folder,and enter the following:

    ```
    neo4j.bat console
    ```
- Open another command prompt, enther "mypro" project,and enter the following:
    
    ```
    npm run dev
    ```
#### [Link to Knowledge Graph](http://sysbio.org.cn:3000/)



### 二.Set up Chatbot

##### 1.Install Anaconda——[Download Link](https://www.anaconda.com/products/individual)

##### 2.Import environment
- Download "environment.yaml" and  "requirements.txt"
- Open a command prompt,and enter the following:

    ```
    conda env create -f environment.yaml
    
    pip install -r requirements.txt
    ```


##### 3.Run Chatbot
- Open a command prompt,and enter the following:
    ```
    conda activate dev
    ```
- Enter "pchatbot" project,and enter the following:

    ```
    python app.py
    ```
#### [Link to Chatbot](http://sysbio.org.cn:5000/Pca/chatbot)


    