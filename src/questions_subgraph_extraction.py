import json
from neo4j import GraphDatabase
import csv
from Neo4j_KG_Maker import KG

# Opening Knowledge graph, to extract data: 
kg = KG("bolt://3.216.91.10:7687", "neo4j", "advance-state-armor")
context_list = kg.extract_subgraphs()

print(context_list)

kg.close()
