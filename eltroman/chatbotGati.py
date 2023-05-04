import sqlite3
import random
import datetime
import re
from collections import ChainMap
import math
import time
import numpy as np
import difflib
import wikipedia
from eletroman import *




# Configuração do chatbot
bot_name = "Gati"
database_name = "conversas.db"

# Inicialização do banco de dados
conn = sqlite3.connect(database_name)
cur = conn.cursor()

# Verifica se a tabela "conversas" existe e cria caso necessário
cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='conversas'")
if cur.fetchone()[0] == 0:
    cur.execute("CREATE TABLE conversas (entrada text, resposta text, sentimento text,status text)")
    conn.commit()


#Array com frase de aprendizado
aprendi=["obrigada,agora eu aprendi","obrigada agora eu entendi","agora tudo faz sentido,obrigado por me ajudar","obrigado por me ensinar","anotado sua resposta,obrigada por me ensinar"]
pergunta=["O que devo falar nessa situação","Nessa situação o que devo dizer?","eu não entendi,poder me ajudar com melhor responta,seja direto e objetivo","Não consegui entender,pode me ensiar,melhor resposta!","Eita não entendi,o que deveria falar?"]
palavras_positivas = ["amor", "feliz", "bom","eu gosto","eu gostei muito","estou feliz"]
palavras_negativas = ["ódio", "triste", "ruim","Não quero","eu não gostei","estou com raiva","não gostei da sua atitude"]
palavras_importantes = set(["oi", "olá", "tchau", "adeus", "sim", "não", "obrigado",'wifi','placa','roteador','eletrônica', 'circuito', 'componente', 'resistor','Arduino', 'capacitor', 'diodo', 'transistor', 'transformador', 'disjuntor', 'relé', 'corrente', 'tensão', 'energia', 'campo elétrico', 'sinal elétrico', 'oscilação', 'amplificação', 'retificação',"obrigada", "por favor", "desculpe",'de', 'que', 'o', 'a', 'em', 'e', 'um', 'para', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'ao', 'ele', 'das', 'ou', 'sua', 'são', 'também', 'à', 'ser', 'pelo', 'pela', 'entre', 'pode', 'seu', 'nos', 'mesmo', 'foi', 'tem', 'só', 'sobre', 'todos', 'essa', 'este', 'muito', 'quando', 'está', 'sem', 'nosso', 'seus', 'você', 'já', 'há', 'essa', 'entre', 'era', 'havia', 'foram', 'mesma', 'nem', 'meu', 'aos', 'ela', 'nós', 'depois', 'onde', 'quem', 'suas', 'muitos', 'lhe', 'deles', 'elas', 'estão', 'temos', 'essa', 'eles', 'estava', 'esteve', 'estiveram', 'estamos', 'estiver', 'estivermos', 'houver', 'houvermos', 'houveram', 'houverei', 'houverá', 'houveremos', 'houverão', 'haja', 'hajamos', 'hajam', 'hei', 'hás', 'há', 'havemos', 'hão', 'houve', 'houvemos', 'houvera', 'houvéramos', 'haja', 'hajamos', 'hajam', 'houveria', 'houveríamos', 'houveriam', 'sou', 'somos', 'são', 'era', 'éramos', 'eram', 'fui', 'foi', 'fomos', 'foram', 'fora', 'foram', 'seja', 'sejamos', 'sejam', 'serei', 'será', 'seremos', 'serão', 'seria', 'seríamos', 'seriam', 'tenho', 'tem', 'temos', 'tém', 'tinha', 'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 'tiveram', 'tivera', 'tiveram', 'tenha', 'tenhamos', 'tenham', 'terei', 'terá', 'teremos', 'terão', 'teria', 'teríamos', 'teriam'])
ultima_reposta=""


# Verifica se o banco de dados está vazio e insere conversas padrão caso necessário
cur.execute("SELECT count(*) FROM conversas")
result = cur.fetchone()
if result[0] == 0:
    conversas = {
        "Olá": {
            "resposta": "Olá",
            "sentimento": "neutro",
            "status":"saudação"
        },
        "Qual é o seu nome?": {
            "resposta": f"Meu nome é {bot_name}, e eu sou um chatbot!",
            "sentimento": "neutro",
            "status":"pergunta,sobre mim"
        },
        "O que você pode fazer?": {
            "resposta": "Eu posso ajudá-lo a responder perguntas ou ter conversas casuais.",
            "sentimento": "duvida",
            "status":"pergunta,sobre mim"
        },
         "Quem criou você?": {
            "resposta": "Foi Programdor Ronan Bastos!.",
            "sentimento": "duvida",
            "status":"pergunta"
        },
    }
    for entrada, dados in conversas.items():
        cur.execute("INSERT INTO conversas (entrada, resposta, sentimento,status) VALUES (?, ?, ?,?)", (entrada, dados["resposta"], dados["sentimento"],dados["status"]))
    conn.commit()



def saudacao_horario():
    agora = datetime.datetime.now()
    hora = agora.hour

    if hora >= 6 and hora < 12:
        saudacao = "Bom dia!"
    elif hora >= 12 and hora < 18:
        saudacao = "Boa tarde!"
    else:
        saudacao = "Boa noite!"

    return saudacao
   
   

# Funções do chatbot
def tokenize(text):
    tokens = []
    current_token = ''
    for char in text:
        if char.isalnum():
            current_token += char
        else:
            if current_token:
                tokens.append(current_token)
                current_token = ''
    if current_token:
        tokens.append(current_token)
    return tokens

def extrair_palavras_chave(frase):
    return set(frase.lower().split())


def bag_of_words(documents):
    words_count = {}
    for document in documents:
        # Separar as palavras usando expressões regulares
        words = re.findall(r'\w+', document.lower())
        for word in words:
            # Incrementar a contagem de cada palavra
            if word in words_count:
                words_count[word] += 1
            else:
                words_count[word] = 1
    return words_count

def pesquisar_wikipedia(entrada):
         
    wikipedia.set_lang("pt")
    try:
        pag = wikipedia.page(entrada)
        print(pag.content)
    except wikipedia.exceptions.PageError:
        print("Nenhuma página encontrada para essa pesquisa.")
    except wikipedia.exceptions.DisambiguationError as e:
        print("Sua pesquisa pode se referir a uma das seguintes páginas: ")
        for option in e.options:
            print("- " + option)

def similaridade_Map(entrada, frases, palavras_importantes):
    palavras_chave_entrada = extrair_palavras_chave(entrada)
    peso_entrada = len(palavras_chave_entrada)
    resultados = []

    for frase in frases:
        palavras_chave_frase = extrair_palavras_chave(frase)
        pc1 = ChainMap(palavras_chave_frase, palavras_importantes)
        pc2 = ChainMap(palavras_chave_entrada, palavras_importantes)
        peso_x = len(palavras_chave_frase | palavras_importantes)
        peso_y = len(palavras_chave_entrada | palavras_importantes)
        peso_xy = len(pc1.maps[0] & pc2.maps[0] | palavras_importantes)

        similaridade = (peso_xy / (math.sqrt(peso_x) * math.sqrt(peso_y))) if peso_xy != 0 else 0

        resultados.append((frase, similaridade))

    return max(resultados, key=lambda x: x[1])[0]

def similaridade(frase1, frase2):
    pc1 = extrair_palavras_chave(frase1,frase2)
    pc2 = extrair_palavras_chave(frase2,frase1)
    peso_x = len(pc1.intersection(pc2)) * 2  # Multiplicando o peso de x por 2
    peso_y = len(pc1.union(pc2))
    score = peso_x + peso_y
    similar = score ** (peso_x * 2 + peso_y * 2)
    return similar**2

def levenshtein_distance(s, t):
    """Retorna a distância de Levenshtein entre as strings s e t"""
    m, n = len(s), len(t)
    if m < n:
        return levenshtein_distance(t, s)
    if n == 0:
        return m
    previous_row = range(n + 1)
    for i, c1 in enumerate(s):
        current_row = [i + 1]
        for j, c2 in enumerate(t):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[n]

def classificar_frase(entrada, frases):
    melhor_frase = None
    melhor_similaridade = 0
    for frase in frases:
        score = similaridade(entrada, frase)
        if score > melhor_similaridade:
            melhor_frase = frase
            melhor_similaridade = score
    return melhor_frase
def create_glossario(texto):
    # Dividir o texto em palavras
    palavras = texto.split()

    # Remover as stop words do texto
    stop_words = set(["a", "o", "e", "é", "de", "do", "da", "em", "para", "com", "que", "um", "uma"])
    palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stop_words]

    # Criar o glossário
    glossario = {}
    for palavra in palavras_sem_stopwords:
        if palavra in glossario:
            glossario[palavra] += 1
        else:
            glossario[palavra] = 1

    # Retornar o glossário ordenado por frequência decrescente
    return sorted(glossario.items(), key=lambda x: x[1], reverse=True)

def mostar_similar(word, word_list):
    """Retorna a palavra mais similar a 'word' em 'word_list' usando a distância de Levenshtein"""
    min_distance = float('inf')
    most_similar_word = None
    for w in word_list:
        distance = levenshtein_distance(word, w)
        if distance < min_distance:
            min_distance = distance
            most_similar_word = w

    if most_similar_word is None:
        return classificar_frase(word, word_list)
    else:   
        return most_similar_word

def determinar_sentimento(frase):
    polaridade = 0
    palavras = frase.lower().split()
    for palavra in palavras:
        if palavra in palavras_positivas:
            polaridade += 1
        elif palavra in palavras_negativas:
            polaridade -= 1
    if polaridade > 0:
        return "positivo"
    elif polaridade < 0:
        return "negativo"
    else:
        return "neutro"

def obter_resposta(entrada):
    sentimento = determinar_sentimento(entrada)
    cur.execute("SELECT resposta FROM conversas WHERE entrada = ? AND sentimento = ? ", (entrada, sentimento))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def buscar_frases(entrada, tabela="frases"):
    try:
        conn = sqlite3.connect("conversas.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT frase FROM {tabela} WHERE frase LIKE ?", (f"%{entrada}%",))
        result = cursor.fetchone()
        if result:
            return most_similar_word(entrada, buscar_respostas(result[0]))
        else:
            return None
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return [random.choice(["Desculpe, ocorreu um erro. Por favor tente novamente.", "Não consegui processar sua solicitação. Tente novamente mais tarde."])]

def obter_todas_frases(banco,tabela,linhas):
    conn = sqlite3.connect(banco)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tabela}")
    frases = [row[linhas] for row in cursor.fetchall()]
    conn.close()
    return frases

