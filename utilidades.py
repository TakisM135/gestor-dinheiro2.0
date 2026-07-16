import os

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def continuar(print_continuar: str, pergunta: str, apagar: bool =True, mostrar: bool =False, mostrar_pergunta: bool =True):
    if apagar:
        limpar()
    if mostrar:
        print(print_continuar)
    if mostrar_pergunta:
        resposta = input(f"{pergunta}")
        return resposta
    
def continuar_infinito(frase: str, limpar: bool = True, infinito: bool = True):
    if infinito:
        while True:
            if limpar is False:
                p: str = continuar(print_continuar=frase, pergunta="Continuar [Y]: ", mostrar=True, apagar=False)
            else:
                p: str = continuar(print_continuar=frase, pergunta="Continuar [Y]: ", mostrar=True)
            if p.upper() != "Y":
                continue
            return 
    if limpar is False:
        p: str = continuar(print_continuar=frase, pergunta="Continuar [Y]: ", mostrar=True, apagar=False)
    else:
        p: str = continuar(print_continuar=frase, pergunta="Continuar [Y]: ", mostrar=True).upper()
    if p != "Y":
        return p
    
    