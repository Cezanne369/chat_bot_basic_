from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

produtos = {}
carrinho = []

@app.route("/bot", methods=["POST"])
def bot():
    incoming = request.values.get('Body', '').lower()

    resp = MessagingResponse()
    msg = resp.message()

    if "produtos" in incoming:
        if not produtos:
            msg.body("⚠ Nenhum produto cadastrado ainda.")
        else:
            texto = "📦 Produtos disponíveis:\n"
            for p,v in produtos.items():
                texto += f"- {p} → R$ {v}\n"
            msg.body(texto)
    elif incoming.startswith("adicionar "):
        try:
            _, resto = incoming.split("adicionar ",1)
            nome, preco = resto.split(" por ")
            produtos[nome] = float(preco)
            msg.body(f"✔ Produto {nome} cadastrado por R$ {preco}")
        except:
            msg.body("Formato inválido. Use: adicionar Nome do Produto por 50")
    else:
        msg.body("Não entendi. Pergunte por 'produtos' ou use 'adicionar ... por ...'")

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
