# Aqui importo o módulo models e sua classe 'People' para realizar manipulações na mesma.
from models import People
# Aqui crio uma função que insere novos registros na minha tabela 'activities'.
def insert_people():
    person = People(name="Ana", age=18)
    # aqui utilizo um método definido na minha classe 'People' que adiciona um registro e salva(commit).
    person.save()
    print(person)

# Aqui crio uma função que realiza consultas no meu banco de dados.
def query():
    person = People.query.all()
    print(person)

# Aqui crio uma função que realiza alterações nos registros no meu banco de dados.
def change_person():
    person = People.query.filter_by(name="Elias").first()
    person.age = 21
    person.save()

# Aqui crio uma função que deleta registros no meu banco de dados.
def delete_person(nome):
    person = People.query.filter_by(name=f"{nome}").first()
    # aqui utilizo o método 'delete()' que deleta meu registra na sessão atual e salva(commit).
    person.delete()

# Aqui crio a condição que possibilitará executar meu arquivo apenas no código fonte.
if __name__ == "__main__":
    #insert_people()
    delete_person("Elias")
    query()