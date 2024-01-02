from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
from PIL import Image
from collections import Counter
import os
import datetime
import time
import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import re
import win32api
import win32print
import tempfile
import copy
from decimal import Decimal
import requests
import pickle
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
from datetime import datetime
from pixqrcodegen import Payload
import uuid
from datetime import date
import pyqtgraph as pg

from Geral.Interface_Code import animabtn_app, fn_dados, animation_faces
from Geral.Outros import carregar_dados, on_closing

dados_P = {'Nome': '', 'Loja': '', 'Senha': '', 'Salvar': False, 'Opacidade': 100, 'Night': True, 'CD_C': False, 'IA_V': False}

item_E = {'Nome': '', 'CC': 0000, 'CB': 000000000, 'Quantidade': 0, 'QuantidadeG': 0, 'VU': 0, 'VV': 0, 'PM': 0} #(Nome do produto), (Codigo de Cadastro), (Codigo de Barra), (quantidade do item), (Valor Unitario), (Valor de Venda), (Promoção)

estoque = []

itens_V = {'Cliente': {}, 'Lista': []}

vendas = []

janela = None
jpesquisa = None
janela_q = None
create_for = None
dinheiro_pa = None

pay_dinheiro = None
returned_values = None
payment_id = None
finalizar = False
contpixs = 10


def reset_estoque():
    global itens_V, estoque
    if len(itens_V['Lista']) > 0:

        for produto in estoque:
            for i, lista in enumerate(itens_V['Lista']):
                if produto['CC'] == lista['CC']:
                    produto['Quantidade'] += lista['Quantidade']
                    del itens_V['Lista'][i]


def save_all(tela, dado, tip):
    try:
        dadosapp = open(f'Dados_User/{tip}', 'w+')

        for i, v in dado.items():
            dadosapp.writelines(f'{i}:{v}:')

        dadosapp.close()
    except:
        show_confirmation_dialog('Erro 301', 2)


def salvar_estoque():
    global estoque
    if not os.path.exists('Dados_User'):
        os.makedirs('Dados_User')

        # Salva os dados da lista estoque no arquivo produtos_ET
    with open('Dados_User/produtos_ET.pkl', 'wb') as f:
        pickle.dump(estoque, f)


def carregar_estoque():
    global estoque
    # Verifica se o arquivo produtos_ET existe
    if os.path.exists('Dados_User/produtos_ET.pkl'):
        # Carrega os dados do arquivo produtos_ET na lista estoque
        with open('Dados_User/produtos_ET.pkl', 'rb') as f:
            estoque = pickle.load(f)

    return estoque


def salvar_vendas():
    global vendas
    # Salva a lista em um arquivo
    with open('Dados_User/vendas.pkl', 'wb') as f:
        pickle.dump(vendas, f)


def carregar_vendas():
    global vendas
    # Verifica se o arquivo existe
    if os.path.exists('Dados_User/vendas.pkl'):
        # Carrega a lista de um arquivo
        with open('Dados_User/vendas.pkl', 'rb') as f:
            vendas = pickle.load(f)


def show_confirmation_dialog(message='', tip=0):
    dialog = QtWidgets.QMessageBox()
    msg_box = QMessageBox()

    if tip == 1:
        dialog.setIcon(QtWidgets.QMessageBox.Question)
        dialog.setText(message)
        dialog.setWindowTitle("Tarefa")
        dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        result = dialog.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            dialog.close()
            return False

        else:
            dialog.close()
            return True

    if tip == 2:
        msg_box.setWindowTitle("Alerta")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)

        msg_box.exec_()

    if tip == 0:
        msg_box.close()
        dialog.close()


def calcular_lucro():
    global vendas, estoque

    # Calcula o valor total dos itens atualmente em estoque
    valor_total_estoque = sum(item['VU'] * item['QuantidadeG'] for item in estoque)

    # Calcula o valor total de vendas
    valor_total_vendas = sum(item['VV'] * item['Quantidade'] for venda in vendas for item in venda['Lista'])

    # Calcula o lucro
    lucro = valor_total_vendas - valor_total_estoque

    return lucro


def calcular_diferenca():
    global vendas, estoque

    # Obtém a data atual
    hoje = date.today()
    hoje = hoje.strftime('%d/%m/%Y')

    # Calcula o total de preços de todos os itens vendidos hoje
    total_vendas_hoje = sum(item['VV'] * item['Quantidade'] for venda in vendas if venda['Cliente']['Data'] == hoje for item in venda['Lista'])

    # Retorna a diferença como um valor positivo
    return total_vendas_hoje


def calcular_media_lucro(lucro_atual):
    global estoque

    # Calcula a quantidade total de itens disponíveis para venda
    quantidade_total = sum(item['Quantidade'] for item in estoque)

    # Calcula a média de lucro por item
    media_lucro = lucro_atual / quantidade_total if quantidade_total > 0 else 0

    return media_lucro


def ranquear_mais_vendidos(tela):
    global vendas

    # Cria um gráfico vazio se ainda não existir
    if not hasattr(tela, 'w'):
        tela.w = pg.PlotWidget()
        tela.w.setBackground(None)  # Deixa o fundo do gráfico transparente
        tela.w.setWindowTitle('')
        tela.w.setLabel('left', '')
        tela.w.setLabel('bottom', '')
        tela.w.setMenuEnabled(False)  # Desabilita o menu de contexto do botão direito
        tela.w.setFixedSize(345, 400)  # Aumenta o tamanho do gráfico na horizontal
        tela.w.setMouseEnabled(x=False, y=False)  # Desabilita o arrasto e o zoom
        tela.w.hideButtons()  # Esconde os botões

        # Adiciona o gráfico ao QFrame
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tela.w)
        tela.barra.setLayout(layout)

    # Limpa o gráfico existente
    tela.w.clear()

    # Verifica se a variável 'vendas' está vazia
    if len(vendas) <= 0:
        return

    # Calcula a quantidade vendida de cada item
    contador = Counter(item['Nome'][:10] for venda in vendas for item in venda['Lista'] for _ in range(item['Quantidade']))

    # Ordena os itens por quantidade vendida em ordem decrescente e pega os 5 primeiros
    itens_mais_vendidos = sorted(contador.items(), key=lambda x: x[1], reverse=True)[:5]

    # Cria um gráfico de barras com os itens mais vendidos
    bg1 = pg.BarGraphItem(x=[i for i in range(len(itens_mais_vendidos))], height=[item[1] for item in itens_mais_vendidos], width=0.3, brush=(200, 200, 200))  # Muda a cor das barras para cinza claro
    tela.w.addItem(bg1)
    tela.w.setXRange(-1, len(itens_mais_vendidos))
    tela.w.setYRange(0, max(item[1] for item in itens_mais_vendidos) + 1)
    tela.w.getAxis('bottom').setTicks([list(enumerate([item[0] for item in itens_mais_vendidos]))])
    tela.w.autoRange()  # Adiciona a escala automática como padrão


def tendencia_de_lucro(tela):
    global vendas, estoque

    # Cria um gráfico vazio se ainda não existir
    if not hasattr(tela, 'w2'):
        tela.w2 = pg.PlotWidget()
        tela.w2.setBackground(None)  # Deixa o fundo do gráfico transparente
        tela.w2.setWindowTitle('')
        tela.w2.setLabel('left', '')
        tela.w2.setLabel('bottom', '')
        tela.w2.setMenuEnabled(False)  # Desabilita o menu de contexto do botão direito
        tela.w2.setFixedSize(345, 400)  # Aumenta o tamanho do gráfico na horizontal
        tela.w2.setMouseEnabled(x=False, y=False)  # Desabilita o arrasto e o zoom
        tela.w2.hideButtons()  # Esconde os botões

        # Adiciona o gráfico ao QFrame
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tela.w2)
        tela.tendenci.setLayout(layout)

    # Limpa o gráfico existente
    tela.w2.clear()

    # Verifica se as variáveis 'vendas' e 'estoque' estão vazias
    if len(vendas) <= 0 or len(estoque) <= 0:
        return

    # Calcula o lucro para cada item vendido
    lucro = [(item['VV'] - estoque_item['VU']) * item['Quantidade'] for venda in vendas for item in venda['Lista'] for estoque_item in estoque if item['Nome'] == estoque_item['Nome']]

    # Cria o gráfico de linha com a tendência de lucro
    tela.w2.plot(lucro)  # Plota o lucro
    tela.w2.autoRange()  # Adiciona a escala automática como padrão


