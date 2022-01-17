from peewee import *


db = PostgresqlDatabase('atlrestaurants', user='postgres', password='', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Restaurants(BaseModel):
    name = CharField()
    address = CharField()
    url = CharField()
    best_dish = CharField()
    phone_num = CharField()
    meal = CharField() 


db.connect()
# db.drop_tables([Restaurants])
# db.create_tables([Restaurants])



# suninmybelly = Restaurants(name ='Sun in My Belly', address = '2161 College Ave NE, Atlanta, GA 30317', url = 'https://www.suninmybelly.com/', best_dish = 'challah french toast', phone_num = '(404) 370-1088', meal='brunch' )
# rocksteady = Restaurants(name = 'Roc Steady', address = '907 Marietta St NW Atlanta, GA 30318', url = 'http://rocksteadyatl.com', best_dish = 'jerk chicken sliders', phone_num = '(470) 788-8120', meal='dinner')
# arepamia = Restaurants(name = 'Arepa Mia', address = '10 N Claredon Ave Avondale Estates, GA 30002', url = 'https://www.arepamiaatlanta.com/', best_dish = 'pabellon', phone_num = '(404) 600-3509', meal='lunch')

# suninmybelly.save()
# rocksteady.save()
# arepamia.save()

################################

from flask import Flask
from flask import request
from flask import jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model


app = Flask(__name__)


@app.route('/' )
def index():
    return 'Welcome to Tastes of ATL'


@app.route('/restaurants' , methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/restaurants/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def restaurants(id = None):
    if request.method == 'GET': 
        if id:
            restaurants = Restaurants.get(Restaurants.id == id)
            restaurants = model_to_dict(restaurants)
            restaurants = jsonify(restaurants)
            return restaurants
        else:

            restaurant = []
            for restaurants in Restaurants.select():
                restaurant.append(model_to_dict(restaurants))
            return jsonify(restaurant)

    if request.method == 'POST':
        restaurants = request.get_json()
        restaurants = dict_to_model(Restaurants, restaurants)
        restaurants.save()
        restaurants = model_to_dict(restaurants)
        restaurants = jsonify(restaurants)
        return restaurants


    if request.method == 'DELETE':
        restaurants = Restaurants.get(Restaurants.id == id)
        restaurants.delete_instance()
        return jsonify({"deleted": True})

    if request.method == 'PUT':
        updated_restaurants = request.get_json()
        restaurants = Restaurants.get(Restaurants.id == id)
        restaurants.name = updated_restaurants['name']
        restaurants.address = updated_restaurants['address']
        restaurants.url = updated_restaurants['url']
        restaurants.best_dish = updated_restaurants['best_dish']
        restaurants.phone_num = updated_restaurants['phone_num']
        restaurants.meal = updated_restaurants['meal']
        restaurants.save()
        restaurants = model_to_dict(restaurants)
        restaurants = jsonify(restaurants)
        return restaurants
        

        


app.run(port=5000, debug=True)


