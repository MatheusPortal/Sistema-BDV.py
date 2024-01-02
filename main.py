#13/07/2023 Criação definitiva do apicativo de gestão de estoque e vendas.

from Geral.Funções_Login import verific_login, loginD, suporte

from Geral.Funções_App import (btn_menu, dados_P, edit_perfil, show_confirmation_dialog, coletar_dadosE, \
    salvar_estoque, carregar_estoque, atualizar_tabela, verific_item, pesquisarV, verificar_e_adicionar, \
    atualiza_lista, remover_item_edit, quantidade_edit, reset_estoque, selected_payment, finalizar_pedido,
                               salvar_vendas, carregar_vendas, status_pix, payment_id, limpar_qr_code, cancel_pay)

from Geral.Interface_Code import fn_dados, colorapp, animabtn_app

from Geral.Outros import open_printer_selector, on_closing, conectar_maquininha, salvar_dados, carregar_dados, \
    on_cl_gl, criar_interface, finalO

from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QTimer, QUrl
import sys
import os
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

temppix = 300


def contdelet(resut):
    if resut is False:
        pasta_dados_user = 'Dados_User'

        # Verifique se a pasta existe
        if os.path.exists(pasta_dados_user) and os.path.isdir(pasta_dados_user):
            # Liste todos os arquivos na pasta
            arquivos = os.listdir(pasta_dados_user)

            # Itere sobre os arquivos e exclua-os
            for arquivo in arquivos:
                caminho_completo = os.path.join(pasta_dados_user, arquivo)
                if os.path.isfile(caminho_completo):
                    os.remove(caminho_completo)
        app.exit()


def btn_aba(tela, bnt):
    if bnt == 0:
        tela.showMinimized()

    if bnt == 1:
        error = 0

        finalO(True)

        on_closing(on_cl_gl())

        res = on_cl_gl()

        for i in res:
            if i is not None:
                error += 1

        if error <= 0:
            reset_estoque()
            salvar_dados()
            salvar_estoque()
            salvar_vendas()
            show_confirmation_dialog()
            app.closeAllWindows()
        else:
            finalO(False)
            show_confirmation_dialog('Erro: Não foi possivel fechar o aplicativo!', 2)

    if bnt == 2:
        if tela.isMaximized():
            tela.showNormal()
        else:
            tela.showMaximized()

        atualizar_tabela(tela)
        atualiza_lista(tela)


def trocatela(condi, tela):
    if condi is False and Tela_Login.isActiveWindow() is False:
        finalO(True)
        error = 0
        on_closing(on_cl_gl())
        res = on_cl_gl()

        for i in res:
            if i is not None:
                error += 1

        if error <= 0:
            reset_estoque()
            salvar_dados()
            salvar_estoque()
            salvar_vendas()
            show_confirmation_dialog()
            app.closeAllWindows()
            Tela_Login.show()

        else:
            finalO(False)
            show_confirmation_dialog('Erro: Não foi possivel fechar o aplicativo!', 2)

    if condi is True and Tela_App.isActiveWindow() is False:
        app.closeAllWindows()
        carregar_dados()
        carregar_estoque()
        carregar_vendas()
        vl = dados_P['Opacidade'] * 100

        Tela_App.show()
        atualizar_tabela(tela)
        atualiza_lista(tela)
        Tela_App.slopaci.setValue(int(vl))
        Tela_App.setWindowOpacity(dados_P['Opacidade'])
        fn_dados(Tela_App, dados_P)
        colorapp(tela, dados_P)
        animabtn_app(tela, tela.navegacao.currentIndex())


