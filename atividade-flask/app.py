from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib
import hmac

app = Flask(__name__)
app.secret_key = "chave-secreta-atividade"
BANCO = "atividade_flask.db"


def calcular_hash(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def conectar_banco():
    conexao = sqlite3.connect(BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    with conectar_banco() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                nome TEXT NOT NULL
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS perfil (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS projetos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                tecnologia TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        usuario = conexao.execute(
            "SELECT id FROM usuarios WHERE usuario = ?",
            ("aluno_exemplo",)
        ).fetchone()

        if usuario is None:
            senha_hash = calcular_hash("Aula@1234")

            cursor = conexao.execute(
                """
                INSERT INTO usuarios (usuario, senha_hash, nome)
                VALUES (?, ?, ?)
                """,
                ("aluno_exemplo", senha_hash, "Aluno Exemplo")
            )

            usuario_id = cursor.lastrowid

            conexao.execute(
                """
                INSERT INTO perfil (usuario_id, titulo, descricao)
                VALUES (?, ?, ?)
                """,
                (
                    usuario_id,
                    "Estudante de Tecnologia",
                    "Estudante do Ensino Médio Técnico interessado em programação e desenvolvimento web."
                )
            )

            conexao.execute(
                """
                INSERT INTO projetos
                (usuario_id, nome, descricao, tecnologia)
                VALUES (?, ?, ?, ?)
                """,
                (
                    usuario_id,
                    "Sistema Flask",
                    "Sistema web com autenticação, hash de senha e páginas restritas.",
                    "Python, Flask e SQLite"
                )
            )

            conexao.execute(
                """
                INSERT INTO projetos
                (usuario_id, nome, descricao, tecnologia)
                VALUES (?, ?, ?, ?)
                """,
                (
                    usuario_id,
                    "GreenMove",
                    "Projeto relacionado à sustentabilidade e tecnologia.",
                    "Python, HTML, CSS e JavaScript"
                )
            )

            conexao.commit()


@app.route("/")
def pagina_inicial():
    return render_template(
        "pagina.html",
        usuario=session.get("usuario"),
        nome=session.get("nome")
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    mensagem = None

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        hash_tentativa = calcular_hash(senha)

        with conectar_banco() as conexao:
            registro = conexao.execute(
                """
                SELECT id, usuario, nome, senha_hash
                FROM usuarios
                WHERE usuario = ?
                """,
                (usuario,)
            ).fetchone()

        if registro is None:
            mensagem = "Usuário ou senha incorretos."

        elif hmac.compare_digest(
            hash_tentativa,
            registro["senha_hash"]
        ):
            session["usuario_id"] = registro["id"]
            session["usuario"] = registro["usuario"]
            session["nome"] = registro["nome"]
            return redirect(url_for("perfil"))

        else:
            mensagem = "Usuário ou senha incorretos."

    return render_template("login.html", mensagem=mensagem)


@app.route("/perfil")
def perfil():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    with conectar_banco() as conexao:
        dados = conexao.execute(
            """
            SELECT titulo, descricao
            FROM perfil
            WHERE usuario_id = ?
            """,
            (session["usuario_id"],)
        ).fetchone()

    return render_template(
        "perfil.html",
        perfil=dados,
        nome=session["nome"]
    )


@app.route("/projetos")
def projetos():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    with conectar_banco() as conexao:
        dados = conexao.execute(
            """
            SELECT nome, descricao, tecnologia
            FROM projetos
            WHERE usuario_id = ?
            """,
            (session["usuario_id"],)
        ).fetchall()

    return render_template(
        "projetos.html",
        projetos=dados,
        nome=session["nome"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("pagina_inicial"))


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
