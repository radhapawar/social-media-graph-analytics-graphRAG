import json
from typing import Any

from neo4j import GraphDatabase
from openai import OpenAI

# =========================
# Config
# =========================
OPENAI_API_KEY = "gpt_api_key"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password"

MODEL_NAME = "gpt-4.1-mini"

# =========================
# Clients
# =========================
client = OpenAI(api_key=OPENAI_API_KEY)

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD),
)

# =========================
# Neo4j helper
# =========================
def run_query(query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    with driver.session() as session:
        result = session.run(query, params or {})
        return [dict(record) for record in result]

# =========================
# Graph tools
# =========================
def get_top_connected_users(limit: int = 10) -> list[dict[str, Any]]:
    query = """
    MATCH (u:User)-[r:SIMILAR_TO]-()
    RETURN u.userId AS user, count(r) AS degree
    ORDER BY degree DESC
    LIMIT $limit
    """
    return run_query(query, {"limit": int(limit)})

def get_strongest_similarity_pairs(limit: int = 10) -> list[dict[str, Any]]:
    query = """
    MATCH (u1:User)-[r:SIMILAR_TO]-(u2:User)
    RETURN u1.userId AS user1, u2.userId AS user2, r.jaccard AS similarity
    ORDER BY similarity DESC
    LIMIT $limit
    """
    return run_query(query, {"limit": int(limit)})

def get_top_tags(limit: int = 10) -> list[dict[str, Any]]:
    query = """
    MATCH (:User)-[:ADOPTED]->(t:Tag)
    RETURN t.name AS tag, count(*) AS adopters
    ORDER BY adopters DESC
    LIMIT $limit
    """
    return run_query(query, {"limit": int(limit)})

def get_user_neighbors(user_id: int, limit: int = 10) -> list[dict[str, Any]]:
    query = """
    MATCH (u:User {userId: $user_id})-[r:SIMILAR_TO]-(v:User)
    RETURN v.userId AS neighbor, r.jaccard AS similarity
    ORDER BY similarity DESC
    LIMIT $limit
    """
    return run_query(query, {"user_id": int(user_id), "limit": int(limit)})

def get_user_summary(user_id: int) -> dict[str, Any]:
    degree_query = """
    MATCH (u:User {userId: $user_id})-[r:SIMILAR_TO]-()
    RETURN count(r) AS degree
    """
    neighbors_query = """
    MATCH (u:User {userId: $user_id})-[r:SIMILAR_TO]-(v:User)
    RETURN v.userId AS neighbor, r.jaccard AS similarity
    ORDER BY similarity DESC
    LIMIT 5
    """
    tags_query = """
    MATCH (u:User {userId: $user_id})-[:ADOPTED]->(t:Tag)
    RETURN t.name AS tag
    LIMIT 10
    """

    degree_rows = run_query(degree_query, {"user_id": int(user_id)})
    neighbors_rows = run_query(neighbors_query, {"user_id": int(user_id)})
    tags_rows = run_query(tags_query, {"user_id": int(user_id)})

    degree = degree_rows[0]["degree"] if degree_rows else 0
    tags = [row["tag"] for row in tags_rows]

    return {
        "user_id": int(user_id),
        "degree": degree,
        "top_neighbors": neighbors_rows,
        "sample_tags": tags,
    }

def get_shared_tags_for_user(user_id: int, limit: int = 10) -> list[dict[str, Any]]:
    query = """
    MATCH (u:User {userId: $user_id})-[:SIMILAR_TO]-(v:User)
    MATCH (u)-[:ADOPTED]->(t:Tag)<-[:ADOPTED]-(v)
    RETURN t.name AS tag, count(*) AS shared_count
    ORDER BY shared_count DESC
    LIMIT $limit
    """
    return run_query(query, {"user_id": int(user_id), "limit": int(limit)})

def get_graph_summary() -> dict[str, Any]:
    users_query = """
    MATCH (u:User)
    RETURN count(u) AS users
    """
    edges_query = """
    MATCH ()-[r:SIMILAR_TO]-()
    RETURN count(r) AS edges
    """
    top_degree_query = """
    MATCH (u:User)-[r:SIMILAR_TO]-()
    RETURN u.userId AS user, count(r) AS degree
    ORDER BY degree DESC
    LIMIT 5
    """
    top_tags_query = """
    MATCH (:User)-[:ADOPTED]->(t:Tag)
    RETURN t.name AS tag, count(*) AS adopters
    ORDER BY adopters DESC
    LIMIT 5
    """

    users = run_query(users_query)[0]["users"]
    edges = run_query(edges_query)[0]["edges"]
    top_degree_users = run_query(top_degree_query)
    top_tags = run_query(top_tags_query)

    return {
        "total_users": users,
        "total_edges": edges,
        "top_degree_users": top_degree_users,
        "top_tags": top_tags,
    }

# =========================
# Tool definitions for GPT
# =========================
TOOLS = [
    {
        "type": "function",
        "name": "get_top_connected_users",
        "description": "Return the most connected users in the similarity graph.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "How many users to return."
                }
            },
            "required": ["limit"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_strongest_similarity_pairs",
        "description": "Return user pairs with the strongest similarity edges.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "How many pairs to return."
                }
            },
            "required": ["limit"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_top_tags",
        "description": "Return the most adopted tags in the graph.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "How many tags to return."
                }
            },
            "required": ["limit"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_user_neighbors",
        "description": "Return the top neighbors of a specific user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The user ID to inspect."
                },
                "limit": {
                    "type": "integer",
                    "description": "How many neighbors to return."
                }
            },
            "required": ["user_id", "limit"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_user_summary",
        "description": "Return a summary of a specific user including degree, top neighbors, and sample adopted tags.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The user ID to summarize."
                }
            },
            "required": ["user_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_shared_tags_for_user",
        "description": "Return the most frequently shared tags among neighbors of a given user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The user ID to inspect."
                },
                "limit": {
                    "type": "integer",
                    "description": "How many tags to return."
                }
            },
            "required": ["user_id", "limit"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_graph_summary",
        "description": "Return global statistics and structure information about the graph.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

TOOL_IMPL = {
    "get_top_connected_users": get_top_connected_users,
    "get_strongest_similarity_pairs": get_strongest_similarity_pairs,
    "get_top_tags": get_top_tags,
    "get_user_neighbors": get_user_neighbors,
    "get_user_summary": get_user_summary,
    "get_shared_tags_for_user": get_shared_tags_for_user,
    "get_graph_summary": get_graph_summary,
}

# =========================
# System prompt
# =========================
SYSTEM_PROMPT = """
You are a graph analysis assistant for a Neo4j-based user similarity project.

You can retrieve graph facts using tools and then explain them.

You help users understand:
- graph structure
- influential users
- similarity relationships
- tag adoption patterns
- neighborhood structure

Rules:
- Answer only from retrieved graph facts.
- Prefer using tools whenever the question is about graph structure, users, tags, neighbors, similarity, or adoption.
- Always provide required tool arguments.
- Use limit=10 unless the user specifies otherwise.
- When the user asks broad questions like "explain the graph", "summarize the graph", or "what patterns exist", use get_graph_summary.
- Be clear, concise, and analytical.
- If graph data is insufficient, say so honestly.
"""

# =========================
# GraphRAG
# =========================
def ask_graph_rag(question: str) -> str:
    first = client.responses.create(
        model=MODEL_NAME,
        instructions=SYSTEM_PROMPT,
        input=question,
        tools=TOOLS,
        tool_choice="auto",
    )

    tool_calls = [item for item in first.output if item.type == "function_call"]

    if not tool_calls:
        return first.output_text

    tool_outputs = []
    for call in tool_calls:
        fn_name = call.name
        fn_args = json.loads(call.arguments) if call.arguments else {}
        result = TOOL_IMPL[fn_name](**fn_args)

        tool_outputs.append({
            "type": "function_call_output",
            "call_id": call.call_id,
            "output": json.dumps(result),
        })

    final = client.responses.create(
        model=MODEL_NAME,
        instructions=SYSTEM_PROMPT,
        previous_response_id=first.id,
        input=tool_outputs,
    )

    return final.output_text

# =========================
# Main
# =========================
def main() -> None:
    with driver.session() as session:
        print("Neo4j connected:", session.run("RETURN 1 AS x").single()["x"])

    print("GPT GraphRAG is ready.")
    print("Ask a graph question, or type 'exit' to quit.\n")

    try:
        while True:
            question = input("You: ").strip()

            if question.lower() in {"exit", "quit", "q"}:
                print("GraphRAG: Goodbye!")
                break

            try:
                answer = ask_graph_rag(question)
                print(f"\nGraphRAG:\n{answer}\n")
            except Exception as e:
                print(f"\nGraphRAG:\nSomething went wrong: {e}\n")
    finally:
        driver.close()

if __name__ == "__main__":
    main()