
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def enviar_mensagem(mensagem):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise ValueError("Configure o token e o chat ID no arquivo .env")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    resposta = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": mensagem
        },
        timeout=15
    )

    resposta.raise_for_status()
    dados = resposta.json()

    if not dados.get("ok"):
        raise RuntimeError("O Telegram não confirmou o envio.")

    print("Mensagem enviada com sucesso!")
