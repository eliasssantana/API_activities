# importo todos os módulos necessários para criação de um banco de dados.
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

# crio meu banco de dados
engine = create_engine("sqlite:///activities.db")
# crio uma nova sessão
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine)) 
# declaro a base do meu banco de dados
Base = declarative_base()
Base.query = db_session.query_property()
#crio uma classe chamada People, a qual herda do Base
class People(Base):
    # crio uma tabela chamada 'people'
    __tablename__ = 'people'
    # crio variáveis que comportam colunas
    id = Column(Integer, primary_key=True) # essa é uma chave primária
    name = Column(String(40), index=True)
    age = Column(Integer)

    # isso é o que aparece quando mando printar uma instância da minha classe
    def __repr__(self):
        return f"<Person {self.name}>"
    # aqui eu crio um método para guardar minhas inserções e comitalas,ou seja,salvá-las na sessão do meu banco de dados 
    def save(self):
        db_session.add(self)
        db_session.commit()
    # aqui eu acesso minha sessão e deleto o arquivo desejado e finalizo com um commit.
    def delete(self):
        db_session.delete(self)
        db_session.commit()
# nova classe criada como herança de Base
class Activities(Base):
    # novamente, crio uma tabela com o nome activities
    __tablename__ = "activities"
    # crio suas colunas
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    person_id = Column(Integer, ForeignKey("people.id"))# aqui eu referecio essa coluna à da classe "People", através de uma chave estrangeira.
    person = relationship("People")# aqui explicito a relação da tabela 'People' com  a 'Activities, atribuindo como argumento o nome da classe.
    def __repr__(self):
            return f"<Activities {self.name}>"
    # aqui eu crio um método para guardar minhas inserções e comitalas,ou seja,salvá-las na sessão do meu banco de dados 
    def save(self):
        db_session.add(self)
        db_session.commit()
    # aqui eu acesso minha sessão e deleto o arquivo desejado e finalizo com um commit.
    def delete(self):
        db_session.delete(self)
        db_session.commit()

# crio uma função geradora do meu aquivo .db, ou seja, meu banco de dados.
def init_db():
    Base.metadata.create_all(bind=engine)
# crio uma condição, a qual só executará seu conteúdo se estiver no arquivo raiz.
if __name__ == "__main__":
    init_db()