
from datetime import datetime
from pathlib import Path
import math
import os
import secrets
import sqlite3

from flask import Flask, render_template, request, redirect, flash, url_for


BASE_DIR = Path(__file__).resolve().parent
DB_NAME = BASE_DIR / "gameleira.db"

app = Flask(__name__)
app.secret_key = os.environ.get("GAMELEIRA_SECRET_KEY") or secrets.token_hex(32)

STATUS_VALIDOS = ["Pendente", "Em andamento", "Concluída"]
PAGAMENTOS_VALIDOS = ["Pendente", "Pago"]
MATERIAIS_VALIDOS = [
    "Papel", "Papelão", "Plástico", "Metal",
    "Vidro", "Eletrônicos", "Outros"
]


def conectar():
    banco = sqlite3.connect(DB_NAME)
    banco.row_factory = sqlite3.Row
    banco.execute("PRAGMA foreign_keys = ON")
    return banco


def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def criar_banco():
    banco = conectar()

    banco.executescript("""
        CREATE TABLE IF NOT EXISTS coletas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            catador TEXT NOT NULL,
            material TEXT NOT NULL,
            peso_kg REAL NOT NULL CHECK (peso_kg > 0),
            valor_kg REAL NOT NULL DEFAULT 0 CHECK (valor_kg >= 0),
            valor_total REAL NOT NULL DEFAULT 0,
            local_coleta TEXT NOT NULL,
            rota TEXT,
            data_coleta TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            pagamento_status TEXT NOT NULL DEFAULT 'Pendente',
            observacoes TEXT,
            data_cadastro TEXT NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coleta_id INTEGER,
            acao TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data_hora TEXT NOT NULL,
            FOREIGN KEY (coleta_id)
                REFERENCES coletas(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_coletas_status
        ON coletas(status);

        CREATE INDEX IF NOT EXISTS idx_coletas_catador
        ON coletas(catador);

        CREATE INDEX IF NOT EXISTS idx_historico_coleta
        ON historico(coleta_id);
    """)

    colunas = {
        linha[1]
        for linha in banco.execute(
            "PRAGMA table_info(coletas)"
        ).fetchall()
    }

    if "pagamento_status" not in colunas:
        banco.execute("""
            ALTER TABLE coletas
            ADD COLUMN pagamento_status TEXT
            NOT NULL DEFAULT 'Pendente'
        """)

    chaves = banco.execute(
        "PRAGMA foreign_key_list(historico)"
    ).fetchall()

    possui_chave = any(
        linha[2] == "coletas" and linha[3] == "coleta_id"
        for linha in chaves
    )

    if not possui_chave:
        orfaos = banco.execute("""
            SELECT COUNT(*)
            FROM historico h
            LEFT JOIN coletas c ON c.id = h.coleta_id
            WHERE h.coleta_id IS NOT NULL
            AND c.id IS NULL
        """).fetchone()[0]

        if orfaos:
            banco.close()
            raise RuntimeError(
                "Existem registros de histórico sem coleta correspondente. "
                "Faça backup do banco antes de corrigir esses registros."
            )

        banco.execute("""
            CREATE TABLE historico_novo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coleta_id INTEGER,
                acao TEXT NOT NULL,
                descricao TEXT NOT NULL,
                data_hora TEXT NOT NULL,
                FOREIGN KEY (coleta_id)
                    REFERENCES coletas(id) ON DELETE CASCADE
            )
        """)

        banco.execute("""
            INSERT INTO historico_novo
            (id, coleta_id, acao, descricao, data_hora)
            SELECT id, coleta_id, acao, descricao, data_hora
            FROM historico
        """)

        banco.execute("DROP TABLE historico")
        banco.execute(
            "ALTER TABLE historico_novo RENAME TO historico"
        )

    banco.execute("""
        CREATE INDEX IF NOT EXISTS idx_historico_coleta
        ON historico(coleta_id)
    """)

    banco.commit()
    banco.close()


def registrar_historico(banco, coleta_id, acao, descricao):
    banco.execute(
        """
        INSERT INTO historico
        (coleta_id, acao, descricao, data_hora)
        VALUES (?, ?, ?, ?)
        """,
        (coleta_id, acao, descricao, agora())
    )


