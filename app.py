from flask import Flask, request, jsonify
from models.meal import Meal
from database import db
from flask_login import LoginManager, current_user
from datetime import datetime

#INICIA FLASK
app = Flask(__name__)
#DB
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.meal_view = 'meal'

'''CRUD'''
@app.route('/meal', methods=['POST'])
def create_meal():
    data = request.json
    name_meal = data.get('name_meal')
    description = data.get('description')
    
    diet_or_not = data.get('diet_or_not')
    
    if name_meal and diet_or_not:

        existing_meal = Meal.query.filter_by(name_meal=name_meal.strip()).first()
        if existing_meal:
            return jsonify({"message": "Já existe uma refeição com esse nome"}), 400
        
        formatted = datetime.now().strftime("%d/%m/%Y %H:%M")  
        date_time = formatted
        meal = Meal(name_meal=name_meal, description=description, date_time=date_time, diet_or_not=diet_or_not)
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message" : "Comida cadastrada com sucesso!", "id": meal.id})
    return jsonify({"message" : "Dados inválidos"}),400

@app.route('/meals', methods=['GET'])
def get_meals():
    meals =  db.session.execute(db.select(Meal).order_by(Meal.name_meal)).scalars()
    output = [
    {
        "id": meal.id,
        "name_meal": meal.name_meal,
        "description": meal.description,
        "date_time": meal.date_time,
        "diet_or_not": meal.diet_or_not
    }
    for meal in meals
]
    return jsonify(output)

@app.route('/meals/<int:id>', methods=['GET'])
def get_meal_by_id(id):
    meal = db.session.get(Meal, id)
    if meal is None:
        return jsonify({"message" : "Comida não encontrada"}), 404
    return jsonify({
        "id": meal.id,
        "name_meal": meal.name_meal,
        "description": meal.description,
        "date_time": meal.date_time,
        "diet_or_not": meal.diet_or_not
    })

@app.route('/meals/<int:id>', methods=['PUT'])
def update_meal_by_id(id):
    meal = db.session.get(Meal,id)
    print(meal)
    if meal is None:
        return jsonify({"message" : "Comida não encontrada"})
    
    data = request.get_json(force=True)
    meal.name_meal = data['name_meal']
    meal.description = data['description']
    meal.date_time = data['date_time']
    meal.diet_or_not = data['diet_or_not']
    print(meal)

    db.session.commit()

    output = [
    {
        "id": meal.id,
        "name_meal": meal.name_meal,
        "description": meal.description,
        "date_time": meal.date_time,
        "diet_or_not": meal.diet_or_not
    }
    ]
    return jsonify({"message" : output})

@app.route('/meals/<int:id>', methods=['DELETE'])
def delete_meal_by_id(id):
    meal = db.session.get(Meal, id)
    print(meal)
    if meal is None:
        return jsonify({"message" : "Comida não encontrada"})
    print(meal)

    db.session.delete(meal)
    db.session.commit()

    output = [
    {
        "id": meal.id,
        "name_meal": meal.name_meal,
        "description": meal.description,
        "date_time": meal.date_time,
        "diet_or_not": meal.diet_or_not
    }
    ]
    return jsonify({"message removido:": output})

    







#DEBUG LOCAL
if __name__ == '__main__':
    app.run(debug=True)