#  Zillow Automation & Form Mitchell

Ce projet est un script d'automatisation en **Python** qui combine le **Web Scraping** et l'**Automated Data Entry**. Il extrait automatiquement des annonces immobilières depuis un clone du site Zillow et injecte les données (adresse, prix, lien) directement dans un Google Form cible sans aucune intervention humaine.

---

##  Fonctionnalités
* **Extraction propre :** Récupération dynamique des adresses, prix et URL des annonces via **BeautifulSoup**.
* **Anti-Bannissement :** Intégration de headers HTTP (`User-Agent`) réalistes pour simuler une navigation humaine.
* **Saisie Automatisée :** Pilotage du navigateur via **Selenium** pour remplir et soumettre les formulaires en boucle.
* **Robustesse :** Gestion des temps de chargement dynamiques avec `WebDriverWait` pour éviter les plantages sur les connexions lentes.

---

##  Technologies Utilisées
* **Python 3**
* **BeautifulSoup4** (Analyse HTML)
* **Requests** (Requêtes HTTP)
* **Selenium WebDriver** (Automatisation du navigateur)

---

##  Installation et Lancement

1. **Cloner le projet :**
   ```bash
   git clone [https://github.com/Noan-abidostricot/zillow-form-automation.git](https://github.com/Noan-abidostricot/zillow-form-automation.git)
   cd zillow-form-automation
