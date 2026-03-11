// --------------------------------------------------
// Neo4j Queries for Social Media Graph Analysis
// --------------------------------------------------


// Count total users
MATCH (u:User)
RETURN count(u) AS total_users;


// Count similarity edges
MATCH ()-[r:SIMILAR_TO]-()
RETURN count(r) AS similarity_edges;


// Count tag adoption relationships
MATCH (:User)-[r:ADOPTED]->(:Tag)
RETURN count(r) AS adoption_edges;


// --------------------------------------------------
// Top Connected Users
// --------------------------------------------------

MATCH (u:User)-[r:SIMILAR_TO]-()
RETURN u.userId AS user, count(r) AS degree
ORDER BY degree DESC
LIMIT 10;


// --------------------------------------------------
// Strongest Similarity Relationships
// --------------------------------------------------

MATCH (u1:User)-[r:SIMILAR_TO]-(u2:User)
RETURN u1.userId AS user1,
       u2.userId AS user2,
       r.jaccard AS similarity
ORDER BY similarity DESC
LIMIT 10;


// --------------------------------------------------
// Tags With Most Adopters
// --------------------------------------------------

MATCH (:User)-[:ADOPTED]->(t:Tag)
RETURN t.name AS tag,
       count(*) AS adopters
ORDER BY adopters DESC
LIMIT 10;


// --------------------------------------------------
// Neighbors of a Specific User
// --------------------------------------------------

MATCH (u:User {userId:132119})-[r:SIMILAR_TO]-(v:User)
RETURN v.userId AS neighbor,
       r.jaccard AS similarity
ORDER BY similarity DESC
LIMIT 10;