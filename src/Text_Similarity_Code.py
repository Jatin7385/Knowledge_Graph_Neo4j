from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "bert-base-cased-finetuned-mrpc"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sequence_0 = "has part"
sequence_1 = "Participant In"

tokens = tokenizer.encode_plus(sequence_0, sequence_1, return_tensors="pt")
classification_logits = model(**tokens)[0]
results = torch.softmax(classification_logits, dim=1).tolist()[0]

classes = ["not paraphrase", "is paraphrase"]
for i in range(len(classes)):
    print(f"{classes[i]}: {round(results[i] * 100)}%")