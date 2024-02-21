import tkinter as tk
from tkinter import filedialog
import pickle
import os


label_resultado_projetos = None  # Definindo a variável global

try:
    with open('usuarios.pickle', 'rb') as file:
        usuarios = pickle.load(file)
except FileNotFoundError:
    usuarios = {}

def save_usuarios():
    with open('usuarios.pickle', 'wb') as file:
        pickle.dump(usuarios, file)

def login():
    username = entry_login.get()
    password = entry_senha.get()

    if username in usuarios and usuarios[username]["senha"] == password:
        label_resultado["text"] = "Login feito com sucesso"
        abrir_tela_projetos(username)
    else:
        label_resultado["text"] = "Usuário ou senha incorretos"

def salvar_projeto(username, nome, cidade, data_projeto, arquivo):
    usuarios[username]["projetos"].append({
        "nome": nome,
        "cidade": cidade,
        "data": data_projeto,
        "caminho_arquivo": arquivo
    })
    save_usuarios()
    label_resultado_projetos["text"] = "Projeto salvo com sucesso"
    ver_projetos(username)

def excluir_projeto(username, index):
    usuarios[username]["projetos"].pop(index)
    label_resultado_projetos["text"] = "Projeto excluído com sucesso"
    save_usuarios()

def ver_projetos(username):
    nova_janela_projetos = tk.Toplevel()
    nova_janela_projetos.title("Projetos Salvos")
    nova_janela_projetos.geometry("600x400+500+200")

    label_titulo = tk.Label(nova_janela_projetos, text="Projetos Salvos:", font=("Arial", 12))
    label_titulo.pack()

    lista_projetos = tk.Listbox(nova_janela_projetos, width=80, height=15)
    lista_projetos.pack()

    for i, projeto in enumerate(usuarios[username]["projetos"]):
        info_projeto = f"Nome: {projeto['nome']} - Cidade: {projeto['cidade']} - Data: {projeto['data']}"
        lista_projetos.insert(tk.END, info_projeto)

        button_excluir = tk.Button(nova_janela_projetos, text="Excluir", command=lambda idx=i: excluir_projeto(username, idx))
        button_excluir.pack()

    def abrir_arquivo_selecionado(event):
        indice_selecionado = lista_projetos.curselection()[0]
        caminho_arquivo = usuarios[username]["projetos"][indice_selecionado].get("caminho_arquivo")
        if caminho_arquivo:
            os.startfile(caminho_arquivo)

    lista_projetos.bind("<Double-Button-1>", abrir_arquivo_selecionado)

def abrir_tela_projetos(username):
    root.withdraw()

    nova_janela = tk.Toplevel()
    nova_janela.title(f"Detalhes do Projeto - Usuário: {username}")
    nova_janela.configure(bg="#d7ebf9")  # Cor de fundo azul claro
    nova_janela.geometry("500x450+400+150")

    label_nome = tk.Label(nova_janela, text="Nome do Projeto:", bg="#d7ebf9", font=("Arial", 10))
    label_nome.pack()

    entry_nome = tk.Entry(nova_janela, font=("Arial", 10))
    entry_nome.pack()

    label_cidade = tk.Label(nova_janela, text="Cidade:", bg="#d7ebf9", font=("Arial", 10))
    label_cidade.pack()

    entry_cidade = tk.Entry(nova_janela, font=("Arial", 10))
    entry_cidade.pack()

    label_data_projeto = tk.Label(nova_janela, text="Data do Projeto:", bg="#d7ebf9", font=("Arial", 10))
    label_data_projeto.pack()

    entry_data_projeto = tk.Entry(nova_janela, font=("Arial", 10))
    entry_data_projeto.pack()

    button_salvar_projeto = tk.Button(nova_janela, text="Salvar Projeto", command=lambda: salvar_projeto(username, entry_nome.get(), entry_cidade.get(), entry_data_projeto.get(), filedialog.askopenfilename()), bg="#0275d8", fg="white", font=("Arial", 10))
    button_salvar_projeto.pack()

    button_ver_projetos = tk.Button(nova_janela, text="Ver Projetos", command=lambda: ver_projetos(username), bg="#0275d8", fg="white", font=("Arial", 10))
    button_ver_projetos.pack()

    global label_resultado_projetos  # Usando a variável global
    label_resultado_projetos = tk.Label(nova_janela, text="", bg="#d7ebf9", font=("Arial", 10))
    label_resultado_projetos.pack()

    def fechar_janela():
        nova_janela.destroy()
        root.deiconify()

    nova_janela.protocol("WM_DELETE_WINDOW", fechar_janela)

root = tk.Tk()
root.title("APLICATIVO DE PROJETOS")
root.geometry("500x400+400+100")  # Aumentei o tamanho da janela
root.configure(bg="#d7ebf9")  # Cor de fundo azul claro

frame_login = tk.Frame(root, bg="#d7ebf9")  # Novo frame para o login
frame_login.pack(pady=50)

label_login = tk.Label(frame_login, text="Login", bg="#d7ebf9", font=("Arial", 12))
label_login.grid(row=0, column=0, pady=10)

entry_login = tk.Entry(frame_login, font=("Arial", 10))
entry_login.grid(row=1, column=0, pady=5)

label_senha = tk.Label(frame_login, text="Senha", bg="#d7ebf9", font=("Arial", 12))
label_senha.grid(row=2, column=0, pady=10)

entry_senha = tk.Entry(frame_login, show="*", font=("Arial", 10))
entry_senha.grid(row=3, column=0, pady=5)

label_resultado = tk.Label(root, text="", bg="#d7ebf9", font=("Arial", 10))
label_resultado.pack()

def cadastrar():
    novo_usuario = entry_login.get()
    nova_senha = entry_senha.get()

    if novo_usuario not in usuarios:
        usuarios[novo_usuario] = {"senha": nova_senha, "nome": "", "cidade": "", "projetos": []}
        label_resultado["text"] = "Cadastro realizado com sucesso"
        save_usuarios()
    else:
        label_resultado["text"] = "Usuário já existente"

frame_botoes = tk.Frame(root, bg="#d7ebf9")  # Novo frame para os botões
frame_botoes.pack(pady=20)

button_login = tk.Button(frame_botoes, text="Login", command=login, bg="#0275d8", fg="white", font=("Arial", 10))
button_login.pack(side=tk.LEFT, padx=10)

button_cadastro = tk.Button(frame_botoes, text="Cadastrar", command=cadastrar, bg="#0275d8", fg="white", font=("Arial", 10))
button_cadastro.pack(side=tk.LEFT, padx=10)



def on_close():
    save_usuarios()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