class AppFace(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi('Style/face.ui', self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.minimiza.clicked.connect(lambda: btn_aba(self, 0))
        self.closeapp.clicked.connect(lambda: btn_aba(self, 1))
        self.ampliar.clicked.connect(lambda: btn_aba(self, 2))

        self.principal.clicked.connect(lambda: btn_menu(self, self.navegacao.currentIndex(), 0))
        self.estoque.clicked.connect(lambda: btn_menu(self, self.navegacao.currentIndex(), 2))
        self.estatistica.clicked.connect(lambda: btn_menu(self, self.navegacao.currentIndex(), 1))
        self.conta.clicked.connect(lambda: btn_menu(self, self.navegacao.currentIndex(), 3))
        self.sair.clicked.connect(lambda: trocatela(btn_menu(self, self.navegacao.currentIndex(), 4), self))

        self.editc.clicked.connect(lambda: edit_perfil(self, 1))
        self.slopaci.valueChanged.connect(lambda: edit_perfil(self, 2, 'slopaci'))
        self.btndark.clicked.connect(lambda: colorapp(self, edit_perfil(self, 2, 'btndark')))
        self.btncadast.clicked.connect(lambda: edit_perfil(self, 2, 'btncadast'))
        self.btnintvend.clicked.connect(lambda: edit_perfil(self, 2, 'btnintvend'))

        self.excluc.clicked.connect(lambda: contdelet(show_confirmation_dialog('Deseja deletar a conta?', 1)))
        self.btnnotaf.clicked.connect(lambda: open_printer_selector(self))
        self.btnbanc.clicked.connect(lambda: conectar_maquininha(self))

        self.addE.clicked.connect(lambda: coletar_dadosE(self))
        self.delE.clicked.connect(lambda: verific_item(self, 0))
        self.editE.clicked.connect(lambda: verific_item(self, 1))

        self.atuaE.clicked.connect(lambda: atualizar_tabela(self))
        self.scancon.clicked.connect(lambda: criar_interface(self))

        self.verificar.clicked.connect(lambda: pesquisarV(self))
        self.add.clicked.connect(lambda: verificar_e_adicionar(self))
        self.remover.clicked.connect(lambda: remover_item_edit(self))
        self.editar.clicked.connect(lambda: quantidade_edit(self))
        self.pagar.clicked.connect(lambda: selected_payment(self))
        self.finalizar.clicked.connect(lambda: finalizar_pedido(self))
        self.cancel.clicked.connect(lambda: cancel_pay(self))

        # Inicialize clickPosition
        self.clickPosition = QtCore.QPoint(0, 0)

        self.barrapp.mouseMoveEvent = self.moveWindow
        self.barrapp.installEventFilter(self)

        # Cria um QTimer para verificar se o arquivo existe
        self.file_check_timer = QTimer()
        self.file_check_timer.timeout.connect(self.check_file_exists)
        self.file_check_timer.start(1000)  # Verifica se o arquivo existe a cada segundo (1000 milissegundos)

    def check_file_exists(self):
        global temppix
        if os.path.isfile('Pagamentos/pixqrcodegen.png') is not True:
            self.tpix.setText(f"")
            self.lotpix.setStyleSheet("""QFrame {
    background-color: rgba(0, 0, 0, 0);
    border-radius: 6px;
    }""")
            limpar_qr_code(self)
            temppix = 300

        if os.path.isfile('Pagamentos/pixqrcodegen.png') and temppix > 0:
            temppix -= 1
            vlue = status_pix(payment_id, self, temppix)

            if len(str(vlue).split()) > 1:
                if temppix <= 0 or vlue[1] <= 0:
                    if vlue[0] is not None:
                        selected_payment(self, vlue[0])
                    if temppix <= 0 or vlue[0] is False:
                        os.remove('Pagamentos/pixqrcodegen.png')
                        self.pagamento.setEnabled(True)

    def eventFilter(self, obj, event):
        if obj == self.barrapp and event.type() == QtCore.QEvent.MouseButtonDblClick:
            btn_aba(self, 2)
            return True
        return super().eventFilter(obj, event)

    def moveWindow(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.isMaximized():
                self.showNormal()
                self.move(self.pos() + event.globalPos() - self.clickPosition)

                barrapp_center = self.barrapp.mapToGlobal(
                    QtCore.QPoint(self.barrapp.width() // 2, self.barrapp.height() // 2))
                self.clickPosition = barrapp_center

                QtGui.QCursor.setPos(barrapp_center)
                event.accept()
                atualizar_tabela(self)
                atualiza_lista(self)
            else:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and not self.isMaximized():
            self.clickPosition = event.globalPos()
            event.accept()


class LoginFace(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi('Style/Login_face.ui', self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.mini.clicked.connect(lambda: Tela_Login.showMinimized())
        self.close.clicked.connect(lambda: app.closeAllWindows())

        self.duv.clicked.connect(lambda: loginD(self, self.loginD.currentIndex()))
        self.Entrar.clicked.connect(lambda: trocatela(verific_login(self, {'Nome': f'{str(self.Nome.text())}', 'Loja': f'{str(self.Loja.text())}', 'Senha': f'{str(self.Senha.text())}', 'Salvar': f'{self.salvar.isChecked()}'}, True), Tela_App))
        self.Envia.clicked.connect(lambda: suporte(self, {'Assunto': f'{self.Assunto.text()}', 'Email': f'{self.email.text()}', 'Detalhes': f'{self.text_area.toPlainText()}'}))
        self.site.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('')))
        self.disco.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('')))

        self.Cima.mouseMoveEvent = self.MoveWindow

    def MoveWindow(self, event):
        self.move(self.pos() + event.globalPos() - self.clickPosition)
        self.clickPosition = event.globalPos()
        event.accept()
        pass

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
        event.accept()
        pass


# Código principal
if __name__ == "__main__":
    try:
        os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'

        pasta_dados_user = 'Pagamentos'

        # Verifique se a pasta existe
        if os.path.exists(pasta_dados_user) and os.path.isdir(pasta_dados_user):
            # Liste todos os arquivos na pasta
            arquivos = os.listdir(pasta_dados_user)

            # Itere sobre os arquivos e exclua-os
            for arquivo in arquivos:
                caminho_completo = os.path.join(pasta_dados_user, arquivo)
                if os.path.isfile(caminho_completo):
                    os.remove(caminho_completo)

        app = QtWidgets.QApplication(sys.argv)
        Tela_Login = LoginFace()
        Tela_App = AppFace()

        # verificação de dados de usuario
        loginV = verific_login(Tela_Login)

        #abrir tela de login de acordo com a verificação
        if loginV is False:
            Tela_Login.show()

        else:
            carregar_dados()
            carregar_estoque()
            carregar_vendas()
            Tela_App.show()

            atualizar_tabela(Tela_App)
            atualiza_lista(Tela_App)
            vl = dados_P['Opacidade'] * 100
            Tela_App.slopaci.setValue(int(vl))
            Tela_App.setWindowOpacity(dados_P['Opacidade'])
            fn_dados(Tela_App, dados_P)
            colorapp(Tela_App, dados_P)
            animabtn_app(Tela_App, Tela_App.navegacao.currentIndex())

        sys.exit(app.exec_())
    except Exception as e:
        finalO(True)
        on_closing(on_cl_gl())

        reset_estoque()
        salvar_dados()
        salvar_estoque()
        salvar_vendas()
        show_confirmation_dialog(f'Não foi possivel abrir o APP {e}', 2)
        show_confirmation_dialog()


