from flask import Flask, render_template, url_for, request, redirect
import random
import re
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
import requests
from selenium import webdriver
import hashlib
import json

app = Flask(__name__)
isWeek = True
isDay = True


def get_domain():
    url2 = "https://privatix-temp-mail-v1.p.rapidapi.com/request/domains/"
    headers = {
        "x-rapidapi-key": "19b9106aa4mshe95c96af81febf8p1d5d13jsn092fdba44b4a",
        "x-rapidapi-host": "privatix-temp-mail-v1.p.rapidapi.com"
    }
    response2 = requests.get(url2, headers=headers)
    type(response2.json())
    return (response2.json())


def mailgen():
    letter = ("abcdefghijklmnopqrstuvwxyz")
    millieu = "".join(random.sample(letter, 13))
    domain_list = get_domain()
    domain = domain_list[random.randint(0, len(domain_list) - 1)]
    mail = str(millieu) + domain
    return mail


def namegen():
    letter = ("abcdefghijklmnopqrstuvwxyz")
    millieu = "".join(random.sample(letter, 13))
    name = str(millieu)
    return name


def hash_email(email):
    """Hache une adresse e-mail en utilisant MD5."""
    email_bytes = email.encode('utf-8')  # Convertir en octets UTF-8
    md5_hash = hashlib.md5(email_bytes)
    return md5_hash.hexdigest()  # Obtenir le hachage en format hexadécimal


