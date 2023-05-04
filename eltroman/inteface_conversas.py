import tkinter as tk
import sqlite3
from tkinter import ttk

# Criando uma conexão com o banco de dados
conn = sqlite3.connect('conversas.db')

conn.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='conversas'")


# Salvando as alterações e fechando a conexão
conn.commit()
conn.close()

# Criando a janela principal
root = tk.Tk()
root.title("Conversas")

# Criando um frame para os dados
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Criando um label para o título da tabela
titulo = tk.Label(frame, text="Conversas:")
titulo.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

# Criando um treeview para exibir os dados da tabela
treeview = ttk.Treeview(frame, columns=("entrada", "resposta", "sentimento", "status"), show="headings")
treeview.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

# Definindo o cabeçalho da tabela
treeview.heading("entrada", text="Entrada")
treeview.heading("resposta", text="Resposta")
treeview.heading("sentimento", text="Sentimento")
treeview.heading("status", text="Status")

# Conectando novamente ao banco de dados SQLite
conn = sqlite3.connect('conversas.db')

# Selecionando os dados da tabela
cursor = conn.execute("SELECT * FROM conversas")

# Iterando sobre os dados e exibindo na tabela
for row in cursor:
    entrada = row[0]
    resposta = row[1]
    sentimento = row[2]
    status = row[3]
    treeview.insert("", "end", values=(entrada, resposta, sentimento, status))

# Fechando a conexão com o banco de dados
conn.close()

# Iniciando o loop principal do Tkinter
root.mainloop()

#________________________________________________________________________________

import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox



# Função para excluir item selecionado
def excluir_item():
    # Obter o item selecionado
    item = treeview.selection()

    # Verificar se um item foi selecionado
    if not item:
        messagebox.showwarning("Aviso", "Por favor, selecione um item para excluir.")
        return

    # Obter o valor do ROWID do item selecionado
    rowid = treeview.item(item, "text")

    # Exibir caixa de diálogo para confirmar exclusão
    if messagebox.askyesno("Excluir item", f"Deseja excluir o item {rowid}?"):
        # Excluir o item do banco de dados
        cursor.execute("DELETE FROM conversas WHERE ROWID=?", (rowid,))
        conn.commit()

        # Excluir o item da Treeview
        treeview.delete(item)

# Criar a janela principal
root = tk.Tk()
root.title("Excluir Conversas")
# Criar a Treeview
treeview = ttk.Treeview(root, columns=("entrada", "resposta", "sentimento", "status"))
treeview.heading("#0", text="ROWID")
treeview.heading("entrada", text="Entrada")
treeview.heading("resposta", text="Resposta")
treeview.heading("sentimento", text="Sentimento")
treeview.heading("status", text="Status")
treeview.pack()

# Conectar ao banco de dados
conn = sqlite3.connect("conversas.db")
cursor = conn.cursor()

# Selecionar os dados da tabela
cursor.execute("SELECT ROWID, entrada, resposta, sentimento, status FROM conversas")
dados = cursor.fetchall()

# Inserir os dados na Treeview
for dado in dados:
    treeview.insert("", "end", text=dado[0], values=(dado[1], dado[2], dado[3], dado[4]))

# Criar o botão "Excluir"
btn_excluir = ttk.Button(root, text="Excluir", command=excluir_item)
btn_excluir.pack()

# Executar a janela principal
root.mainloop()

# Fechar a conexão com o banco de dados
conn.close()
