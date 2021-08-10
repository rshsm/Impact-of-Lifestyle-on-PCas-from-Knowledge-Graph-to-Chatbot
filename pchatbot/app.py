from question_classifier import *
from question_parser import *
from answer_search import *
from helper import lifestyle_pipei
import os

class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionParser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = 'Sorry, no answers can be found, please try another!'
        # 判断输入的是否是lfst
        max_lfst = 3
        lfst_seg = [tk.lower() for tk in sent.strip().strip(',.?!').split()]
        if(len(lfst_seg) <= max_lfst and len(lfst_seg) >= 1 and sent.startswith(('pcaoc', 'pbase')) == False):
            deal_seg = ' '.join(lfst_seg)
            candidate_lfsts = lifestyle_pipei(deal_seg)
            if(len(candidate_lfsts) == 0):
                return answer
            if(deal_seg == candidate_lfsts[0]):
                return 'Congratulations! The lifestyle ' + candidate_lfsts[0] + ' exists in our KG, Please send your further request.'
            else:
                return 'In our KG, the lifestyle(s) related to your query is/are: ' + '; '.join(candidate_lfsts) + '.'
            

        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)
handle = ChatBotGraph()

chatbot = ChatBot("Anthony")
conversation = [
    "Hello!",
    "Hi!"
]

trainer = ListTrainer(chatbot)

trainer.train(conversation)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    usermsg = request.args.get('msg')
    answer = handle.chat_main(usermsg)
    return str(answer)

if __name__ == "__main__":
    app.run()
