from PyQt5 import QtGui
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


def animabtn_app(tela, btn):
    from Geral.Funções_App import dados_P

    if dados_P['Night']:
        if btn == 0:
            tela.principal.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(62, 65, 72);
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                border-top-right-radius: 30px;
                border-bottom-right-radius: 30px;
                }
            """)
        else:
            tela.principal.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(54, 57, 62);
                border-radius: 30px;
                }
            QPushButton:hover {
            background-color: rgb(57, 59, 66);
            border-radius: 25px;
            }
            """)

        if btn == 1:
            tela.estatistica.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(62, 65, 72);
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                border-top-right-radius: 30px;
                border-bottom-right-radius: 30px;
                }
            """)

        else:
            tela.estatistica.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(54, 57, 62);
                border-radius: 30px;
                }
            QPushButton:hover {
            background-color: rgb(57, 59, 66);
            border-radius: 25px;
            }
            """)

        if btn == 2:
            tela.estoque.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(62, 65, 72);
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                border-top-right-radius: 30px;
                border-bottom-right-radius: 30px;
                }
            """)

        else:
            tela.estoque.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(54, 57, 62);
                border-radius: 30px;
                }
            QPushButton:hover {
            background-color: rgb(57, 59, 66);
            border-radius: 25px;
            }
            """)

        if btn == 3:
            tela.conta.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(62, 65, 72);
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                border-top-right-radius: 30px;
                border-bottom-right-radius: 30px;
                }
            """)

        else:
            tela.conta.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(54, 57, 62);
                border-radius: 30px;
                }
            QPushButton:hover {
            background-color: rgb(57, 59, 66);
            border-radius: 25px;
            }
            """)

        if btn == 4:
            tela.sair.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(62, 65, 72);
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                border-top-right-radius: 30px;
                border-bottom-right-radius: 30px;
                }
            """)

        else:
            tela.sair.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(54, 57, 62);
                border-radius: 30px;
                }
            QPushButton:hover {
            background-color: rgb(57, 59, 66);
            border-radius: 25px;
            }
            """)

    else:
        if btn == 0:
            tela.principal.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(153, 153, 153);
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                border-top-right-radius: 30px;
                border-bottom-right-radius: 30px;
                }
            """)
        else:
            tela.principal.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(143, 143, 143);
                border-radius: 30px;
                }
            QPushButton:hover {
            background-color: rgb(133, 133, 133);
            border-radius: 25px;
            }
            """)

        if btn == 1:
            tela.estatistica.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(153, 153, 153);
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                border-top-right-radius: 30px;
                border-bottom-right-radius: 30px;
                }
            """)

        else:
            tela.estatistica.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(143, 143, 143);
                border-radius: 30px;
                }
            QPushButton:hover {
            background-color: rgb(133, 133, 133);
            border-radius: 25px;
            }
            """)

        if btn == 2:
            tela.estoque.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(153, 153, 153);
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                border-top-right-radius: 30px;
                border-bottom-right-radius: 30px;
                }
            """)

        else:
            tela.estoque.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(143, 143, 143);
                border-radius: 30px;
                }
            QPushButton:hover {
            background-color: rgb(133, 133, 133);
            border-radius: 25px;
            }
            """)

        if btn == 3:
            tela.conta.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(153, 153, 153);
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                border-top-right-radius: 30px;
                border-bottom-right-radius: 30px;
                }
            """)

        else:
            tela.conta.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(143, 143, 143);
                border-radius: 30px;
                }
            QPushButton:hover {
            background-color: rgb(133, 133, 133);
            border-radius: 25px;
            }
            """)

        if btn == 4:
            tela.sair.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(153, 153, 153);
                border-top-left-radius: 30px;
                border-bottom-left-radius: 30px;
                border-top-right-radius: 30px;
                border-bottom-right-radius: 30px;
                }
            """)

        else:
            tela.sair.setStyleSheet("""QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(143, 143, 143);
                border-radius: 30px;
                }
            QPushButton:hover {
            background-color: rgb(133, 133, 133);
            border-radius: 25px;
            }
            """)


def animation_faces(tela, area, camp=''):
    if area == 'config':
        if tela.lanome.text() == '':
            tela.lanome.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-radius: 0px;
            border: 0px solid rgb(212, 212, 212);
            border-left: 1px solid rgb(255, 0, 0);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }

            QLineEdit:hover {
            border-left: 1px solid rgb(54, 57, 62);
            }""")

        else:
            tela.lanome.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-radius: 0px;
            border: 0px solid rgb(212, 212, 212);
            border-left: 1px solid rgb(212, 212, 212);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }

            QLineEdit:hover {
            border-left: 1px solid rgb(54, 57, 62);
            }""")

        if tela.laloja.text() == '':
            tela.laloja.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-radius: 0px;
            border: 0px solid rgb(212, 212, 212);
            border-left: 1px solid rgb(255, 0, 0);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }

            QLineEdit:hover {
            border-left: 1px solid rgb(54, 57, 62);
            }""")

        else:
            tela.laloja.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-radius: 0px;
            border: 0px solid rgb(212, 212, 212);
            border-left: 1px solid rgb(212, 212, 212);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }

            QLineEdit:hover {
            border-left: 1px solid rgb(54, 57, 62);
            }""")

        if tela.lasenha.text() == '':
            tela.lasenha.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-radius: 0px;
            border: 0px solid rgb(212, 212, 212);
            border-left: 1px solid rgb(255, 0, 0);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }

            QLineEdit:hover {
            border-left: 1px solid rgb(54, 57, 62);
            }""")

        else:
            tela.lasenha.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-radius: 0px;
            border: 0px solid rgb(212, 212, 212);
            border-left: 1px solid rgb(212, 212, 212);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }

            QLineEdit:hover {
            border-left: 1px solid rgb(54, 57, 62);
            }""")

    if area == 'login':
        if camp == 'Nome':
            tela.Nome.setStyleSheet("""QLineEdit {
                            color: rgb(255, 255, 255);
                            border-bottom-right-radius: 0px;
                            border-bottom: 1px solid rgb(200, 0, 0);
                            background-color: rgba(0, 0, 0, 0);
                            padding: 5px;
                            }
                            """)
            tela.Nome.clear()

        if camp == 'NNome':
            tela.Nome.setStyleSheet("""QLineEdit {
                            color: rgb(255, 255, 255);
                            border-bottom-right-radius: 0px;
                            border-bottom: 1px solid rgb(255, 255, 255);
                            background-color: rgba(0, 0, 0, 0);
                            padding: 5px;
                            }
                            """)

        if camp == 'Loja':
            tela.Loja.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-bottom-right-radius: 0px;
            border-bottom: 1px solid rgb(200, 0, 0);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }
            """)
            tela.Loja.clear()

        if camp == 'NLoja':
            tela.Loja.setStyleSheet("""QLineEdit {
                            color: rgb(255, 255, 255);
                            border-bottom-right-radius: 0px;
                            border-bottom: 1px solid rgb(255, 255, 255);
                            background-color: rgba(0, 0, 0, 0);
                            padding: 5px;
                            }
                            """)

        if camp == 'Senha':
            tela.Senha.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-bottom-right-radius: 0px;
            border-bottom: 1px solid rgb(200, 0, 0);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }
            """)
            tela.Senha.clear()

        if camp == 'NSenha':
            tela.Senha.setStyleSheet("""QLineEdit {
                            color: rgb(255, 255, 255);
                            border-bottom-right-radius: 0px;
                            border-bottom: 1px solid rgb(255, 255, 255);
                            background-color: rgba(0, 0, 0, 0);
                            padding: 5px;
                            }
                            """)

        if camp == 'Geral':
            tela.Nome.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-bottom-right-radius: 0px;
            border-bottom: 1px solid rgb(200, 0, 0);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }
            """)
            tela.Nome.clear()

            tela.Loja.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-bottom-right-radius: 0px;
            border-bottom: 1px solid rgb(200, 0, 0);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }
            """)
            tela.Loja.clear()

            tela.Senha.setStyleSheet("""QLineEdit {
            color: rgb(255, 255, 255);
            border-bottom-right-radius: 0px;
            border-bottom: 1px solid rgb(200, 0, 0);
            background-color: rgba(0, 0, 0, 0);
            padding: 5px;
            }
            """)
            tela.Senha.clear()

    if area == 'lsuport':
        if camp == 'Assunto':
            tela.Assunto.setStyleSheet("""QLineEdit {
                            color: rgb(255, 255, 255);
                            border-bottom-right-radius: 0px;
                            border-bottom: 1px solid rgb(200, 0, 0);
                            background-color: rgba(0, 0, 0, 0);
                            padding: 5px;
                            }
                            """)

        if camp == 'Email':
            tela.email.setStyleSheet("""QLineEdit {
                                            color: rgb(255, 255, 255);
                                            border-bottom-right-radius: 0px;
                                            border-bottom: 1px solid rgb(200, 0, 0);
                                            background-color: rgba(0, 0, 0, 0);
                                            padding: 5px;
                                            }
                                            """)

        if camp == 'Detalhes':
            tela.text_area.setStyleSheet("""QPlainTextEdit {
                                                            color: rgb(255, 255, 255);
                                                            border-radius: 3px;
                                                            border: 1px solid rgb(200, 0, 0);
                                                            background-color: rgba(0, 0, 0, 0);
                                                            padding: 5px;
                                                            }
                                                            """)

        if camp == '':
            tela.Assunto.setStyleSheet("""QLineEdit {
                color: rgb(255, 255, 255);
                border-bottom-right-radius: 0px;
                border-bottom: 1px solid rgb(255, 255, 255);
                background-color: rgba(0, 0, 0, 0);
                padding: 5px;
                }
                """)
            tela.email.setStyleSheet("""QLineEdit {
                                color: rgb(255, 255, 255);
                                border-bottom-right-radius: 0px;
                                border-bottom: 1px solid rgb(255, 255, 255);
                                background-color: rgba(0, 0, 0, 0);
                                padding: 5px;
                                }
                                """)
            tela.text_area.setStyleSheet("""QPlainTextEdit {
                                                color: rgb(255, 255, 255);
                                                border-radius: 3px;
                                                border: 1px solid rgb(255, 255, 255);
                                                background-color: rgba(0, 0, 0, 0);
                                                padding: 5px;
                                                }
                                                """)
            tela.text_area.clear()
            tela.email.clear()
            tela.Assunto.clear()


def fn_dados(tela, list):
    tela.lanome.setText(f"{list['Nome']}")
    tela.laloja.setText(f"{list['Loja']}")
    tela.lasenha.setText(f"{list['Senha']}")

    if list['Salvar'] is True:
        tela.lasv.setChecked(True)
    else:
        tela.lasv.setChecked(False)

    if list['Night'] is True:
        tela.btndark.setIcon(QtGui.QIcon('Icons/on.ico'))

    else:
        tela.btndark.setIcon(QtGui.QIcon('Icons/off.ico'))

    if list['CD_C'] is True:
        tela.btncadast.setIcon(QtGui.QIcon('Icons/on.ico'))

    else:
        tela.btncadast.setIcon(QtGui.QIcon('Icons/off.ico'))

    if list['IA_V'] is True:
        tela.btnintvend.setIcon(QtGui.QIcon('Icons/on.ico'))

    else:
        tela.btnintvend.setIcon(QtGui.QIcon('Icons/off.ico'))


def colorapp(tela, id):
    if id['Night']:
        tela.Area_trabalho.setStyleSheet("""background-color: rgb(62, 65, 72);
        border-top-left-radius: 5px;
        border-top-left: 10px solid rgb(32, 34, 37);""")

    if id['Night'] is False:
        tela.Area_trabalho.setStyleSheet("""background-color: rgb(153, 153, 153);
        border-top-left-radius: 5px;
        border-top-left: 10px solid rgb(32, 34, 37);""")

    animabtn_app(tela, tela.navegacao.currentIndex())



