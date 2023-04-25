from transformers import pipeline
import json

qa_model = pipeline("question-answering")

file1 = open("./question_context.txt","r+")
lines = file1.readlines()


# Open JSON File : 
file = open('space_race_q.json')

# Return JSON Object as a dictionary]

data = json.load(file)


print("Dataset title : " , data['title'])
print("Number of qas, context sets : " , len(data["paragraphs"]))

qas_list = data["paragraphs"]
# To get the particular set of qas with context : 

# print("QAS Set are as follows : ")
for i in range(len(qas_list)):
    print(qas_list[i])
questions_answers_list = data['paragraphs'][0]["qas"]
# print(questions_answers_list)
# print(data['paragraphs'][0]["qas"])
context = data['paragraphs'][0]["context"]

# print("Context : ", context)


for i in range(len(lines)):
    print(lines[i])
    question = lines[i].split(",")
    q = question[0]
    ans = question[1].strip()
    print(ans)
    if(ans == 'X'):
        ans = context
    print("Question : ", q)
    print(qa_model(question = q, context = ans))

# question = "Where do I live?"
# context = "My name is Merve and I live in İstanbul."
# print(qa_model(question = question, context = context))
## {'answer': 'İstanbul', 'end': 39, 'score': 0.953, 'start': 31}