def grafico_vendas_estoque(tela):
    global vendas, estoque

    # Cria um gráfico vazio se ainda não existir
    if not hasattr(tela, 'w3'):
        tela.w3 = pg.PlotWidget()
        tela.w3.setBackground(None)  # Deixa o fundo do gráfico transparente
        tela.w3.setWindowTitle('')
        tela.w3.setLabel('left', '')
        tela.w3.setLabel('bottom', '')
        tela.w3.setMenuEnabled(False)  # Desabilita o menu de contexto do botão direito
        tela.w3.setFixedSize(345, 400)  # Aumenta o tamanho do gráfico na horizontal
        tela.w3.setMouseEnabled(x=False, y=False)  # Desabilita o arrasto e o zoom
        tela.w3.hideButtons()  # Esconde os botões

        # Adiciona o gráfico ao QFrame
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tela.w3)
        tela.pizza.setLayout(layout)

    # Limpa o gráfico existente
    tela.w3.clear()

    # Verifica se as variáveis 'vendas' e 'estoque' estão vazias
    if len(vendas) <= 0 or len(estoque) <= 0:
        return

    # Calcula a quantidade total vendida e em estoque para cada item
    total_vendas = [sum(item['Quantidade'] for item in venda['Lista']) for venda in vendas]
    total_estoque = [item['Quantidade'] for item in estoque]

    # Cria o gráfico de linha
    venda_plot = tela.w3.plot(total_vendas, pen='b')  # Plota as vendas em azul
    estoque_plot = tela.w3.plot(total_estoque, pen='r')  # Plota o estoque em vermelho
    tela.w3.autoRange()  # Adiciona a escala automática como padrão

    # Cria uma legenda e adiciona os itens de plotagem
    legend = pg.LegendItem()
    legend.addItem(venda_plot, 'Vendas')  # Adiciona um título à linha de vendas
    legend.addItem(estoque_plot, 'Estoque')  # Adiciona um título à linha de estoque
    legend.setParentItem(tela.w3.getPlotItem())  # Adiciona a legenda ao gráfico


def btn_menu(tela, aba, btn):
    global dados_P, estoque, vendas
    salvar_estoque()
    salvar_vendas()
    carregar_estoque()
    carregar_vendas()

    if btn != aba and btn != 4:
        tela.navegacao.setCurrentIndex(btn)
        if btn == 0:
            atualiza_lista(tela)

        if btn == 1:
            lc = calcular_lucro()
            pl = calcular_diferenca()
            md = calcular_media_lucro(lc)

            ranquear_mais_vendidos(tela)
            tendencia_de_lucro(tela)
            grafico_vendas_estoque(tela)

            if md < 0:
                md = 0

            if pl < 0:
                pl = 0

            if lc < 0:
                lc = 0.0

            tela.Lucro.setText(f'{locale.currency(lc, grouping=True)}')
            tela.Perda.setText(f'{locale.currency(pl, grouping=True)}')
            tela.Gastos.setText(f'{locale.currency(md, grouping=True)}')

        if btn == 2:
            atualizar_tabela(tela)

        if btn == 3:
            conta_config(tela)
            outros = carregar_dados()

            if outros['Scanner']:
                tela.scanner.setText(outros['Scanner'])
            else:
                tela.scanner.setText('Nenhum Scanner Conectado')

            if outros['impressoras_conectadas']:
                tela.notst.setText(outros['impressoras_conectadas'])
            else:
                tela.notst.setText("Nenhuma Impressora Conectada")

            if outros['Pix']:
                tela.cardst.setText(outros['Pix'][0]['Chave Pix'])
            else:
                tela.cardst.setText("Nenhuma Chave Cadastrada")

        if tela.editc.text() != 'EDITAR' and btn != 3:
            tela.lanome.setText(dados_P['Nome'])
            tela.laloja.setText(dados_P['Loja'])
            tela.lasenha.setText(dados_P['Senha'])
            edit_perfil(tela, 1)

    else:
        if btn == 4:
            resp = show_confirmation_dialog("Deseja ir para tela de Login?", 1)

            if resp is False:
                userlogin = open('Dados_User/dados_perfil', 'r+')
                valor = userlogin.readline().split(':')
                compare = {}

                for i, c in enumerate(valor):
                    if i % 2 == 1:
                        compare[valor[i - 1]] = c

                compare['Salvar'] = False

                userlogin.close()
                userlogin = open('Dados_User/dados_perfil', 'w+')

                for i, v in compare.items():
                    userlogin.writelines(f'{i}:{v}:')

                userlogin.close()
                compare.clear()

            return resp

    animabtn_app(tela, btn)


def conta_config(tl):
    global dados_P

    # Verifique se o arquivo 'dados_perfil' existe na pasta 'Dados_User'
    arquivo_perfil = os.path.join('Dados_User', 'dados_perfil')

    if os.path.exists(arquivo_perfil):
        # O arquivo existe, tente lê-lo
        with open(arquivo_perfil, 'r') as file:
            conteudo = file.read().strip()

        # Verifique se o arquivo está vazio ou se a leitura foi bem-sucedida
        if conteudo:
            dados = {}
            campos = conteudo.split(':')

            try:
                for i, v in enumerate(campos):
                    if i % 2 == 1:
                        dados[campos[i-1]] = v

            except:
                os.remove(arquivo_perfil)
                tl.close()
                show_confirmation_dialog("Erro Inesperado", 2)

        else:
            os.remove(arquivo_perfil)
            tl.close()
            show_confirmation_dialog("Erro Inesperado", 2)
    else:
        tl.close()
        show_confirmation_dialog("Erro Inesperado", 2)

    if len(dados_P['Nome']) == 0 and len(dados_P['Senha']) == 0:
        for k, v in dados.items():
            dados_P[k] = v

        userlogin = open('Dados_User/dados_perfil', 'w+')

        for i, v in dados_P.items():
            userlogin.writelines(f'{i}:{v}:')
        userlogin.close()
        dados.clear()

    fn_dados(tl, dados_P)


def edit_perfil(tela, tip, btn=''):
    global dados_P

    if tip == 1:
        if tela.editc.text() == 'EDITAR':
            tela.editc.setStyleSheet("""QPushButton {
            color: rgb(255, 255, 255);
            background-color: rgb(97, 103, 112);
            border-radius: 10px;
            border: 1px solid rgb(22, 24, 26);
            }""")
            tela.editc.setText('CONFIRMAR')
            tela.lanome.setEnabled(True)
            tela.laloja.setEnabled(True)
            tela.lasenha.setEnabled(True)
            tela.lasv.setEnabled(True)
            tela.lanome.setFocus()

        else:
            caracter = "''!@#$%¨&*()_-+=[]{}~^´`:;/?.,<>|"
            test = [tela.lanome.text(), tela.laloja.text(), tela.lasenha.text()]

            for i, d in enumerate(test):
                for l in d:
                    if l in caracter[:]:
                        if i == 0:
                            tela.lanome.clear()

                        if i == 1:
                            tela.laloja.clear()

                        if i == 2:
                            tela.lasenha.clear()

            if tela.lanome.text() != '' and tela.laloja.text() != '' and tela.lasenha.text() != '':
                tela.editc.setStyleSheet("""QPushButton {
                            color: rgb(255, 255, 255);
                            background-color: rgb(54, 57, 62);
                            border-radius: 10px;
                            border: 1px solid rgb(22, 24, 26);
                            }""")
                tela.editc.setText('EDITAR')
                tela.lanome.setEnabled(False)
                tela.laloja.setEnabled(False)
                tela.lasenha.setEnabled(False)
                tela.lasv.setEnabled(False)
                animation_faces(tela, 'config')

                dados_P['Nome'] = tela.lanome.text()
                dados_P['Loja'] = tela.laloja.text()
                dados_P['Senha'] = tela.lasenha.text()
                dados_P['Salvar'] = tela.lasv.isChecked()
                save_all(tela, dados_P, 'dados_perfil')

            else:
                animation_faces(tela, 'config')

    if tip == 2:
        if btn == 'slopaci':
            valor = tela.slopaci.value() / 100
            dados_P['Opacidade'] = valor
            tela.setWindowOpacity(valor)

        if btn == 'btndark':
            if dados_P['Night'] is True:
                dados_P['Night'] = False
            else:
                dados_P['Night'] = True

        if btn == 'btncadast':
            if dados_P['CD_C'] is True:
                dados_P['CD_C'] = False
            else:
                dados_P['CD_C'] = True

        if btn == 'btnintvend':
            if dados_P['IA_V'] is True:
                dados_P['IA_V'] = False

            else:
                dados_P['IA_V'] = True

        fn_dados(tela, dados_P)
        save_all(tela, dados_P, 'dados_perfil')
        return dados_P


# Função para validar a entrada
def validate_entry(value, max_length):
    return len(value) <= int(max_length)


