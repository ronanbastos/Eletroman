import sqlite3

# Nome do banco de dados
database_name = "conversas.db"

# Conexão com o banco de dados
conn = sqlite3.connect(database_name)

cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS frases (id INTEGER PRIMARY KEY AUTOINCREMENT, frase TEXT)")

with open("falas.txt", 'r') as f:
    data = f.read()

    frases = data.split('\n')
    print(frases)  
    for frase in frases:
        cursor.execute("INSERT INTO frases (frase) VALUES (?)", (frase.strip(),))
          
    conn.commit()
    conn.close()
    print("insert completo com sucesso!")
