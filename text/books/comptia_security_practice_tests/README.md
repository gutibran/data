# How I prepared the text
1. Converted PDF to text
2. Manually copied portions into their respective folders; answers, questions, miscellaneous, raw
3. Used regular expressions to space out text so that is easier to create JSON representations of the questions and answers

This is what was used for the questions. Still had to manually clean up a few lines because of the the text was parsed in step 1. Not sure how to fix hypenated words. I need to learn how to form better regular expressions.
```python
formatted_question_text = None
with open(question_file, "r") as file:
    question_text = file.read()
    question_text = re.sub(r'\n(?![A-D]\.)', ' ', question_text)
    question_text = re.sub(r'(\b\d{1,3}\.\s)', r'\n\1', question_text)
    question_text = re.sub(r'(D\..*?)(?=\n|$)', r'\1\n', question_text)
    question_text = re.sub(r' (\d{1,3} \.)', r'\n\1', question_text)
    formatted_question_text = question_text

with open(question_file, "w") as file:
    file.write(formatted_question_text)
```

This is what was used for the answers.
```python
formatted_answer_text = ""
with open(answer_file, "r") as file:
    answer_text = file.read()
    print(answer_text)
    answer_text = re.sub(r'\n', '', answer_text)
    pattern = re.compile(r'(\b\d{1,3}\.)')
    formatted_answer_text = re.sub(pattern, r'\n\1', answer_text)

with open(answer_file, "w") as file:
    print(formatted_answer_text)
    file.write(formatted_answer_text)
```

Overall I used some regular expressions to format the text so that it is easier to work with manually. I tried to use MistralAI7B and ChatGPT but they kept acting stupid so I had to "big dick it" and just edit some stuff manually. I know this commit is going to go on someones project that tracks for "offensive" or vulgar words. It has been a long night. Free exposure I guess.

4. Consolidatng the questions and answers into a single JSON file.
I have to manually edit some parts of the questions and answers because there are hypens in the middle of some words (in the pdf it was for the text moving to the next page). Also some of the questions have a graphic so I converted the image to a base64 string. This is so that when this data has been consolidated and ready for the bot to use it can decode and post the image to twitter easily. There may still be some errors within the text that may require manual clean up. Finnally got the process down. There are some hiccups and some additional processing but it gets about 93.69% percent of the job done which is a lot more efficient and effective than doing this shit by hand so it is good in my eyes. There is still room for improvement.
```python
import json
import re
import base64
import sys

# turn the parts of the answer into a list
answer_blocks = []
with open(answers_fil, "r") as file:
    for line in file.readlines():
        answer_blocks.append(line)
        
# turn the parts of the question block into a list
question_blocks = []
with open(questions_file, "r") as file:
    question_block = ""
    for line in file.readlines():
        if line == "\n":
            question_blocks.append(question_block)
            question_block = ""
            continue
        question_block += line

# since both lengths are the same I can iterate through both lists with one interator variable
questions = []
for i in range(len(question_blocks)):
    question = {}
    
    # extract question text and label it
    question_block = question_blocks[i].split("\n")
    question_block = [part for part in question_block if part != ""]
    question_id_pattern = re.compile(r'\b(\d{1,3}\.\s)')
    print(question_block)
    question_id = int(question_id_pattern.findall(question_block[0])[0].replace(".", "").strip())
    question_text = re.sub(r'^\d{1,3}\.\s*', '', question_block[0].strip())

    question["question_id"] = question_id
    question["question_text"] = question_text
    
    # check if the question has an image
    if len(question_block) > 5:
        question["png_base64"] = question_block[1]
        question["choice_a"] =  question_block[2].strip()
        question["choice_b"] = question_block[3].strip()
        question["choice_c"] = question_block[4].strip()
        question["choice_d"] = question_block[5].strip()
    else:
        question["choice_a"] =  question_block[1].strip()
        question["choice_b"] = question_block[2].strip()
        question["choice_c"] = question_block[3].strip()
        question["choice_d"] = question_block[4].strip()

    # extract answer text and label it
    answer_block = answer_blocks[i].split("\n")
    answer_block = [part for part in answer_block if part != ""]
    answer_id_pattern = re.compile(r'\b(\d{1,3}\.\s)')
    answer_id = int(answer_id_pattern.findall(answer_block[0])[0].strip().replace(".", ""))
    answer_letter = re.search(r'\b([A-Z]\.)', answer_block[0]).group(0).replace(".", "")

    # need to write a method to handle when the text is over 250 characters or buy a subscriptoin
    answer_text =  re.search(r'([A-Z]\.)\s*(.*)', answer_block[0]).group(2)

    if answer_id != question_id:
        print(answer_id, question_id)
        sys.exit()

    question["answer_letter"] = answer_letter
    question["answer_text"] = answer_text

    # should be a list of objects each object wilkl have the tweet id and its reply id for when the answer is posted
    question["tweet_ids"] = []
    questions.append(question)
    result["domain_objective_1_general_security"] = questions

# save data into json
with open(json_output_file, "w") as json_file:
    json.dump(result, json_file)
```

Used this to set each question_id to a uuid. Had to do this because each question within their respective objective domain started its question id naming from 1 to N. I am keeping track of which questions were tweeted by their original id. I noticed that this would not work because it overwrite questions and the it would be all fucked up.
```python
import uuid
import json

# rename all questions to have uuid;s
questions = download_data()
domain_objectives = questions.keys()
for domain_objective in questions:
    for question in questions[domain_objective]:
        question["question_id"] = str(uuid.uuid4())

with open("./data.json", "w") as json_file:
    json.dump(questions, json_file)
```

After getting all the questions and answers into single JSON file I merged them together under one object and under one file. The final result is in data.json Everything is organized properly, just need to get rid of hypens within the question and answer test and add base64 encoded binary strings of the images. After that the data is ready to be used in the Twitter bot.


# Problems that need to be automated (need to figure out how to do this for future data collecting)
- differentiate words that require hypens and words that do not require hypen (pdf text word wrap)
- improve skill at building regular expressions
- improve "prompt engineering" to hand these tasks off to a GPT
