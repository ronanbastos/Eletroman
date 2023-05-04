import time
import math
import difflib
import re
import collections
import itertools
import string
from collections import ChainMap
from chatbotGati import *
       


palavras_importantes = ['eletrônica', 'circuito', 'componente', 'resistor','Arduino', 'capacitor', 'diodo', 'transistor', 'transformador', 'disjuntor', 'relé', 'corrente', 'tensão', 'energia', 'campo elétrico', 'sinal elétrico', 'oscilação', 'amplificação', 'retificação']

mensagens = {
    
    "1": f"""
         Potência elétrica é a taxa na qual a energia
         elétrica é transferida em um circuito.
         Eletrônica é uma área da física que estuda o
         controle da corrente elétrica em circuitos,
         componentes e sistemas eletrônicos.\n""",
    "2": "Corrente elétrica é o fluxo de elétrons através de um condutor. \n",
    "3": "Resistência elétrica é a oposição que um material oferece à passagem da corrente elétrica.\n",
    "4": "Tensão elétrica é a diferença de potencial elétrico entre dois pontos de um circuito.\n",
    "5": "Capacitores são componentes eletrônicos que armazenam energia elétrica em um campo elétrico.\n",
    "6": "Indutores são componentes eletrônicos que armazenam energia elétrica em um campo magnético.\n",
    "7": "Diodos são componentes eletrônicos que permitem a passagem da corrente elétrica em um sentido apenas.\n",
    "8": "Transistores são componentes eletrônicos que permitem a amplificação e controle da corrente elétrica.\n",
    "9": "Circuitos integrados são componentes eletrônicos que contêm vários componentes eletrônicos em um único chip.\n"

}

