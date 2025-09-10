from flask import Flask, render_template, request
import re

app = Flask(__name__)

PALABRAS_RESERVADAS = {"while", "for", "if"}

IDENTIFICADOR_REGEX = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
NUMERO_REGEX = r"^\d+(\.\d+)?$"
SIMBOLOS_VALIDOS = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '>=', '<=', '(', ')', '{', '}', ';'}

def clasificar_token(token):
    if token in PALABRAS_RESERVADAS:
        return "palabras_reservadas"
    elif token in SIMBOLOS_VALIDOS:
        return "simbolos"
    elif re.match(NUMERO_REGEX, token):
        return "numeros"
    elif re.match(IDENTIFICADOR_REGEX, token):
        return "identificadores"
    else:
        return "desconocidos"

@app.route("/", methods=["GET", "POST"])
def index():
    tokens = {
        "palabras_reservadas": [],
        "identificadores": [],
        "numeros": [],
        "simbolos": [],
        "desconocidos": []
    }
    entrada = ""

    if request.method == "POST":
        entrada = request.form["palabra"].strip()
        posibles_tokens = re.findall(r'\w+|==|!=|>=|<=|[^\s]', entrada)

        for token in posibles_tokens:
            tipo = clasificar_token(token)
            tokens[tipo].append(token)

    return render_template("index.html", tokens=tokens, entrada=entrada)

if __name__ == "__main__":
    app.run(debug=True)
