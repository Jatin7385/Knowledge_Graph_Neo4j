import json

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
# print("Context : " , context)

# Getting each question from the dataset and answer
# print(questions_answers_list[0])
# print(questions_answers_list[0]["question"])
# print(questions_answers_list[0]["id"])
# print(questions_answers_list[0]["answers"])
# print(questions_answers_list[0]["answers"][0]["text"])
# print(questions_answers_list[0]["answers"][0]["answer_start"])
for i in range(len(questions_answers_list)):
    print(questions_answers_list[i])
    print(questions_answers_list[i]["question"])
    print(questions_answers_list[i]["id"])
    print(questions_answers_list[i]["answers"])
    print(questions_answers_list[i]["answers"][0]["text"])
    print(questions_answers_list[i]["answers"][0]["answer_start"])

file.close()