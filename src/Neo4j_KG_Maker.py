from neo4j import GraphDatabase
import csv
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class KG:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.flag = 0
        self.entities = []
        self.final_relations = []
        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")

    def close(self):
        self.driver.close()

    def create_graph(self):
        with self.driver.session() as tx:
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

    def run_match_command(self, tx, relcmd, namee):
        namecmd = "{name : $name}"
        cmd = f"MATCH (n:Entity {namecmd})-[r : {relcmd}]-(m) RETURN n, r, m"
        graph_response = tx.run(cmd, name = namee)
        answer = [record.data() for record in graph_response]
        return answer
    
    def generate_context_from_subgraphs(self, answer):
        context = ""
        context = answer[0]["r"][0]["name"] + " " + answer[0]["r"][1] + " " + answer[0]["r"][2]["name"]
        context = context.replace("_", " ")
        print(context)
        return context

    def extract_subgraphs(self):
        with self.driver.session() as tx:
            question_relations = []

            with open('question_relations.csv',mode = "r") as file:
                csvFile = csv.reader(file)
                
                for lines in csvFile:
                    if(len(lines) == 0):continue
                    question_relations.append(lines)
            
            print("Question relations are : ")

            answers_list = []

            context_list = []
            for i in range(len(question_relations)):
                print(question_relations[i])
                relcmd = question_relations[i][1]
                # Entity taken as first entity
                namee = question_relations[i][0]
                answer = self.run_match_command(tx,relcmd,namee)
                # print(answer)
                if(len(answer) == 0):
                    # Entity taken as second entity
                    namee = question_relations[i][2]
                    answer = self.run_match_command(tx, relcmd, namee)
                context = "X"
                if(len(answer) != 0):
                    context = self.generate_context_from_subgraphs(answer)
                context_list.append(context)
                answers_list.append(answers_list)

            print("Answers list : ")
            print(answers_list)
        return context_list

                # Since both the entities are not accurate as such. We will run the match command twice
                # Once with one entity and relation. Secondly with the second entity and relation
                # Then backup can be to use just the entity, and then search for the relation in the list
                # Then the final backup can be to use just the relation and search for entities.

                # If nothing works/ Length of response list is 0, then we will give the context as the entire context to BERT

    def neo4j_work(self):
        pass

    def extract_relations_from_model_output(self,text):
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

    def are_relations_equal(self,r1, r2):
            return all(r1[attr] == r2[attr] for attr in ["head", "type", "tail"])
    def exists_relation(self,r1):
        return any(self.are_relations_equal(r1, r2) for r2 in self.final_relations)
    def add_relation(self,r):
        if not self.exists_relation(r):
            self.final_relations.append(r)
    def print_relations(self,):
        print("Relations:")
        for r in self.final_relations:
            self.entities.append(r["head"])
            self.entities.append(r["tail"])
            print(f"  {r}")
        return self.entities
    def from_small_text_to_kb(self,text, verbose=False):
        # kb = KB()

        # Tokenizer text
        model_inputs = self.tokenizer(text, max_length=512, padding=True, truncation=True,
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
        generated_tokens = self.model.generate(
            **model_inputs,
            **gen_kwargs,
        )
        decoded_preds = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)

        # create kb
        for sentence_pred in decoded_preds:
            relations = self.extract_relations_from_model_output(sentence_pred)
            for r in relations:
                self.add_relation(r)

        return self.final_relations


    def getEntities(self):
        return self.entities
    
    def getFinalRelations(self):
        return self.final_relations
        

        