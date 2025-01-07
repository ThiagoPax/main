from flask import Flask
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

feeds = [
    {
        "name": "Vasco",
        "url": "https://ge.globo.com/busca/?q=Vasco&order=recent&species=not%C3%ADcias"
    },
    {
        "name": "Flamengo",
        "url": "https://ge.globo.com/busca/?q=Flamengo&order=recent&species=not%C3%ADcias"
    }
]

def gerar_feed(feed):
    response = requests.get(feed["url"])
    soup = BeautifulSoup(response.text, 'html.parser')
    item_selector = "li.widget--card.widget--info"
    title_selector = "div.widget--info__title"
    description_selector = "p.widget--info__description"

    items = []
    for item in soup.select(item_selector):
        title = item.select_one(title_selector).get_text(strip=True) if item.select_one(title_selector) else "Sem título"
        description = item.select_one(description_selector).get_text(strip=True) if item.select_one(description_selector) else "Sem descrição"
        items.append(f"{title}: {description}")

    return "\n".join(items)

@app.route("/")
def home():
    resultado = []
    for feed in feeds:
        try:
            items = gerar_feed(feed)
            resultado.append(f"Feed do {feed['name']}:\n{items}\n")
        except Exception as e:
            resultado.append(f"Erro ao processar o feed {feed['name']}: {e}")
    return "OK - Feeds atualizados com sucesso!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
