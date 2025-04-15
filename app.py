from flask import Flask, render_template, url_for, request, redirect
import random
import re
import time
from webdriver_manager.core.utils import read_version_from_cmd 
from webdriver_manager.core.os_manager import PATTERN
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
import requests
from selenium import webdriver
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import json

app = Flask(__name__)
isWeek = True
isDay = True



def get_domain():
    url2 = "https://privatix-temp-mail-v1.p.rapidapi.com/request/domains/"
    headers = {
    	'x-rapidapi-key': "YOUR-API-KEY",
    	'x-rapidapi-host': "privatix-temp-mail-v1.p.rapidapi.com"
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


def link_boisson_gen():
    link = "https://basic-fit-qr-code-generator.herokuapp.com/create-qr-code?data=V000"
    numbers = ("0123456789")
    millieu = "".join(random.sample(numbers, 6))
    link_final = link + str(millieu)
    return link_final
    

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


def execute_week(ua,nom,prenom):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chromium_path 
    
    chrome_options.add_argument("--headless=new")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    mail = mailgen()
    hashed_email = hash_email(mail)

    driver.get(
        'https://amigos.basic-fit.com/register?sig=eb13261d3788ee141c96dd065e78c7dd4d61b6adf42497fb0f648cbbc1f4faf9&id=001R6000002Hbq1IAC&campaign=701R6000002HbhyIAC&utm_id=b3f2de58-8206-40ac-b3de-a37f3a0f8e11&sfmc_id=220296788&sfmc_activityid=ecfebade-1f92-4e07-a413-ed832b598534')
    time.sleep(3)
    BoxS = driver.find_element(By.XPATH, '//*[@id="genderForm"]/div[2]/label[1]').click()
    BoxDOB = driver.find_element(By.XPATH, '//*[@id="birthdate"]').send_keys("01-01-2000")
    BoxName = driver.find_element(By.XPATH, '//*[@id="firstname"]').send_keys(nom)
    BoxName2 = driver.find_element(By.XPATH, '//*[@id="lastname"]').send_keys(prenom)
    BoxMail = driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(mail)
    BoxCGV = driver.find_element(By.XPATH, '//*[@id="j_id0:j_id2:opt2"]/div/label').click()
    BoxSend = driver.find_element(By.XPATH, '//*[@id="signup"]/div[3]/button').click()

    time.sleep(10)
    driver.quit()
    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/" + hashed_email + "/"
    headers = {
    	'x-rapidapi-key': "289c9da465mshccf2c0d825a384ap19abaajsn7d24fb64b295",
    	'x-rapidapi-host': "privatix-temp-mail-v1.p.rapidapi.com"
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
            save_visitor_info(ua, src_value, "day NL", nom, prenom, src_value)
            return (src_value)



    else:
        print("Balise img du QR code non trouvÃ©e.")


def execute_day(ua,nom,prenom):
    url = "https://member.basic-fit.com/api/signUpForm/signUp"
    mail = mailgen()
    payload = {
        "firstName": "aaa",
        "lastName": "aa",
        "email": mail,
        "locale": "fr-FR",
        "dateOfBirth": "2005-10-10T00:00:00.000Z",
        "promotions": True,
        "tos": True,
        "campaignId": "2Hl7qICv6IYQIWyHqWQou0"
    }

    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
        "Content-Type": "application/json",
        "Origin": "https://member.basic-fit.com",
        "Referer": "https://member.basic-fit.com/fr-FR/signup/ValentinesDay_2025_Daypass",
        "Sec-Ch-Ua": '"Not A(Brand";v="8", "Chromium";v="132"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "DNT": "1",
        "Priority": "u=1, i"
    }

    cookies = {
        "FPID": "FPID2.2.J7aVDG247PE618tbiawuU3Jmz2Kxc8d0DpG10yKdzw4%3D.1720734771",
        "_scid": "0d25c416-d5c2-4f57-a24e-b90db0df8ff6",
        "bf-country": "FR"
        # Ajoute d'autres cookies ici si nécessaire
    }

    response = requests.post(url, json=payload, headers=headers, cookies=cookies)
    print(response.status_code)
    print(response.text)
    time.sleep(5)
    hashed_email = hash_email(mail)
    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/" + hashed_email + "/"
    headers = {
    	'x-rapidapi-key': "fb2313f171msh26fa22f8bbc3988p1f5d0bjsn655962b30059",
    	'x-rapidapi-host': "privatix-temp-mail-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    print(response.text)
    pattern = r'<img alt="Basic Fit" border="0" src="https://basic-fit-qr-code-generator\.herokuapp\.com/create-qr-code\?data=[^"]+" style="display: block;max-width: 100%;" width="400">'

    # Recherche dans le mail_html du premier dictionnaire
    match = re.search(pattern, response.json()[0]['mail_html'])

    if match:
        qr_code_img = match.group()  # RÃ©cupÃ©rer le texte correspondant
        pattern = r'src="([^"]*)"'
        match = re.search(pattern, qr_code_img)

        if match:
            src_value = match.group(1)
            save_visitor_info(ua, src_value, "day", nom, prenom, src_value)
            return (src_value)



    else:
        print("Balise img du QR code non trouvÃ©e.")
        
def execute_day2(ua,nom,prenom):
    chrome_options = webdriver.ChromeOptions()
    #version = read_version_from_cmd(path,pattern=[CHROME])
    chrome_options.binary_location = chromium_path 
    chrome_options.add_argument("--headless=new")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    mail = mailgen()
    hashed_email = hash_email(mail)

    driver.get(
        'https://amigos.basic-fit.com/register?sig=9deb982768874f73e6a083e0d5792fa56b285068d443276748d33f4178d3e2d2&id=0015I00000iI7xfQAC&campaign=7015I00000023UTQAY&utm_source=sfmc&utm_term=fr_fittastic_2023%7c01_fullwidth_image_text_cta%7cbtn%7cbtn%7cNL%7cNL&utm_content=305888&utm_id=b3f2de58-8206-40ac-b3de-a37f3a0f8e11&sfmc_id=199304836&sfmc_activityid=f9af55d7-401c-4324-9d04-16bb4557fdc6&utm_medium=email')
    time.sleep(3)
    BoxS = driver.find_element(By.XPATH, '//*[@id="genderForm"]/div[2]/label[1]').click()
    BoxDOB = driver.find_element(By.XPATH, '//*[@id="birthdate"]').send_keys("01-01-2000")
    BoxName = driver.find_element(By.XPATH, '//*[@id="firstname"]').send_keys(nom)
    BoxName2 = driver.find_element(By.XPATH, '//*[@id="lastname"]').send_keys(prenom)
    BoxMail = driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(mail)
    BoxCGV = driver.find_element(By.XPATH, '//*[@id="j_id0:j_id2:opt2"]/div/label').click()
    BoxSend = driver.find_element(By.XPATH, '//*[@id="signup"]/div[3]/button').click()

    time.sleep(10)
    driver.quit()
    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/" + hashed_email + "/"
    headers = {
    	'x-rapidapi-key': "289c9da465mshccf2c0d825a384ap19abaajsn7d24fb64b295",
    	'x-rapidapi-host': "privatix-temp-mail-v1.p.rapidapi.com"
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
            save_visitor_info(ua, src_value, "day", nom, prenom, src_value)
            return (src_value)



    else:
        print("Balise img du QR code non trouvÃ©e.")


def save_visitor_info(user_agent, link, type_qr, nom, prenom, image_tag=None, additional_data=None):
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
        "Nom": nom,
        "Prenom": prenom,
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
    nom = namegen()
    prenom = namegen()
    if request.form['prenom'] != "":
        prenom = request.form['prenom']
    if request.form['nom'] != "":
        nom = request.form['nom']
    return render_template('index.html', link=execute_week(user_agent,nom,prenom), isDay=False, isWeek=True)


@app.route('/result_day', methods=['POST', 'GET'])
def result_day():
    user_agent = request.headers.get('User-Agent')
    nom = namegen()
    prenom = namegen()
    if request.form['prenom'] != "":
        prenom = request.form['prenom']
    if request.form['nom'] != "":
        nom = request.form['nom']
    return render_template('index.html', link=execute_day(user_agent,nom,prenom), isWeek=False, isDay=True)


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

@app.route('/get_boisson_image', methods=['POST', 'GET'])
def boisson_affiche():
    if request.method == 'POST':
        link = link_boisson_gen()
        return render_template('boissonNew.html', link=link, isGen=True)
    return render_template('boissonNew.html', isGen=False)

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


@app.route('/app')
def appGen():
    return render_template("qrAppGen.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80,debug=True,)

