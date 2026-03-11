# Neo4j Graph Schema

This project models a social media tagging network using a graph database.

The graph captures relationships between **users and tags** and measures similarity between users.

---

# Node Types

## User

Represents a social media user.

Properties:

| Property | Description |
|--------|-------------|
| userId | Unique identifier for a user |

Example:
(User {userId:132119})



---

## Tag

Represents a hashtag or topic adopted by users.

Properties:

| Property | Description |
|--------|-------------|
| name | Tag name |

Example:
(Tag {name:"machinelearning"})



---

# Relationship Types

## ADOPTED

Represents when a user adopted a tag.

Pattern:
(User)-[:ADOPTED {timestamp}]->(Tag)



Properties:

| Property | Description |
|--------|-------------|
| timestamp | Time when the tag was adopted |

---

## SIMILAR_TO

Represents similarity between two users based on shared tag usage.

Pattern:
(User)-[:SIMILAR_TO {jaccard, shared_tags}]->(User)



Properties:

| Property | Description |
|--------|-------------|
| jaccard | Jaccard similarity score |
| shared_tags | Number of tags shared by both users |