# Função para coletar os dados dos campos de entrada
def coletar_dadosE(tela, lista={}, subs=False):
    global janela, finalizar, dados_P

    if finalizar:
        return

    # Criar a janela
    if janela:
        on_closing([janela], 3)
        janela = None

    def calcular_lucro(*args):
        k = vu_var.get()
        if k != '':
            ve = Decimal(locale.atof(k))

            if len(vendas) > 0 and len(estoque) > 0:
                total_vendas = Decimal(sum(item['VV'] for venda in vendas for item in venda['Lista']))
                total_estoque = Decimal(sum(item['VU'] for item in estoque))
                lucro_percentual = (total_vendas / total_estoque) / 100
            else:
                lucro_percentual = Decimal('0.65')  # Lucro de 65% se as listas estiverem vazias

            lucro = (ve * lucro_percentual) + ve
            lucro = round(lucro, 2)  # Arredondar para duas casas decimais

            lucro = locale.currency(lucro, grouping=True, symbol=None)
            vv_var.set(lucro)  # Já está formatado para moeda

    def validar_comprimento(value, s, st=False):
        s = int(s)
        if s >= 13:
            if st:
                value = ler_codigo_barras()

                if value is not None:
                    value = str(value)
                    cb_entry.insert(0, value)
                else:
                    value = ''

            informacoes_produto = obter_codigo_produto_e_informacoes(value)

            if informacoes_produto:
                nome = f'{informacoes_produto["nome_produto"]}'.split()

                if informacoes_produto['nome_produto'] != 'N/A' and len(nome) >= 3:
                    np = nome[0][:6] + ' ' + nome[-3] + ' ' + nome[-2] + ' ' + nome[-1]
                else:
                    if len(nome) > 0:
                        np = nome[0]
                    else:
                        np = 'N/A'

                lis = {'Codigo De Cadastro': f'{informacoes_produto["codigo_produto"]}',
                       'Nome Do Produto': f'{np}',
                       'Valor De Estoque(R$)': f'{informacoes_produto["preco"]}',
                       'Quantidade': f'{informacoes_produto["unidade_embalagem"]}'}

                if lis['Codigo De Cadastro'] != 'N/A':
                    cc_entry.insert(0, lis['Codigo De Cadastro'])

                if lis['Nome Do Produto'] != 'N/A':
                    nome_entry.insert(0, lis['Nome Do Produto'])

                if lis['Valor De Estoque(R$)'] != 'N/A':
                    vu_entry.insert(0, lis['Valor De Estoque(R$)'])

                if lis['Quantidade'] != 'N/A':
                    quantidade_entry.insert(0, lis['Quantidade'])
            return True

    root = tk.Tk()
    root.title("Cadastrar Produto")
    root.geometry("300x330")
    root.resizable(False, False)

    validate_cmd = root.register(validate_entry)

    # Criar os campos de entrada com rótulos
    tk.Label(root, text="Nome Do Produto").pack()
    nome_entry = tk.Entry(root, validate="key", validatecommand=(validate_cmd, "%P", "30"))
    nome_entry.pack()

    tk.Label(root, text="Codigo De Cadastro").pack()
    cc_entry = tk.Entry(root, validate="key", validatecommand=(validate_cmd, "%P", "5"))
    cc_entry.pack()

    validate_cmd = root.register(validar_comprimento)
    tk.Label(root, text="Codigo De Barra").pack()
    cb_entry = tk.Entry(root, validate="key", validatecommand=(validate_cmd, "%P", "13"))
    cb_entry.pack()

    tk.Label(root, text="Quantidade Do Item").pack()
    quantidade_entry = tk.Entry(root, validate="key", validatecommand=(validate_cmd, "%P", "10"))
    quantidade_entry.pack()

    tk.Label(root, text="Valor De Estoque(R$)").pack()
    vu_var = tk.StringVar()
    vu_entry = tk.Entry(root, textvariable=vu_var, validate="key", validatecommand=(validate_cmd, "%P", "15"))
    vu_entry.pack()

    if dados_P['IA_V'] and len(lista) <= 0:
        vu_var.trace("w", calcular_lucro)

    tk.Label(root, text="Valor De Venda(R$)").pack()
    vv_var = tk.StringVar()
    vv_entry = tk.Entry(root, textvariable=vv_var, validate="key", validatecommand=(validate_cmd, "%P", "15"))
    vv_entry.pack()

    tk.Label(root, text="Promoção(%)").pack()
    pm_entry = tk.Entry(root, validate="key", validatecommand=(validate_cmd, "%P", "5"))
    pm_entry.pack()

    if len(lista) > 0:
        nome_entry.insert(0, f"{lista['Nome']}")
        cc_entry.insert(0, f"{lista['CC']}")
        cb_entry.insert(0, f"{lista['CB']}")
        quantidade_entry.insert(0, f"{lista['Quantidade']}")

        vu_entry.insert(0, f"{locale.format_string('%.2f', lista['VU'], True)}")
        vv_entry.insert(0, f"{locale.format_string('%.2f', lista['VV'], True)}")

        pm_entry.insert(0, f"{lista['PM']}".replace('.', ','))

    frame = tk.Frame(root)
    frame.pack(pady=10)

    botao = tk.Button(frame, text="Cadastrar", command=lambda: salvar_dadosE(tela,
                                                                             [nome_entry,
                                                                              cc_entry,
                                                                              cb_entry,
                                                                              quantidade_entry,
                                                                              vu_entry,
                                                                              vv_entry,
                                                                              pm_entry], subs))
    botao.grid(row=0, column=0)

    cb = tk.Button(frame, text="Ler Codigo", command=lambda: validar_comprimento(None, 13, True))
    cb.grid(row=0, column=1)

    janela = root
    janela.protocol("WM_DELETE_WINDOW", lambda: on_closing([janela], 3))

    # Iniciar o loop principal da janela
    root.mainloop()


def salvar_dadosE(tela, campos, sub=False):
    global item_E, estoque, janela
    try:
        # Salva o nome com a primeira letra em maiúsculo
        item_E['Nome'] = campos[0].get().title()

        # Trata o campo do código de cadastro removendo caracteres não numéricos
        cc = re.sub(r'\D', '', campos[1].get())
        item_E['CC'] = int(cc)

        # Trata o campo do código de barras removendo caracteres não numéricos
        cb = re.sub(r'\D', '', campos[2].get())
        item_E['CB'] = int(cb)

        item_E['Quantidade'] = int(campos[3].get())

        # Trata o campo do valor unitário substituindo vírgulas por pontos e convertendo para float
        item_E['VU'] = round(float(locale.atof(campos[4].get())), 2)

        # Trata o campo do valor de venda substituindo vírgulas por pontos e convertendo para float
        item_E['VV'] = round(float(locale.atof(campos[5].get())), 2)

        # Verifica se o campo PM está vazio
        if len(campos[6].get()) > 0:
            pm_value = int(campos[6].get().replace(',', '.'))
            # Verifica se o valor está entre 0 e 100 (inclusive)
            if 0 <= pm_value <= 100:
                item_E['PM'] = pm_value
        else:
            item_E['PM'] = 0  # ou qualquer valor padrão que você queira definir para PM quando ele estiver vazio

        status = salvar_no_estoque(tela, sub)

    except ValueError as e:
        show_confirmation_dialog(f"{str(e)}", 2)
    else:
        if status is True:
            show_confirmation_dialog("Dados coletados com sucesso!", 2)
            # Limpa todos os campos de entrada
            campos[0].delete(0, 'end')
            campos[1].delete(0, 'end')
            campos[2].delete(0, 'end')
            campos[3].delete(0, 'end')
            campos[4].delete(0, 'end')
            campos[5].delete(0, 'end')
            campos[6].delete(0, 'end')
            on_closing([janela], 3)
            coletar_dadosE(tela)


def on_cl_local():
    global janela, jpesquisa, janela_q, create_for, dinheiro_pa
    return janela, jpesquisa, janela_q, create_for, dinheiro_pa


def reset_on_cl(janelas, j):
    global janela, jpesquisa, janela_q, create_for, dinheiro_pa

    if j == -1:
        for k, i in enumerate(janelas):
            if k >= 3:
                if k == 3:
                    janela = i
                if k == 4:
                    jpesquisa = i
                if k == 5:
                    janela_q = i
                if k == 6:
                    create_for = i
                if k == 7:
                    create_for = i

    else:
        if j == 3:
            janela = janelas[0]
        if j == 4:
            jpesquisa = janelas[0]
        if j == 5:
            janela_q = janelas[0]
        if j == 6:
            create_for = janelas[0]
        if j == 7:
            dinheiro_pa = janelas[0]


