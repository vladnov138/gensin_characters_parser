import pandas as pd
from bs4 import BeautifulSoup
import requests

# index_character (id), name (world), hero (name), url (img), group (anime/games/cartoons)

site_url = "https://genshin-info.ru"
genre = "Игры"

html = requests.get(f"{site_url}/wiki/personazhi/").text
soup = BeautifulSoup(html, 'html.parser')
cards = soup.find_all("div", {"class": "itemList__item"})
print(f"Обнаружено карточек персонажей: {len(cards)}")

characters = []
for idx, card in enumerate(cards[3:]):
    card_url = f"{site_url}{card.find_next('a').attrs['href']}"
    card_html = requests.get(card_url).text
    card_soup = BeautifulSoup(card_html, 'html.parser')

    rating_bar = card_soup.find("div", {"class": "characterDetail__ratingItem"})
    world_name = None
    if rating_bar is not None:
        world_name = rating_bar.text.strip()

    character_name = card_soup.find("div", {"class": "characterPromo__name"}).text

    div_img = card_soup.find("div", {"class": "itemcard__img"})
    img_url = f"{site_url}{div_img.find("img")['data-src']}"

    rarely = len(card_soup.find_all("i", {"class": "fa fa-star"}))

    props = card_soup.find_all("span", {"class": "characterPromo__propV"})
    element = props[1].text.strip()
    weapon = props[2].text.strip()

    characters.append({
        "index_character": idx,
        "name": world_name,
        "hero": character_name,
        "url": img_url,
        "group": genre,
        "rarely": rarely,
        "element": element,
        "weapon": weapon
    })

pd.DataFrame(characters).to_csv("characters.csv", index=False)
