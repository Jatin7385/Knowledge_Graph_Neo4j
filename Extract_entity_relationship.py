# To extract entity relationships from an english dataset : 

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import spacy
from itertools import combinations
from neo4j_test import GraphDatabase

uri = "neo4j+s://9740dbf3a051f4c9b6ed9ad679e631ef.neo4jsandbox.com:7687"
driver = GraphDatabase.driver(uri, auth = ("neo4j","salutes-pattern-facilitation"))

# Step 1 : 
## Prepare the dataset : (Load the dataset, perform necessary cleaning and preprocessing such as removing noise, stop words and stemming)
text = "The quick brown fox jumps over the lazy dog"
stop_words = set(stopwords.words('english'))

# Step 2 : 
## Tokenization : (Use a tokenization library such as NLTK to split the text into individual words or phrases)

word_tokens = word_tokenize(text)
print(text)
print(word_tokens)


### Convert the words into lower case and remove stop words : 
word_tokens = [w for w in word_tokens if not w.lower() in stop_words]

print("Stop words removed, and lower cased : ")
print(word_tokens)


# Step 3 : 
## Part of Speech Tagging : (Use POS tagging library such as NLTK to label each word in the text with its corresponding part of Speech)
pos_tags = pos_tag(word_tokens)
print("POS Tags : " , pos_tags)

# Step 4 : 
## Dependency Parsing : (Use a dependency parsing library such as spacy or Stanford CoreNLP to identify the grammatical structure of the sentence and the relationships between words)
print("Result of dependency parsing")
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos, 
          [child for child in token.children])

# Step 5 : 
## Named Entity Recognition(NER) : (Use a NER library such as NLTK to identify the entities in the texts such as people, organization, locations etc)
print("After NER")
doc = nlp("John works at Google in California.")
# entities = []
# for ent in doc.ents:
#     # print(ent.text, ent.label_)
#     entities.append((ent.text, ent.label_))

# print("Entities : ")
# print(entities)

# # For relationships :
# relationships = [] 
# for combination in combinations(entities,2):
#     relationships.append(combination)

# Extract the entities and relationships
entities = [(ent.text, ent.label_) for ent in doc.ents]
relationships = [(token.head.text, token.dep_, token.text) for token in doc if token.dep_ == "nsubj"]

print(doc)
for token in doc:
    print("Token head text : ", token.head.text)
    print("Dep : ", token.dep_)
    print("Text : ", token.text)
    print("*************************")
print("Entities : ")
print(entities)
print("Relationships : ")
print(relationships)

# Define the function to create nodes and relationships in the graph
def create_graph(tx, entity1, entity2, relation):
    tx.run("MERGE (e1:Entity {name: $entity1}) "
           "MERGE (e2:Entity {name: $entity2}) "
           "MERGE (e1)-[r:RELATION]->(e2) "
           "SET r.name = $relation",
           entity1=entity1, entity2=entity2, relation=relation)

# Create the nodes and relationships in the graph
with driver.session() as session:
    for entity1, label1 in entities:
        for entity2, label2 in entities:
            for head, dep, tail in relationships:
                if entity1 == head and entity2 == tail:
                    print("entity1 : ", head)
                    print("relationship : ", dep)
                    print("entity 2 : ", tail)
                    session.write_transaction(create_graph, entity1, entity2, dep)


# salutes-pattern-facilitation
# neo4j+s://9740dbf3a051f4c9b6ed9ad679e631ef.neo4jsandbox.com:7687