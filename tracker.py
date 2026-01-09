from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
   pass

db=SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///project.db"
db.init_app(app)

class Exercise(db.Model):
 id: Mapped[int] = mapped_column(primary_key=True)
 workout: Mapped[str] = mapped_column(nullable=False)
 rep: Mapped[int] = mapped_column(nullable=False)
 sets: Mapped[int] = mapped_column(nullable=False)

with app.app_context():
  db.create_all()

@app.route("/")
def tracker():
  exercise = Exercise(workout="double arm swing",sets=3,rep=10)
  db.session.add(exercise)
  db.session.commit()

  exercises = Exercise.query.all()
  

  return jsonify([
     {
        "id": e.id,
        "workout": e.workout,
        "sets": e.sets,
        "rep": e.rep
    }
    for e in exercises
    ])


