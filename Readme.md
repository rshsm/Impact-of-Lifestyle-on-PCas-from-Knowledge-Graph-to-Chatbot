# Impact-of-Lifestyle-on-PCas-from-Knowledge-Graph-to-Chatbot-

This repository is about the paper Modeling the Impact of Lifestyle on PCas: from Knowledge Graph to Chatbot by Fei Ye <sup>1*</sup>, ; Baivab Sinha<sup>1*</sup>; Yalan Chen<sup>2*</sup>;Tong Tang<sup>1</sup>; Rongrong Wu<sup>1</sup>; Mengqiao He<sup>1</sup>,Xiaonan Zheng<sup>3</sup>; Qiang Wei<sup>3</sup>, Bairong Shen<sup>1</sup>

><sup>1</sup>Institutes for Systems Genetics, Frontiers Science Center for Disease-related Molecular Network, West China Hospital, Sichuan University, Chengdu, 610041, China.
><sup>2</sup>Department of Medical Informatics, School of Medicine, Nantong University, Nantong, China.
><sup>3</sup>Department of Urology, West China Hospital, Sichuan University, Chengdu, China.

### Live version of Chatbot

[Link to Knowledge Graph](http://sysbio.org.cn:3000/)

### Live Version of Knowledge Graph

[Link to Chatbot](http://sysbio.org.cn:5000/Pca/chatbot)

**Background:** Personal lifestyle is an important cause of prostate cancer (PCa), hence establishing a corresponding knowledge graph (KG) is a convenient way for preventing and assessing risks. However, currently, there exists no work on the construction and application of this kind of KG.

**Objective:** In this paper, we established a KG based on PCa-associated lifestyles, called PCalfst_KG, which extracts knowledge from the existing Knowledge Base (KB). Then we visualized it and designed a chatbot based on a dialogue system whose responses come from PCalfst_KG.

**Methods:** From the existing KB, we define entities based on the items and corresponding relationships based on the primary key and foreign key. We establish the PCalfst_KG by importing the triples into the Neo4j server. The visualization is based on node.js and d3.js technology. The dialogue system uses the Flask framework to determine the classification of questions through entity recognition and relationship extraction and later uses the query template to search the answers from the PCalfst_KG.

**Results:** The PCalfst_KG contains 11 types of entities and 14 types of relationships, the total number of nodes and links is 21546 and 66493, respectively. Also, the entity “Lifestyle”, “Paper”, “Baseline” and “Outcome” contain multiple attributes. The established chatbot can answer 12 basic questions and predict the probability of a certain lifestyle resulting in a certain PCa.

**Conclusions:** The lifestyle-associated KB is transformed into a professional KG and conveniently visualized. We have initially constructed a chatbot based on PCalfst_KG to help researchers or physicians learn more about PCa interactively.



# Set-up

## Data Acquisition

The PCaLiStDB which is standardized for PCa_LWAS is publicly available [here](http://www.sysbio.org.cn/pcalistdb/). In the PCaListDB database, there exists a total of 3024 lifestyles items comprising 394 protective items, 556 risk items, 45 uninfluential items, 52 ambivalent items, and 1977 items that lack adequate literature support. These items are summarized and classified into three SQL tables.


The types of entity and corresponding count in PCalfst_KG

|       Entity   |Properties                     |Count                        |
|----------------|-------------------------------|-----------------------------|
|       Lifestyle   |factor_type; fenlei; index_name; inv_papers; level_class; name; paper_count; pca_type; unit.                     |2290                        |
|       Paper   |area; author; duration; gene; name; sample_size; study_type; title; year.                     |300                        |
|       Baseline   |group_number; index_name; name; notes; pmid; stratification; value.                     |2570                        |
|       Outcome   |aj_value; eaj; eunaj; index_name; name; notes; pcatype; pmid; stratification; unaj_value; unit.                     |15586                        |
|       PCa   |Properties                     |79                        |
|       Nation   |Properties                     |31                        |
|       Unit   |Properties                     |125                        |
|       Gene   |Properties                     |38                        |
|       FirClass   |Properties                     |11                        |
|       SecClass   |Properties                     |294                        |
|       ThrClass   |Properties                     |22                        |

## Set up Knowledge Graph

### 1. Install Java  
- [Download Java version:1.8](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html)  
- Configure environment variables  

- Verify installation of Java,Open a command prompt,and enter the following:
    ```
    java -version
    ```

### 2. Install nodejs
Node.js is a run-time environment which includes everything you need to execute a program written in JavaScript. It’s used for running scripts on the server to render content before it is delivered to a web browser.

NPM stands for Node Package Manager, which is an application and repository for developing and sharing JavaScript code.

Step 1: Download Node.js Installer
In a web browser, navigate to [nodejs website](https://nodejs.org/en/download/). Click the Platform Installer button to download the latest default version

Step 3: Verify Installation
Open a command prompt (or PowerShell), and enter the following:
```
node -v
```
The system should display the Node.js version installed on your system. You can do the same for NPM:
```
npm -v
```
### 3. Flask
Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. 

Installing
Install and update using pip:
```python
$ pip install -U Flask
```
A Simple Example
```python
# save this as app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
```
```python
$ flask run
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
### 4. Neo4j
Neo4j is available both as a standalone server, or an embeddable component. You can [download](https://neo4j.com/download/) from here .


Step 1 Clone [this](https://github.com/neo4j/neo4j-browser) repo

Step 2 Install yarn globally (not required but recommended): npm install -g yarn

Step 3 Install project dependencies: yarn

Step 4 yarn start and point your web browser to http://localhost:8080.
Step 5 Configure environment variables
- Verify installation of Neo4j,Open a command prompt,and enter the following:
    ```
    neo4j.bat console
    ```

###  5. Run Knowledge Graph
- Open a command prompt
- Enter the bin directory under the neo4j folder,and enter the following:

    ```
    neo4j.bat console
    ```
- Open another command prompt, enther "mypro" project,and enter the following:
    
    ```
    npm run dev
    ```

## Set up Chatbot



### 1.Install Anaconda——[Download Link](https://www.anaconda.com/products/individual)

### 2.Import environment
- Download "environment.yaml" and  "requirements.txt"
- Open a command prompt,and enter the following:

    ```python
    conda env create -f environment.yaml
    
    pip install -r requirements.txt
    ```


### 3.Run Chatbot
- Open a command prompt,and enter the following:
    ```python
    conda activate dev
    ```
- Enter "pchatbot" project,and enter the following:

    ```python
    python app.py
    ```


# Architecture


<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/128831502-adc810c0-980f-44ff-9e32-8893a3be5b4e.png" />
	</br>
  <b>Flow chart for establishing the PCalfst_KG </b>
</p>
	


<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/129159640-b3755360-722d-4309-826f-b8e2dd8589e1.png" />
	</br>
  <b>The principle of visualizing the core knowledge graph for the inquired lifestyles</b>
</p>


### Chat Bot


<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/128831785-b15faee7-c309-43dd-a6ef-bc00c714a794.png" />
	</br>
  <b>The realization principle of the dialogue system based on Pcalfst_KG</b>
</p>

# Results 

### Knowledge Graph

<p align="center">
<img src="https://user-images.githubusercontent.com/10841083/128841351-411cc5ab-649d-4d38-b700-8e9075af76b0.png" />
  </br>
  <b>KG of “genistein”; (b)&(c) outcomes of  PCa caused by “genistein” and “milk” </b>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/128841106-b61e7aae-46a5-4a11-a85d-e0548e31f357.png" />
  </br>
  <b>Display of the core knowledge graph of four examples visualized by d3</b>
</p>
<p align = "center">
  <img src="https://user-images.githubusercontent.com/10841083/128838086-273ac1d5-d4b4-4260-88ee-6dd119c2e073.png" />
	</br>
	<b>Display of properties and values of associated nodes of “genistein”</b>
</p>

### Chat Bot

#### Sample Questions:

> green tea

> What is the unit of green tea?

> Can you give me some surveys about green tea?

> What kind of PCa may green tealeads?
 
> Which gene may total pca connected with?

> When green tea leads to the pca,please give me the possible outcomes?

> Which factor is green tea belongsto?


<p align = "center">
  <img src="https://user-images.githubusercontent.com/10841083/129159716-864fd937-8495-4445-964c-8d23f373fa2d.png" />
	</br>
	<b>The realization principle of the chatbot based on Pcalfst_KG</b>
</p>






