import os
import json
import tkinter as tk
from tkinter import Tk, ttk, StringVar
from ttkthemes import ThemedTk
import serial.tools.list_ports
import win32print
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


# Variáveis globais
janela_impressora = None
janela_cadastro = None
Porta = None

close = False

conectados = {'impressoras_conectadas': '', 'Pix': [], 'Scanner': ''}


def open_printer_selector(tela):
    from Geral.Funções_App import show_confirmation_dialog
    global janela_impressora, close

    if close:
        return

    if janela_impressora:
        on_closing([janela_impressora], 2)

    def listar_impressoras():
        impressoras = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
        impressoras_listbox.delete(0, tk.END)
        for impressora in impressoras:
            impressoras_listbox.insert(tk.END, impressora)

    def conectar_impressora():
        global conectados
        selecionado = impressoras_listbox.curselection()
        if selecionado:
            impressora_selecionada = impressoras_listbox.get(selecionado[0])
            show_confirmation_dialog(f"Impressora conectada com sucesso:\n{impressora_selecionada}", 2)

            conectados['impressoras_conectadas'] = impressora_selecionada
            salvar_dados()
            tela.notst.setText(conectados['impressoras_conectadas'])
            on_closing([janela_impressora], 2)

    # Criar a janela principal
    root = ThemedTk(theme="arc")  # Use o tema 'arc'
    root.title("Selecionar Impressora")
    root.geometry("400x230")  # Defina um tamanho fixo para a janela
    root.resizable(False, False)  # Impede o redimensionamento

    # Lista de impressoras
    impressoras_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
    impressoras_listbox.pack(fill=tk.X, padx=10, pady=10)

    # Botões de atualizar e conectar
    botoes_frame = tk.Frame(root)
    botoes_frame.pack()

    atualizar_button = ttk.Button(botoes_frame, text="Atualizar", command=listar_impressoras)
    atualizar_button.pack(side=tk.LEFT, padx=10)

    conectar_button = ttk.Button(botoes_frame, text="Conectar", command=conectar_impressora)
    conectar_button.pack(side=tk.LEFT, padx=10)

    # Inicialmente, liste as impressoras
    listar_impressoras()

    janela_impressora = root  # Atribua a janela à variável global

    janela_impressora.protocol("WM_DELETE_WINDOW", lambda: on_closing([janela_impressora], 2))

    root.mainloop()


def conectar_maquininha(tela):
    from Geral.Funções_App import show_confirmation_dialog
    global janela_cadastro, close, conectados

    # Dicionário para mapear estados para DDDs
    ddd_estados = {
        'Acre': '68', 'Alagoas': '82', 'Amapá': '96', 'Amazonas': '92', 'Bahia': '71', 'Ceará': '85',
        'Distrito Federal': '61', 'Espírito Santo': '27', 'Goiás': '62', 'Maranhão': '98', 'Mato Grosso': '65',
        'Mato Grosso do Sul': '67', 'Minas Gerais': '31', 'Pará': '91', 'Paraíba': '83', 'Paraná': '41',
        'Pernambuco': '81', 'Piauí': '86', 'Rio de Janeiro': '21', 'Rio Grande do Norte': '84',
        'Rio Grande do Sul': '51', 'Rondônia': '69', 'Roraima': '95', 'Santa Catarina': '48', 'São Paulo': '11',
        'Sergipe': '79', 'Tocantins': '63'
    }

    if close:
        return

    if janela_cadastro:
        on_closing([janela_cadastro], 0)

    def realizar_cadastro():
        nome_destinatario = nome_destinatario_entry.get()
        chave_pix = chave_pix_entry.get()
        estado_natal = estado_natal_var.get()

        # Verifica se a chave Pix contém o DDD. Se não, adiciona o DDD.
        if len(chave_pix) == 9:  # Se o número de telefone não contém o DDD
            chave_pix = "+55" + ddd_estados[estado_natal] + chave_pix

        # Formata o número de telefone para o formato padrão brasileiro
        chave_pix = chave_pix[:4] + chave_pix[4:10] + chave_pix[10:]

        if nome_destinatario and chave_pix and estado_natal:
            conectados['Pix'].clear()
            conectados['Pix'].append({
                'Nome Do Destinatário': nome_destinatario,
                'Chave Pix': chave_pix,
                'Estado Natal': estado_natal  # Salva apenas o nome do estado
            })
            show_confirmation_dialog("Cadastro realizado com sucesso.", 2)
            on_closing([janela_cadastro], 0)
            salvar_dados()
            tela.cardst.setText(conectados['Pix'][0]['Chave Pix'])
        else:
            show_confirmation_dialog("Por favor, preencha todos os campos.", 2)

    root = Tk()
    root.title("Chave Pix")
    root.geometry('300x200')
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use('clam')  # Tema moderno
    style.configure('TButton', font=('calibri', 10, 'bold'), borderwidth='4')
    style.configure('TLabel', font=('calibri', 10), borderwidth='4', background=root.cget('bg'))  # Cor de fundo do rótulo igual à janela
    style.configure('TEntry', font=('calibri', 10))

    nome_destinatario_label = ttk.Label(root, text="Nome Do Destinatário:")
    nome_destinatario_label.pack()
    nome_destinatario_entry = ttk.Entry(root)
    nome_destinatario_entry.pack()

    chave_pix_label = ttk.Label(root, text="Chave Pix (TEL):")
    chave_pix_label.pack()
    chave_pix_entry = ttk.Entry(root)
    chave_pix_entry.pack()

    estado_natal_label = ttk.Label(root, text="Estado Natal:")
    estado_natal_label.pack()
    estados = list(ddd_estados.keys())  # Usa os nomes completos dos estados
    estado_natal_var = StringVar(root)
    estado_natal_var.set(estados[0])
    estado_natal_optionmenu = ttk.OptionMenu(root, estado_natal_var, *estados)
    estado_natal_optionmenu.pack()

    cadastrar_button = ttk.Button(root, text="Cadastrar", command=realizar_cadastro)
    cadastrar_button.pack(pady=10)

    janela_cadastro = root
    janela_cadastro.protocol("WM_DELETE_WINDOW", lambda: on_closing([janela_cadastro], 0))

    root.mainloop()


