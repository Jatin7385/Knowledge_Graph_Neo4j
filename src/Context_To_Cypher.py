from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import math
import torch
import wikipedia
from newspaper import Article, ArticleException
from GoogleNews import GoogleNews
import IPython
from pyvis.network import Network
import json
from neo4j_test import GraphDatabase


# Database Credentials
uri             = "bolt://54.237.204.100:7687"
userName        = "neo4j"
password        = "grid-workings-admiralties"

# Entities list :
entities = []

# Relations list
final_relations = []

# Connect to the neo4j database server
graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

# CQL to query all the universities present in the graph
cqlNodeQuery = "MATCH (x:university) RETURN x"

# CQL to create a graph containing some of the Ivy League universities

cqlCreate = """CREATE (cornell:university { name: "Cornell University"}),

(yale:university { name: "Yale University"}),

(princeton:university { name: "Princeton University"}),

(harvard:university { name: "Harvard University"}),

 

(cornell)-[:connects_in {miles: 259}]->(yale),

(cornell)-[:connects_in {miles: 210}]->(princeton),

(cornell)-[:connects_in {miles: 327}]->(harvard),

 

(yale)-[:connects_in {miles: 259}]->(cornell),

(yale)-[:connects_in {miles: 133}]->(princeton),

(yale)-[:connects_in {miles: 133}]->(harvard),

 

(harvard)-[:connects_in {miles: 327}]->(cornell),

(harvard)-[:connects_in {miles: 133}]->(yale),

(harvard)-[:connects_in {miles: 260}]->(princeton),

 

(princeton)-[:connects_in {miles: 210}]->(cornell),

(princeton)-[:connects_in {miles: 133}]->(yale),

(princeton)-[:connects_in {miles: 260}]->(harvard)"""


# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")

def neo4j_work():
    pass

def extract_relations_from_model_output(text):
    relations = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    text_replaced = text.replace("<s>", "").replace("<pad>", "").replace("</s>", "")
    for token in text_replaced.split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                relations.append({
                    'head': subject.strip(),
                    'type': relation.strip(),
                    'tail': object_.strip()
                })
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                relations.append({
                    'head': subject.strip(),
                    'type': relation.strip(),
                    'tail': object_.strip()
                })
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        relations.append({
            'head': subject.strip(),
            'type': relation.strip(),
            'tail': object_.strip()
        })
    return relations



# class KB():
#     def __init__(self):
#         self.relations = []

#     def are_relations_equal(self, r1, r2):
#         return all(r1[attr] == r2[attr] for attr in ["head", "type", "tail"])

#     def add_relation(self, r):
#         if not self.exists_relation(r):
#             self.relations.append(r)

#     def print(self):
#         print("Relations:")
#         for r in self.relations:
#             print(f"  {r}")

def are_relations_equal(r1, r2):
        return all(r1[attr] == r2[attr] for attr in ["head", "type", "tail"])
def exists_relation(r1):
    return any(are_relations_equal(r1, r2) for r2 in final_relations)
def add_relation(r):
    if not exists_relation(r):
        final_relations.append(r)
def print_relations():
    print("Relations:")
    for r in final_relations:
        entities.append(r["head"])
        entities.append(r["tail"])
        print(f"  {r}")
    return entities

def from_small_text_to_kb(text, verbose=False):
    # kb = KB()

    # Tokenizer text
    model_inputs = tokenizer(text, max_length=512, padding=True, truncation=True,
                            return_tensors='pt')
    if verbose:
        print(f"Num tokens: {len(model_inputs['input_ids'][0])}")

    # Generate
    gen_kwargs = {
        "max_length": 216,
        "length_penalty": 0,
        "num_beams": 3,
        "num_return_sequences": 3
    }
    generated_tokens = model.generate(
        **model_inputs,
        **gen_kwargs,
    )
    decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)

    # create kb
    for sentence_pred in decoded_preds:
        relations = extract_relations_from_model_output(sentence_pred)
        for r in relations:
            add_relation(r)

    return final_relations


# Open JSON File : 
file = open('space_race_q.json')

# Return JSON Object as a dictionary]

data = json.load(file)


print("Dataset title : " , data['title'])
print("Number of qas, context sets : " , len(data["paragraphs"]))

qas_list = data["paragraphs"]
# To get the particular set of qas with context : 

# print("QAS Set are as follows : ")
# for i in range(len(qas_list)):
#     print(qas_list[i])
questions_answers_list = data['paragraphs'][0]["qas"]
# print(questions_answers_list)
# print(data['paragraphs'][0]["qas"])
context = data['paragraphs'][0]["context"]

print("Context : ", context)
print("Relations : ")
kb = from_small_text_to_kb(context, verbose=True)

# entities = list(set(entities))
entities = print_relations()
entities = list(set(entities))
print(entities)
# for i in range(len(final_relations)):
#     print(final_relations[i])

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