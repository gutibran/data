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

4. Consolidated the questions and answers into a single JSON file.