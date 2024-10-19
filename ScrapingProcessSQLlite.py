import requests
from tabulate import tabulate
import time
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import schedule
import re

# Google API Key
api_key = 'YOUR_KEY'

# Custom Search Engine ID
cx = 'YOUR_ID'

# List of keywords for search
keywords = ["deepfake attacks", "deepfake propaganda techniques","Deepfake tactics", "deepfake news","Deepfake manipulation","Deepfake videos","Synthetic media manipulation","AI-generated fake content","Manipulated media","Deepfake social engineering","Deepfake audio manipulation","Deepfake text generation","Deepfake image manipulation","Deepfake cybersecurity risks","Deepfake content authenticity","Deepfake voice cloning","Deepfake content creation tools"]

# Function to search and parse results
def search_and_parse_results(query, num_results):
    # Check if the query result is already cached
    if query in cache:
        return cache[query]

    # URL for Google Custom Search API
    url = f'URL_GOOGLE'

    # Making the request
    response = requests.get(url)
    data = response.json()

    # Checking if 'items' key exists in the JSON dictionary
    if 'items' in data:
        print(f"Results for keyword: {query}")
        # Extracting links
        links = [item['link'] for item in data['items']]
        # Cache the result
        cache[query] = links
        return links
    else:
        print(f"No results found for keyword: {query}.")
        return []

# Dictionary to store links for each keyword
links_dict = {}

# Cache to store search results
cache = {}

# For each keyword, perform a search and gather links
for keyword in keywords:
    links = search_and_parse_results(keyword, 10)  # Change '10' to the desired number of results
    links_dict[keyword] = links
    # Introduce a delay to avoid exceeding the quota
    time.sleep(2)

# Printing the gathered links in a tabulated format
for keyword, links in links_dict.items():
    print(f"Links for keyword: {keyword}")
    table = [[i + 1, link] for i, link in enumerate(links)]
    print(tabulate(table, headers=["#", "URL"], tablefmt="grid"))
    print()


# Printing the gathered links in a tabulated format
for keyword, links in links_dict.items():
    print(f"Links for keyword: {keyword}")
    table = [[i + 1, link] for i, link in enumerate(links)]
    print(tabulate(table, headers=["#", "URL"], tablefmt="grid"))
    print()


if keywords:
    first_keyword = keywords[0]
    if first_keyword in links_dict:
        print(f"URLs pour le mot-clé : {first_keyword}")
        for link in links_dict[first_keyword]:
            print(link)
    else:
        print("Aucun résultat trouvé pour le premier mot-clé.")
else:
    print("Aucun mot-clé spécifié.")


# Fonction pour se connecter à la base de données SQLite
def connect_to_database():
    try:
        connection = sqlite3.connect('deepfake.db')
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à SQLite: {e}")
        return None