def salvar_no_estoque(tela, sub):
    global item_E, estoque

    item_E['QuantidadeG'] = item_E['Quantidade']
    # Verifica se todos os campos em item_E estão preenchidos
    item_E_sem_PM = {chave: valor for chave, valor in item_E.items() if chave != 'PM'}

    if all(item_E_sem_PM.values()):
        # Verifica se o CC e CB já existem na lista estoque
        for item in estoque:
            if item['CC'] == item_E['CC'] or item['CB'] == item_E['CB']:
                # Pergunta ao usuário se ele deseja acrescentar os valores ao item existente
                if sub is False:
                    resp = show_confirmation_dialog(f"O item {item['Nome']} já existe. Deseja acrescentar os valores?", 1)
                    if resp is False:
                        # Substitui o valor unitário e soma a quantidade
                        item['VU'] = item_E['VU']
                        item['VV'] = item_E['VV']
                        item['Quantidade'] += item_E['Quantidade']

                        if item['Quantidade'] >= item['QuantidadeG']:
                            item['QuantidadeG'] = item['Quantidade']

                        item['PM'] = item_E['PM']
                        atualizar_tabela(tela)
                else:
                    item['Nome'] = item_E['Nome']
                    item['CC'] = item_E['CC']
                    item['CB'] = item_E['CB']
                    item['VU'] = item_E['VU']
                    item['VV'] = item_E['VV']
                    item['Quantidade'] = item_E['Quantidade']
                    item['QuantidadeG'] = item['Quantidade']

                    item['PM'] = item_E['PM']
                    atualizar_tabela(tela)
                return True

        # Se o CC e CB não existem na lista estoque, adiciona uma cópia de item_E à lista estoque
        estoque.append(item_E.copy())
        # Esvazia item_E
        for key in item_E:
            item_E[key] = '' if isinstance(item_E[key], str) else 0
        atualizar_tabela(tela)
        return True
    else:
        show_confirmation_dialog('Por favor, preencha todos os campos!', 2)
        return False


def atualizar_tabela(tela):
    global estoque, finalizar

    if finalizar:
        return

    # Define o número de linhas e colunas da tabela
    tela.produtoslist.setRowCount(len(estoque))
    tela.produtoslist.setColumnCount(6)

    # Define os cabeçalhos das colunas
    tela.produtoslist.setHorizontalHeaderLabels(["Nome", "Codigo", "Quantidade", "Valor Unitário(R$)", "Valor de Venda(R$)", "Desconto(%)"])
    totale = 0

    # Pega o comprimento horizontal atual do QTableWidget
    width = tela.produtoslist.width()
    # Divide o comprimento pela quantidade de colunas
    section_size = (width / 6) + 2

    # Adiciona os dados à tabela
    for i, item in enumerate(estoque):
        total = item['VU'] * item['QuantidadeG']
        totale += total

        tela.produtoslist.setItem(i, 0, QTableWidgetItem(f"Nome: {item['Nome']}"))
        tela.produtoslist.setItem(i, 1, QTableWidgetItem(f"Cod. Cadastro: {item['CC']}"))
        tela.produtoslist.setItem(i, 2, QTableWidgetItem(f"Quantidade: {item['Quantidade']}"))
        tela.produtoslist.setItem(i, 3, QTableWidgetItem(f"Val. Unitário: {locale.currency(item['VU'], grouping=True)}"))
        tela.produtoslist.setItem(i, 4, QTableWidgetItem(f"Val. Venda: {locale.currency(item['VV'], grouping=True)}"))
        tela.produtoslist.setItem(i, 5, QTableWidgetItem(f"Desconto: {item['PM']}%"))

    tela.Totest.setText(f"Estoque: {locale.currency(totale, grouping=True)}")

    # Aplica o resultado no horizontalHeaderDefaultSectionSize e horizontalHeaderMinimumSectionSize
    tela.produtoslist.horizontalHeader().setMinimumSectionSize(section_size)
    tela.produtoslist.horizontalHeader().setDefaultSectionSize(section_size)


def verific_item(tela, cod):
    global estoque, itens_V, finalizar

    if finalizar:
        return

    selected_items = tela.produtoslist.selectedItems()
    # Pega os dados da coluna do item selecionado
    selected_data = {}
    for item in selected_items:
        if ':' in item.text():
            key, value = item.text().split(':')
            key = key.strip()
            value = value.strip()
            if key == 'Cod. Cadastro':
                key = 'CC'
            if key in ['CC', 'Quantidade']:
                value = int(value)
            selected_data[key] = value

    # Remove as chaves 'Valor Total' e 'Desconto'
    keys_to_remove = ['Val. Venda', 'Val. Unitário', 'Desconto']
    for key in keys_to_remove:
        selected_data.pop(key, None)

    if len(selected_data) > 0:
        for dic in estoque:
            if all(item in dic.items() for item in selected_data.items()):
                # Cria uma caixa de diálogo para confirmar a exclusão
                if cod == 0:
                    ms = show_confirmation_dialog(f"Deseja realmente deletar {dic['Nome']} do estoque?", 1)
                    if ms is False:
                        if len(itens_V['Lista']) > 0:
                            for i, prod in enumerate(itens_V['Lista']):
                                if dic['CC'] == prod['CC']:
                                    del itens_V['Lista'][i]

                        estoque.remove(dic)
                        salvar_estoque()
                        carregar_estoque()

                        atualiza_lista(tela)
                        atualizar_tabela(tela)

                else:
                    coletar_dadosE(tela, dic, True)


def obter_codigo_produto_e_informacoes(gtin):
    url = f'https://world.openfoodfacts.org/api/v0/product/{gtin}.json'
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados_produto = resposta.json().get('product', {})
        nome_produto = dados_produto.get('product_name', 'N/A')
        unidade_embalagem = dados_produto.get('product', {}).get('quantity', {}).get('unit', 'N/A')
        quantidade = dados_produto.get('quantity', 'N/A')
        preco = dados_produto.get('product', {}).get('price', {}).get('amount', 'N/A')

        # Extração de um possível código de produto de 5 dígitos
        codigo_produto = gtin[8:13] if len(gtin) == 13 else 'N/A'

        return {
            'codigo_produto': codigo_produto,
            'nome_produto': nome_produto,
            'unidade_embalagem': unidade_embalagem,
            'quantidade': quantidade,
            'preco': preco
        }
    else:
        show_confirmation_dialog(f'Erro ao obter informações do produto GTIN {gtin}. Código de status: {resposta.status_code}', 2)
        return None


def ler_codigo_barras():
    global finalizar

    # Se finalizar for True, retorna sem fazer nada
    if finalizar:
        return None

    # Aqui você colocaria o código para se conectar ao leitor de código de barras e ler o código
    # Por exemplo:
    try:
        porta = carregar_dados()
        with serial.Serial(porta['Scanner'], 9600, timeout=3) as ser:
            codigo_barras = ser.readline().decode().strip()
            if len(codigo_barras) > 0:
                print(1)
                return codigo_barras
            else:
                show_confirmation_dialog(f'Leitor não detectou o codigo', 2)
                return None

    except serial.SerialException as e:
        show_confirmation_dialog(f'Erro ao tentar conectar ao scanner: {str(e)}', 2)
        return None
    except Exception as e:
        show_confirmation_dialog(f'Ocorreu um erro inesperado: {str(e)}', 2)
        return None


