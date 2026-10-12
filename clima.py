
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from collections import Counter

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def buscar_clima(cidade):
    if not API_KEY:
        raise ValueError(
            "Configure OPENWEATHER_API_KEY no arquivo .env"
        )

    url = "https://api.openweathermap.org/data/2.5/forecast"

    parametros = {
        "q": f"{cidade},BR",
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    try:
        resposta = requests.get(
            url,
            params=parametros,
            timeout=15
        )

        resposta.raise_for_status()
        dados = resposta.json()

        nome_cidade = dados["city"]["name"]
        fuso = dados["city"]["timezone"]

        agora_local = (
            datetime.now(timezone.utc)
            + timedelta(seconds=fuso)
        )
        data_hoje = agora_local.date()

        previsoes = []

        for item in dados["list"]:
            horario_local = (
                datetime.fromtimestamp(
                    item["dt"],
                    tz=timezone.utc
                )
                + timedelta(seconds=fuso)
            )

            if horario_local.date() == data_hoje:
                previsoes.append(item)

        if not previsoes:
            raise ValueError(
                "Não encontrei previsões para hoje."
            )

        temperaturas = [
            item["main"]["temp"]
            for item in previsoes
        ]

        descricoes = [
            item["weather"][0]["description"]
            for item in previsoes
        ]

        descricao_principal = Counter(
            descricoes
        ).most_common(1)[0][0]

        chance_chuva = max(
            item.get("pop", 0)
            for item in previsoes
        ) * 100

        temperatura_minima = min(temperaturas)
        temperatura_maxima = max(temperaturas)

        mensagem = (
            f"🌤️ KLYMOR — PREVISÃO DO DIA\n\n"
            f"📍 Cidade: {nome_cidade}\n"
            f"📅 Data: {data_hoje.strftime('%d/%m/%Y')}\n\n"
            f"🌡️ Temperatura mínima prevista: "
            f"{temperatura_minima:.1f} °C\n"
            f"🔥 Temperatura máxima prevista: "
            f"{temperatura_maxima:.1f} °C\n"
            f"🌦️ Condição predominante: "
            f"{descricao_principal.capitalize()}\n"
            f"🌧️ Maior probabilidade de chuva: "
            f"{chance_chuva:.0f}%\n\n"
            f"🤖 Previsão gerada pelo KLYMOR."
        )

        return mensagem

    except requests.exceptions.HTTPError as erro:
        if erro.response is not None:
            if erro.response.status_code == 404:
                raise ValueError("Cidade não encontrada.") from erro

            if erro.response.status_code == 401:
                raise ValueError(
                    "Chave da OpenWeatherMap inválida."
                ) from erro

        raise RuntimeError(
            f"Erro HTTP ao consultar o clima: {erro}"
        ) from erro

    except requests.exceptions.RequestException as erro:
        raise RuntimeError(
            f"Erro de conexão com a API: {erro}"
        ) from erro


if __name__ == "__main__":
    print(buscar_clima("Osasco"))
