import hashlib
import wx
import mysql.connector
from mysql.connector import Error


MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "140606"
MYSQL_DATABASE = "sistema_cadastro"


def conectar_banco():
    conexao_inicial = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    cursor_inicial = conexao_inicial.cursor()
    cursor_inicial.execute(
        f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    cursor_inicial.close()
    conexao_inicial.close()

    conexao = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome_usuario VARCHAR(100) NOT NULL UNIQUE,
            hash_senha CHAR(64) NOT NULL
        )
    """)
    conexao.commit()
    cursor.close()
    return conexao


def gerar_hash(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def carregar_usuarios():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome_usuario, hash_senha FROM usuarios")
    usuarios = {nome: hash_senha for nome, hash_senha in cursor.fetchall()}
    cursor.close()
    conexao.close()
    return usuarios


def criar_usuario_padrao():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    quantidade = cursor.fetchone()[0]
    if quantidade == 0:
        cursor.execute(
            "INSERT INTO usuarios (nome_usuario, hash_senha) VALUES (%s, %s)",
            ("admin", gerar_hash("1234"))
        )
    conexao.commit()
    cursor.close()
    conexao.close()


def verificar_login(usuario, senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT hash_senha FROM usuarios WHERE nome_usuario = %s",
        (usuario,)
    )
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None and resultado[0] == gerar_hash(senha)


def trocar_senha(usuario, nova_senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE usuarios SET hash_senha = %s WHERE nome_usuario = %s",
        (gerar_hash(nova_senha), usuario)
    )
    alterou = cursor.rowcount > 0
    conexao.commit()
    cursor.close()
    conexao.close()
    return alterou


class Alterarsenha(wx.Frame):
    def __init__(self):
        super().__init__(
            None,
            title="Alterar Senha",
            size=(500, 400)
        )
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(
            wx.Colour(30, 50, 70))

        self.titulo = wx.StaticText(
            self.panel,
            label="Alterar Senha"
        )
        self.titulo.SetForegroundColour(
            wx.Colour(255, 255, 255)
        )
        self.font = wx.Font(
            20,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Times New Roman"
        )

        self.titulo.SetFont(self.font)

        self.usuario = wx.StaticText(
            self.panel,
            label="Digite seu usuário",
            size=(170, -1),
        )

        self.NovaSenha = wx.StaticText(
            self.panel,
            label="Digite sua nova senha",
            size=(170, -1),
        )

        self.confisenha = wx.StaticText(
            self.panel,
            label="Confirme sua nova senha",
            size=(170, -1),
        )

        self.botalterar = wx.Button(
            self.panel,
            label="Alterar senha"
        )

        self.usuario.SetForegroundColour(
            wx.Colour(255, 255, 255)
        )

        self.NovaSenha.SetForegroundColour(
            wx.Colour(255, 255, 255)
        )

        self.confisenha.SetForegroundColour(
            wx.Colour(255, 255, 255)
        )

        self.botalterar.SetForegroundColour(
            wx.Colour(0, 0, 0)
        )

        self.font = wx.Font(
            10,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Times New Roman"
        )

        self.usuario.SetFont(self.font)
        self.NovaSenha.SetFont(self.font)
        self.confisenha.SetFont(self.font)
        self.botalterar.SetFont(self.font)

        self.usuario2 = wx.TextCtrl(
            self.panel,
            size=(200, -1)
        )

        self.novasenha2 = wx.TextCtrl(
            self.panel,
            size=(200, -1),
            style=wx.TE_PASSWORD
        )

        self.confisenha2 = wx.TextCtrl(
            self.panel,
            size=(200, -1),
            style=wx.TE_PASSWORD
        )

        self.botalterar.Bind(
            wx.EVT_BUTTON,
            self.alterar_senha,
        )

        self.sizer_principal = wx.BoxSizer(wx.VERTICAL)

        self.sizer_principal.Add(
            self.titulo,
            0,
            wx.ALL | wx.CENTER,
            10,
        )

        self.sizer_usuario = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer_usuario.Add(
            self.usuario,
            0,
            wx.CENTER | wx.RIGHT,
            10,
        )

        self.sizer_usuario.Add(
            self.usuario2,
            0,
            wx.CENTER
        )

        self.sizer_principal.Add(
            self.sizer_usuario,
            0,
            wx.CENTER | wx.TOP,
            10,
        )

        self.sizer_nova_senha = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer_nova_senha.Add(
            self.NovaSenha,
            0,
            wx.CENTER | wx.RIGHT,
            10,
        )

        self.sizer_nova_senha.Add(
            self.novasenha2,
            0,
            wx.CENTER
        )

        self.sizer_principal.Add(
            self.sizer_nova_senha,
            0,
            wx.CENTER | wx.TOP,
            10,
        )

        self.sizer_confisenha = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer_confisenha.Add(
            self.confisenha,
            0,
            wx.CENTER | wx.RIGHT,
            10
        )

        self.sizer_confisenha.Add(
            self.confisenha2,
            0,
            wx.CENTER
        )

        self.sizer_principal.Add(
            self.sizer_confisenha,
            0,
            wx.CENTER | wx.TOP,
            10
        )

        self.sizer_principal.Add(
            self.botalterar,
            0,
            wx.CENTER | wx.TOP,
            20
        )

        self.panel.SetSizer(self.sizer_principal)
        self.Centre()

    def alterar_senha(self, evento):
        usuario = self.usuario2.GetValue().strip()
        nova_senha = self.novasenha2.GetValue()
        confirmacao = self.confisenha2.GetValue()

        if not usuario or not nova_senha or not confirmacao:
            wx.MessageBox(
                "Preencha todos os campos.",
                "Atenção",
                wx.OK | wx.ICON_WARNING
            )
            return

        if usuario not in carregar_usuarios():
            wx.MessageBox(
                "Usuário não encontrado.",
                "Erro",
                wx.OK | wx.ICON_ERROR
            )
            return

        if nova_senha != confirmacao:
            wx.MessageBox(
                "As senhas não conferem.",
                "Erro",
                wx.OK | wx.ICON_ERROR
            )
            self.confisenha2.Clear()
            return

        trocar_senha(usuario, nova_senha)
        wx.MessageBox(
            "Senha alterada com sucesso!",
            "Sucesso",
            wx.OK | wx.ICON_INFORMATION
        )
        self.Close()



class JanelaPrincipal(wx.Frame):
    def __init__(self, janela_login, usuario):
        super().__init__(
            None,
            title="Sistema",
            size=(500, 400)
        )
        self.janela_login = janela_login
        self.sair_para_login = False

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(
            wx.Colour(30, 50, 70))

        self.titulo = wx.StaticText(
            self.panel,
            label=f"Bem-vindo, {usuario}!"
        )
        self.titulo.SetForegroundColour(
            wx.Colour(255, 255, 255)
        )
        self.titulo.SetFont(
            wx.Font(
                20,
                wx.FONTFAMILY_ROMAN,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD,
                faceName="Times New Roman"
            )
        )

        self.botsair = wx.Button(
            self.panel,
            label="Sair"
        )
        self.botsair.SetForegroundColour(
            wx.Colour(0, 0, 0)
        )
        self.botsair.SetFont(
            wx.Font(
                10,
                wx.FONTFAMILY_ROMAN,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD,
                faceName="Times New Roman"
            )
        )
        self.botsair.Bind(wx.EVT_BUTTON, self.sair)

        self.sizer_principal = wx.BoxSizer(wx.VERTICAL)

        self.sizer_principal.AddStretchSpacer(1)

        self.sizer_principal.Add(
            self.titulo,
            0,
            wx.ALL | wx.CENTER,
            10,
        )

        self.sizer_principal.Add(
            self.botsair,
            0,
            wx.ALL | wx.CENTER,
            10,
        )

        self.sizer_principal.AddStretchSpacer(1)

        self.panel.SetSizer(self.sizer_principal)
        self.Bind(wx.EVT_CLOSE, self.ao_fechar)
        self.Centre()

    def sair(self, evento):
        self.sair_para_login = True
        self.Close()

    def ao_fechar(self, evento):
        if self.sair_para_login:
            self.janela_login.Show()
        else:
            self.janela_login.Destroy()
        evento.Skip()



class Janela(wx.Frame):
    def __init__(self):
        super().__init__(
            None,
            title="Cadastro",
            size=(500, 400)
        )
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(
            wx.Colour(30, 50, 70))

        self.titulo = wx.StaticText(
            self.panel,
            label="Sistema de Cadastro"
        )
        self.titulo.SetForegroundColour(
            wx.Colour(255, 255, 255)
        )
        self.font = wx.Font(
            20,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Times New Roman"
        )

        self.titulo.SetFont(self.font)

        self.login1 = wx.StaticText(
            self.panel,
            label="Usuário"
        )
        self.login1.SetForegroundColour(
            wx.Colour(255, 255, 255)
        )

        self.font = wx.Font(
            10,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Times New Roman"
        )

        self.login1.SetFont(self.font)

        self.senha = wx.StaticText(
            self.panel,
            label="Senha"
        )
        self.senha.SetForegroundColour(
            wx.Colour(255, 255, 255)
        )
        self.font = wx.Font(
            10,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Times New Roman"
        )

        self.senha.SetFont(self.font)

        self.login = wx.TextCtrl(self.panel)

        self.senha2 = wx.TextCtrl(
            self.panel,
            style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER
        )

        self.botao = wx.Button(
            self.panel,
            label="Entrar"
        )

        self.resetsenha = wx.Button(
            self.panel,
            label="Esqueceu sua senha?"
        )

        self.botao.SetForegroundColour(
            wx.Colour(0, 0, 0)
        )

        self.resetsenha.SetForegroundColour(
            wx.Colour(0, 0, 0)
        )

        self.font = wx.Font(
            10,
            wx.FONTFAMILY_ROMAN,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            faceName="Times New Roman"
        )

        self.botao.SetFont(self.font)
        self.resetsenha.SetFont(self.font)

        self.botao.Bind(
            wx.EVT_BUTTON,
            self.fazer_login,
        )

        self.senha2.Bind(
            wx.EVT_TEXT_ENTER,
            self.fazer_login,
        )

        self.resetsenha.Bind(
            wx.EVT_BUTTON,
            self.abrir_resetsenha,
        )

        self.sizer_principal = wx.BoxSizer(wx.VERTICAL)

        self.sizer_principal.Add(
            self.titulo,
            0,
            wx.ALL | wx.CENTER,
            10,
        )

        self.sizer_secundario = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer_secundario.Add(
            self.login1,
            0,
            wx.ALL | wx.CENTER,
            10,

        )

        self.sizer_secundario.Add(
            self.login,
            0,
            wx.ALL | wx.CENTER,
            10,
        )

        self.sizer_secundario.Add(
            self.senha,
            0,
            wx.ALL | wx.CENTER,
            10,
        )

        self.sizer_secundario.Add(
            self.senha2,
            0,
            wx.ALL | wx.CENTER,
            10,
        )

        self.sizer_principal.Add(
            self.sizer_secundario,
            0,
            wx.CENTER,
        )

        self.sizer_principal.Add(
            self.botao,
            0,
            wx.ALL | wx.CENTER,
            10,
        )

        self.sizer_principal.Add(
            self.resetsenha,
            0,
            wx.ALL | wx.CENTER,
            10,
        )

        self.panel.SetSizer(self.sizer_principal)
        self.SetMinSize((530, 500))
        self.Centre()

    def fazer_login(self, evento):
        usuario = self.login.GetValue().strip()
        senha = self.senha2.GetValue()

        if not usuario or not senha:
            wx.MessageBox(
                "Preencha usuário e senha.",
                "Atenção",
                wx.OK | wx.ICON_WARNING
            )
            return

        if verificar_login(usuario, senha):
            self.login.Clear()
            self.senha2.Clear()
            self.Hide()
            principal = JanelaPrincipal(self, usuario)
            principal.Show()
        else:
            wx.MessageBox(
                "Usuário ou senha incorretos.",
                "Erro",
                wx.OK | wx.ICON_ERROR
            )
            self.senha2.Clear()

    def abrir_resetsenha(self, evento):
        janela = Alterarsenha()
        janela.Show()


if __name__ == "__main__":
    app = wx.App(False)
    try:
        criar_usuario_padrao()
        janela = Janela()
        janela.Show()
        app.MainLoop()
    except Error as erro:
        wx.MessageBox(
            "Nao foi possivel conectar ao MySQL.\n\n"
            "Confira se o servidor MySQL esta iniciado e se "
            "MYSQL_HOST, MYSQL_USER e MYSQL_PASSWORD estao corretos.\n\n"
            f"Detalhes: {erro}",
            "Erro de conexao com o banco",
            wx.OK | wx.ICON_ERROR
        )
