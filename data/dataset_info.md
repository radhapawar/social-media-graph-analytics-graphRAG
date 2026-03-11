# Dataset Information

This project uses a large-scale social media tagging dataset to study **user behavior, similarity, homophily, and influence** in tagging networks.

Due to the large size of the raw dataset, the data files are **not included in this repository**.

Instead, we provide:

- The original dataset source
- Instructions to reproduce the processed datasets used in the project

---

# Original Dataset

Dataset Source:

https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

The dataset contains information about **user interactions with tags over time**.

Each interaction represents a **user adopting a tag at a specific time**.

---

# Raw Dataset Structure

Each record contains:
userId | tag | timestamp


Where:

| Field | Description |
|------|-------------|
| userId | Unique identifier for a user |
| tag | Tag or keyword used by the user |
| timestamp | Time when the tag was adopted |

---

# Dataset Statistics

| Metric | Value |
|------|------|
| Total interactions | ~284 million |
| Unique users | 138,287 |
| Unique tags | 34,175 |

---

# Processed Datasets Used in This Project

The notebook generates the following intermediate datasets used in the analysis.

### 1. User Tag Adoption Data
user_tag_adoption_FINAL.csv


Contains the cleaned dataset of user-tag adoption events.

Columns:
userId | tag | timestamp


---

### 2. User Similarity Graph
user_similarity_topk_strict.csv


Represents similarity edges between users.

Columns:
u1 | u2 | jaccard | shared_tags



Where:

| Column | Description |
|------|-------------|
| u1 | User 1 |
| u2 | User 2 |
| jaccard | Jaccard similarity between users |
| shared_tags | Number of tags shared by both users |

---

# How to Reproduce the Dataset

Run the notebook:
notebooks/Social_Media_Final.ipynb


The notebook performs the following steps:

1. Data loading
2. Data cleaning and preprocessing
3. Construction of user-tag adoption dataset
4. Similarity computation between users
5. Graph filtering
6. Homophily and influence analysis
7. Export of similarity graph

---

# Important Note

The raw dataset is very large (~284M interactions), so it is not stored in the repository.

The provided notebook fully reproduces the **data preprocessing and graph construction pipeline**.