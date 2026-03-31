# Social Media Graph Analytics with GraphRAG

**Team:** Radha Pawar, Rohan Chimne, Simoni Dalal, Shivangi Gupta, Alisha Surabhi, Justin Yang
**Stack:** Python · Neo4j · GPT API · GraphRAG

---

The dataset for this project is a social media tagging system: 284 million interactions, 138,287 users, 34,175 unique tags. Each record is a user, a tag they adopted, and a timestamp.

The goal wasn't just to analyze that dataset. It was to build something you could actually *talk to* — where instead of writing a Cypher query or running a pandas groupby, you could ask "which users influenced user 132119's tag adoption?" and get a real, interpreted answer.

That's the GraphRAG idea: combine a graph database (Neo4j) with an LLM (GPT) so the LLM can translate natural language into graph queries, execute them, and explain the results in plain English. It's a pattern that's increasingly used in enterprise analytics tooling and I wanted to build it from scratch to understand how it actually works.

## Building the similarity network

284 million records is too large to work with directly. We built a user-tag adoption matrix and computed **Jaccard similarity** between every pair of users based on shared tag adoptions:

```
Jaccard(A, B) = |tags adopted by both| / |tags adopted by either|
```

Then applied a threshold to filter out weak relationships — keeping only edges that represent a real behavioral connection. The resulting graph went into Neo4j with two node types (`User`, `Tag`) and two relationship types (`ADOPTED` with a timestamp, `SIMILAR_TO` with Jaccard score and shared tag count as properties).

Storing in a graph database matters because multi-hop traversals and neighbor aggregations are O(log n) in Neo4j and O(n²) in a flat structure.

## What the analysis found

**Homophily lift: 1.04.** Users connected in the similarity network share slightly more behavioral overlap than random pairs — the network has real structure, not just noise.

**Influence lift: 5.42.** Users are 5.4x more likely to adopt a tag if their network neighbors have already adopted it. That's not a trivial number. It means the network isn't just capturing who's similar — it's capturing actual influence pathways. For content seeding or viral marketing strategy, knowing which nodes to activate first matters enormously.

## The GraphRAG interface

This was the most experimental part. The system works like this:

1. User asks a question in natural language
2. GPT interprets the question and decides which graph operation to run
3. GPT generates a Cypher query and passes it to Neo4j
4. Neo4j executes and returns results
5. GPT takes the raw results and generates an explanation in plain English

Example interaction:

```
User: Who are the most connected users?

System: Based on degree centrality in the similarity network:
  User 132119 — 30 connections (strongest hub in the network)
  User 103945 — 28 connections
  User 127339 — 28 connections

These users adopted tags across a wide range of topic categories,
making them hubs that connect otherwise-separate communities.

User: Tell me about user 132119

System: User 132119 is the most connected node in the similarity
network, with 30 direct SIMILAR_TO relationships. They share the
most tags with users 103945 (47 shared tags, Jaccard 0.34) and
127339 (43 shared tags, Jaccard 0.31). Their tag adoption pattern
spans multiple topic domains — likely why they're a central hub.
```

## Running it

You'll need Neo4j (Desktop or AuraDB free tier) and an OpenAI API key.

```bash
git clone https://github.com/radhapawar/social-media-graph-analytics-graphRAG.git
cd social-media-graph-analytics-graphRAG
pip install pandas numpy neo4j openai matplotlib
```

Update the config at the top of the main notebook with your Neo4j credentials and OpenAI API key, then run notebooks in order: preprocessing → graph construction → analytics → GraphRAG interface.

The raw dataset (~284M records) isn't in the repo for size reasons. The preprocessing notebook explains how to load it from the original source and build the similarity graph from scratch.

## What I'd build next

**Temporal analysis** — the influence lift of 5.42x is a static snapshot, but the interesting question is *when* influence happens. Is adoption most likely in the 24 hours after a neighbor adopts a tag, or a week later? Understanding the time window would make the influence model much more actionable.

**Community detection** — Louvain or Label Propagation to automatically identify topic clusters. Right now you can query for individual users but you can't easily get "show me all users in the fitness community."

**Streamlit deployment** — wrapping the GraphRAG interface in a web app so it's usable without opening a Jupyter notebook.