def buscar_respostas(pergunta):
  
    conn = sqlite3.connect('conversas.db')
    cur = conn.cursor()
    respostas = set()
    for resposta in cur.execute("SELECT resposta FROM conversas WHERE entrada LIKE ?", ('%' + pergunta + '%',)):
        respostas.add(resposta[0])
    conn.close()
    return list(respostas)
        
def adicionar_conversa(entrada, resposta):
    sentimento = determinar_sentimento(entrada)
    cur.execute("INSERT INTO conversas (entrada, resposta, sentimento) VALUES (?, ?, ?)", (entrada, resposta, sentimento))
    conn.commit()
def adicionar_number(entrada):
              
               
    sentimento = "calcular"
    operacoes = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b, "/": lambda a, b: a / b}
    for operador, funcao in operacoes.items():
        if operador in entrada:
            numeros = entrada.split(f"quanto é ")[-1].split(operador)
            n1, n2 = int(numeros[0]), int(numeros[1])
            resposta = funcao(n1, n2)
            print(f"{bot_name}: {resposta}")
            cur.execute("INSERT INTO conversas (entrada, resposta, sentimento) VALUES (?, ?, ?)", (entrada, resposta, sentimento))
            conn.commit()
            break


def cosine_similarity(input_str, phrases):
    # Criar matriz de frequência dos termos
    freq_matrix = np.zeros((len(phrases), len(input_str)), dtype=int)
    for i, phrase in enumerate(phrases):
        for j, term in enumerate(input_str):
            freq_matrix[i, j] = phrase.count(term)

    # Calcular o peso de cada termo em relação ao documento inteiro
    term_weight = np.zeros(len(input_str))
    for j, term in enumerate(input_str):
        term_count = np.count_nonzero(freq_matrix[:, j])
        term_weight[j] = np.log10(len(phrases) / term_count) if term_count > 0 else 0

    # Calcular o peso de cada frase em relação ao documento inteiro
    phrase_weight = np.zeros(len(phrases))
    for i in range(len(phrases)):
        phrase_weight[i] = np.sum(freq_matrix[i, :] * term_weight)

    # Calcular a similaridade de cada frase com o input_str
    input_weight = np.zeros(len(input_str))
    for j, term in enumerate(input_str):
        input_weight[j] = term_weight[j] * input_str.count(term)
    input_norm = np.linalg.norm(input_weight)
    similarity = np.zeros(len(phrases))
    for i in range(len(phrases)):
        phrase_norm = np.linalg.norm(freq_matrix[i, :] * term_weight)
        dot_product = np.dot(freq_matrix[i, :] * term_weight, input_weight)
        similarity[i] = dot_product / (phrase_norm * input_norm) if phrase_norm > 0 else 0

    # Retornar as frases ordenadas por ordem de similaridade
    return [phrases[i] for i in np.argsort(similarity)[::-1]]

