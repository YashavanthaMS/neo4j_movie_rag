"""Cypher query templates.

Each template has:
  description : used in the LLM router prompt
  params      : parameter names (and type) the router must extract
  cypher      : parameterised, read-only Cypher
Matching is case-insensitive and uses CONTAINS so "matrix" finds "The Matrix".
"""

TEMPLATES = {
    "movies_by_actor": {
        "description": "Movies an actor/actress has appeared in (filmography).",
        "params": {"name": "str"},
        "cypher": """
            MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
            WHERE toLower(p.name) CONTAINS toLower($name)
            RETURN p.name AS actor, m.title AS movie, m.released AS year, r.roles AS roles
            ORDER BY m.released LIMIT 25
        """,
    },
    "actors_in_movie": {
        "description": "Cast list of a movie, with character roles.",
        "params": {"title": "str"},
        "cypher": """
            MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
            WHERE toLower(m.title) CONTAINS toLower($title)
            RETURN m.title AS movie, p.name AS actor, r.roles AS roles
            LIMIT 40
        """,
    },
    "movie_details": {
        "description": "General info about a movie: year, tagline, directors, cast.",
        "params": {"title": "str"},
        "cypher": """
            MATCH (m:Movie) WHERE toLower(m.title) CONTAINS toLower($title)
            OPTIONAL MATCH (d:Person)-[:DIRECTED]->(m)
            OPTIONAL MATCH (a:Person)-[:ACTED_IN]->(m)
            RETURN m.title AS movie, m.released AS year, m.tagline AS tagline,
                   collect(DISTINCT d.name) AS directors, collect(DISTINCT a.name) AS cast
            LIMIT 5
        """,
    },
    "director_of_movie": {
        "description": "Who directed (or wrote/produced) a given movie.",
        "params": {"title": "str"},
        "cypher": """
            MATCH (m:Movie) WHERE toLower(m.title) CONTAINS toLower($title)
            OPTIONAL MATCH (d:Person)-[:DIRECTED]->(m)
            OPTIONAL MATCH (w:Person)-[:WROTE]->(m)
            OPTIONAL MATCH (pr:Person)-[:PRODUCED]->(m)
            RETURN m.title AS movie, collect(DISTINCT d.name) AS directors,
                   collect(DISTINCT w.name) AS writers, collect(DISTINCT pr.name) AS producers
            LIMIT 5
        """,
    },
    "movies_by_director": {
        "description": "Movies directed by a given person.",
        "params": {"name": "str"},
        "cypher": """
            MATCH (p:Person)-[:DIRECTED]->(m:Movie)
            WHERE toLower(p.name) CONTAINS toLower($name)
            RETURN p.name AS director, m.title AS movie, m.released AS year
            ORDER BY m.released LIMIT 25
        """,
    },
    "person_info": {
        "description": "Info about a person: birth year and how many films they acted in / directed.",
        "params": {"name": "str"},
        "cypher": """
            MATCH (p:Person) WHERE toLower(p.name) CONTAINS toLower($name)
            RETURN p.name AS person, p.born AS born,
                   count { (p)-[:ACTED_IN]->() } AS films_acted,
                   count { (p)-[:DIRECTED]->() } AS films_directed
            LIMIT 5
        """,
    },
    "coactors": {
        "description": "Which actors worked most often with a given actor (co-stars).",
        "params": {"name": "str"},
        "cypher": """
            MATCH (p:Person)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(co:Person)
            WHERE toLower(p.name) CONTAINS toLower($name) AND p <> co
            RETURN p.name AS actor, co.name AS coactor, count(m) AS films_together,
                   collect(m.title)[..5] AS movies
            ORDER BY films_together DESC LIMIT 15
        """,
    },
    "movies_between_years": {
        "description": "Movies released between two years (inclusive).",
        "params": {"start": "int", "end": "int"},
        "cypher": """
            MATCH (m:Movie) WHERE m.released >= $start AND m.released <= $end
            RETURN m.title AS movie, m.released AS year
            ORDER BY m.released LIMIT 30
        """,
    },
    "movie_reviews": {
        "description": "Reviews and ratings of a movie.",
        "params": {"title": "str"},
        "cypher": """
            MATCH (p:Person)-[r:REVIEWED]->(m:Movie)
            WHERE toLower(m.title) CONTAINS toLower($title)
            RETURN m.title AS movie, p.name AS reviewer, r.rating AS rating, r.summary AS summary
            LIMIT 10
        """,
    },
    "top_rated_movies": {
        "description": "Highest rated movies according to reviews in the graph.",
        "params": {},
        "cypher": """
            MATCH (:Person)-[r:REVIEWED]->(m:Movie)
            RETURN m.title AS movie, round(avg(r.rating), 1) AS avg_rating, count(r) AS reviews
            ORDER BY avg_rating DESC, reviews DESC LIMIT 5
        """,
    },
    "recommend_similar_movies": {
        "description": "Recommend movies similar to a given movie (shared actors/directors).",
        "params": {"title": "str"},
        "cypher": """
            MATCH (m:Movie) WHERE toLower(m.title) CONTAINS toLower($title)
            WITH m LIMIT 1
            MATCH (m)<-[:ACTED_IN|DIRECTED]-(p:Person)-[:ACTED_IN|DIRECTED]->(rec:Movie)
            WHERE rec <> m
            RETURN m.title AS based_on, rec.title AS recommendation, rec.released AS year,
                   count(DISTINCT p) AS shared_people, collect(DISTINCT p.name)[..4] AS shared_with
            ORDER BY shared_people DESC, year DESC LIMIT 5
        """,
    },
    "recommend_for_actor_fans": {
        "description": "Recommend movies for someone who likes an actor, excluding that actor's own films but featuring their frequent co-stars.",
        "params": {"name": "str"},
        "cypher": """
            MATCH (p:Person)-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(co:Person)
            WHERE toLower(p.name) CONTAINS toLower($name) AND p <> co
            WITH p, co, count(*) AS w
            MATCH (co)-[:ACTED_IN]->(rec:Movie)
            WHERE NOT (p)-[:ACTED_IN]->(rec)
            RETURN rec.title AS recommendation, rec.released AS year,
                   sum(w) AS score, collect(DISTINCT co.name)[..4] AS featuring
            ORDER BY score DESC LIMIT 5
        """,
    },
    "connection_path": {
        "description": "How two people are connected through movies (shortest path, e.g. Bacon number).",
        "params": {"name1": "str", "name2": "str"},
        "cypher": """
            MATCH (a:Person), (b:Person)
            WHERE toLower(a.name) CONTAINS toLower($name1)
              AND toLower(b.name) CONTAINS toLower($name2)
            WITH a, b LIMIT 1
            MATCH path = shortestPath((a)-[:ACTED_IN|DIRECTED*..8]-(b))
            RETURN [n IN nodes(path) | coalesce(n.name, n.title)] AS path
        """,
    },
}
