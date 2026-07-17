from utilidades import limpar, continuar, continuar_infinito
from banco_dados import Banco, Emails_bloqueado, sessao
from sqlalchemy import select
from datetime import datetime
import time

# ---- Aussiliar ----
    
def verificar(email_cliente: str):
    email_procura = sessao.execute(select(Banco).where(Banco.email == email_cliente)).scalar_one_or_none()
    email_procura_bloqueado = sessao.execute(select(Emails_bloqueado).where(Emails_bloqueado.email == email_cliente)).scalar_one_or_none()
    if email_procura is not None:
        continuar_infinito(frase="---- EMAIL JÁ ESTA SENDO UTILIZADO ----\n")
        return True
    if email_procura_bloqueado is not None:
        continuar_infinito(frase="---- EMAIL ESTÁ BLOQUEADO ----\n")
        return True

def idade_insufeciente(email_cliente: str, idade_cliente: int):
    email_procura = sessao.execute(select(Emails_bloqueado).where(Emails_bloqueado.email == email_cliente)).scalar_one_or_none()
    if email_procura is None and idade_cliente >= 18 and idade_cliente < 100:
        return False
    
    if idade_cliente > 100 and idade_cliente < 1000:
        p = Emails_bloqueado(email=email_cliente, idade=idade_cliente, ano=datetime.now().year - idade_cliente)
        sessao.add(p)
        sessao.commit()
        continuar_infinito(frase=f"---- TENS MUITA IDADE (So podias criar conta com este email em: ({p.ano}) ----\n")
        return
    elif idade_cliente >= 1000:
        return 1
    
    if email_procura is None:
        p = Emails_bloqueado(email=email_cliente, idade=idade_cliente, ano=(18 - idade_cliente) + datetime.now().year)
        sessao.add(p)
        sessao.commit()
        continuar_infinito(frase=f"---- NÃO TENS IDADE SUFECIENTE (So podes criar conta com este email em: ({p.ano}) ----\n")
    return True

def pedir_idade(nome: str, email: str):
    while True:
        try:
            resposta: int = int(input("Digite sua idade: "))
        except ValueError:
            continuar(print_continuar="---- SUA IDADE NÃO É UM NUMERO ----\n", pergunta="", mostrar=True, mostrar_pergunta=False)
            continue
        if resposta < 0:
            continuar(print_continuar="---- SUA IDADE NÃO PODE SER MENOR QUE ZERO ----\n", pergunta="", mostrar=True, mostrar_pergunta=False)
            continue
        menor_idade: bool = idade_insufeciente(email_cliente=email, idade_cliente=resposta)
        if menor_idade:
            return 1
        continuar(print_continuar=f"---- CRIAR CONTA ----\nDigite o seu nome: {nome[0]}\nDigite seu email: {email}\nDigite sua idade: {resposta}", pergunta="", mostrar=True, mostrar_pergunta=False)
        return resposta
    
def continuar_iniciar_sessao():
    while True:
        try:
            escolha: int = int(continuar(print_continuar="---- EMAIL OU SENHA INCORRETO ----", pergunta="1. Tentar novamente\n2. Criar conta\nEscolha: ", mostrar=True))
        except ValueError:
            continue
        if escolha not in [1, 2]:
            continue
        return escolha


# ---- Principal ----

def menu_inicial():
    while True:
        try:
            escolha_inicial: int = int(continuar(print_continuar="---- MENU INICIAL ----", pergunta="1. Criar conta\n2. Iniciar sessão\n3. Sair\nEscolha: ", mostrar=True))
        except ValueError:
            continue
        if escolha_inicial not in [1, 2, 3]:
            continue

        if escolha_inicial == 1:
            while True:
                nome_conta: str = continuar(print_continuar="---- CRIAR CONTA ----", pergunta="Digite o seu nome: ", mostrar=True).title().split()
                limpar()
                print(f"---- CRIAR CONTA ----\nDigite o seu nome: {nome_conta[0]}")
                email_conta: str = input("Digite seu email: ").strip()

                if verificar(email_cliente=email_conta):
                    return "", False
            
                idade_conta: int = pedir_idade(nome=nome_conta, email=email_conta)
                if idade_conta == 1:
                    continuar(print_continuar="---- NÃO TENS IDADE SUFECIENTE ----\n", pergunta="", mostrar=True, mostrar_pergunta=False)
                    continue

                senha_conta: str = input("Digite sua senha: ").strip()

                p = Banco(nome=nome_conta[0], email=email_conta, idade=idade_conta, senha=senha_conta)
                sessao.add(p)
                sessao.commit() 
                continuar_infinito(frase="---- CONTA CRIADA COM SUCESSO ----\n")
                procura = sessao.execute(select(Banco).where(Banco.email==email_conta, Banco.senha==senha_conta)).scalar_one_or_none()
                return procura, True
            
        elif escolha_inicial == 2:
            while True:
                email_conta: str = continuar(print_continuar="---- INICIAR SESSÃO ----", pergunta="Digite seu email: ", mostrar=True).strip()
                senha_conta: str = input("Digite sua senha: ").strip()

                procura = sessao.execute(select(Banco).where(Banco.email==email_conta, Banco.senha==senha_conta)).scalar_one_or_none()
            
                if procura is None:
                    resultado: int = continuar_iniciar_sessao()
                    if resultado == 1:
                        continue
                    else:
                        break
                else:
                    sessao_inicial: bool = True
                    return procura, sessao_inicial
                
        elif escolha_inicial == 3:
            continuar(print_continuar="\n---------- ADEUS ----------\n", pergunta="", mostrar=True, mostrar_pergunta=False)
            return escolha_inicial, False
        else:
            continuar(print_continuar="\n---- ESCOLHA ÍNDESPONIVEL ----\n", pergunta="Continuar [Y]: ".upper(), mostrar=True)
            continue
        continue