def get_similarity_scores(input_string, possible_responses):
    similarity_scores = []
    for response in possible_responses:
        # Calcula a similaridade entre a string de entrada e cada possível resposta
        similarity = np.sum([1 for i in range(len(input_string)) if input_string[i] == response[i]])
        # Adiciona o score de similaridade na lista
        similarity_scores.append(similarity)
    
    # Ordena as respostas pela similaridade decrescente
    sorted_responses = [response for _, response in sorted(zip(similarity_scores, possible_responses), reverse=True)]
    # Calcula as probabilidades baseado na similaridade
    probabilities = [score/len(input_string) for score in similarity_scores]
    
    return sorted_responses, probabilities

def similar_phrases_with_subject(subject, phrases):
    # Extrair o sujeito da frase
    input_str = subject.split()
    input_str = [word for word in input_str if word.isalpha()]

    # Calcular a similaridade das frases com o input_str
    similar_phrases = cosine_similarity(input_str, phrases)

    # Filtrar as frases que têm o sujeito e criar um array com todas as frases similares
    all_similar_phrases = []
    for phrase in similar_phrases:
        if subject in phrase:
            all_similar_phrases.append(phrase)

    return all_similar_phrases

def check_previous_responses(response):
    """Verifica se a resposta já foi dada anteriormente pelo chatbot"""
    if response == ultima_reposta:
            return True
    return False

