from sqlmodel import SQLModel, Field, create_engine, Relationship
from enum import Enum
from datetime import date

#Definindo os bancos que poderá escolher
class Bancos(Enum):
    #Basicamente os bancos nesse projeto serão esses três
    NUBANK = 'Nubank'
    SANTANDER = 'Santander'
    INTER = 'Inter'

#Defindo os status que pode ter:
class Status(Enum):
    #Por enquanto só haverá esses dois status
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'

class Tipos(Enum):
    ENTRADA = 'Entrada'
    SAIDA = 'Saida'

#Vamos criar uma tabela com os campos abaixo:
class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    #o id será uma chave primária
    valor: float
    #valor será float
    banco: Bancos = Field(default=Bancos.NUBANK)
    #banco terá Bancos que se vier vazio receberá por padrão NUBANK
    status: Status = Field(default=Status.ATIVO)
    #status terá Status que se vier vazio receberá por padrão ATIVO

#Vamos criar uma tabela com os campos abaixo:
class Historico(SQLModel, table=True):
    id: int = Field(primary_key=True)
    #o id será uma chave primária
    conta_id: int = Field(foreign_key="conta.id")
    #Aramazena o id da conta que a transferência foi feita
    conta: Conta = Relationship()
    #Aqui etá sendo feita uma relação entre as tabelas
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    #Se tipo não for informado por padrão foi Entrada
    valor: float
    #Valor será float
    data: date
    #Dat será date

#Váriavel com o nome do arquivo sqlte
sqlite_file_name = 'database.db'
#Váriavel com o urll que será usado para mandar as tabelas
sqlite_url = f"sqlite:///{sqlite_file_name}"

#Variável responsável pela conexão com o banco de dados
engine = create_engine(sqlite_url, echo=False)

#Stenta criar a tabela apenas se esse arquivo for chamado diretamente nãocomo módulo
if __name__ == "__main__":
    # SQLModel.metadata contém as definições da tabela, enquanto que .create_all(engine) usa a variável engine que é a conexão com o banco para criar as tabelas
    SQLModel.metadata.create_all(engine)
