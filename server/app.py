# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {"message":"Welcome to the pet directory!"}
    return make_response(
        body,
        200
    )


@app.route('/demo_json/<int:id>')
def demo_json(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet:
        pet_dict = {"id": pet.id, 
                    "name" : pet.name, 
                    "species" : pet.species}
        status_code = 200
    else:
        pet_dict={"message" : f"Pet {id} not found."}
        status_code = 404

    return make_response(pet_dict, status_code)

@app.route("/species/<string:species>")
def pet_by_species(species):
    pets =[]
    for pet in Pet.query.filter(Pet.species == species).all():
        pet_dict={'id':pet.id,
                  'name': pet.name
                 }
        pets.append(pet_dict)
    body={'count':len(pets),
          'pets': pets
         }
    status_code = 200
    return make_response(body,status_code)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
