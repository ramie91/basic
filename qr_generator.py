"""
Générateur de QR codes avec logique hash pour intégration app
"""
import hashlib
import time
import string
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Constantes
CARD_NUMBER = os.getenv('QR_CARD_NUMBER', 'V00347833')


def generate_random_guid(length=3):
    """
    Génère un GUID aléatoire (code client).
    
    Args:
        length: Longueur du GUID à générer (par défaut 3)
    
    Returns:
        Chaîne aléatoire composée de lettres majuscules et chiffres
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_random_card_number(length=8, prefix='V'):
    """
    Génère un numéro de carte aléatoire.
    
    Args:
        length: Nombre de chiffres après le préfixe
        prefix: Préfixe du numéro de carte
    
    Returns:
        Numéro de carte au format V########
    """
    digits = ''.join(random.choice(string.digits) for _ in range(length))
    return f"{prefix}{digits}"


def generate_hash(card_nr, guid, iat, device_id):
    """
    Génère un hash SHA256 selon la logique de Basic Fit.
    
    Args:
        card_nr: Numéro de carte
        guid: GUID ou code client
        iat: Timestamp Unix
        device_id: Identifiant du dispositif
    
    Returns:
        Les 8 derniers caractères du hash en majuscules
    """
    data_to_hash = card_nr + guid + str(iat) + device_id
    hash_object = hashlib.sha256(data_to_hash.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    hash_last_8 = hash_hex[-8:].upper()
    return hash_last_8


def generate_qr_string(device_id, card_nr=None, timestamp=None):
    """
    Génère la chaîne de données pour le QR code au format GM2.
    
    Args:
        device_id: Identifiant du dispositif (obligatoire)
        card_nr: Numéro de carte (utilise la constante par défaut)
        timestamp: Timestamp Unix (utilise le timestamp actuel par défaut)
    
    Returns:
        Chaîne formatée: GM2:CARD_NUMBER:GUID:TIMESTAMP:HASH
    """
    if card_nr is None:
        card_nr = CARD_NUMBER
    if timestamp is None:
        timestamp = int(time.time())
    
    # Générer un GUID aléatoire
    guid = generate_random_guid(3)
    
    hash_value = generate_hash(card_nr, guid, timestamp, device_id)
    qr_string = f"GM2:{card_nr}:{guid}:{timestamp}:{hash_value}"
    
    return qr_string

