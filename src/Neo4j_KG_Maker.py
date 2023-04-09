from neo4j import GraphDatabase

class KG:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.flag = 0

    def close(self):
        self.driver.close()

    def run_queries(self):
        with self.driver.session() as session:
            session.execute_write(self.run)

    @staticmethod
    def run(tx):
        # Reading the commands from a text file : 
        file1 = open("./commands.txt","r+")
        lines = file1.readlines()
        flag = 0
        print(lines)
        for i in range(len(lines)): 
            lines[i] = lines[i].replace(" \n","")
            print(lines[i])
            if(lines[i] == "***"):
                flag = 1
                print("Hello")
                continue
            if(flag == 0):
                x = lines[i].split(",")
                msg = x[1].strip()
                com = x[0]
                print(x[1])
                result = tx.run(com,name = msg)
                print(result)
            else:
                result = tx.run(lines[i])
                print(result)
        file1.close()

kg = KG("bolt://44.203.229.74:7687", "neo4j", "thermometer-sponges-basins")
kg.run_queries()
kg.close()