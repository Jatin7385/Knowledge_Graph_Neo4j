# Knowledge_Graph_Neo4j
Creating Knowledge Graphs from Contexts/ Texts

## Instructions : 
- The working code is in the src folder
- Before using, change the url and credentials of the neo4j sandbox

## The logic of the project : (Use Lemmatization before extracting entities and relationships... That way, the relationships stay constant....) Go over NLP Stages/ Concepts..... Revisit Relationship extraction and the entire KG Maker file in the code...
This project tries to utilize Knowledge Graphs for question answering systems.
We use a Neo4j Knowledge Graph for the same...

- The code begins with the Context_To_Graph.py File, where we take a sample context from the SQUAD Dataset.
- Then we perform Named Entity Recognition, Relationship extraction etc to extract the entities and relationships.
- We use these to create the graphs by generating Cypher queries using f"".
- Finally we run the cypher queries generated in the commands.txt file, using the Neo4j Driver to generate the knowledge graph with entities and relationships

- Now we move onto the Question_To_Context.py file, where we take all sample contexts from the SQUAD dataset.
- We perform NER, Relationship extractions on each of the questions to extract entities/relationships that can be used for searching in the KG.
- We make a (head, type_, tail) triplet tupple, for extraction. Then put it in the question_relations.csv file
- Now we use the triplets to find the context from KG. We use the MATCH command to extract a subgraph. First we try to see if the first entity to find a subgraph. If nothing there, then we try with the second entity. If still nothing found, then we put an X signifying that the entire Context would have to be passed for BERT to get the answer.
- We can try something like this : ( Since both the entities are not accurate as such. We will run the match command twice
                # Once with one entity and relation. Secondly with the second entity and relation
                # Then backup can be to use just the entity, and then search for the relation in the list
                # Then the final backup can be to use just the relation and search for entities.)
- Note : Relations and entities are not accurate, I found a random code on Google that does it, still haven't understood it completely.
- We can also use, text similarity models for Subgraph extraction instead of using ==, which makes it a soft checking in KG, and can increase the chances of finding a good answer in the KG.
-

- Now we move onto the BERT QA System.
- We are using the transformers library for the same, and using multiple variants of BERT transformers for QA.
- We are extracting the q and context from the txt file, and if X is shown, then using the entire context as the answer
- We then, first use the context generated with whatever we could find in the KG, and try to answer the question. If the probability is low, then we pass the entire context instead to get the answer.