def pesquisarV(tela):
    global estoque, jpesquisa, finalizar

    if finalizar:
        return

    if jpesquisa:
        on_closing([jpesquisa], 4)
        jpesquisa = None

    def adicionar():
        try:
            # Obtém o item selecionado
            item_selecionado = tree.selection()[0]

            # Obtém o valor da coluna "Cod. Cadastro" do item selecionado
            cod_cadastro = tree.item(item_selecionado, "values")[1]  # O índice 1 corresponde à segunda coluna

            # Chama a função verificar_e_adicionar com o valor obtido
            verificar_e_adicionar(tela, CC=int(cod_cadastro))
            on_closing([jpesquisa], 4)
        except:
            show_confirmation_dialog('Nenhum item selecionado', 2)

    def buscar():
        termo_busca = campo_busca.get()
        if termo_busca == 'Pesquisa':
            termo_busca = ''
        else:
            termo_busca = termo_busca.title()  # Converte a primeira letra para maiúscula
        resultados = [item for item in estoque if termo_busca in [str(item['Nome']), str(item['CC']), str(item['CB'])]]
        for i in tree.get_children():
            tree.delete(i)
        if resultados:
            for resultado in resultados:
                tree.insert('', 'end', values=(
                    resultado['Nome'], resultado['CC'], resultado['Quantidade'],
                    f"{locale.currency(resultado['VV'], grouping=True)}", f"{resultado['PM']}%"))
        else:
            tree.insert('', 'end', values=("Nenhum item encontrado", "", "", "", ""))
        campo_busca.delete(0, tk.END)  # Limpa o campo de pesquisa após a busca

    def ler_e_buscar():
        codigo_barras = ler_codigo_barras()
        campo_busca.delete(0, tk.END)  # Limpa o campo de pesquisa
        campo_busca.insert(0, codigo_barras)  # Insere o código de barras lido no campo de pesquisa
        buscar()  # Realiza a busca com o código de barras

    def clear_placeholder(event):
        if campo_busca.get() == 'Pesquisa':
            campo_busca.delete(0, tk.END)

    def add_placeholder(event):
        if campo_busca.get() == '':
            campo_busca.insert(0, 'Pesquisa')

    root = tk.Tk()
    root.title("Pesquisa de Estoque")
    root.geometry("1050x300")  # Tamanho fixo da janela
    root.resizable(0, 0)  # Desabilita o redimensionamento da janela

    # Frame para conter o campo de busca e os botões
    frame_busca = tk.Frame(root)
    frame_busca.pack(side='bottom', pady=10)  # Adiciona um padding vertical de 10px

    campo_busca = tk.Entry(frame_busca, width=50)
    campo_busca.insert(0, 'Pesquisa')  # Placeholder text
    campo_busca.bind("<FocusIn>", clear_placeholder)
    campo_busca.bind("<FocusOut>", add_placeholder)
    campo_busca.pack(side='left', padx=2)

    botao_busca = tk.Button(frame_busca, text="Buscar", command=buscar, bg='#090C0D', fg='white', padx=10,
                            pady=0)  # Adiciona uma aparência moderna ao botão
    botao_busca.pack(side='left', padx=2)  # Adiciona um padding horizontal de 10px

    botao_adicionar = tk.Button(frame_busca, text="Adicionar", command=adicionar, bg='#090C0D', fg='white', padx=10,
                                pady=0)  # Adiciona uma aparência moderna ao botão
    botao_adicionar.pack(side='left', padx=2)

    botao_ler = tk.Button(frame_busca, text="Cod. Barras", command=ler_e_buscar, bg='#090C0D', fg='white', padx=10, pady=0)

    botao_ler.pack(side='left', padx=2)

    tree = ttk.Treeview(root, columns=('Nome', 'CC', 'Quantidade', 'VV', 'PM'), show='headings')

    # Centraliza os valores da tabela
    for col in ('Nome', 'CC', 'Quantidade', 'VV', 'PM'):
        tree.column(col, anchor='center')

    tree.heading('Nome', text='Nome')
    tree.heading('CC', text='Cod. Cadastro')
    tree.heading('Quantidade', text='Quantidade')
    tree.heading('VV', text='Val. Venda')
    tree.heading('PM', text='Promoção')

    # Adiciona um padding vertical de 10px no topo da tabela
    tree.pack(padx=20, pady=20)

    jpesquisa = root
    jpesquisa.protocol("WM_DELETE_WINDOW", lambda: on_closing([jpesquisa], 4))

    root.mainloop()


def atualiza_lista(Tela, cod=0):
    global estoque, itens_V

    for i, lista in enumerate(itens_V['Lista']):
        if lista['Quantidade'] <= 0:
            del itens_V['Lista'][i]

    # Define o número de linhas e colunas da tabela
    Tela.vendidos.setRowCount(len(itens_V['Lista']))
    Tela.vendidos.setColumnCount(6)

    # Define os cabeçalhos das colunas
    Tela.vendidos.setHorizontalHeaderLabels(["N°", "Nome", "Cod. Cadastro", "Cod. Barras", "Unid", "Valor"])

    # Pega o comprimento horizontal atual do QTableWidget
    width = Tela.vendidos.width()

    # Divide o comprimento pela quantidade de colunas
    section_size = (width / 6) + 1
    totalist = 0

    for i, item in enumerate(itens_V['Lista']):
        # Calcula o desconto
        des = (item['VV'] - ((item['PM'] / 100) * item['VV'])) * item['Quantidade']

        # Adiciona os detalhes do item à QTableWidget
        Tela.vendidos.setItem(i, 0, QTableWidgetItem(f"{i + 1}"))
        Tela.vendidos.setItem(i, 1, QTableWidgetItem(f"{item['Nome']}"))
        Tela.vendidos.setItem(i, 2, QTableWidgetItem(f"{item['CC']}"))
        Tela.vendidos.setItem(i, 3, QTableWidgetItem(f"{item['CB']}"))
        Tela.vendidos.setItem(i, 4, QTableWidgetItem(f"{item['Quantidade']}x"))
        Tela.vendidos.setItem(i, 5, QTableWidgetItem(f"{locale.currency(des, grouping=True)}"))
        totalist += des
        Tela.subto.setText(f"{locale.currency(totalist, grouping=True)}")

        # Centraliza os itens
        for j in range(6):
            Tela.vendidos.item(i, j).setTextAlignment(QtCore.Qt.AlignCenter)

    # Aplica o resultado no horizontalHeaderDefaultSectionSize e horizontalHeaderMinimumSectionSize
    Tela.vendidos.horizontalHeader().setMinimumSectionSize(section_size)
    Tela.vendidos.horizontalHeader().setDefaultSectionSize(section_size)

    if len(itens_V['Lista']) <= 0:
        Tela.subto.setText(f"R$ 0,00")

        Tela.numb.setText(f'00000')
        Tela.codb.setText(f'0000000000000')
        Tela.nomei.setText(f'Nome')
        Tela.unid.setText(f'0x')
        Tela.valouni.setText(f'R$ 0,00')
        Tela.desconto.setText(f'R$ 0,00')
        Tela.valotot.setText(f'R$ 0,00')
        Tela.troco.setText('R$ 0,00')
        Tela.tot.setText('TOTAL PAGO: R$ 0,00')
        Tela.Caixa.setText('CAIXA LIVRE')

    else:
        if cod != 0:
            for produto in itens_V['Lista']:
                if str(produto['CC']) == str(cod):
                    Tela.numb.setText(f'{produto["CC"]}')
                    Tela.codb.setText(f'{produto["CB"]}')
                    Tela.nomei.setText(f'{produto["Nome"]}')
                    Tela.unid.setText(f'{produto["Quantidade"]}x')
                    Tela.valouni.setText(f'{locale.currency(produto["VV"], grouping=True)}')

                    desco = produto['VV'] * (produto['PM'] / 100)
                    Tela.desconto.setText(f'{locale.currency(desco, grouping=True)}')

                    vlto = (produto['VV'] - desco) * produto['Quantidade']
                    Tela.valotot.setText(f'{locale.currency(vlto, grouping=True)}')

        if float(Decimal(locale.atof(str(Tela.tot.text()).strip('TOTAL PAGO: R$ ')))) > 0:
            troc = (float(Decimal(locale.atof(str(Tela.tot.text()).strip('TOTAL PAGO: R$ ')))) -
                    float(Decimal(locale.atof(str(Tela.subto.text()).strip('TOTAL PAGO: R$ ')))))

            if troc <= 0:
                Tela.troco.setText('R$ 0,00')
            else:
                Tela.troco.setText(f'{locale.currency(troc, grouping=True)}')