def execute_week(ua):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)

    mail = mailgen()
    hashed_email = hash_email(mail)

    driver.get('https://member.basic-fit.com/fr-FR/signup/FitTogether')
    time.sleep(3)
    BoxP = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div[2]/a').click()
    time.sleep(3)
    BoxDOB = driver.find_element(By.XPATH, '//*[@id=":Rqilttsrrla:"]').send_keys("01012000")
    BoxName = driver.find_element(By.XPATH, '//*[@id=":Railttsrrla:"]').send_keys(namegen())
    BoxName2 = driver.find_element(By.XPATH, '//*[@id=":Riilttsrrla:"]').send_keys(namegen())
    BoxMail = driver.find_element(By.XPATH, '//*[@id=":R1ailttsrrla:"]').send_keys(mail)
    BoxCGV = driver.find_element(By.XPATH, '//*[@id=":Rjilttsrrla:"]').click()
    BoxSend = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div/form/button').click()

    time.sleep(10)
    driver.quit()
    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/" + hashed_email + "/"
    headers = {
        "x-rapidapi-key": "19b9106aa4mshe95c96af81febf8p1d5d13jsn092fdba44b4a",
        "x-rapidapi-host": "privatix-temp-mail-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    pattern = r'<img alt="Basic Fit" border="0" src="https://basic-fit-qr-code-generator\.herokuapp\.com/create-qr-code\?data=[^"]+" style="display: block;max-width: 100%;" width="400">'

    # Recherche dans le mail_html du premier dictionnaire
    match = re.search(pattern, response.json()[0]['mail_html'])

    if match:
        qr_code_img = match.group()  # RÃ©cupÃ©rer le texte correspondant
        pattern = r'src="([^"]*)"'
        match = re.search(pattern, qr_code_img)

        if match:
            src_value = match.group(1)
            save_visitor_info(ua, src_value, "week", src_value)
            return src_value



    else:
        print("Balise img du QR code non trouvÃ©e.")


def execute_day(ua):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    mail = mailgen()
    hashed_email = hash_email(mail)

    driver.get(
        'https://amigos.basic-fit.com/register?sig=9deb982768874f73e6a083e0d5792fa56b285068d443276748d33f4178d3e2d2&id=0015I00000iI7xfQAC&campaign=7015I00000023UTQAY&utm_source=sfmc&utm_term=fr_fittastic_2023%7c01_fullwidth_image_text_cta%7cbtn%7cbtn%7cNL%7cNL&utm_content=305888&utm_id=b3f2de58-8206-40ac-b3de-a37f3a0f8e11&sfmc_id=199304836&sfmc_activityid=f9af55d7-401c-4324-9d04-16bb4557fdc6&utm_medium=email')
    time.sleep(3)
    BoxS = driver.find_element(By.XPATH, '//*[@id="genderForm"]/div[2]/label[1]').click()
    BoxDOB = driver.find_element(By.XPATH, '//*[@id="birthdate"]').send_keys("01-01-2000")
    BoxName = driver.find_element(By.XPATH, '//*[@id="firstname"]').send_keys(namegen())
    BoxName2 = driver.find_element(By.XPATH, '//*[@id="lastname"]').send_keys(namegen())
    BoxMail = driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(mail)
    BoxCGV = driver.find_element(By.XPATH, '//*[@id="j_id0:j_id2:opt2"]/div/label').click()
    BoxSend = driver.find_element(By.XPATH, '//*[@id="signup"]/div[3]/button').click()

    time.sleep(10)
    driver.quit()
    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/" + hashed_email + "/"
    headers = {
        "x-rapidapi-key": "19b9106aa4mshe95c96af81febf8p1d5d13jsn092fdba44b4a",
        "x-rapidapi-host": "privatix-temp-mail-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    pattern = r'<img alt="Basic Fit" border="0" src="https://basic-fit-qr-code-generator\.herokuapp\.com/create-qr-code\?data=[^"]+" style="display: block;max-width: 100%;" width="400">'

    # Recherche dans le mail_html du premier dictionnaire
    match = re.search(pattern, response.json()[0]['mail_html'])

    if match:
        qr_code_img = match.group()  # RÃ©cupÃ©rer le texte correspondant
        pattern = r'src="([^"]*)"'
        match = re.search(pattern, qr_code_img)

        if match:
            src_value = match.group(1)
            save_visitor_info(ua, src_value, "day", src_value)
            return (src_value)



    else:
        print("Balise img du QR code non trouvÃ©e.")


def save_visitor_info(user_agent, link, type_qr, image_tag=None, additional_data=None):
    """Sauvegarde les informations du visiteur dans le fichier approprié."""

    try:
        # Lecture du fichier pour récupérer le dernier ID
        with open("visitor_log.json", "r") as f:
            lines = f.readlines()
            if lines:  # Vérifie si le fichier n'est pas vide
                last_line = lines[-1]
                last_data = json.loads(last_line)
                next_id = last_data["id"] + 1
            else:
                next_id = 1  # Premier ID si le fichier est vide
    except FileNotFoundError:
        next_id = 1
    data = {
        "id": next_id,
        "timestamp": datetime.now().isoformat(),
        "user_agent": user_agent,
        "link": link,
        "image_tag": image_tag,
        "duree": type_qr
    }
    if additional_data:
        data.update(additional_data)

    try:
        filename = "visitor_log.json"
        with open(filename, "a") as f:  # 'a' pour ajouter à la fin du fichier
            json.dump(data, f)
            f.write("\n")  # Ajoute une nouvelle ligne pour séparer les entrées
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")


def display_visitor_info():
    """Lit et affiche les informations des visiteurs depuis le fichier JSON."""

    try:
        with open("visitor_log.json", "r") as f:
            for line in f:
                data = json.loads(line)
                print(f"Timestamp: {data['timestamp']}, User Agent: {data['user_agent']}")
                # Affichez d'autres données si nécessaire
    except FileNotFoundError:
        print("Aucune donnée de visiteur trouvée.")
    except Exception as e:
        print(f"Erreur lors de la lecture des données : {e}")


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", isDay=isDay, isWeek=isWeek)


@app.route('/result_week', methods=['POST', 'GET'])
def result_week():
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html', link=execute_week(user_agent), isDay=False, isWeek=True)


@app.route('/result_day', methods=['POST', 'GET'])
def result_day():
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html', link=execute_day(user_agent), isWeek=False, isDay=True)


@app.route('/history')
def result_history():
    valid_entries = []  # Liste pour stocker les entrées valides
    try:
        with open("visitor_log.json", "r") as f:
            lines = f.readlines()  # Lire toutes les lignes du fichier
            for line in lines:
                data = json.loads(line)
                timestamp = datetime.fromisoformat(data["timestamp"])
                # Vérification de la date d'expiration uniquement pour les QR codes de type "week"
                if data["duree"] == "week":
                    if timestamp + timedelta(weeks=2) >= datetime.now():
                        valid_entries.append(data)
                else:  # Si ce n'est pas un QR code "week", on le conserve
                    valid_entries.append(data)

        # Réécriture du fichier avec les entrées valides
        with open("visitor_log.json", "w") as f:
            for entry in valid_entries:
                json.dump(entry, f)
                f.write("\n")
    except FileNotFoundError:
        pass  # Gérer le cas où le fichier n'existe pas encore

    # Suppression de la première entrée affichée (si elle est expirée)
    if valid_entries and valid_entries[0]["duree"] == "week" and datetime.fromisoformat(valid_entries[0]["timestamp"]) + timedelta(weeks=2) < datetime.now():
        valid_entries.pop(0)  # Supprimer la première entrée si elle est expirée

    return render_template('index.html', isWeek=False, isDay=False, visitor_data=valid_entries)


@app.route('/mark_used/<int:qr_id>', methods=['POST'])
def mark_used(qr_id):
    try:
        # Lecture du fichier principal
        with open("visitor_log.json", "r") as f:
            entries = [json.loads(line) for line in f]

        # Recherche de l'entrée avec l'ID correspondant
        used_entry = None
        for i, entry in enumerate(entries):
            if entry["id"] == qr_id:
                used_entry = entry
                del entries[i]  # Supprimer l'entrée du fichier principal
                break

        if used_entry:
            used_entry["essais_restants"] = 2  # Initialiser les essais restants à 2

            # Ajout de l'entrée au fichier "used_qr_codes.json"
            try:
                with open("used_qr_codes.json", "r") as f:
                    used_entries = [json.loads(line) for line in f]
            except FileNotFoundError:
                used_entries = []

            used_entries.append(used_entry)

            with open("used_qr_codes.json", "w") as f:
                for entry in used_entries:
                    json.dump(entry, f)
                    f.write("\n")

            # Réécriture du fichier principal
            with open("visitor_log.json", "w") as f:
                for entry in entries:
                    json.dump(entry, f)
                    f.write("\n")

            return redirect(url_for('boissons'))
        else:
            return "QR code non trouvé."

    except Exception as e:
        return f"Erreur: {e}"



@app.route('/boissons')
def boissons():
    used_entries = []
    try:
        with open("used_qr_codes.json", "r") as f:
            for line in f:
                used_entries.append(json.loads(line))
    except FileNotFoundError:
        pass

    return render_template('boissons.html', used_entries=used_entries)


@app.route('/use_drink/<int:qr_id>', methods=['POST'])
def use_drink(qr_id):
    try:
        # Lecture du fichier used_qr_codes.json
        with open("used_qr_codes.json", "r") as f:
            used_entries = [json.loads(line) for line in f]

        # Recherche de l'entrée avec l'ID correspondant et réduction du nombre d'essais
        for i, entry in enumerate(used_entries):
            if entry["id"] == qr_id:
                entry["essais_restants"] -= 1
                if entry["essais_restants"] == 0:
                    del used_entries[i]  # Supprimer l'entrée si essais restants = 0
                break

        # Réécriture du fichier avec les entrées restantes
        with open("used_qr_codes.json", "w") as f:
            for entry in used_entries:
                json.dump(entry, f)
                f.write("\n")
        return redirect(url_for('boissons'))  # Rediriger vers la page /boissons

    except Exception as e:
        return f"Erreur: {e}"


if __name__ == "__main__":
    app.run(debug=True)