def dados_formulario(form):
    catador = form.get("catador", "").strip()
    material = form.get("material", "").strip()
    local = form.get("local_coleta", "").strip()
    rota = form.get("rota", "").strip()
    data_coleta = form.get("data_coleta", "").strip()
    status = form.get("status", "Pendente").strip()
    pagamento_status = form.get(
        "pagamento_status", "Pendente"
    ).strip()
    observacoes = form.get("observacoes", "").strip()

    try:
        peso = float(
            form.get("peso_kg", "0").replace(",", ".")
        )
        valor_kg = float(
            form.get("valor_kg", "0").replace(",", ".")
        )
    except ValueError:
        raise ValueError(
            "Peso e valor por quilo precisam ser números válidos."
        )

    if not catador or not material or not local or not data_coleta:
        raise ValueError("Preencha os campos obrigatórios.")

    try:
        data_validada = datetime.strptime(
            data_coleta, "%Y-%m-%d"
        )

        if data_validada.strftime("%Y-%m-%d") != data_coleta:
            raise ValueError

    except ValueError:
        raise ValueError(
            "Informe uma data válida para a coleta."
        )

    if material not in MATERIAIS_VALIDOS:
        raise ValueError("Selecione um material válido.")

    if not math.isfinite(peso) or not math.isfinite(valor_kg):
        raise ValueError(
            "Peso e valor por quilo precisam ser números finitos."
        )

    if peso <= 0 or valor_kg < 0:
        raise ValueError(
            "O peso deve ser maior que zero e o valor por quilo "
            "não pode ser negativo."
        )

    if status not in STATUS_VALIDOS:
        raise ValueError("Selecione uma situação válida.")

    if pagamento_status not in PAGAMENTOS_VALIDOS:
        raise ValueError("Selecione uma situação de pagamento válida.")

    produto = peso * valor_kg

    if not math.isfinite(produto):
        raise ValueError(
            "O valor total calculado está fora do limite permitido."
        )

    total = round(produto, 2)

    return (
        catador, material, peso, valor_kg, total,
        local, rota, data_coleta, status,
        pagamento_status, observacoes
    )


