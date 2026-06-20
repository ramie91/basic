"""
Fonctions d'automatisation Selenium pour l'enregistrement et récupération de QR codes
"""
import time
import re
import requests
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service, Service as ChromiumService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

from helpers import mailgen, hash_email
from visitor_tracker import save_visitor_info

load_dotenv()

API_KEY = os.getenv('RAPIDAPI_KEY')
API_HOST = os.getenv('RAPIDAPI_HOST', 'privatix-temp-mail-v1.p.rapidapi.com')


def _setup_chrome_options(chromium_path=None):
    """Configure les options Chrome/Chromium."""
    chrome_options = webdriver.ChromeOptions()
    if chromium_path:
        chrome_options.binary_location = chromium_path
    
    chrome_options.add_argument("--headless=new")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    return chrome_options


def _extract_qr_from_email(hashed_email):
    """Extrait le lien QR code de l'email reçu."""
    url = f"https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/{hashed_email}/"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    
    response = requests.get(url, headers=headers)
    pattern = r'<img alt="Basic Fit" border="0" src="https://basic-fit-qr-code-generator\.herokuapp\.com/create-qr-code\?data=[^"]+" style="display: block;max-width: 100%;" width="400">'
    
    match = re.search(pattern, response.json()[0]['mail_html'])
    
    if match:
        qr_code_img = match.group()
        pattern = r'src="([^"]*)"'
        match = re.search(pattern, qr_code_img)
        if match:
            return match.group(1)
    
    print("Balise img du QR code non trouvée.")
    return None


def execute_week(ua, nom, prenom, chromium_path=None):
    """
    Enregistrement semaine: utilise Selenium pour remplir le formulaire et récupère le QR code.
    
    Args:
        ua: User-Agent
        nom: Nom de l'utilisateur
        prenom: Prénom de l'utilisateur
        chromium_path: Chemin vers Chromium (optionnel)
    """
    chrome_options = _setup_chrome_options(chromium_path)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    mail = mailgen()
    hashed_email = hash_email(mail)
    
    try:
        driver.get(
            'https://amigos.basic-fit.com/register?sig=eb13261d3788ee141c96dd065e78c7dd4d61b6adf42497fb0f648cbbc1f4faf9&id=001R6000002Hbq1IAC&campaign=701R6000002HbhyIAC&utm_id=b3f2de58-8206-40ac-b3de-a37f3a0f8e11&sfmc_id=220296788&sfmc_activityid=ecfebade-1f92-4e07-a413-ed832b598534'
        )
        time.sleep(3)
        
        driver.find_element(By.XPATH, '//*[@id="genderForm"]/div[2]/label[1]').click()
        driver.find_element(By.XPATH, '//*[@id="birthdate"]').send_keys("01-01-2000")
        driver.find_element(By.XPATH, '//*[@id="firstname"]').send_keys(nom)
        driver.find_element(By.XPATH, '//*[@id="lastname"]').send_keys(prenom)
        driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(mail)
        driver.find_element(By.XPATH, '//*[@id="j_id0:j_id2:opt2"]/div/label').click()
        driver.find_element(By.XPATH, '//*[@id="signup"]/div[3]/button').click()
        
        time.sleep(10)
    finally:
        driver.quit()
    
    src_value = _extract_qr_from_email(hashed_email)
    
    if src_value:
        save_visitor_info(ua, src_value, "week", nom, prenom, src_value)
        return src_value
    
    return None


def execute_day(ua, nom, prenom):
    """
    Enregistrement jour: utilise l'API directement pour s'inscrire et récupère le QR code.
    
    Args:
        ua: User-Agent
        nom: Nom de l'utilisateur
        prenom: Prénom de l'utilisateur
    """
    url = "https://member.basic-fit.com/api/signUpForm/signUp"
    mail = mailgen()
    
    payload = {
        "firstName": nom,
        "lastName": prenom,
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
    }
    
    response = requests.post(url, json=payload, headers=headers, cookies=cookies)
    print(f"Status: {response.status_code}")
    
    time.sleep(5)
    hashed_email = hash_email(mail)
    src_value = _extract_qr_from_email(hashed_email)
    
    if src_value:
        save_visitor_info(ua, src_value, "day", nom, prenom, src_value)
        return src_value
    
    return None


def execute_day2(ua, nom, prenom, chromium_path=None):
    """
    Variante Selenium pour enregistrement jour.
    
    Args:
        ua: User-Agent
        nom: Nom de l'utilisateur
        prenom: Prénom de l'utilisateur
        chromium_path: Chemin vers Chromium (optionnel)
    """
    chrome_options = _setup_chrome_options(chromium_path)
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    
    mail = mailgen()
    hashed_email = hash_email(mail)
    
    try:
        driver.get(
            'https://amigos.basic-fit.com/register?sig=9deb982768874f73e6a083e0d5792fa56b285068d443276748d33f4178d3e2d2&id=0015I00000iI7xfQAC&campaign=7015I00000023UTQAY&utm_source=sfmc&utm_term=fr_fittastic_2023%7c01_fullwidth_image_text_cta%7cbtn%7cbtn%7cNL%7cNL&utm_content=305888&utm_id=b3f2de58-8206-40ac-b3de-a37f3a0f8e11&sfmc_id=199304836&sfmc_activityid=f9af55d7-401c-4324-9d04-16bb4557fdc6&utm_medium=email'
        )
        time.sleep(3)
        
        driver.find_element(By.XPATH, '//*[@id="genderForm"]/div[2]/label[1]').click()
        driver.find_element(By.XPATH, '//*[@id="birthdate"]').send_keys("01-01-2000")
        driver.find_element(By.XPATH, '//*[@id="firstname"]').send_keys(nom)
        driver.find_element(By.XPATH, '//*[@id="lastname"]').send_keys(prenom)
        driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(mail)
        driver.find_element(By.XPATH, '//*[@id="j_id0:j_id2:opt2"]/div/label').click()
        driver.find_element(By.XPATH, '//*[@id="signup"]/div[3]/button').click()
        
        time.sleep(10)
    finally:
        driver.quit()
    
    src_value = _extract_qr_from_email(hashed_email)
    
    if src_value:
        save_visitor_info(ua, src_value, "day", nom, prenom, src_value)
        return src_value
    
    return None
