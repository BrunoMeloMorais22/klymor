
from clima import buscar_clima
from telegram import enviar_mensagem


def main():
    print("Inicializando KLYMOR...")

    try:
        mensagem = buscar_clima("Osasco")
        print(mensagem)

        enviar_mensagem(mensagem)

        print("Previsão enviada ao Telegram!")

    except Exception as erro:
        print(f"Erro ao executar KLYMOR: {erro}")


if __name__ == "__main__":
    main()