# Função para fechar a janela da impressora ao fechar o aplicativo principal
def on_closing(janelas=None, j=-1):
    global janela_cadastro, janela_impressora, Porta
    from Geral.Funções_App import reset_on_cl

    for i, janela in enumerate(janelas):
        if janela is not None:
            janela.destroy()
            janelas[i] = None

            if j == 0:
                janela_cadastro = None
            if j == 2:
                janela_impressora = None
            if j == 1:
                Porta = None

            if j == -1:
                janela_cadastro = None
                janela_impressora = None
                Porta = None

    reset_on_cl(janelas, j)


def salvar_dados():
    global conectados
    os.makedirs('Dados_User', exist_ok=True)

    with open('Dados_User/dados.json', 'w') as f:
        json.dump(conectados, f)


def carregar_dados():
    global conectados
    try:
        with open('Dados_User/dados.json', 'r') as f:
            conectados = json.load(f)
            return conectados
    except FileNotFoundError:
        salvar_dados()
        return None


def on_cl_gl():
    from Geral.Funções_App import on_cl_local
    global janela_impressora, janela_cadastro, Porta
    mais = on_cl_local()

    listar = [janela_cadastro, janela_impressora, Porta]
    for v in mais:
        listar.append(v)

    return listar


def criar_interface(tela):
    global lista_portas, Porta, conectados, close
    if close:
        return

    if Porta:
        on_closing([Porta], 1)

    def conectar():
        porta_selecionada = lista_portas.get(lista_portas.curselection()).split(' | ')[0]
        try:
            # Tente conectar à porta selecionada
            conexao = serial.Serial(porta_selecionada, 9600)
            conectados['Scanner'] = conexao.portstr
            from Geral.Funções_App import show_confirmation_dialog
            show_confirmation_dialog(f'Conectado com sucesso à porta {conexao.portstr}', 2)
            tela.scanner.setText(conectados['Scanner'])
            on_closing([Porta], 1)
            salvar_dados()
        except serial.SerialException as e:
            from Geral.Funções_App import show_confirmation_dialog
            show_confirmation_dialog(f'Não foi possível conectar à porta selecionada: {str(e)}', 2)


    root = tk.Tk()
    root.title('Conectar Scanner')
    root.geometry('500x250')  # Ajuste o tamanho da janela aqui
    root.resizable(False, False)  # Desativa o redimensionamento da janela

    frame = tk.Frame(root)
    frame.pack(pady=5)  # Adiciona um padding vertical de 5px

    lista_portas = tk.Listbox(frame, width=50, height=10)  # Ajuste o tamanho da lista aqui

    # Liste todas as portas seriais disponíveis
    portas = serial.tools.list_ports.comports()
    for porta in portas:
        lista_portas.insert(tk.END,
                            f'{porta.device} | {porta.description}')  # Adiciona o nome do dispositivo ao lado da porta

    lista_portas.pack()
    Porta = root

    botao_conectar = tk.Button(frame, text='Conectar', command=conectar, width=20)
    botao_conectar.pack(pady=10)

    Porta.protocol("WM_DELETE_WINDOW", lambda: on_closing([Porta], 1))
    root.mainloop()


def finalO(cond):
    from Geral.Funções_App import final
    global close

    close = final(cond)

