"""
Application Flask pour gestion des QR codes Basic Fit
"""
from flask import Flask, render_template, url_for, request, redirect, jsonify

from helpers import namegen
from automation import execute_week, execute_day, execute_day2
from qr_generator import generate_qr_string, generate_random_card_number
from visitor_tracker import (
    get_valid_entries,
    mark_qr_used,
    use_drink,
    get_used_entries
)


app = Flask(__name__)
IS_WEEK = True
IS_DAY = True


@app.route('/')
@app.route('/home')
def home():
    """Page d'accueil."""
    return render_template("index.html", isDay=IS_DAY, isWeek=IS_WEEK)


@app.route('/result_week', methods=['POST', 'GET'])
def result_week():
    """Génère un QR code pour la semaine."""
    user_agent = request.headers.get('User-Agent')
    nom = namegen()
    prenom = namegen()
    
    if request.form.get('prenom'):
        prenom = request.form['prenom']
    if request.form.get('nom'):
        nom = request.form['nom']
    
    link = execute_week(user_agent, nom, prenom)
    return render_template('index.html', link=link, isDay=False, isWeek=True)


@app.route('/result_day', methods=['POST', 'GET'])
def result_day():
    """Génère un QR code pour le jour."""
    user_agent = request.headers.get('User-Agent')
    nom = namegen()
    prenom = namegen()
    
    if request.form.get('prenom'):
        prenom = request.form['prenom']
    if request.form.get('nom'):
        nom = request.form['nom']
    
    link = execute_day(user_agent, nom, prenom)
    return render_template('index.html', link=link, isWeek=False, isDay=True)


@app.route('/history')
def result_history():
    """Affiche l'historique des QR codes valides."""
    valid_entries = get_valid_entries()
    return render_template('index.html', isWeek=False, isDay=False, visitor_data=valid_entries)


@app.route('/mark_used/<int:qr_id>', methods=['POST'])
def mark_used(qr_id):
    """Marque un QR code comme utilisé."""
    if mark_qr_used(qr_id):
        return redirect(url_for('boissons'))
    else:
        return "QR code non trouvé."


@app.route('/get_boisson_image', methods=['POST', 'GET'])
def boisson_affiche():
    """Affiche la page de génération de boisson."""
    if request.method == 'POST':
        device_id = request.form.get('device_id', '').strip()

        if not device_id:
            return render_template(
                'boissonNew.html',
                isGen=False,
                error="Veuillez entrer un Device ID."
            )

        card_number = generate_random_card_number()
        qr_string = generate_qr_string(device_id=device_id, card_nr=card_number)
        link = "https://basic-fit-qr-code-generator.herokuapp.com/create-qr-code?data=" + qr_string
        return render_template(
            'boissonNew.html',
            link=link,
            isGen=True,
            generated_card=card_number,
            qr_string=qr_string
        )
    return render_template('boissonNew.html', isGen=False)


@app.route('/boissons')
def boissons():
    """Affiche la liste des boissons disponibles."""
    used_entries = get_used_entries()
    return render_template('boissons.html', used_entries=used_entries)


@app.route('/use_drink/<int:qr_id>', methods=['POST'])
def use_drink_route(qr_id):
    """Utilise une boisson."""
    if use_drink(qr_id):
        return redirect(url_for('boissons'))
    else:
        return "Erreur lors de l'utilisation de la boisson."


@app.route('/app')
def appGen():
    """Page de génération d'app."""
    return render_template("qrAppGen.html")


@app.route('/generate_qr_app', methods=['POST'])
def generate_qr_app():
    """
    Génère un QR code avec la logique hash GM2.
    Reçoit le device_id et le numéro de carte,
    puis retourne la chaîne QR et l'URL du QR code.
    """
    try:
        data = request.get_json()
        device_id = data.get('device_id', '').strip()
        card_number = data.get('card_number', '').strip()
        
        if not device_id:
            return jsonify({'error': 'Device ID manquant'}), 400
        if not card_number:
            return jsonify({'error': 'Numéro de carte manquant'}), 400
        
        # Générer la chaîne QR code avec hash
        # GUID sera généré aléatoirement dans generate_qr_string
        qr_string = generate_qr_string(device_id=device_id, card_nr=card_number)
        
        # Créer l'URL du QR code via le service externe
        base_url = "https://basic-fit-qr-code-generator.herokuapp.com/create-qr-code?data="
        qr_url = base_url + qr_string
        
        return jsonify({
            'qr_string': qr_string,
            'qr_url': qr_url,
            'success': True
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

