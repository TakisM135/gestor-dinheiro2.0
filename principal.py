from autenticacao import menu_inicial
from movimentos import menu

sessao_inicial: bool = False

while True:
    if sessao_inicial is False:
        utilizador, sessao_inicial = menu_inicial()
        if utilizador == 3:
            break
        else:
            continue
    r = menu(utilizador)
    if r:
        sessao_inicial: bool = False
    
