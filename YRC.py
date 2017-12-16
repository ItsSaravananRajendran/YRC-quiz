from flask import Flask, render_template, request
import os
import sys
import random

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


easySet = []
medSet = []
diffSet = []
global randRange

def readQuestion():
    data = None
    my_dir = os.path.dirname(__file__)
    filePath = os.path.join(my_dir, 'Easy')
    with open(filePath, 'r') as inputData:
        data= inputData.read().split('\n')

    questions = {}
    option = []
    count = 0
    for line in data:
        if count%6 == 0:
            questions = {}
            questions['Q'] = line
            option = []
        elif count%6 == 5:
            questions['O'] = option
            questions['A'] = line.lower()
            easySet.append(questions)
        else:
            option.append(line)
        count += 1

    filePath = os.path.join(my_dir, 'med')
    with open(filePath, 'r') as inputData:
        data= inputData.read().split('\n')

    questions = {}
    option = []
    count = 0
    for line in data:
        if count%6 == 0:
            questions = {}
            questions['Q'] = line
            option = []
        elif count%6 == 5:
            questions['O'] = option
            questions['A'] = line.lower()
            medSet.append(questions)
        else:
            option.append(line)
        count += 1

    filePath = os.path.join(my_dir, 'diff')
    with open(filePath, 'r') as inputData:
        data = inputData.read().split('\n')

    questions = {}
    option = []
    count = 0
    for line in data:
        if count % 6 == 0:
            questions = {}
            questions['Q'] = line
            option = []
        elif count % 6 == 5:
            questions['O'] = option
            questions['A'] = line.lower()
            diffSet.append(questions)
        else:
            option.append(line)
        count += 1

def getRand(ls):
    return [I for I in range(len(ls))]

@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/start',methods=['POST','GET'])
def question():
    global  randRange
    randRange = [I for I in range(len(easySet))]
    questionNo = random.choice(randRange)
    question = easySet[questionNo]['Q']
    option = easySet[questionNo]['O']
    attempted = 0
    return render_template('display.html',score=0,questionNo=questionNo,status="",option=option,question=question,difficulty="Easy",attempted=attempted+1)

@app.route('/question',methods=['POST','GET'])
def nextQuestion():
    global  randRange
    questionNo = int(request.form['questionNo'])
    difficulty = request.form['difficulty']
    score = int(request.form['score'])
    answer = request.form['question']
    attempted = int(request.form['attempted'])
    ques = None
    if difficulty == "Easy":
        ques = easySet[questionNo]
    elif difficulty == "Med":
        ques = medSet[questionNo]
    elif difficulty == "Diff":
        ques = diffSet[questionNo]
    if answer == "None":
        return render_template('display.html', score=score, questionNo=questionNo, status="Select an answer", option=ques['O'], question=ques['Q'],difficulty=difficulty,attempted=attempted)
    else:
        if answer == ques['A']:
            score +=1
            randRange.remove(questionNo)
        attempted += 1
        if attempted > 7 :
            if score > 4 :
                difficulty = "Med"
                randRange = getRand(medSet)
            else:
                return render_template('Score.html', score=score)

        if attempted == 14 :
            if score > 8:
                difficulty = "Diff"
                randRange = getRand(diffSet)
            else:
                return render_template('Score.html', score=score)

        if attempted == 18 and score > 9:
            return render_template('Score.html',score=score)
        questionNo = random.choice(randRange)
        if difficulty == "Easy":
            ques = easySet[questionNo]
        elif difficulty == "Med":
            ques = medSet[questionNo]
        elif difficulty == "Diff":
            ques = diffSet[questionNo]


    return render_template('display.html',score=score,questionNo=questionNo,status="",option=ques['O'],question=ques['Q'],difficulty=difficulty,attempted=attempted)


if __name__ == '__main__':
    readQuestion()
    app.run()
