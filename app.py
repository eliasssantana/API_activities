from flask import Flask, json,request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from werkzeug.wrappers import response
from models import People, Activities, Users

auth = HTTPBasicAuth() # crio um objeto do método verificador
app = Flask(__name__) # crio uma instância da classe Flask 
api = Api(app) # aqui crio uma API da intância flask

# dicionário de usuário e senha
# USERS = {
#     "Elias": "2077",
#     "John": "9873"
# }

# função verficadora; onde irei validar o usuário e senha
@auth.verify_password # anotação que informa que a função verifica a senha.
def verification(username, password):
    if not (username, password):
        return False
    return Users.query.filter_by(username=username, password=password)

class Person(Resource):
    @auth.login_required # anotação que informa que o login é requerido.
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
        try:
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
        except AttributeError:
            response = {
                "status":"erro",
                "message": "person not found"
            }
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
    @auth.login_required
    def get(self):
        pessoas = People.query.all()
        response = [{"id":i.id,"name":i.name,"age":i.age} for i in pessoas]
        return response
    
    def post(self):
        data = request.json #isso equivale à json.loads(request.data).
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
        response = [{"id": i.id,"name": i.name,"person":i.person.name,"status": i.status} for i in activities]
        return response
    def post(self):
        data = request.json
        person = People.query.filter_by(name=data['person']).first()
        activity = Activities(name=data['name'], person = person, status = data['status'])
        activity.save()
        response = {
            'pessoa': activity.person.name,
            'name': activity.name,
            'id': activity.id,
            'status': activity.status
        }
        return response

class Person_Activities(Resource):
    def get(self,name):
        try:
            person = People.query.filter_by(name=name).first()
            activity = Activities.query.filter_by(person=person).first()
            response = {
                "person": activity.person.name,
                "activities": activity.name
            }
        except AttributeError:
            response = {
                "status":"erro",
                "message": "record not found."
            }
        return response

class Activities_status(Resource):
    def get(self,id):
        activity = Activities.query.filter_by(id=id).first()
        response = {
            "activities": activity.name
        }
        return response



api.add_resource(Person,"/person/<string:name>")
api.add_resource(PeopleList,"/person")
api.add_resource(ActivitiesList,"/activities/")
api.add_resource(Person_Activities,"/activities/<string:name>")
api.add_resource(Activities_status,"/activity/<int:id>")

if __name__=="__main__":
    app.run(debug=True)