def verificar_e_adicionar(Tela, CC=0):
    # Obtenha o valor do QLineEdit
    global estoque, itens_V, finalizar

    if finalizar:
        return

    cont = 0

    if CC == 0:
        valor_pesquisa = Tela.itemid.text()
    else:
        valor_pesquisa = str(CC)

    if len(valor_pesquisa) <= 0:
        valor_pesquisa = str(ler_codigo_barras())

    # Verifique se o valor de pesquisa não está vazio
    if len(valor_pesquisa) > 0 and valor_pesquisa != 'None':
        # Percorra cada item no estoque
        for item in estoque:
            # Se o valor de pesquisa corresponder ao 'Nome' do item no estoque
            if valor_pesquisa.capitalize() == str(item['CC']) or valor_pesquisa.capitalize() == str(item['CB']):
                # Verifique se a quantidade é maior que 0
                if item['Quantidade'] > 0:
                    # Verifique se o item já existe na lista de itens_V
                    for i in itens_V['Lista']:
                        if i['CC'] == item['CC']:
                            # Se o item já existir, incremente a quantidade
                            i['Quantidade'] += 1
                            if item['PM'] != i['PM']:
                                i['PM'] = item['PM']

                            Tela.itemid.clear()

                            Tela.numb.setText(f'{i["CC"]}')
                            Tela.codb.setText(f'{i["CB"]}')
                            Tela.nomei.setText(f'{i["Nome"]}')
                            Tela.unid.setText(f'{i["Quantidade"]}x')
                            Tela.valouni.setText(f'{locale.currency(i["VV"], grouping=True)}')

                            desco = i['VV'] * (i['PM'] / 100)
                            Tela.desconto.setText(f'{locale.currency(desco, grouping=True)}')
                            vlto = (i['VV'] - desco) * i['Quantidade']
                            Tela.valotot.setText(f'{locale.currency(vlto, grouping=True)}')
                            break

                    else:
                        # Se o item não existir na lista, copie o dicionário e altere a quantidade para 1
                        item_copiado = item.copy()
                        item_copiado['Quantidade'] = 1

                        Tela.numb.setText(f'{item_copiado["CC"]}')
                        Tela.codb.setText(f'{item_copiado["CB"]}')
                        Tela.nomei.setText(f'{item_copiado["Nome"]}')
                        Tela.unid.setText(f'{item_copiado["Quantidade"]}x')
                        Tela.valouni.setText(f'{locale.currency(item_copiado["VV"], grouping=True)}')

                        desco = item_copiado['VV'] * (item_copiado['PM'] / 100)
                        Tela.desconto.setText(f'{locale.currency(desco, grouping=True)}')
                        vlto = (item_copiado['VV'] - desco) * item_copiado['Quantidade']
                        Tela.valotot.setText(f'{locale.currency(vlto, grouping=True)}')

                        # Adicione o item copiado à lista de itens_V
                        itens_V['Lista'].append(item_copiado)
                        Tela.itemid.clear()

                    item['Quantidade'] -= 1
                    Tela.Caixa.setText('CAIXA OCUPADO')

                else:
                    show_confirmation_dialog(f'Item {item["Nome"]} Fora de estoque!', 2)
                    Tela.itemid.clear()
            else:
                cont += 1
                if cont >= len(estoque):
                    show_confirmation_dialog(f'Item não cadastrado!', 2)
                    Tela.itemid.clear()

        atualiza_lista(Tela)

    else:
        if valor_pesquisa != 'None':
            show_confirmation_dialog(f'Nenhum resultado encontrado!', 2)


def remover_item_edit(Tela, id=0, num=0):
    global estoque, itens_V, finalizar

    if finalizar:
        return

    # Obtém as linhas selecionadas
    linhas_selecionadas = Tela.vendidos.selectionModel().selectedRows()

    # Verifica se alguma linha foi selecionada
    if linhas_selecionadas:
        # Obtém a primeira linha selecionada
        linha = linhas_selecionadas[0]

        # Obtém o valor da coluna "Cod. Cadastro" da linha selecionada
        cod_cadastro = Tela.vendidos.item(linha.row(), 2).text()  # O índice 1 corresponde à segunda coluna

        # Percorre cada item na lista de itens_V
        for i, item in enumerate(itens_V['Lista']):
            # Se o valor de pesquisa corresponder ao 'CC' do item na lista
            if str(cod_cadastro) == str(item['CC']):
                if id == 0:
                    # Remove o item da lista
                    perg = show_confirmation_dialog(f'Deseja deletar {item["Nome"]}?', 1)
                    if perg is False:
                        for valor in estoque:
                            if str(valor['CC']) == str(cod_cadastro):
                                valor['Quantidade'] += item['Quantidade']

                        del itens_V['Lista'][i]

                        linha = linha.row()
                        linha = int(linha)

                        if len(itens_V['Lista']) >= 1:
                            if (linha - 1) >= 0:
                                linha = linha - 1

                            if (linha + 1) <= len(itens_V['Lista']) - 1:
                                linha = linha + 1

                            cod_cadastro = Tela.vendidos.item(linha, 2).text()

                        atualiza_lista(Tela, cod_cadastro)

                else:
                    for valor in estoque:
                        if item["CC"] == valor['CC']:
                            reset = item['Quantidade']

                            if item['Quantidade'] > num:
                                devol = item['Quantidade'] - num

                                item['Quantidade'] -= devol
                                valor['Quantidade'] += devol

                            else:
                                num -= 1

                                item['Quantidade'] += num

                                if (valor['Quantidade'] - num) >= 0:
                                    valor['Quantidade'] -= num

                                else:
                                    item['Quantidade'] = reset
                                    show_confirmation_dialog(f'Estoque de {item["Nome"]} insuficiente!', 2)

                            return valor['CC']
                break
    else:
        show_confirmation_dialog('Nenhum item selecionado!', 2)


def quantidade_edit(tela):
    # Obtém o valor do campo de entrada
    global itens_V, janela_q, finalizar

    if finalizar:
        return

    if janela_q:
        on_closing([janela_q], 5)
        janela_q = None

    def imprimir_quantidade():
        quantidade = campo_quantidade.get()

        if len(quantidade) > 0 and quantidade != 'Quantidade':
            try:
                # Imprime o valor
                vl = int(quantidade)
                v = remover_item_edit(tela, 1, vl)
                atualiza_lista(tela, v)
                on_closing([janela_q], 5)
            except:
                show_confirmation_dialog('Digite um valor valido!', 2)
        else:
            show_confirmation_dialog('Nenhum valor inserido!', 2)

    def clear_placeholder(event):
        if campo_quantidade.get() == 'Quantidade':
            campo_quantidade.delete(0, tk.END)

    def add_placeholder(event):
        if campo_quantidade.get() == '':
            campo_quantidade.insert(0, 'Quantidade')

    # Cria uma nova janela Tkinter
    janela = tk.Tk()

    janela.geometry("250x100")  # Tamanho fixo da janela
    janela.title("Editar Lista")

    janela.resizable(0, 0)  # Desabilita o redimensionamento da janela
    # Cria um novo campo de entrada
    campo_quantidade = tk.Entry(janela, width=23)
    campo_quantidade.insert(0, 'Quantidade')  # Placeholder text
    campo_quantidade.bind("<FocusIn>", clear_placeholder)
    campo_quantidade.bind("<FocusOut>", add_placeholder)
    campo_quantidade.pack(side='top')
    campo_quantidade.pack(pady=10)

    # Cria um novo botão que chama a função imprimir_quantidade quando clicado
    botao_confirmar = tk.Button(janela, text="Confirmar", command=imprimir_quantidade, width=20)
    botao_confirmar.pack(pady=3)

    janela_q = janela
    janela_q.protocol("WM_DELETE_WINDOW", lambda: on_closing([janela_q], 5))
    # Inicia o loop principal da janela Tkinter
    janela.mainloop()


def validate_input(input, input_type):
    global finalizar
    if finalizar:
        return

    if input_type == "name":
        return input.title().isalpha()
    elif input_type in ["cpf", "phone"]:
        return input.isdigit()


def submit_fields(name_entry, cpf_entry, phone_entry):
    global returned_values, create_for, finalizar
    if finalizar:
        return

    name = name_entry.get()
    cpf = cpf_entry.get()
    phone = phone_entry.get()

    if not all([validate_input(name, "name"), validate_input(cpf, "cpf"), validate_input(phone, "phone")]):
        show_confirmation_dialog('Entrada inválida. Por favor, verifique os campos e tente novamente.', 2)
    else:
        returned_values = [name, cpf, phone]
        on_closing([create_for], 6)


def cancel():
    global create_for, returned_values, finalizar
    if finalizar:
        return

    resp = show_confirmation_dialog('Deseja não cadastrar o cliente?', 1)

    if resp is False:
        returned_values = None
        on_closing([create_for], 6)


