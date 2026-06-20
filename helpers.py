"""
Fonctions utilitaires et d'aide
"""
import random
import re
import hashlib
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('RAPIDAPI_KEY')
API_HOST = os.getenv('RAPIDAPI_HOST', 'privatix-temp-mail-v1.p.rapidapi.com')


def get_domain():
    """Récupère la liste des domaines de mail temporaires disponibles."""
    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/domains/"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    response = requests.get(url, headers=headers)
    return response.json()


def mailgen():
    """Génère une adresse e-mail temporaire aléatoire."""
    letter = "abcdefghijklmnopqrstuvwxyz"
    middle = "".join(random.sample(letter, 13))
    domain_list = get_domain()
    domain = domain_list[random.randint(0, len(domain_list) - 1)]
    mail = str(middle) + domain
    return mail


def namegen():
    """Génère un nom/prénom aléatoire."""
    letter = "abcdefghijklmnopqrstuvwxyz"
    name = "".join(random.sample(letter, 13))
    return name


def hash_email(email):
    """Hache une adresse e-mail en utilisant MD5."""
    email_bytes = email.encode('utf-8')
    md5_hash = hashlib.md5(email_bytes)
    return md5_hash.hexdigest()


def link_boisson_gen():
    """Génère un lien de code QR pour boisson."""
    base_link = "https://basic-fit-qr-code-generator.herokuapp.com/create-qr-code?data=V000"
    numbers = "0123456789"
    suffix = "".join(random.sample(numbers, 6))
    link_final = base_link + suffix
    return link_final
