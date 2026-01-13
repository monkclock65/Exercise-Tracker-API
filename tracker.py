
from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,String
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
   pass

db=SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///project.db"
db.init_app(app)

class Exercise(db.Model):
 id: Mapped[int] = mapped_column(Integer,primary_key=True)
 workout: Mapped[str] = mapped_column(String,nullable=False)
 weight: Mapped[int] = mapped_column(Integer,nullable=False)
 rep: Mapped[int] = mapped_column(Integer,nullable=False)
 sets: Mapped[int] = mapped_column(Integer,nullable=False)


with app.app_context():
  db.create_all()

@app.route("/exercises")
def get_data():

  exercise = Exercise.query.all()
  

  return jsonify([
     {
        "id": e.id,
        "workout": e.workout,
        "weight": e.weight,
        "sets": e.sets,
        "rep": e.rep
    }
    for e in exercise
    ])
@app.route("/exercises/<int:id>")
def get_data_by_id(id):
   e_id = db.session.get(Exercise, id)
   if e_id:
      return jsonify(
         {
            "id": e_id.id,
            "workout": e_id.workout,
            "weight": e_id.weight,
            "sets": e_id.sets,
            "rep": e_id.rep
         }
      ), 200
   else:
      return jsonify({"message": "Exercise not found"}), 404
@app.route("/exercises", methods=["POST"])
def add_exercise():
    data = request.get_json() or {}
    required = ["workout", "weight", "rep", "sets"]
    for i in required:
            if i not in data:
                return jsonify({"message": f"Missing field: {i}"}), 400
    e = Exercise(
        workout=data.get("workout"),
        weight=data.get("weight"),
        rep=data.get("rep"),
        sets=data.get("sets"),
    )
    db.session.add(e)
    db.session.commit()
    
    return jsonify({
         "id": e.id,
         "workout": e.workout,
         "weight": e.weight,
         "sets": e.sets,
         "rep": e.rep
    }), 201
@app.route("/exercises/<int:id>", methods=["PATCH"])
def update_exercise(id):
      e_id = db.session.get(Exercise, id)
      if e_id: 
         data = request.get_json() or {}
         for field in ["workout", "weight", "rep", "sets"]:
            if field in data:
               setattr(e_id, field, data[field])
         db.session.commit()
         return jsonify({"message": "Exercise updated successfully"}), 200
      else:
         return jsonify({"message": "Exercise not found"}), 404
@app.route("/exercises/<int:id>", methods=["PUT"])
def replace_exercise(id):
    e_id = db.session.get(Exercise, id)
    if e_id:
        data = request.get_json() or {}
        required = ["workout", "weight", "rep", "sets"]
        for i in required:
            if i not in data:
                return jsonify({"message": f"Missing field: {i}"}), 400
            setattr(e_id, i, data[i])
        db.session.commit()
        return jsonify({"message": "Exercise replaced successfully"}), 200
    else:
        return jsonify({"message": "Exercise not found"}), 404

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
      e_id = db.session.get(Exercise, id)
      if e_id:
         db.session.delete(e_id)
         db.session.commit()
         return "", 204
      else:
         return jsonify({"message": "Exercise not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)