import sqlite3
import tkinter as tk
from tkinter import messagebox

# Cria conexão com o banco de dados
conn = sqlite3.connect('conversas.db')
c = conn.cursor()

def procurar_frase():
    # Limpa a ListBox
    frases_listbox.delete(0, tk.END)

    # Busca a frase no banco de dados
    busca = f"%{procurar_entry.get()}%"
    c.execute("SELECT * FROM frases WHERE frase LIKE ?", (busca,))
    frases = c.fetchall()

    # Exibe os resultados na ListBox
    for frase in frases:
        frases_listbox.insert(tk.END, f"ID: {frase[0]} - {frase[1]}")
        
def excluir_tudo():
    resposta = messagebox.askyesno("Confirmar exclusão", "Tem certeza que deseja excluir todo o banco de dados?")
    if resposta:
        c.execute("DELETE FROM frases")
        conn.commit()
        load_frases()

# Cria a janela principal
root = tk.Tk()
root.title("Minhas frases")

# Cria o widget ListBox para mostrar as frases
frases_listbox = tk.Listbox(root)
frases_listbox.pack(fill="both", expand=True)

# Função para carregar as frases na ListBox
def load_frases():
    frases_listbox.delete(0, tk.END) # Limpa a ListBox
    c.execute("SELECT * FROM frases")
    frases = c.fetchall()
    for frase in frases:
        frases_listbox.insert(tk.END, f"ID: {frase[0]} - {frase[1]}")

# Função para excluir a frase selecionada na ListBox
def excluir_frase():
    # Verifica se há uma frase selecionada na ListBox
    if not frases_listbox.curselection():
        messagebox.showwarning("Aviso", "Selecione uma frase para excluir.")
        return
    
    # Pega o ID da frase selecionada
    id_frase = frases_listbox.get(frases_listbox.curselection()).split(" ")[1]

    # Pergunta ao usuário se ele realmente quer excluir a frase
    resposta = messagebox.askyesno("Confirmar exclusão", "Tem certeza que deseja excluir essa frase?")
    if resposta:
        # Executa o comando SQL para excluir a frase do banco de dados
        c.execute("DELETE FROM frases WHERE id = ?", (id_frase,))
        conn.commit()

        # Carrega novamente as frases na ListBox após a exclusão
        load_frases()

# Botão para carregar as frases na ListBox
carregar_button = tk.Button(root, text="Carregar frases", command=load_frases)
carregar_button.pack(side="left")



busca_label = tk.Label(root, text="Digite a frase a ser buscada:")
busca_label.pack(side="left")

# Cria um campo de entrada para que o usuário possa digitar a frase
procurar_entry = tk.Entry(root)
procurar_entry.pack(side="left")

procurar_button = tk.Button(root, text="Procurar frase", command=procurar_frase)
procurar_button.pack(side="left")

# Botão para excluir a frase selecionada na ListBox ou pagar tudo
excluir_button = tk.Button(root, text="Excluir frase", command=excluir_frase)
excluir_button.pack(side="left")
excluir_button.place(x=650, y=10)
excluir_tudo_button = tk.Button(root, text="Excluir todo", command=excluir_tudo)
excluir_tudo_button.pack(side="left")
excluir_tudo_button.place(x=725, y=10)
root.geometry("800x600+150+50")

# Inicia o loop principal da janela
root.mainloop()

# Fecha a conexão com o banco de dados
conn.close()
