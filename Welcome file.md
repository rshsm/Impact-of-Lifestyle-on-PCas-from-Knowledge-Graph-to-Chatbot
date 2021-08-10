# Impact-of-Lifestyle-on-PCas-from-Knowledge-Graph-to-Chatbot-

This repository is about the paper Modeling the Impact of Lifestyle on PCas: from Knowledge Graph to Chatbot by Fei Ye <sup>1*</sup>, ; Baivab Sinha<sup>1*</sup>; Yalan Chen<sup>2*</sup>;Tong Tang<sup>1</sup>; Rongrong Wu<sup>1</sup>; Mengqiao He<sup>1</sup>,Xiaonan Zheng<sup>3</sup>; Qiang Wei<sup>3</sup>, Bairong Shen<sup>1</sup>

><sup>1</sup>Institutes for Systems Genetics, Frontiers Science Center for Disease-related Molecular Network, West China Hospital, Sichuan University, Chengdu, 610041, China.
><sup>2</sup>Department of Medical Informatics, School of Medicine, Nantong University, Nantong, China.
><sup>3</sup>Department of Urology, West China Hospital, Sichuan University, Chengdu, China.


**Background:** Personal lifestyle is an important cause of prostate cancer (PCa), hence establishing a corresponding knowledge graph (KG) is a convenient way for preventing and assessing risks. However, currently, there exists no work on the construction and application of this kind of KG.

**Objective:** In this paper, we established a KG based on PCa-associated lifestyles, called PCalfst_KG, which extracts knowledge from the existing Knowledge Base (KB). Then we visualized it and designed a chatbot based on a dialogue system whose responses come from PCalfst_KG.

**Methods:** From the existing KB, we define entities based on the items and corresponding relationships based on the primary key and foreign key. We establish the PCalfst_KG by importing the triples into the Neo4j server. The visualization is based on node.js and d3.js technology. The dialogue system uses the Flask framework to determine the classification of questions through entity recognition and relationship extraction and later uses the query template to search the answers from the PCalfst_KG.

**Results:** The PCalfst_KG contains 11 types of entities and 14 types of relationships, the total number of nodes and links is 21546 and 66493, respectively. Also, the entity “Lifestyle”, “Paper”, “Baseline” and “Outcome” contain multiple attributes. The established chatbot can answer 12 basic questions and predict the probability of a certain lifestyle resulting in a certain PCa.

**Conclusions:** The lifestyle-associated KB is transformed into a professional KG and conveniently visualized. We have initially constructed a chatbot based on PCalfst_KG to help researchers or physicians learn more about PCa interactively.

# Gallery

For more examples, visit our  [project page](http://rpg.ifi.uzh.ch/timelens).

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





		
Lifestyle	factor_type; fenlei; index_name; inv_papers; level_class; name; paper_count; pca_type; unit.	2290
Paper	area; author; duration; gene; name; sample_size; study_type; title; year.	300
Baseline	group_number; index_name; name; notes; pmid; stratification; value.	2570
Outcome	aj_value; eaj; eunaj; index_name; name; notes; pcatype; pmid; stratification; unaj_value; unit.	15586
PCa	-	79
Nation	-	31
Unit	-	125
Gene	-	38
FirClass	-	11
SecClass	-	294
ThrClass	-	222




## Install nodejs
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
## Flask
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
## Neo4j
Neo4j is available both as a standalone server, or an embeddable component. You can [download](https://neo4j.com/download/) from here .


Step 1 Clone [this](https://github.com/neo4j/neo4j-browser) repo

Step 2 Install yarn globally (not required but recommended): npm install -g yarn

Step 3 Install project dependencies: yarn


yarn start and point your web browser to http://localhost:8080.

## Project Set Up

Knowledge Graph

## Architecture

### Knowledge Graph

Flow chart for establishing the PCalfst_KG
<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/128831502-adc810c0-980f-44ff-9e32-8893a3be5b4e.png" />
</p>
	


The principle of visualizing the core knowledge graph for the inquired lifestyles
	<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/128831706-8c9e7d19-3034-405c-98d6-49c9d793351f.png" />
</p>
	


### Chat Bot

The realization principle of the dialogue system based on Pcalfst_KG
		<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/128831785-b15faee7-c309-43dd-a6ef-bc00c714a794.png" />
</p>

## Result

### Knowledge Graph

Figure. 2(a) KG of “genistein”; (b)&(c) outcomes of  PCa caused by “genistein” and “milk” 
		<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/128837731-5b6a31ce-c88d-41ac-8cfd-89052b2a4b1f.png" />
</p>
		<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/128837758-8069726f-813d-40dc-a3ff-e527d93126ac.png" />
</p>
		<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/128837787-b35589b4-65d2-4972-bf6a-479d532daa03.png" />
</p>


Display of the core knowledge graph of four examples visualized by d3
		<p align="center">
  <img src="https://user-images.githubusercontent.com/10841083/128837911-ba9dd54a-cb05-4d02-a571-328136e856bc.png" />
</p>


(a) “genistein”



<p align = "center">
  <img src="https://user-images.githubusercontent.com/10841083/128837944-817f2800-11f7-4874-87c9-5ea54a5d4bf6.png" />
</p>

(b) “green tea”

<p align = "center">
  <img src="https://user-images.githubusercontent.com/10841083/128837980-d75ad465-1e51-409b-b29f-31a89b17eb3b.png" />
</p>


(c) “bacon”
<p align = "center">
  <img src="https://user-images.githubusercontent.com/10841083/128838016-97cbd004-aac0-4202-947a-942ef75a7cec.png" />
</p>

(d) “miso soup”

<p align = "center">
  <img src="https://user-images.githubusercontent.com/10841083/128838086-273ac1d5-d4b4-4260-88ee-6dd119c2e073.png" />
</p>


Display of properties and values of associated nodes of “genistein”



### Chat Bot

<p align = "center">
  <img src="https://user-images.githubusercontent.com/10841083/128838217-141ec9ce-bee9-4751-a85e-b341a17a40fe.png" />
	</br>
	<b>The realization principle of the chatbot based on Pcalfst_KG</b>
</p>


