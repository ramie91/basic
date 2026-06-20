"""
Gestion du suivi des visiteurs et des QR codes
"""
import json
from datetime import datetime, timedelta


def save_visitor_info(user_agent, link, type_qr, nom, prenom, image_tag=None, additional_data=None):
    """
    Sauvegarde les informations du visiteur dans le fichier visitor_log.json.
    
    Args:
        user_agent: User-Agent du visiteur
        link: Lien du QR code
        type_qr: Type de QR code ('week' ou 'day')
        nom: Nom du visiteur
        prenom: Prénom du visiteur
        image_tag: Tag image (optionnel)
        additional_data: Données additionnelles (optionnel)
    """
    try:
        # Lecture du fichier pour récupérer le dernier ID
        with open("visitor_log.json", "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                last_data = json.loads(last_line)
                next_id = last_data["id"] + 1
            else:
                next_id = 1
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
        with open(filename, "a") as f:
            json.dump(data, f)
            f.write("\n")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")


def display_visitor_info():
    """Lit et affiche les informations des visiteurs depuis le fichier JSON."""
    try:
        with open("visitor_log.json", "r") as f:
            for line in f:
                data = json.loads(line)
                print(f"Timestamp: {data['timestamp']}, User Agent: {data['user_agent']}")
    except FileNotFoundError:
        print("Aucune donnée de visiteur trouvée.")
    except Exception as e:
        print(f"Erreur lors de la lecture des données : {e}")


def get_valid_entries():
    """
    Récupère les entrées valides de visitor_log.json.
    Filtre les QR codes 'week' expirés et réécrit le fichier.
    """
    valid_entries = []
    
    try:
        with open("visitor_log.json", "r") as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                timestamp = datetime.fromisoformat(data["timestamp"])
                
                # Vérification de la date d'expiration pour les QR codes 'week'
                if data["duree"] == "week":
                    if timestamp + timedelta(weeks=2) >= datetime.now():
                        valid_entries.append(data)
                else:
                    valid_entries.append(data)
        
        # Réécriture du fichier avec les entrées valides
        with open("visitor_log.json", "w") as f:
            for entry in valid_entries:
                json.dump(entry, f)
                f.write("\n")
    
    except FileNotFoundError:
        pass
    
    return valid_entries


def mark_qr_used(qr_id):
    """
    Marque un QR code comme utilisé et le déplace vers used_qr_codes.json.
    
    Args:
        qr_id: ID du QR code à marquer
    
    Returns:
        True si succès, False sinon
    """
    try:
        # Lecture du fichier principal
        with open("visitor_log.json", "r") as f:
            entries = [json.loads(line) for line in f]
        
        # Recherche de l'entrée avec l'ID correspondant
        used_entry = None
        for i, entry in enumerate(entries):
            if entry["id"] == qr_id:
                used_entry = entry
                del entries[i]
                break
        
        if not used_entry:
            return False
        
        used_entry["essais_restants"] = 2
        
        # Ajout de l'entrée au fichier used_qr_codes.json
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
        
        return True
    
    except Exception as e:
        print(f"Erreur: {e}")
        return False


def use_drink(qr_id):
    """
    Utilise une boisson (réduit les essais restants).
    
    Args:
        qr_id: ID du QR code
    
    Returns:
        True si succès, False sinon
    """
    try:
        # Lecture du fichier used_qr_codes.json
        with open("used_qr_codes.json", "r") as f:
            used_entries = [json.loads(line) for line in f]
        
        # Recherche de l'entrée et réduction des essais
        for i, entry in enumerate(used_entries):
            if entry["id"] == qr_id:
                entry["essais_restants"] -= 1
                if entry["essais_restants"] == 0:
                    del used_entries[i]
                break
        
        # Réécriture du fichier
        with open("used_qr_codes.json", "w") as f:
            for entry in used_entries:
                json.dump(entry, f)
                f.write("\n")
        
        return True
    
    except Exception as e:
        print(f"Erreur: {e}")
        return False


def get_used_entries():
    """Récupère les entrées du fichier used_qr_codes.json."""
    used_entries = []
    try:
        with open("used_qr_codes.json", "r") as f:
            for line in f:
                used_entries.append(json.loads(line))
    except FileNotFoundError:
        pass
    
    return used_entries
