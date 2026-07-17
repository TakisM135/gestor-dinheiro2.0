from utilidades import limpar, continuar, continuar_infinito
from banco_dados import Banco, Emails_bloqueado, Cliente, sessao
from datetime import datetime

# ---- Aussiliar ----

def tipo(valor: float):
    while True:
        tipo_escolha: str = continuar(print_continuar=f"---- ADICIONAR MOVIMENTO ----\nDigite um valor: {float(valor)}", pergunta="Digite o Tipo ['Gasto' ou 'Reccebido']: ", mostrar=True)
        if tipo_escolha.strip().title() not in ['Gasto', 'Recebido']:
            continuar_infinito("---- NÃO ESTA NAS OPÇÕES ----\n")
            continue
        return tipo_escolha
    
def continuacao():
    while True:
        limpar()
        escolha: str = input("---- DESEJA CONTINUAR ----\n\n[Y/N]: ").strip().upper()
        if escolha not in ["Y", "N"]:
            continue
        return escolha
   
# ---- Principal ----

def menu(utilizador):
    while True:
        try:
            escolha: int = int(continuar(print_continuar="---- MENU ----", pergunta="1. Adicionar um movimento\n2. Ver todos os movimentos\n3. Terminar sessão\nEscolha: ", mostrar=True))
        except ValueError:
            continue
        if escolha not in [1, 2, 3, 4]:
            continue

        if escolha == 1:
            while True:
                try:
                    valor_escolha: float = float(continuar(print_continuar="---- ADICIONAR MOVIMENTO ----", pergunta="Digite um valor: ", mostrar=True))
                except ValueError:
                    continue

                tipo_escolha: str = tipo(valor=valor_escolha)
                categoria_escolha: str = input("Digite a Categoria: ").strip().title()
                descricao_escolha: str = input("Digite a Descrição: ").strip().title()
        
                conti: str = continuacao()
                if conti == "N":
                    return
            
                p = Cliente(id_conta=utilizador.id, valor=valor_escolha, tipo=tipo_escolha, categoria=categoria_escolha, descricao=descricao_escolha, data=datetime.today())
                sessao.add(p)
                sessao.commit()
                continuar_infinito("---- MOVIMENTO ADICIONADO COM SUCESSO ----\n")
                return
            
        elif escolha == 2:
            limpar()
            cliente = sessao.query(Cliente).filter_by(id_conta=utilizador.id).all()
            if not cliente:
                continuar_infinito("---- NENHUMA COMPRA ASSOCIADA NA SUA CONTA ----\n")
                continue
            while True:
                limpar()
                numero: int = 0
                for compra in cliente:
                    numero += 1
                    formato: str = str(compra.data)
                    print(f"---- COMPRA {numero} ----\nValor: {compra.valor}\nTipo: {compra.tipo}\nCategoria: {compra.categoria}\nDescrição: {compra.descricao}\nData: {formato[0:10]}\n")

                continuar_escolha: str = continuar_infinito(frase="---- DESEJA CONTINUAR ----\n", limpar=False, infinito=False)
                if continuar_escolha == "y" or continuar_escolha == "Y":
                    return
                continue
        elif escolha == 3:
            return True
        

     

        
        