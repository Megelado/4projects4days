from models import Conta, engine, Bancos, Status, Historico, Tipos
#Importa do arquivo models.py a conexão com o banco a engine, o nome do banco Conta, e bancos
from sqlmodel import Session, select
#Do módulo sqlmodel eu importo Session, select
from datetime import date, timedelta

#Define a função criar_conta, que recebe um objeto do tipo Conta como parâmetro
def criar_conta(conta: Conta):
    #Abre a sessão com o banco de dadss
    with Session(engine) as session:
        #Cria uma consulta para ver se já existe uma conta com o mesmo banco, verifica lá na tabela
        statement = select(Conta).where(Conta.banco==conta.banco)
        #Executa a consulta e pega todos os resultados encontrados
        results = session.exec(statement).all()
        
        #Se já existir uma conta nesse banco, imprime uma mensagem e interrompe a função
        if results:
            print('Já existe uma conta nesse banco!')
            return
            #Sai da função sem criar uma nova conta
        
        #Senão adiciona uma nova conta no banco de dados
        session.add(conta)
        #Confirma/salva no banco de dados
        session.commit()
        #Retorna o objeto conta criado
        return conta

#Define a função listar_contas
def listar_contas():
    #Abre uma conexão com o baco de dados
    with Session(engine) as session:
        #Seleciona todas as contas no banco de dados
        statement = select(Conta)
        #Executa a consulta e pega todos os resultados
        results = session.exec(statement).all()
    #Retorna esses resultados
    return results


def desativar_conta(id):
    #Abre uma conexão com o baco de dados
    with Session(engine) as session:
        #Seleciona a conta com o id selecionado
        statement = select(Conta).where(Conta.id==id)
        #Executa a consulta e pega o primeiro resultado, pois id é único pois é chave primária
        conta = session.exec(statement).first()
        #Se a conta que deve ser desativada tiver dinheiro dará um ValueError
        if conta.valor > 0:
            raise ValueError('Essa conta ainda possui saldo.')
        #Caso não tenha dinheiro na conta ela será desativada
        conta.status = Status.INATIVO
        #Agora eu confirmo/salvo essas alterações
        session.commit()


#Definimos função tranferi_saldo(o id da conta que o dinheiro será tranferido, o id da conta que receberá a transferência, o valor que será tranferido)
def tranferir_saldo(id_conta_saida, id_conta_entrada, valor):
    #Conexão com o banco
    with Session(engine) as session:
        #Faço uma consulta para pegar o id da conta que o dinheiro será tranferido
        statement = select(Conta).where(Conta.id==id_conta_saida)
        #Pego o primeiro id
        conta_saida = session.exec(statement).first()
        #Se o dinheiro na conta for menor que o valor a ser tranferido a tranferência será interrompida
        if conta_saida.valor < valor:
            raise ValueError('Saldo insuficiente!')
        #Faço uma consulta para pegar o id da conta que receberá a transferência
        statement = select(Conta).where(Conta.id==id_conta_entrada)
        #Pego o primeiro id
        conta_entrada = session.exec(statement).first()

        #O dinheiro da tranferência será diminuido no saldo da conta de saída
        conta_saida.valor -= valor
        #O dinheiro da tranferência será somado ao saldo da conta de entrada
        conta_entrada.valor += valor
        #Agora eu confirmo/salvo essas alterações
        session.commit()


#Definimos essa função para  ver o historico de tranferencias da conta
def movimentar_dinheiro(historico: Historico):
    #Conexão com o banco
    with Session(engine) as session:
        #Pegar o id da conta que fez as transferências
        statement = select(Conta).where(Conta.id==historico.conta_id)
        #Pegar o primeiro
        conta = session.exec(statement).first()
        #TO DO: VVALIDAR SE A CONTA ESTÁ ATIVA

        #Se historico for de entrada
        if historico.tipo == Tipos.ENTRADA:
            #A conta receberá o valor que estiver no historio
            conta.valor += historico.valor
        #senão, asume-se que é saida
        else:
            #Antes de ser realizada a saida é verificado se há saldo suficiente na conta
            if conta.valor < historico.valor:
                #Se não houver o suficente acontece um ValueError
                raise ValueError("Saldo insuficiente!")
            #Senão, ou seja se houver o suficiente, diminui esse valor da conta
            conta.valor -= historico.valor

        #Adiciona o historico á sessão do banco
        session.add(historico)
        #Confirma/salva essa transação no banco
        session.commit()
        #Retorna o historico após ser salvo no banco
        return historico


#Definimos essa função para somar o saldo de todas as contas
def total_contas():
    #Conexão ao servidor
    with Session(engine) as session:
        #Faz uma cosulta de todas as contas
        statement = select(Conta)
        #Pega todos esses dados
        contas = session.exec(statement).all()
    
    #Inicializa o contador em 0
    total = 0
    #Para cada conta em contas
    for conta in contas:
        #Total receberá a soma do saldo de todas as contas
        total += conta.valor

    #Retorna esse total em float, ou seja com centavos
    return float(total)


#Definimos essa função para buscar o histórico entre as datas
def buscar_historico_entre_datas(data_inicio: date, data_fim: date):
    #Conexão com o banco de dados
    with Session(engine) as session:
        #Consultar no historico por data ser maior ou igual a data_inicio, e ser menor ou igual a data_fim
        statement = select(Historico).where(
            Historico.data >= data_inicio,
            Historico.data <= data_fim
        )
        #Pego esses dados
        resultados = session.exec(statement).all()
        #Retorno eles
        return resultados


#Definimos uma função que criará um gráfico por conta
def criar_grafico_por_conta():
    #Fazer a conexão com o sbanco de dados
    with Session(engine) as session:
        #Fazer uma consultaapenas com contas ativas
        statement = select(Conta).where(Conta.status==Status.ATIVO)
        #Pegar todos os resultados dessa consulta
        contas = session.exec(statement).all()
        #i será cada objeto na lista, banco.value é ao qual a conta está se referindo, tudo i=na lista contas
        bancos = [i.banco.value for i in contas]
        #total recebe os valores de cada objeto na listas como i.value para cada i na lista contas
        total = [i.valor for i in contas]
        #importando a biblioteca matplotlib.pyplot como plt
        import matplotlib.pyplot as plt
        #são o eixo x e o eixo y, x são os bancos, e y os valores correspondentes
        plt.bar(bancos, total)
        #mostra
        plt.show()

