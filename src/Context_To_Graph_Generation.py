from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import math
import torch
import wikipedia
from newspaper import Article, ArticleException
from GoogleNews import GoogleNews
import IPython
from pyvis.network import Network
import json
from neo4j import GraphDatabase
from Neo4j_KG_Maker import KG
import csv


# Database Credentials
uri             = "bolt://3.216.91.10:7687"
userName        = "neo4j"
password        = "advance-state-armor"

# Now lets make the Knowledge Graph : 
kg = KG(uri, userName, password)

# # Entities list :
# entities = []

# # Relations list
# final_relations = []

# Connect to the neo4j database server
graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))


# Open JSON File : 
file = open('space_race_q.json')

# Return JSON Object as a dictionary]

data = json.load(file)


print("Dataset title : " , data['title'])
print("Number of qas, context sets : " , len(data["paragraphs"]))

qas_list = data["paragraphs"]
# To get the particular set of qas with context : 

print("QAS Set are as follows : ")
for i in range(len(qas_list)):
    print(qas_list[i])
questions_answers_list = data['paragraphs'][0]["qas"]
print(questions_answers_list)
print(data['paragraphs'][0]["qas"])
context = data['paragraphs'][0]["context"]

print("Context : ", context)
print("Relations : ")


kb = kg.from_small_text_to_kb(context, verbose=True)

entities = kg.getEntities()
final_relations = kg.getFinalRelations()
entities = list(set(entities))
entities = kg.print_relations()
entities = list(set(entities))
print(entities)
for i in range(len(final_relations)):
    print(final_relations[i])

# CQL to create a entities in the KG
cqlCommands = []
for i in range(len(entities)):
    name_entity = entities[i].replace(' ', '_')
    name_entity = name_entity.replace(',', '')
    type_entity = "Entity" # We need to change this according to the NER from Spacy
    cqlCreate = f"CREATE ({name_entity} : {type_entity}) SET {name_entity}.name = $name,{name_entity}  \n"
    cqlCommands.append(cqlCreate)
    print(cqlCreate)

cqlCommands.append("*** \n")

for i in range(len(final_relations)):
    rel = final_relations[i]
    head = rel["head"].replace(' ', '_')
    head = head.replace(',', '')
    type_ = rel["type"].replace(' ', '_')
    type_ = type_.replace(',', '')
    tail = rel["tail"].replace(' ','_')
    tail = tail.replace(',','')
    cqlRelation = f"MATCH ({head} : Entity) , ({tail} : Entity) WHERE {head}.name = '{head}' AND {tail}.name = '{tail}' CREATE ({head}) -[:{type_}]->({tail}) \n"
    cqlCommands.append(cqlRelation)
    # print(rel)
    print(cqlRelation)

print(cqlCommands)

# Writing the commands to a text file : 
file1 = open("commands.txt","w")
file1.writelines(cqlCommands)
file1.close()


kg.create_graph()
# kg.close()