def create_form():
    global create_for, finalizar

    if finalizar:
        return

    if create_for:
        on_closing([create_for], 6)
        create_for = None

    root = tk.Tk()
    root.title("Formulário")
    root.geometry("250x150")  # Tamanho fixo da janela
    root.resizable(0, 0)  # Desabilita o redimensionamento da janela

    # Centraliza os widgets na janela
    root.grid_columnconfigure(0, weight=1)

    # Adiciona um espaço no topo da janela
    root.grid_rowconfigure(0, minsize=5)

    name_entry = tk.Entry(root, width=25)
    cpf_entry = tk.Entry(root, width=25)
    phone_entry = tk.Entry(root, width=25)

    # Adiciona texto de orientação aos campos de entrada
    name_entry.insert(0, 'Cliente')
    cpf_entry.insert(0, 'CPF')
    phone_entry.insert(0, 'Telefone')

    # Limpa o texto de orientação quando o campo de entrada é clicado
    name_entry.bind("<FocusIn>", lambda args: name_entry.delete('0', 'end'))
    cpf_entry.bind("<FocusIn>", lambda args: cpf_entry.delete('0', 'end'))
    phone_entry.bind("<FocusIn>", lambda args: phone_entry.delete('0', 'end'))

    # Retorna o texto de orientação quando o campo de entrada não está mais em foco
    name_entry.bind("<FocusOut>", lambda args: name_entry.insert(0, 'Cliente') if not name_entry.get() else None)
    cpf_entry.bind("<FocusOut>", lambda args: cpf_entry.insert(0, 'CPF') if not cpf_entry.get() else None)
    phone_entry.bind("<FocusOut>", lambda args: phone_entry.insert(0, 'Telefone') if not phone_entry.get() else None)

    name_entry.grid(row=1, column=0, pady=(5, 4))
    cpf_entry.grid(row=2, column=0, pady=4)
    phone_entry.grid(row=3, column=0, pady=4)

    create_for = root

    confirm_button = tk.Button(root, text='Confirmar',
                               command=lambda: submit_fields(name_entry, cpf_entry, phone_entry))
    cancel_button = tk.Button(root, text='Cancelar', command=lambda: cancel())

    # Define o mesmo tamanho para os botões
    max_len = max(len(confirm_button.cget('text')), len(cancel_button.cget('text')))

    confirm_button.config(width=max_len)
    cancel_button.config(width=max_len)

    # Distancia um pouco mais os botões
    confirm_button.place(x=48, y=110)
    cancel_button.place(x=129, y=110)

    create_for.protocol("WM_DELETE_WINDOW", lambda: cancel())

    root.mainloop()


def fecha(tela, vl):
    global pay_dinheiro, dinheiro_pa, finalizar

    if finalizar:
        return

    vl = Decimal(locale.atof(vl.get()))
    vl = float(vl)

    if vl <= 0:
        show_confirmation_dialog('Não é possivel sair sem o valor total!', 2)
    else:
        tela.tot.setText(f'TOTAL PAGO: {locale.currency(vl, grouping=True)}')
        # Extrair o valor monetário da string
        sub = Decimal(locale.atof(str(tela.subto.text()).strip('R$ ')))
        sub = float(sub)

        troc = vl - sub

        if troc >= 0:
            tela.troco.setText(f'{locale.currency(troc, grouping=True)}')

        pay_dinheiro = vl
        on_closing([dinheiro_pa], 7)


def dinheiro_pay(tela):
    global dinheiro_pa, finalizar

    if finalizar:
        return

    if dinheiro_pa:
        on_closing([dinheiro_pa], 7)

    root = tk.Tk()
    root.title("Valor")
    root.geometry("250x150")  # Tamanho fixo da janela
    root.resizable(0, 0)  # Desabilita o redimensionamento da janela

    # Centraliza os widgets na janela
    root.grid_columnconfigure(0, weight=1)

    # Adiciona um espaço no topo da janela
    root.grid_rowconfigure(0, minsize=5)

    vl = tk.Entry(root, width=25)

    # Adiciona texto de orientação aos campos de entrada
    vl.insert(0, 'Total Pago (R$)')

    # Limpa o texto de orientação quando o campo de entrada é clicado
    vl.bind("<FocusIn>", lambda args: vl.delete('0', 'end'))

    # Retorna o texto de orientação quando o campo de entrada não está mais em foco
    vl.bind("<FocusOut>", lambda args: vl.insert(0, 'Total Pago (R$)') if not vl.get() else None)
    vl.grid(row=1, column=0, pady=(5, 4))

    dinheiro_pa = root

    confirm_button = tk.Button(root, text='Confirmar',  command=lambda: fecha(tela, vl))
    confirm_button.config(width=20)
    # Distancia um pouco mais os botões
    confirm_button.place(x=48, y=110)

    dinheiro_pa.protocol("WM_DELETE_WINDOW", lambda: on_closing([dinheiro_pa], 7))

    root.mainloop()


def limpar_qr_code(tela):
    # Verifica se o QFrame já tem um layout
    if tela.qrcod.layout() is not None:
        # Remove todos os widgets do layout
        for i in reversed(range(tela.qrcod.layout().count())):
            tela.qrcod.layout().itemAt(i).widget().setParent(None)


def gerar_qrcode(dados, tela):
    global dados_P
    # Limpa o QFrame
    limpar_qr_code(tela)

    # Cria um objeto Payload
    payload = Payload(dados['Nome Do Destinatário'], dados['Chave Pix'], dados['Preço'], dados['Estado Natal'], dados['Loja'])

    # Gera a Payload Pix e o QR Code
    payload.gerarPayload()

    # Verifica se a pasta "Pagamentos" existe, se não, cria a pasta
    if not os.path.exists('Pagamentos'):
        os.makedirs('Pagamentos')

    # Carrega a imagem do QR Code
    img = Image.open('pixqrcodegen.png')

    # Redimensiona a imagem para caber no QFrame de 190x180
    img = img.resize((185, 185), Image.LANCZOS)

    # Salva a imagem redimensionada na pasta "Pagamentos"
    img.save('Pagamentos/pixqrcodegen.png')

    # Converte a imagem do QR Code para um formato que o PyQt pode usar
    qimg = QPixmap('Pagamentos/pixqrcodegen.png')

    # Cria um widget de etiqueta (label) com a imagem
    label = QLabel()
    label.setPixmap(qimg)

    # Define um layout de grade para o QFrame se ainda não tiver um
    if tela.qrcod.layout() is None:
        tela.qrcod.setLayout(QGridLayout())

    # Adiciona o widget de etiqueta ao centro da grade
    tela.qrcod.layout().addWidget(label)

    # Define uma folha de estilo para arredondar as bordas do widget
    tela.qrcod.setStyleSheet("QWidget {border-radius: 10px;}")

    tela.lotpix.setStyleSheet("""QFrame {
    background-color: rgb(32, 34, 37);
    border-radius: 6px;
    }""")
    os.remove('pixqrcodegen.png')


def status_pix(payment_id, tela, time):
    global contpixs

    update_countdown(tela, time)
    contpixs -= 1

    if time <= 0 or contpixs <= 0:
        show_confirmation_dialog()
        stats = show_confirmation_dialog('Pagamento realizado?', 1)
        tempix = contpixs
        contpixs = 10
        return stats, tempix


def update_countdown(tela, remaining_time):
    # Converte o tempo restante em minutos e segundos
    minutes, seconds = divmod(remaining_time, 60)

    # Atualiza o texto em tpix
    if seconds >= 10:
        tela.tpix.setText(f"Aguardando Tempo Limite: {minutes}:{seconds}")
    else:
        tela.tpix.setText(f"Aguardando Tempo Limite: {minutes}:0{seconds}")


