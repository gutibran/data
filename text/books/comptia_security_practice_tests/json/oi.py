import uuid
import json
with open("./data.json", "r+") as json_file:
    questions = json.load(json_file)
    domain_objectives = questions.keys()
    for domain_objective in questions:
        for question in questions[domain_objective]:
            question["question_id"] = str(uuid.uuid4())
    json.dump(questions, json_file)
