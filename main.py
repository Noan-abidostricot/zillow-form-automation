import random
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --- CONFIGURATION ---
URL_ZILLOW = "https://appbrewery.github.io/Zillow-Clone/?"
URL_GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLScc_Et4J--VsfrtCu_f5l87vYckYCSdjvmAXBM_7q3Yqfjr6A/viewform?usp=header"

# Un User-Agent pour imiter un vrai navigateur Chrome sur Windows
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def extraire_annonces(url):
    """Scrape le site et renvoie une liste de dictionnaires en ratissant large."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    annonces_nettoyees = []

    # On récupère tous les éléments de chaque type présents sur la page
    tous_les_liens = soup.select("a.property-card-link")
    tous_les_prix = soup.select("span.PropertyCardWrapper__StyledPriceLine")
    toutes_les_adresses = soup.select("address")

    # On vérifie qu'on a bien trouvé des données
    if not tous_les_liens:
        # Si le sélecteur de classe a changé, on prend TOUS les liens dans les cartes
        tous_les_liens = soup.find_all("a", href=True)
        # On ne garde que ceux qui contiennent une annonce (souvent ils ont /details/ ou l'URL complète)
        tous_les_liens = [link for link in tous_les_liens if "zillow" in link["href"] or "/details/" in link["href"]]

    # zip() permet de boucler en même temps sur les 3 listes
    for lien_tag, prix_tag, adresse_tag in zip(tous_les_liens, tous_les_prix, toutes_les_adresses):
        lien = lien_tag["href"].strip()
        # Si le lien est relatif (ex: "/details/..."), on lui recolle le début de l'URL
        if lien.startswith("/"):
            lien = f"https://www.zillow.com{lien}"

        adresse = adresse_tag.get_text().strip().replace("|", "")

        prix_brut = prix_tag.get_text()
        prix = re.split(r"[+/]", prix_brut)[0].strip()

        annonces_nettoyees.append(
            {"adresse": adresse, "prix": prix, "lien": lien}
        )

    return annonces_nettoyees


def remplir_formulaire(liste_annonces, url_formulaire):
    """Prend la liste des annonces et les injecte une par une dans Google Form."""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    driver.get(url_formulaire)

    for annonce in liste_annonces:
        # Attendre que les champs soient visibles
        wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, "input[type='text']")
            )
        )
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")

        # Remplissage avec les données du dictionnaire
        inputs[0].send_keys(annonce["adresse"])
        inputs[1].send_keys(annonce["prix"])
        inputs[2].send_keys(annonce["lien"])

        # Petite pause aléatoire pour faire plus "humain"
        time.sleep(random.uniform(0.5, 1.5))

        # Bouton Envoyer
        submit = driver.find_element(By.XPATH, "//span[text()='Envoyer']")
        submit.click()

        # Attendre et cliquer sur "Envoyer une autre réponse"
        wait.until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "Envoyer une autre réponse")
            )
        )
        driver.find_element(By.LINK_TEXT, "Envoyer une autre réponse").click()

    driver.quit()


# --- ORCHESTRATION ---
if __name__ == "__main__":
    print("Démarre l'extraction des données...")
    donnees = extraire_annonces(URL_ZILLOW)
    print(f"{len(donnees)} annonces récupérées avec succès.")

    print("Lancement du robot de soumission...")
    remplir_formulaire(donnees, URL_GOOGLE_FORM)
    print("Toutes les annonces ont été envoyées !")