def selected_payment(tela, pix=None):
    global estoque, itens_V, vendas, dados_P, returned_values, pay_dinheiro, dinheiro_pa, finalizar, payment_id

    if finalizar:
        return

    # Verifica a seleção atual
    selected_payment = tela.pagamento.currentText()

    if dinheiro_pa is None:
        if len(itens_V['Lista']) > 0:
            tela.pagamento.setEnabled(False)
            tela.add.setEnabled(False)
            tela.remover.setEnabled(False)
            tela.verificar.setEnabled(False)
            tela.editar.setEnabled(False)

            # Imprime a seleção atual
            total = Decimal(locale.atof(str(tela.tot.text()).strip('TOTAL PAGO: R$ ')))
            total = float(total)
            # Obtenha a data atual
            data_atual = datetime.now()

            # Formate a data como uma string no formato DD/MM/AAAA
            data_str = data_atual.strftime('%d/%m/%Y')

            if total <= 0:
                if dados_P['CD_C'] is True:
                    create_form()

                    if returned_values is None:
                        if len(vendas) > 0:
                            clint = len(vendas) + 1
                            itens_V['Cliente']['Nome'] = f'Cliente{clint}'
                            itens_V['Cliente']['CPF'] = 'N/A'
                            itens_V['Cliente']['Telefone'] = 'N/A'
                            itens_V['Cliente']['Data'] = data_str

                        else:
                            itens_V['Cliente']['Nome'] = 'Cliente1'
                            itens_V['Cliente']['CPF'] = 'N/A'
                            itens_V['Cliente']['Telefone'] = 'N/A'
                            itens_V['Cliente']['Data'] = data_str
                    else:
                        itens_V['Cliente']['Nome'] = returned_values[0]
                        itens_V['Cliente']['CPF'] = returned_values[1]
                        itens_V['Cliente']['Telefone'] = returned_values[2]
                        itens_V['Cliente']['Data'] = data_str
                else:
                    if len(vendas) > 0:
                        clint = len(vendas) + 1
                        itens_V['Cliente']['Nome'] = f'Cliente{clint}'
                        itens_V['Cliente']['CPF'] = 'N/A'
                        itens_V['Cliente']['Telefone'] = 'N/A'
                        itens_V['Cliente']['Data'] = data_str

                    else:
                        itens_V['Cliente']['Nome'] = 'Cliente1'
                        itens_V['Cliente']['CPF'] = 'N/A'
                        itens_V['Cliente']['Telefone'] = 'N/A'
                        itens_V['Cliente']['Data'] = data_str

            if selected_payment == 'DINHEIRO' and os.path.isfile('Pagamentos/pixqrcodegen.png') is False:
                troc = Decimal(locale.atof(str(tela.troco.text()).strip('R$ ')))
                troc = float(troc)

                if troc <= 0:
                    dinheiro_pay(tela)
                else:
                    resp = show_confirmation_dialog('Valor pago já ultrapassado, deseja editar?', 1)
                    if resp is False:
                        dinheiro_pay(tela)

                itens_V['Cliente']['Pagamento'] = 'DINHEIRO'

            if selected_payment == 'PIX' and total <= 0:
                dados1 = carregar_dados()
                pixc = dados1['Pix']

                if len(pixc) <= 0:
                    show_confirmation_dialog('Essa versão ainda não suporta pagamento por PIX :/', 2)
                else:
                    sub = Decimal(locale.atof(str(tela.subto.text()).strip('R$ ')))
                    sub = float(sub)

                    # Gera um ID de pagamento único
                    payment_id = str(uuid.uuid4())

                    pixc[0]['Preço'] = f'{sub:.2f}'
                    pixc[0]['Chave Pix'] = f"{pixc[0]['Chave Pix']}".replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
                    pixc[0]['Loja'] = f'{payment_id[:10]}'.replace('-', '')

                    if os.path.isfile('Pagamentos/pixqrcodegen.png'):
                        if pix is None:
                            show_confirmation_dialog('Pagamento em andamento!', 2)
                    else:
                        gerar_qrcode(pixc[0], tela)
                        payment_id = pixc[0]['Loja']

                    if pix is False:
                        tela.tot.setText(f'TOTAL PAGO {locale.currency(sub, grouping=True)}')
                        itens_V['Cliente']['Pagamento'] = 'PIX'
                        finalizar_pedido(tela)

            elif selected_payment == 'DINHEIRO' and os.path.isfile('Pagamentos/pixqrcodegen.png') is not False or selected_payment == 'PIX' and total > 0:
                show_confirmation_dialog('Você não pode alterar o meio de pagamento em processo de finalização', 2)

        else:
            show_confirmation_dialog('Nenhuma lista de compras pendente!', 2)

    else:
        show_confirmation_dialog('A venda já está em processo final!', 2)


def final(cond):
    global finalizar
    finalizar = cond

    return finalizar


def finalizar_pedido(tela):
    global itens_V, vendas, pay_dinheiro, dados_P
    tot = Decimal(locale.atof(str(tela.tot.text()).strip('TOTAL PAGO: R$ ')))
    tot = float(tot)
    sub = Decimal(locale.atof(str(tela.subto.text()).strip('R$ ')))
    sub = float(sub)

    troc = tot - sub

    if troc >= 0 and len(itens_V['Lista']) and tot > 0:
        rsp = show_confirmation_dialog('Deseja finalizar a compra?', 1)

        if rsp is False:
            impres = carregar_dados()

            st = None
            n = None

            nota = gerar_nota_fiscal(sub, tot, troc)

            if impres['impressoras_conectadas'] != '':
                st = imprimir_nota(nota, impres['impressoras_conectadas'])

            if st is False or impres['impressoras_conectadas'] == '':
                n = show_confirmation_dialog('A impressão não pôde ser realizada. Você gostaria de concluir a '
                                                 'compra mesmo sem a nota fiscal?', 1)

            if n is False or st is True:
                temp = copy.deepcopy(itens_V)
                vendas.append(temp)
                itens_V['Cliente'].clear()
                itens_V['Lista'].clear()
                atualiza_lista(tela)
                tela.pagamento.setEnabled(True)
                tela.add.setEnabled(True)
                tela.remover.setEnabled(True)
                tela.verificar.setEnabled(True)
                tela.editar.setEnabled(True)

    else:
        show_confirmation_dialog("Não foi possivel finalizar a compra!", 2)


def gerar_nota_fiscal(sub, tot, troc):
    global itens_V

    # Calcula o comprimento do primeiro item da lista de compras
    comprimento_primeiro_item = len(f'V. total: {locale.currency(sub, grouping=True)} - T. pago: '
                                    f'{locale.currency(tot, grouping=True)} - Troc.: '
                                    f'{locale.currency(troc, grouping=True)}\n')

    nota = '-' * (comprimento_primeiro_item + 20) + '\n'
    nota += f' Loja: {dados_P["Loja"]:>{comprimento_primeiro_item - len(dados_P["Loja"]) + 3}}\n'
    nota += '-' * (comprimento_primeiro_item + 20) + '\n'

    nota += f' {"N:":<10}| {"Prod:":<10}| {"Cod:":<10}| {"Qtd:":<10}| {"Valor:":<8}\n'
    nota += f' ' * (comprimento_primeiro_item + 20) + '\n'

    for i, item in enumerate(itens_V['Lista']):
        total = (item['VV'] * item['Quantidade']) - ((item['PM'] / 100) * item['VV'])
        n = f'{i + 1:03d}'
        qt = f'{item["Quantidade"]:03d}x'

        nome = item["Nome"]
        if len(nome) > 8:
            nome = nome[:8]
        elif len(nome) < 8:
            nome += ' ' * ((8 - len(nome)) + 3)

        nota += f' {str(n):<10} {nome:<10} {str(item["CC"]):<10} {qt:<10} {locale.currency(total, grouping=True):<8}\n'

    nota += f' ' * (comprimento_primeiro_item + 20) + '\n'

    nota += '-' * (comprimento_primeiro_item + 20) + '\n'
    nota += f'{" V. total:":<{comprimento_primeiro_item + 15 - 4}} ' + locale.currency(sub, grouping=True) + '\n'
    nota += f'{" T. pago:":<{comprimento_primeiro_item + 15 - 4}} ' + locale.currency(tot, grouping=True) + '\n'
    nota += f'{" Troc.:":<{comprimento_primeiro_item + 15 - 4}} ' + locale.currency(troc, grouping=True) + '\n'

    nota += '-' * (comprimento_primeiro_item + 20) + '\n'

    return nota


def imprimir_nota(nota, impressora, timeout=10):
    # Define a impressora padrão
    win32print.SetDefaultPrinter(impressora)

    try:
        # Salva a nota em um arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_nota:
            temp_nota.write(nota.encode())
            temp_nota_path = temp_nota.name

        # Tenta imprimir o arquivo
        win32api.ShellExecute(0, "print", temp_nota_path, None, ".", 0)

        # Obtém o nome do trabalho de impressão
        job_name = os.path.basename(temp_nota_path)

        # Verifica o status da fila de impressão
        start_time = time.time()

        # Obtém o nome da impressora padrão
        impressora = win32print.GetDefaultPrinter()

        time.sleep(2)

        while True:
            # Obtém um identificador para a impressora
            hPrinter = win32print.OpenPrinter(impressora)

            # Obtém as informações da impressora
            informacoes_impressora = win32print.GetPrinter(hPrinter, 2)

            # Fecha o identificador para a impressora
            win32print.ClosePrinter(hPrinter)

            if informacoes_impressora['cJobs'] <= 0:
                return True

            # Se a impressão demorar muito, cancela
            if time.time() - start_time > timeout:
                # Abre a impressora
                hPrinter = win32print.OpenPrinter(impressora)

                # Limpa a fila de impressão
                win32print.SetPrinter(hPrinter, 0, None, win32print.PRINTER_CONTROL_PURGE)

                # Fecha a impressora
                win32print.ClosePrinter(hPrinter)
                return False

            # Aguarda antes de verificar novamente
            time.sleep(1)

    except Exception as e:
        return False


def cancel_pay(tela):
    global itens_V, vendas, dados_P
    reset_estoque()
    itens_V['Cliente'].clear()
    itens_V['Lista'].clear()
    atualiza_lista(tela)

    tela.pagamento.setEnabled(True)
    tela.add.setEnabled(True)
    tela.remover.setEnabled(True)
    tela.verificar.setEnabled(True)
    tela.editar.setEnabled(True)

    if os.path.isfile('Pagamentos/pixqrcodegen.png'):
        os.remove('Pagamentos/pixqrcodegen.png')

