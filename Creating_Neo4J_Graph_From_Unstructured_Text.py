## This is a Text to a Knowledge graph pipeline

# Pipeline Input : 
## PDF, Scrape Webpages, Text Files, Emails, Messaging Platforms

## Pipelining Output : Knowledge Graph
### Nodes or entities(Nodes can have various labels and Properties)
### Links or relationships(Links can be of various types and can have many properties)

################################################################################################33333
## Information Extraction Pipeline Steps
# Input Data -> (Step 1) Conference resolution -> (Step 2) Named Entity Linking -> (Step 3) Relationship Extraction -> (Step 4) Store results in Knowledge Graph

# First 3 steps are NLP techniques

###############################################################################################################333333
import spacy

def get_coref_clusters(doc):
    return doc._.coref_resolved

nlp = spacy.load("en_core_web_lg")
# Register the coref_clusters extension
# spacy.tokens.Doc.set_extension("coref_clusters", getter=get_coref_clusters, force=True)

doc = nlp("John has a dog. He loves him.")

'''
Step 1 : CONFERENCE RESOLUTION :-
Conference resolution is the task of finding all expressions that refer to the same entity in a text. It is an important step for a lot of higher
level NLP tasks that involve Natural Language understanding such as document summarization, question answering, and information extraction.

-   Personal Pronouns
-   Location Pronouns
-   Possessive pronouns
...............

Example : 
Input text : Elon musk was born in South Africa. There, he briefly attended classes at the University of Pretoria
    |
    |
    V
Output Text : Elon musk was born in South Africa. In "South Africa, Elon Musk" briefly attended classes at the University of Pretoria
'''

# for cluster in doc._.coref_clusters:
#     print(cluster.mentions)

#################################################################################################################################

'''
Step 2 : Named Entity Recongnition : 
Named entity recognition is a subtask of information extraction that seeks to locate and classify named entities mentioned in unstructured text into pre-defined categories
such as person names, organizations, locations, medical codes, time expressions, quantities, monetary values, percentages

"Elon Musk(Person)" was born in "South Africa (GPE)". In "South Africa(GPE)", "Elon Musk(Person)" briefly attended classes at "The University of Pretoria(Org)"

Limitations : 
- A single real world entity can have many different text records
- There is no silver bullet NLP model, various domains require various custom models
- No model is 100% accurate

Solving entity disambiguation - Entity Linking : 
In entity linking, words of interest(Names of persons, locations and companies) are mapped from an input text to corresponding unique entities
in a target knowledge base. The target knowledge base depends on the intended application, but for entity linking systems intended to work on open-domain
text it is common to use knowledge-bases derived from Wikipedia. Entity linking techniques that map named entities to Wikipedia entities are also called wikification

Elon Musk(Person - Q317521) was bron in South Africa. Mr. Musk(Person - Q317521) attended the University of Pretoria. Engineering lessons were favorite by Elon(Person - Q317521).

Co-occurence graphs :  By way of definition, co-occuence networks are the collective interconnection of terms based on their paired presence within a specified unit of text
                        -Co-occur->
(South Africa)                                  (University of Pretoria)
                -Co-occur->(Elon musk)-Co-occur->
            
''' 
for ent in doc.ents:
    print(ent.text, ent.label_)

spacy.displacy.render(doc, style = "ent", jupyter = True)

'''
Step 3 : Relationship Extraction
Relationship extraction is the task of extracting semantic relationships from a text. Extracted relationships a pair of entities and fall into a number of semantic categories(Born, employed, attended)

(Elon Musk) -Born-> (South Africa)

- Rule based relationship extraction using grammatical dependencies
- NLP model approach

Rule based Relation Extraction : Using grammatical dependencies to extract relations.
      <---nsubjpass-
      <-AuxPass-      -Prep-> --Pobj->
Elon Musk    was    born   in  South Africa
  PropN      AUX    VERB   ADP    PROPN

Relation extraction with NLP models : 
- Choosing the right model
- Types of extracted relationships based on the training data
- Wiki80 dataset
- TACRED dataset
- Custom dataset

WIKI80 training dataset : 
- 80 different relationship types
- Conforms to Wikidata/ Wikipedia relationships type standards
- If you use wikipedia for entity linking and models based on Wiki80 dataset, you are esentially creating a knowledge graph that conforms to Wikipedia ontology

'''