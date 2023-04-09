# To extract the first context and questions from the space race datasets
import json
import spacy
import wikipedia

nlp = spacy.load("en_core_web_lg")

# Open JSON File : 
file = open('space_race_q.json')

# Return JSON Object as a dictionary]

data = json.load(file)

qas_list = data["paragraphs"]

questions_answers_list = data['paragraphs'][0]["qas"]

context = data['paragraphs'][0]["context"]

context_sentences = context.split(".")
print(context_sentences)

# print(questions_answers_list)

# print("Context : " , context)

doc = nlp(context)

#### Named Entity Recognition

entities = []

for ent in doc.ents:
    # print(ent.text, ent.label_)
    entities.append((ent.text, ent.label_))

print(entities)
# spacy.displacy.serve(doc, style='dep')


### Performing Entity linking for entity disambiguation( Some errors coming in Disambiguation. This needs to be sorted out later)

#### For each named entity, use the Wikipedia library to retrieve a list of candidate entities.
# def get_candidate_entities(entity):
#     try:
#         return wikipedia.search(entity)
#     except wikipedia.exceptions.DisambiguationError as e:
#         return e.options
    

# candidate_entites = {}

# for entity, label in entities:
#     candidate_entites[entity] = get_candidate_entities(entity)

# print("Candidate_entites : ", candidate_entites)
# #### For each candidate entity, use the Wikipedia library to retrieve the corresponding Wikipedia page and extract the page summary.
# summaries = {}
# for entity, candidates in candidate_entites.items():
#     for candidate in candidates:
#         try:
#             page = wikipedia.page(candidate)
#             summary = page.summary
#             summaries[candidate] = summary
#         except wikipedia.exceptions.PageError:
#             pass
# print("***********************************************************************************")
# print("Summaries : " , summaries)
#### Use a disambiguation method to select the correct entity for each named entity. One simple method is to select the candidate entity with the highest cosine similarity between its summary and the context of the named entity.


#Step 3 : Relationship Extraction
## Using Wiki80 Dataset