import json
from neo4j import GraphDatabase
import csv
from Neo4j_KG_Maker import KG

# Opening Knowledge graph, to extract data: 
kg = KG("bolt://44.203.229.74:7687", "neo4j", "thermometer-sponges-basins")
context_list = kg.extract_subgraphs()

print(context_list)

kg.close()
