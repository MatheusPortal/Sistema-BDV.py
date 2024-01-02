from Geral.Interface_Code import *
from PyQt5 import QtCore, QtGui
import os
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


def loginD(tela, face=0):
    if face == 1:
        tela.duv.setIcon(QtGui.QIcon('Icons/sup.png'))
        tela.loginD.setCurrentIndex(0)
    else:
        tela.duv.setIcon(QtGui.QIcon('Icons/login.png'))
        tela.duv.setIconSize(QtCore.QSize(25, 25))
        tela.loginD.setCurrentIndex(1)


def verific_login(tela, listname={}, status=False):
    from Geral.Funções_App import dados_P
    global dados_P

    caracter = "''!@#$%¨&*()_-+=[]{}~^´`:;/?.,<>|"

    if len(listname) > 0:
        for k, v in listname.items():
            for l in v:
                if l in caracter:
                    listname[k] = ''
                    break

    if os.path.isfile(f"Dados_User/dados_perfil"):
        userlogin = open('Dados_User/dados_perfil', 'r+')
        valor = userlogin.readline().split(':')
        compare = {}

        for i, c in enumerate(valor):
            if i % 2 == 1:
                compare[valor[i-1]] = c

        userlogin.close()
        valor.clear()

        if compare['Salvar'] is True or compare['Salvar'] == 'True':
            dados_P['Nome'] = compare['Nome']
            dados_P['Loja'] = compare['Loja']
            dados_P['Senha'] = compare['Senha']
            dados_P['Opacidade'] = compare['Opacidade']
            dados_P['Salvar'] = compare['Salvar']
            dados_P['Night'] = compare['Night']
            dados_P['CD_C'] = compare['CD_C']
            dados_P['IA_V'] = compare['IA_V']
            compare.clear()

            for k, v in dados_P.items():
                if k != 'Nome' and k != 'Loja' and k != 'Senha':
                    if k == 'Opacidade':
                        dados_P[k] = float(dados_P[k])
                    else:
                        if dados_P[k].lower() == 'true':
                            dados_P[k] = True
                        elif dados_P[k].lower() == 'false':
                            dados_P[k] = False
                        else:
                            # Lidar com outros tipos ou valores inválidos
                            pass

            return True

        else:
            errorcamp = []
            if len(listname) != 0:
                for k, v in compare.items():
                    if k != 'Salvar' and v != listname[k]:
                        errorcamp.append(v)
                        if k == 'Nome':
                            animation_faces(tela, 'login', 'Nome')

                        if k == 'Loja':
                            animation_faces(tela, 'login', 'Loja')

                        if k == 'Senha':
                            animation_faces(tela, 'login', 'Senha')
                            break

                    if k != 'Salvar' and v == listname[k]:
                        if k == 'Nome':
                            animation_faces(tela, 'login', 'NNome')

                        if k == 'Loja':
                            animation_faces(tela, 'login', 'NLoja')

                        if k == 'Senha':
                            animation_faces(tela, 'login', 'NSenha')
                            break

                if len(errorcamp) <= 0:
                    dados_P['Nome'] = listname['Nome']
                    dados_P['Loja'] = listname['Loja']
                    dados_P['Senha'] = listname['Senha']
                    dados_P['Salvar'] = listname['Salvar']
                    dados_P['Opacidade'] = compare['Opacidade']
                    dados_P['Night'] = compare['Night']
                    dados_P['CD_C'] = compare['CD_C']
                    dados_P['IA_V'] = compare['IA_V']
                    errorcamp.clear()

                    for k, v in dados_P.items():
                        if k != 'Nome' and k != 'Loja' and k != 'Senha':
                            if k == 'Opacidade':
                                dados_P[k] = float(dados_P[k])
                            else:
                                if dados_P[k].lower() == 'true':
                                    dados_P[k] = True
                                elif dados_P[k].lower() == 'false':
                                    dados_P[k] = False
                                else:
                                    # Lidar com outros tipos ou valores inválidos
                                    pass

                    userlogin = open('Dados_User/dados_perfil', 'w+')

                    for i, v in dados_P.items():
                        userlogin.writelines(f'{i}:{v}:')

                    userlogin.close()
                    return True

            else:
                animation_faces(tela, 'login', 'Geral')
                if status is False:
                    return False

    else:
        if len(listname) != 0:
            if len(listname['Nome']) == 0:
                animation_faces(tela, 'login', 'Nome')
            else:
                animation_faces(tela, 'login', 'NNome')

            if len(listname['Loja']) == 0:
                animation_faces(tela, 'login', 'Loja')
            else:
                animation_faces(tela, 'login', 'NLoja')

            if len(listname['Senha']) == 0:
                animation_faces(tela, 'login', 'Senha')
            else:
                animation_faces(tela, 'login', 'NSenha')

            if len(listname['Nome']) != 0 and len(listname['Loja']) != 0 and len(listname['Senha']) != 0:
                dados_P['Nome'] = listname['Nome']
                dados_P['Loja'] = listname['Loja']
                dados_P['Senha'] = listname['Senha']
                if listname['Salvar'] == 'True':
                    dados_P['Salvar'] = True
                else:
                    dados_P['Salvar'] = False

                try:
                    userlogin = open('Dados_User/dados_perfil', 'w+')

                    for i, v in dados_P.items():
                        userlogin.writelines(f'{i}:{v}:')
                    userlogin.close()

                    return True

                except FileExistsError:
                    animation_faces(tela, 'login', 'Geral')

        if status is False:
            return False


def suporte(tela, lista):
    erro = []

    for k, v in lista.items():
        if len(v) <= 0:
            erro.append(k)

    if len(erro) > 0:
        for v in erro:
            if v == 'Assunto':
                animation_faces(tela, 'lsuport', 'Assunto')
            if v == 'Email':
                animation_faces(tela, 'lsuport', 'Email')
            if v == 'Detalhes':
                animation_faces(tela, 'lsuport', 'Detalhes')

    else:
        animation_faces(tela, 'lsuport')


