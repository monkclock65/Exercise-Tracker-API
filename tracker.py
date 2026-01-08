from flask import Flask

app = Flask(__name__)

@app.route("/")
def tracker():
 class Exercise:
    def __init__(self,name,set,rep):
         self.name = name
         self.set = set
         self.rep = rep

 routine = Exercise("double arm swing",3,10)

 return routine.name