def chatbot_functions(text):
    tokens = tokenize(text)
    fraseSegundaria=obter_todas_frases(database_name, "frases", 1)
    documentos =fraseSegundaria
    similaridade = similaridade_Map(text, documentos, palavras_importantes)
    glossario = create_glossario(text)
    similar = mostar_similar('help', ['ajuda', 'assistência', 'socorro'])
    sentimento = determinar_sentimento(text)
    
    return tokens, similaridade, glossario, similar, sentimento                
# Loop principal do chatbot
fraseSegundaria=obter_todas_frases(database_name, "frases", 1)
print(saudacao_horario())
print(f"Bem-vindo ao {bot_name}! Digite 'sair' para encerrar o programa.")
def conversa():
    while True:
        try:
            entrada = input("Você: ")
            if entrada.lower() == "pesquisar na internet":
                entrada = input("O que você deseja pesquisar na Wikipedia:")
                resultado = pesquisar_wikipedia(entrada)
                print(resultado)
            if entrada.lower() == "sair":
                print(f"{bot_name}: Tchau, até mais!")
                break
            if entrada.lower() == "aprender agora":
                    print(f"{bot_name}: Ok! Me ensina uma frase?")
                    entrada = input("Você: ").strip()

                    if entrada == "":
                        print(f"{bot_name}: Desculpe, não entendi o que você disse. Tente novamente.")
                        continue # sai do loop principal do programa

                    nova_resposta = input(f"{bot_name}: Qual seria a melhor resposta para sua pergunta? ").strip()
                    
                    if nova_resposta == "":
                        print(f"{bot_name}: Desculpe, Tente novamente mais tarde.")
                        continue  # sai do loop principal do programa
                    if len(nova_resposta) == 0:
                        print(f"{bot_name}: Desculpe,Tente novamente mais tarde.")
                        continue  # sai do loop principal do programa

                    adicionar_conversa(entrada, nova_resposta)
                    print(f"{bot_name}: {random.choice(aprendi)}") 
                
            resposta = mostar_similar(entrada,buscar_respostas(entrada)) 
            
            if resposta is None:
                
                valor = chatbot_functions(entrada)
                #resposta_seg = similaridade_Map(entrada,fraseSegundaria,palavras_importantes)
                resposta_seg = valor[1]
         
                          
                if resposta_seg is not None and len(resposta_seg)>0:
                           
                           
                            print(f"{bot_name}: {resposta_seg}")
                           
                              
                else:
                            nova_resposta = input(f"{bot_name}: Desculpe, eu não entendi. Qual seria a melhor resposta para sua pergunta? ")
                        
                            if nova_resposta.strip() == "":
                                print(f"{bot_name}: {random.choice(fraseSegundaria)}")
                          
                                
                            else:
                                adicionar_conversa(entrada, nova_resposta)
                                print(f"{bot_name}: {random.choice(aprendi)}")
                           
                      
                    
            else:
                print(f"{bot_name}: {resposta}")
               
             
                
        except KeyboardInterrupt:
            print(f"\n{bot_name}: Tchau, até mais!")
            break

        except Exception as e:
            
            print(f"{bot_name}: Desculpe,Por favor tente novamente.\n")
            print(f"Aqui esta tipo de erro : \n {e} \n")



