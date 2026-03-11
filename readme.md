# Social Media Graph Analytics with GraphRAG

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Neo4j](https://img.shields.io/badge/GraphDB-Neo4j-green)
![OpenAI](https://img.shields.io/badge/AI-GPT-orange)
![Graph Analytics](https://img.shields.io/badge/Analytics-Network%20Science-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)




This project analyzes user behavior in a social media tagging system using **graph analytics and GraphRAG**.

The system builds a **user similarity network** based on shared tag adoption and studies **homophily and influence patterns** in the network.

The project integrates:

- Python data processing
- Neo4j graph database
- Graph similarity modeling
- GPT-powered GraphRAG querying

The final system allows users to **ask natural language questions about the graph and retrieve insights interactively**.

---

# Dataset

This project uses a **social media tagging dataset**.

Dataset Source:  
[Kaggle Dataset Link]

The dataset contains user interactions with tags over time.

### Dataset Statistics

| Metric | Value |
|------|------|
| Total interactions | ~284 million |
| Unique users | 138,287 |
| Unique tags | 34,175 |

Each record contains:
User ID | Tag | Timestamp



The raw dataset is **not included in this repository** due to its large size.

The notebook in `notebooks/` reproduces the full **data preprocessing and graph construction pipeline**.

---

# Project Workflow

The project follows this pipeline:

1. Data preprocessing in Python (Google Colab)
2. Construction of user similarity graph using Jaccard similarity
3. Graph filtering to retain strong similarity relationships
4. Homophily and influence analysis
5. Graph storage in Neo4j
6. Python integration with Neo4j
7. GraphRAG system using GPT API for natural language querying

---

# Project Architecture

The system combines **large-scale data processing, graph analytics, and AI-powered graph querying**.

![Project Architecture](diagrams/architecture.png)

### Architecture Components

1. **Data Processing (Python / Colab)**  
   Large-scale preprocessing and similarity computation.

2. **Graph Construction**  
   Build user similarity network based on tag overlap.

3. **Neo4j Graph Database**  
   Store and query the social network.

4. **Python Graph Query Layer**  
   Connects Neo4j with the GraphRAG interface.

5. **GPT API Integration**  
   Converts natural language questions into graph queries.


## End-to-End Pipeline

The project follows a complete data-to-AI pipeline combining large-scale data processing, graph analytics, and AI-powered querying.

![End-to-End Pipeline](diagrams/pipeline.png)

### Pipeline Steps

1. **Data Collection**
   - Social media tagging dataset collected from Kaggle
   - Contains user interactions with tags over time

2. **Data Preprocessing (Python / Colab)**
   - Cleaned and filtered large-scale user-tag interactions
   - Created user-tag adoption matrix
   - Reduced dataset size to manageable graph scale

3. **User Similarity Computation**
   - Computed **Jaccard similarity** between users based on shared tags
   - Applied strict filtering to retain meaningful relationships
   - Generated similarity edge dataset

4. **Graph Construction**
   - Nodes created for **Users** and **Tags**
   - Relationships created for:
     - `ADOPTED`
     - `SIMILAR_TO`

5. **Graph Storage in Neo4j**
   - Graph data imported into Neo4j
   - Cypher queries used for graph analysis

6. **Graph Analytics**
   - Network connectivity analysis
   - Homophily detection
   - Influence analysis

7. **GraphRAG System**
   - GPT interprets user questions
   - Generates Cypher queries
   - Queries Neo4j graph
   - Returns interpreted insights

---

# Graph Model

The system models the social network using **two node types and two relationships**.

## Nodes

### User

Represents a social media user.
User {
userId
}


### Tag

Represents a hashtag or topic adopted by users.
Tag {
name
}



---

## Relationships

### ADOPTED

Represents when a user adopted a tag.
(User)-[:ADOPTED {timestamp}]->(Tag)


---

### SIMILAR_TO

Represents similarity between users based on shared tag usage.
(User)-[:SIMILAR_TO {jaccard, shared_tags}]->(User)



Edge properties:

| Property | Description |
|------|------|
| jaccard | similarity score between users |
| shared_tags | number of tags used by both users |

---

# Graph Schema

The Neo4j graph schema representing users, tags, and similarity relationships.

![Graph Schema](diagrams/graph_schema.png)

---

# User Similarity Network

The similarity graph reveals clusters of users connected by shared tag adoption behavior.

Nodes represent users and edges represent `SIMILAR_TO` relationships based on Jaccard similarity.

Clusters indicate groups of users with **similar interests**, while highly connected nodes represent **hub users** in the network.

![User Similarity Network](diagrams/network_visualization.png)

---

# GraphRAG System

The system integrates **GPT with Neo4j** to allow natural language queries over the graph.

Users can ask questions such as:

- Who are the most connected users?
- Which users share the strongest similarity?
- Tell me about user 132119

### GraphRAG Pipeline

User Question
↓
GPT interprets question
↓
Graph tool selected
↓
Cypher query executed in Neo4j
↓
Results returned
↓
GPT generates explanation



Example interaction:

![GraphRAG Demo](diagrams/graphrag_demo.png)

---

# Key Results

### Homophily Analysis

Homophily Lift ≈ **1.04**

This indicates that users connected in the similarity graph share **slightly more behavioral similarity than random user pairs**.

### Influence Analysis

Influence Lift ≈ **5.42**

This indicates **strong evidence that users influence each other's tag adoption behavior**.

Users are significantly more likely to adopt tags previously used by their neighbors.

---

# Repository Structure

The project repository is organized as follows:

![Repository Structure](diagrams/repo_structure.png)


---

# Technologies Used

- Python
- Pandas
- NumPy
- Neo4j
- Cypher Query Language
- OpenAI GPT API
- GraphRAG Architecture

---

# Author

**Rohan Chimne**  
MS Business Analytics  
McCombs School of Business  
University of Texas at Austin

---

# Demo

Example interaction with the GraphRAG system:

User: Who are the most connected users?

GraphRAG:
User 132119 – 30 connections
User 103945 – 28 connections
User 127339 – 28 connections



### GraphRAG Interactive Demo

Below is an example interaction with the GraphRAG system.

![GraphRAG Demo](diagrams/graphrag_demo.png)

The system converts natural language questions into **Cypher queries executed on the Neo4j graph database**.


## Key Contribution;:


• Construction of a **user similarity network** from large social media interaction data  
• Graph modeling of **user-tag relationships** and behavioral similarity  
• Analysis of **homophily and influence patterns** in the network  
• Integration of **Neo4j graph database with GPT-powered GraphRAG querying**  
• Development of an **interactive natural language interface for graph exploration**


This project demonstrates how **graph analytics and large language models can be combined** to analyze large-scale social networks.


## Future Improvements

Potential extensions of this work include:

• Implementing **Graph Neural Networks (GNNs)** for link prediction  
• Adding **community detection algorithms** for deeper network insights  
• Deploying the system as an **interactive web application**  
• Scaling the pipeline using **distributed graph processing frameworks**