# Fonction pour créer la table informations
def create_table():
    try:
        connection = connect_to_database()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS informations (
                                id INTEGER PRIMARY KEY,
                                title TEXT NOT NULL,
                                content TEXT,
                                summary TEXT,
                                url TEXT NOT NULL,
                                date_created TEXT NOT NULL
                            )''')
            connection.commit()
            print("Table 'informations' créée avec succès.")
    except Error as e:
        print(f"Erreur lors de la création de la table 'informations': {e}")
    finally:
        if connection:
            connection.close()

# Fonction pour insérer les données extraites dans la base de données SQLite
def insert_into_database(data):
    try:
        connection = connect_to_database()
        if connection is not None:
            cursor = connection.cursor()
            # Traitement du contenu avec spaCy
            doc = nlp(data['content'])
            # Exemple : extraction du résumé (première phrase ici pour simplifier)
            summary = next(doc.sents).text if doc.sents else ''
            summary = ""  # Temporairement vide car spaCy n'est pas utilisé
            query = "INSERT INTO informations (title, content, summary, url, date_created) VALUES (?, ?, ?, ?, ?)"
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(query, (data['title'], data['content'], summary, data['url'], current_time))
            connection.commit()
            print("Données insérées avec succès.")
    except Error as e:
        print(f"Erreur lors de l'insertion des données: {e}")
    finally:
        if connection:
            connection.close()

# Function to extract information from URL
def extract_information(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.text.strip() if soup.title else "Title not found"

        # Extraction du contenu textuel
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.text.strip() for p in paragraphs])
        
        data = {'title': title, 'content': content, 'url': url}
        insert_into_database(data)  # Insérer les données dans la base de données
        return data
    except Exception as e:
        print(f"Error occurred for URL: {url}\nError message: {e}")
        return None

# Fonction pour se connecter à la base de données SQLite
create_table()

# Votre boucle pour extraire les informations des URL
for url_list in links_dict.values():
    for link in url_list:
        result = extract_information(link)
        if result:
            print("Title:", result['title'])
            print("Content:", result['content'])
            print("URL:", result['url'])
            print()  # Ajoute une ligne vide entre chaque résultat
        else:
            print("Failed to extract information from the URL.")


# Fonction pour afficher les données de la base de données SQLite
def display_database():
    try:
        connection = connect_to_database()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM informations")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print("ID:", row[0])
                    print("Title:", row[1])
                    print("Content:", row[2])
                    print("Summary:", row[3])
                    print("URL:", row[4])
                    print("Date Created:", row[5])
                    print()  # Ajoute une ligne vide entre chaque enregistrement
            else:
                print("La table informations est vide.")
    except Error as e:
        print(f"Erreur lors de l'affichage des données de la base de données: {e}")
    finally:
        if connection:
            connection.close()

# Appel de la fonction pour afficher les données de la base de données
display_database()


slack_token = "TOKEN"
client = WebClient(token=slack_token)

def send_slack_notification(message):
    try:
        response = client.chat_postMessage(channel='#votre-canal', text=message)
        print("Notification Slack envoyée avec succès")
    except SlackApiError as e:
        print(f"Erreur lors de l'envoi de la notification Slack: {e}")


def update_database(data):
    connection = None
    try:
        connection = connect_to_database()
        if connection is not None:
            cursor = connection.cursor()
            # Vérifier si l'URL est déjà présente
            check_query = "SELECT * FROM informations WHERE url = ?"
            cursor.execute(check_query, (data['url'],))
            result = cursor.fetchone()
            if result:
                print("L'URL existe déjà dans la base de données. Mise à jour ignorée.")
                # Mettre à jour les données existantes
                # Traitement du contenu avec spaCy
                doc = nlp(data['content'])
                # Exemple : mise à jour du résumé
                summary = next(doc.sents).text if doc.sents else ''
                update_query = "UPDATE informations SET title = ?, content = ? WHERE url = ?"
                cursor.execute(update_query, (data['title'], data['content'], data['url']))
                connection.commit()
                send_slack_notification(f"Mise à jour dans la base de données : {data['url']}")
            else:
                # Insérer les nouvelles données
                insert_query = "INSERT INTO informations (title, content, url) VALUES (?, ?, ?)"
                cursor.execute(insert_query, (data['title'], data['content'], data['url']))
                connection.commit()
                print("Données insérées avec succès.")
                send_slack_notification(f"Nouvelle entrée ajoutée à la base de données : {data['url']}")
    except Error as e:
        print(f"Erreur lors de la mise à jour de la base de données: {e}")
    finally:
        if connection:
            connection.close()


def monitor_new_information(keywords):
    while True:
        print("Début de la surveillance pour de nouvelles informations...")
        for keyword in keywords:
            print(f"Recherche de nouvelles informations pour le mot-clé : {keyword}")
            search_results = search_and_parse_results(keyword, 10)  # Vous pouvez ajuster le nombre de résultats souhaités
            for url in search_results:
                print(f"Extraction des informations de l'URL : {url}")
                information = extract_information(url)
                if information:
                    print(f"Mise à jour de la base de données pour l'URL : {url}")
                    update_database(information)
                time.sleep(1)  # Pause pour éviter de surcharger le serveur ou de dépasser les limites de l'API
        print("Surveillance terminée pour aujourd'hui. Reprise dans 24 heures.")
        time.sleep(86400)  # Pause de 24 heures avant de recommencer


# Planifiez la surveillance pour s'exécuter toutes les 24 heures
schedule.every(24).hours.do(monitor_new_information, keywords=keywords)

while True:
    schedule.run_pending()
    time.sleep(1)


# Fonction pour nettoyer et prétraiter le texte
def clean_text(text):
    # Supprimer les balises HTML
    text = re.sub('<[^<]+?>', '', text)
    # Mettre en minuscule
    text = text.lower()
    # Supprimer les caractères spéciaux et la ponctuation
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Supprimer les liens
    text = re.sub(r'http\S+', '', text)
    # Supprimer les espaces supplémentaires
    text = re.sub('\s+', ' ', text).strip()
    return text

# Nettoyage et prétraitement des données scrappées
cleaned_data = []
for url_list in links_dict.values():
    for link in url_list:
        result = extract_information(link)
        if result:
            # Nettoyer le titre et le contenu
            clean_title = clean_text(result['title'])
            clean_content = clean_text(result['content'])
            # Ajouter les données nettoyées à la liste
            cleaned_data.append({'title': clean_title, 'content': clean_content, 'url': result['url']})

# Afficher les données nettoyées
for data in cleaned_data:
    print("Title:", data['title'])
    print("Content:", data['content'])
    print("URL:", data['url'])
    print()