correlacoes ={
    'Circuito': ['Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Componente': ['Circuito', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Resistor': ['Circuito', 'Componente', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Capacitor': ['Circuito', 'Componente', 'Resistor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Diodo': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Transistor': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Indutor': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Transformador': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Fonte de alimentação': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Amplificador': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Oscilador', 'Microcontrolador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Oscilador': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Microcontrolador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Microcontrolador': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Sensor': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Atuador': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Protocolo de comunicação': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Atuador', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Placa de circuito impresso': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Solda', 'Teste e medição'],
    'Amplificador': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Oscilador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Oscilador': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Microcontrolador': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Sensor': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Atuador': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Protocolo de comunicação': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Atuador', 'Placa de circuito impresso', 'Solda', 'Teste e medição'],
    'Placa de circuito impresso': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Solda', 'Teste e medição'],
    'Solda': ['Circuito', 'Componente', 'Resistor', 'Capacitor', 'Diodo', 'Transistor', 'Indutor', 'Transformador', 'Fonte de alimentação', 'Amplificador', 'Oscilador', 'Microcontrolador', 'Sensor', 'Atuador', 'Protocolo de comunicação', 'Placa de circuito impresso', 'Teste e medição']

}   
    
# Definir a tabela de cores dos resistores
cores = {"preto": 0, "marrom": 1, "vermelho": 2, "laranja": 3, "amarelo": 4,
         "verde": 5, "azul": 6, "violeta": 7, "cinza": 8, "branco": 9}

def get_related_terms(term):
    if term in correlacoes:
        print(correlacoes[term]," \n ")
    else:
        return []
    
            
def calcular_consumo():
    print("Digite o padrão de consulta de consumo desse jeito  led>10 - diodo>2 \n")
    consumo = {'led': 0.02, 'diodo': 0.1, 'resistor': 0.25, 'capacitor': 0.05, 'transistor': 0.2,"arduino": 0.3,'arduino_uno': 0.05, 'sensor_temperatura': 0.01, 'servo_motor': 0.3, 'modulo_bluetooth': 0.1, 'display_lcd': 0.1}

    entrada = input("Digite o consumo: ")
    elementos = entrada.split(" - ")
    consumo_total = 0

    for elemento in elementos:
        nome, valor = elemento.split(">")
        consumo_total += consumo.get(nome, 0) * float(valor)

    print("O consumo total do sistema é de {:.2f} watts.".format(consumo_total))

def classificar_frase(entrada, frases, palavras_importantes):
    melhor_frase = None
    melhor_similaridade = 0
    palavras_importantes = set(palavras_importantes) # agora é um conjunto
    
    for frase in frases:
        dist_lev = levenshtein_distance(entrada, frase)
        if dist_lev == 0:
            melhor_frase = frase
            break
        else:
            sim = similaridade_Map(entrada, [frase], palavras_importantes)
            score = 1/(dist_lev+1) * sim[1]
            if score > melhor_similaridade:
                melhor_frase = frase
                melhor_similaridade = score
    
    return melhor_frase


def verificar_voltagem():

    # Converte as voltagens para valores numéricos
    voltagem_desejada = float(input("Digite a voltagem desejada: "))
    voltagem_medida = float(input("Digite a voltagem medida: "))

    # Define uma tolerância de 5% para a voltagem medida
    tolerancia = 0.05

    # Calcula a diferença entre a voltagem desejada e a voltagem medida
    diferenca = abs(voltagem_desejada - voltagem_medida)
    print(f"A diferença atual: {diferenca}")
    
    # Verifica se a voltagem medida está dentro da tolerância
    if diferenca <= voltagem_desejada * tolerancia:
         print("A voltagem está dentro da tolerância permitida.")
    else:
         print("Atenção! A voltagem está fora da tolerância permitida.")


def calcular_tempo():
    capacidade = float(input("Digite a capacidade da bateria (em mAh): "))
    tensao = float(input("Digite a tensão da bateria (em volts): "))
    consumo_total = float(input("Digite o consumo total do sistema (em watts): "))
    tempo = capacidade / (consumo_total * tensao)
    print(f"""  A bateria durará aproximadamente {tempo:.2f} horas.
              É importante lembrar que esse cálculo é
              apenas uma estimativa e a  duração real da bateria
              pode variar dependendo de vários fatores,
              como a eficiência do sistema e as condições de uso.
              \n""")
def calcula_tensao_saida_regulador():
    """
    Calcula a tensão de saída de um regulador de tensão linear.
    vin: tensão de entrada em volts
    vout: tensão de saída desejada em volts
    iout: corrente de saída desejada em ampères
    r: resistência do resistor de saída em ohms
    vdropout: tensão de queda (dropout) do regulador em volts
    """
    vin = float(input("Digite o valor de Vin (V): "))
    vout = float(input("Digite o valor de Vout (V): "))
    iout = float(input("Digite o valor de Iout (A): "))
    dropout = float(input("Digite o valor de Dropout (V): "))
    
    # Realiza o cálculo
    vin_min = vout + dropout
    r1 = (vin - vin_min) / iout
    r2 = vout / iout
    p_dissipada = (vin - vout) * iout
    
    # Imprime os resultados
    print("Valor mínimo de Vin: {:.2f} V".format(vin_min))
    print("Valor do resistor R1: {:.2f} Ω".format(r1))
    print("Valor do resistor R2: {:.2f} Ω".format(r2))
    print("Potência dissipada no regulador: {:.2f} W".format(p_dissipada))
    
def capacitor_valor():
    
        valor_capacitor = float(input("Digite o valor do capacitor em microfarads: "))
        tensao_capacitor = float(input("Digite a tensão do capacitor em volts: "))
        constante_tempo = float(input("Digite o valor da constante: "))
        valor_resistor = constante_tempo / (0.693 * tensao_capacitor * math.log(2, 10) * valor_capacitor * 10**-6)
        print("O valor do resistor necessário é de", round(valor_resistor, 2), "ohms. \n")

        
def explicar_elemento(elemento):
   baixa_tensao = {
    "resistor": "O resistor é um componente que oferece resistência à passagem de corrente elétrica. Ele é utilizado em circuitos elétricos para limitar a corrente em um determinado ponto, dissipar energia térmica, ou para obter um determinado valor de tensão ou corrente.",
    "capacitor": "O capacitor é um componente que armazena energia elétrica em forma de campo elétrico. Ele é utilizado em circuitos elétricos para armazenar energia, filtrar sinais elétricos, ou para obter um determinado valor de tempo em um circuito.",
    "diodo": "O diodo é um componente que permite a passagem de corrente elétrica em apenas um sentido. Ele é utilizado em circuitos elétricos para retificar sinais elétricos, gerar pulsos, ou para limitar a corrente em um determinado ponto.",
    "transistor": "O transistor é um componente que amplifica ou comuta sinais elétricos. Ele é utilizado em circuitos eletrônicos para amplificar sinais, gerar oscilações, ou para controlar a corrente em um determinado ponto.",
    "led": "O LED (Light Emitting Diode) é um diodo emissor de luz. Ele é utilizado em circuitos eletrônicos para indicar o estado de um dispositivo, como por exemplo, se está ligado ou desligado.",
    "sensor de temperatura": "O sensor de temperatura é um componente que mede a temperatura de um ambiente ou de um dispositivo. Ele é utilizado em circuitos eletrônicos para controlar o funcionamento de dispositivos que dependem da temperatura, como por exemplo, um ar condicionado.",
    "servo motor": "O servo motor é um motor que possui um sistema de controle de posição e velocidade. Ele é utilizado em circuitos eletrônicos para controlar o movimento de dispositivos, como por exemplo, um robô.",
    "módulo Bluetooth": "O módulo Bluetooth é um componente que permite a comunicação sem fio entre dispositivos. Ele é utilizado em circuitos eletrônicos para transmitir dados entre dispositivos, como por exemplo, um smartphone e um microcontrolador.",
    "display LCD": "O display LCD (Liquid Crystal Display) é um componente que exibe informações em forma de caracteres ou gráficos. Ele é utilizado em circuitos eletrônicos para exibir informações em dispositivos como relógios, computadores, eletrodomésticos, entre outros."
    }
   alta_tensao = {"transformador": "O transformador é um componente que converte a tensão elétrica de um circuito para outra tensão elétrica, com maior ou menor valor. Ele é utilizado em circuitos elétricos para adaptar a tensão elétrica de um dispositivo, ou para isolar eletricamente dois circuitos.",
                    "disjuntor": "O disjuntor é um componente que desliga automaticamente um circuito elétrico em caso de sobrecarga ou curto-circuito. Ele é utilizado em circuitos elétricos para garantir a segurança das pessoas e dos equipamentos.",
                    "relé": "O relé é um componente que permite a abertura ou fechamento de um circuito elétrico, de forma remota ou automática. Ele é utilizado em circuitos elétricos para acionar dispositivos à distância, ou para automatizar processos industriais."}
   if elemento in baixa_tensao:
        print("Explicando sobre o", elemento, "em baixa tensão:\n")
        print(baixa_tensao[elemento])
   elif elemento in alta_tensao:
        print("Explicando sobre o", elemento, "em alta tensão:\n")
        print(alta_tensao[elemento])
   else:
        print("Elemento não reconhecido.")

      
# Função para ler o valor do resistor
def ler_resistor():
    print("Insira as cores das três faixas do resistor:")
    print(cores," \n")
    cor1 = input("Primeira faixa: ").lower()
    cor2 = input("Segunda faixa: ").lower()
    cor3 = input("Terceira faixa: ").lower()
    
    # Calcular o valor do resistor com base nas cores
    valor = (cores[cor1]*10 + cores[cor2]) * (10**cores[cor3])
    print("O valor do resistor é: {} ohms".format(valor))
    print("\n ")

print("Bem-vindo ao tutorial de Eletrônica!")
print("Escolha um tópico para saber mais:\n")

# Prompt interativo
while True:

    
    print(f"""
   0: Sair
   1: O que é eletrônica?
   2: O que é corrente elétrica?
   3: O que é resistência elétrica?
   4: O que é tensão elétrica?
   5: O que são capacitores?
   6: O que são indutores?
   7: O que são diodos?
   8: O que são transistores?
   9: O que são circuitos integrados?
   10: Verificar três faixas do resistor
   11: Verificar valor do resistor
   12: Verificar consumo enegia
   13: Verificar consumo bateria
   14: Verificar voltagem desejada
   15: Verificar relação de componentes
   16: Verificar tensao saida
   chatbot: Falar sobre eletronica \n""")
   

    op = input("Escolha uma opção: ")

    if op == "chatbot":
        print("Função chatbot True!\n")
        conversa()

    elif op in mensagens:
        print(mensagens[op])     

    elif op == "10":
         ler_resistor()
         time.sleep(5)     
    elif op == "11":
         capacitor_valor()
         time.sleep(5)
    elif op == "12":
         calcular_consumo()
    elif op == "14":
         verificar_voltagem()
    elif op == "13":
         calcular_tempo()
         time.sleep(5)     
    elif op =="15":
        term = input("Qual correlação entre os termos seja pesquisar: ")
        get_related_terms(term)
    elif op == "16":
         calcula_tensao_saida_regulador()
         time.sleep(5)        
    elif op == "0" or op =="sair":
        print("Até mais!\n")
        break
    else:
        print("Opção inválida. Tente novamente.\n")
   
 
