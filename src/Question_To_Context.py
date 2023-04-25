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

# Now lets make the Knowledge Graph : 
kg = KG(uri, userName, password)

# Extracting the questions present in the dataset : 
questions = []
for i in range(len(questions_answers_list)):
    question = questions_answers_list[i]["question"]
    questions.append(question)

print("Context : ", context)
print("Relations : ")
kb = kg.from_small_text_to_kb(context, verbose=True)

entities = kg.getEntities()
final_relations = kg.getFinalRelations()

entities1 = []
final_final_relations = []


# Writing the question relations/entities to a text file : 
with open("question_relations.csv", mode = "w") as file:
    # Write the relations to the file : 
    csvwriter = csv.writer(file)
    # Named entity recognition and relationship extraction of the questions present : 
    for i in range(len(questions)):
        # Reinitializing kg : 
        kg = KG(uri, userName, password)
        final_relations = []
        entity = []
        file_list = []
        kb = kg.from_small_text_to_kb(questions[i], verbose=True)
        # entities = list(set(entities))
        entities = kg.print_relations()
        print("Entity : ", entity)
        entities = list(set(entities))
        entities1.append(entities)
        final_relations = kg.getFinalRelations()
        for j in range(len(final_relations)):
            file_list = []
            head = final_relations[j]['head']
            head = head.replace(",","")
            head = head.replace(" ","_")
            type_ = final_relations[j]['type']
            type_ = type_.replace(",","")
            type_ = type_.replace(" ","_")
            tail = final_relations[j]['tail']
            tail = tail.replace(",","")
            tail = tail.replace(" ","_")
            file_list.append(head)
            file_list.append(type_)
            file_list.append(tail)
            csvwriter.writerow(file_list)
        final_final_relations.append(final_relations)

    print(entities)
    print(final_final_relations)


# Extracting data based on Knowledge Graph: 
context_list = kg.extract_subgraphs()

print(questions)
print(context_list)

to_be_written = []
for i in range(len(questions)):
    to_write = questions[i] + "," + context_list[i] + " \n"
    to_be_written.append(to_write)

print(to_be_written)
# Writing the commands to a text file : 
file1 = open("question_context.txt","w")
file1.writelines(to_be_written)
file1.close()