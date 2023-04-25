# Knowledge_Graph_Neo4j
Creating Knowledge Graphs from Contexts/ Texts

## Instructions : 
- The working code is in the src folder
- Before using, change the url and credentials of the neo4j sandbox

## The logic of the project : 
This project tries to utilize Knowledge Graphs for question answering systems.
We use a Neo4j Knowledge Graph for the same...

- The code begins with the Context_To_Graph.py File, where we take a sample context from the SQUAD Dataset.
- Then we perform Named Entity Recognition, Relationship extraction etc to extract the entities and relationships.
- We use these to create the graphs by generating Cypher queries using f"".
- Finally we run the cypher queries generated in the commands.txt file, using the Neo4j Driver to generate the knowledge graph with entities and relationships
- 