@app.route("/")
def inicio():
    banco = conectar()

    status = request.args.get("status", "")
    busca = request.args.get("busca", "").strip()

    sql = "SELECT * FROM coletas WHERE ativo=1"
    parametros = []

    if status in STATUS_VALIDOS:
        sql += " AND status=?"
        parametros.append(status)

    if busca:
        sql += """
            AND (
                catador LIKE ?
                OR material LIKE ?
                OR local_coleta LIKE ?
                OR rota LIKE ?
            )
        """
        parametros.extend([f"%{busca}%"] * 4)

    sql += " ORDER BY date(data_coleta) DESC, id DESC"

    coletas = banco.execute(sql, parametros).fetchall()

    indicadores = {
        "total": banco.execute(
            "SELECT COUNT(*) FROM coletas WHERE ativo=1"
        ).fetchone()[0],

        "pendentes": banco.execute(
            "SELECT COUNT(*) FROM coletas WHERE ativo=1 "
            "AND status='Pendente'"
        ).fetchone()[0],

        "andamento": banco.execute(
            "SELECT COUNT(*) FROM coletas WHERE ativo=1 "
            "AND status='Em andamento'"
        ).fetchone()[0],

        "concluidas": banco.execute(
            "SELECT COUNT(*) FROM coletas WHERE ativo=1 "
            "AND status='Concluída'"
        ).fetchone()[0],

        "peso": banco.execute(
            "SELECT COALESCE(SUM(peso_kg),0) FROM coletas "
            "WHERE ativo=1 AND status='Concluída'"
        ).fetchone()[0],

        "valor": banco.execute(
            "SELECT COALESCE(SUM(valor_total),0) FROM coletas "
            "WHERE ativo=1 AND status='Concluída'"
        ).fetchone()[0],

        "a_pagar": banco.execute(
            "SELECT COALESCE(SUM(valor_total),0) FROM coletas "
            "WHERE ativo=1 AND pagamento_status='Pendente'"
        ).fetchone()[0],
    }

    banco.close()

    return render_template(
        "index.html",
        coletas=coletas,
        indicadores=indicadores,
        status_selecionado=status,
        busca=busca,
        materiais=MATERIAIS_VALIDOS,
        status_validos=STATUS_VALIDOS,
        pagamentos_validos=PAGAMENTOS_VALIDOS,
        hoje=datetime.now().strftime("%Y-%m-%d")
    )


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    try:
        dados = dados_formulario(request.form)
    except ValueError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("inicio"))

    banco = conectar()

    cursor = banco.execute("""
        INSERT INTO coletas
        (
            catador, material, peso_kg, valor_kg, valor_total,
            local_coleta, rota, data_coleta, status,
            pagamento_status, observacoes, data_cadastro
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (*dados, agora()))

    coleta_id = cursor.lastrowid

    registrar_historico(
        banco,
        coleta_id,
        "Cadastro",
        f"Coleta cadastrada para {dados[0]}: "
        f"{dados[2]:.2f} kg de {dados[1]} em {dados[5]}."
    )

    banco.commit()
    banco.close()

    flash("Coleta cadastrada com sucesso!", "sucesso")
    return redirect(url_for("inicio"))


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    banco = conectar()

    coleta = banco.execute(
        "SELECT * FROM coletas WHERE id=? AND ativo=1",
        (id,)
    ).fetchone()

    if coleta is None:
        banco.close()
        return "Coleta não encontrada.", 404

    if request.method == "POST":
        try:
            dados = dados_formulario(request.form)
        except ValueError as erro:
            banco.close()
            flash(str(erro), "erro")
            return redirect(url_for("editar", id=id))

        banco.execute("""
            UPDATE coletas
            SET catador=?, material=?, peso_kg=?, valor_kg=?,
                valor_total=?, local_coleta=?, rota=?, data_coleta=?,
                status=?, pagamento_status=?, observacoes=?
            WHERE id=?
        """, (*dados, id))

        registrar_historico(
            banco,
            id,
            "Edição",
            f"Registro atualizado. Catador: {dados[0]}; "
            f"material: {dados[1]}; peso: {dados[2]:.2f} kg."
        )

        banco.commit()
        banco.close()

        flash("Coleta atualizada com sucesso!", "sucesso")
        return redirect(url_for("inicio"))

    banco.close()

    return render_template(
        "editar.html",
        coleta=coleta,
        materiais=MATERIAIS_VALIDOS,
        status_validos=STATUS_VALIDOS,
        pagamentos_validos=PAGAMENTOS_VALIDOS
    )


@app.route("/atualizar-status/<int:id>", methods=["POST"])
def atualizar_status(id):
    status = request.form.get("status", "")

    if status not in STATUS_VALIDOS:
        flash("Situação inválida.", "erro")
        return redirect(url_for("inicio"))

    banco = conectar()

    coleta = banco.execute(
        "SELECT status FROM coletas WHERE id=? AND ativo=1",
        (id,)
    ).fetchone()

    if coleta is None:
        banco.close()
        return "Coleta não encontrada.", 404

    anterior = coleta["status"]

    if anterior != status:
        banco.execute(
            "UPDATE coletas SET status=? WHERE id=?",
            (status, id)
        )

        registrar_historico(
            banco,
            id,
            "Alteração de situação",
            f"Situação alterada de {anterior} para {status}."
        )

    banco.commit()
    banco.close()

    flash("Situação atualizada.", "sucesso")
    return redirect(url_for("inicio"))


@app.route("/atualizar-pagamento/<int:id>", methods=["POST"])
def atualizar_pagamento(id):
    situacao = request.form.get("pagamento_status", "")

    if situacao not in PAGAMENTOS_VALIDOS:
        flash("Situação de pagamento inválida.", "erro")
        return redirect(url_for("inicio"))

    banco = conectar()

    coleta = banco.execute(
        "SELECT pagamento_status FROM coletas "
        "WHERE id=? AND ativo=1",
        (id,)
    ).fetchone()

    if coleta is None:
        banco.close()
        return "Coleta não encontrada.", 404

    anterior = coleta["pagamento_status"]

    if anterior != situacao:
        banco.execute(
            "UPDATE coletas SET pagamento_status=? WHERE id=?",
            (situacao, id)
        )

        registrar_historico(
            banco,
            id,
            "Pagamento",
            f"Pagamento alterado de {anterior} para {situacao}."
        )

    banco.commit()
    banco.close()

    flash("Pagamento atualizado.", "sucesso")
    return redirect(url_for("inicio"))


@app.route("/rotas")
def rotas():
    banco = conectar()

    registros = banco.execute("""
        SELECT
            COALESCE(NULLIF(rota,''),'Sem rota definida') AS nome_rota,
            COUNT(*) AS quantidade,
            COALESCE(SUM(peso_kg),0) AS peso,
            SUM(
                CASE WHEN status='Concluída' THEN 1 ELSE 0 END
            ) AS concluidas
        FROM coletas
        WHERE ativo=1
        GROUP BY COALESCE(NULLIF(rota,''),'Sem rota definida')
        ORDER BY nome_rota
    """).fetchall()

    banco.close()

    return render_template("rotas.html", rotas=registros)


@app.route("/historico")
def historico_geral():
    banco = conectar()

    registros = banco.execute("""
        SELECT h.*, c.catador, c.material, c.peso_kg
        FROM historico h
        LEFT JOIN coletas c ON c.id=h.coleta_id
        ORDER BY h.id DESC
    """).fetchall()

    arquivadas = banco.execute(
        "SELECT * FROM coletas WHERE ativo=0 ORDER BY id DESC"
    ).fetchall()

    banco.close()

    return render_template(
        "historico_geral.html",
        registros=registros,
        arquivadas=arquivadas
    )


@app.route("/historico/<int:id>")
def historico_coleta(id):
    banco = conectar()

    coleta = banco.execute(
        "SELECT * FROM coletas WHERE id=?",
        (id,)
    ).fetchone()

    registros = banco.execute(
        "SELECT * FROM historico WHERE coleta_id=? ORDER BY id DESC",
        (id,)
    ).fetchall()

    banco.close()

    if coleta is None:
        return "Coleta não encontrada.", 404

    return render_template(
        "historico.html",
        coleta=coleta,
        registros=registros
    )


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    banco = conectar()

    coleta = banco.execute(
        "SELECT * FROM coletas WHERE id=? AND ativo=1",
        (id,)
    ).fetchone()

    if coleta is None:
        banco.close()
        return "Coleta não encontrada.", 404

    banco.execute(
        "UPDATE coletas SET ativo=0 WHERE id=?",
        (id,)
    )

    registrar_historico(
        banco,
        id,
        "Arquivamento",
        f"Registro arquivado: {coleta['catador']} - "
        f"{coleta['material']} - {coleta['peso_kg']:.2f} kg."
    )

    banco.commit()
    banco.close()

    flash(
        "Coleta arquivada; o histórico foi preservado.",
        "sucesso"
    )

    return redirect(url_for("inicio"))


@app.route("/excluir-permanente/<int:id>", methods=["POST"])
def excluir_permanente(id):
    banco = conectar()

    try:
        banco.execute("BEGIN")

        coleta = banco.execute(
            "SELECT id FROM coletas WHERE id=? AND ativo=0",
            (id,)
        ).fetchone()

        if coleta is None:
            banco.rollback()
            flash(
                "Registro não encontrado ou ainda não está arquivado.",
                "erro"
            )

        else:
            cursor = banco.execute(
                "DELETE FROM coletas WHERE id=? AND ativo=0",
                (id,)
            )

            if cursor.rowcount != 1:
                banco.rollback()
                flash(
                    "Não foi possível confirmar a exclusão do registro.",
                    "erro"
                )
            else:
                banco.commit()
                flash(
                    f"Coleta #{id} e histórico excluídos permanentemente.",
                    "sucesso"
                )

    except sqlite3.Error:
        banco.rollback()
        flash("Não foi possível excluir o registro.", "erro")

    finally:
        banco.close()

    return redirect(url_for("historico_geral"))


@app.template_filter("moeda")
def moeda(valor):
    return (
        "R$ {:,.2f}".format(float(valor or 0))
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


criar_banco()


if __name__ == "__main__":
    app.run(debug=False)
