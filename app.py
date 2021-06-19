from flask import Flask, json,request
from flask_restful import Resource, Api
from werkzeug.wrappers import response
from models import People, Activities

app = Flask(__name__)
api = Api(app)

class Person(Resource):
    def get(self,name):
        person = People.query.filter_by(name=name).first()
        try:
            response = {
                "name": person.name,
                "age": person.age,
                "id": person.id
            }
        except AttributeError:
            response = {
                'status':"ERRO",
                'message':"Person not found."
            }
        return response
    
    def put(self,name):
        person = People.query.filter_by(name=name).first()
        dados = request.json
        print("to aqui")
        if "name" in dados:
            person.name = dados["name"]
        if "age" in dados:
            person.age = dados["age"]
        response = {
            "name" : person.name,
            "age": person.age
        }
        person.save()
        return response

    def delete(self, name):
        try:
            person = People.query.filter_by(name=name).first()
            message = f"{person} deleted successfully"
            person.delete()
            response = {'status':'success','message': message}
        except AttributeError:
            message = f"{name} not found"
            response = {
                "status":"erro",
                "message": message
            }
        return response

class PeopleList(Resource):
    def get(self):
        pessoas = People.query.all()
        response = [{"id":i.id,"name":i.name,"age":i.age} for i in pessoas]
        return response
    
    def post(self):
        data = request.json #isso equivale à json.load(request.data).
        person = People(name=data['name'],age=data['age'],id = data['id'])
        person.save()
        response = {
            "name": person.name,
            "age": person.age,
            "id": person.id
        }
        return response

class ActivitiesList(Resource):
    def get(self):
        activities = Activities.query.all()
        response = [{"id": i.id,"name": i.name,"person":i.person.name}for i in activities]
        return response
    def post(self):
        data = request.json
        person = People.query.filter_by(name=data['person']).first()
        activity = Activities(name=data['name'], person = person)
        activity.save()
        response = {
            'pessoa': activity.person.name,
            'name': activity.name,
            'id': activity.id
        }
        return response
api.add_resource(Person,"/person/<string:name>")
api.add_resource(PeopleList,"/person")
api.add_resource(ActivitiesList,"/activities")

if __name__=="__main__":
    app.run(debug=True)