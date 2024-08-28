from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Percorso del file JSON
JSON_FILE = './prenotazioni.json'

# Funzione per caricare le prenotazioni dal file JSON
def carica_prenotazioni():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    return []

# Funzione per salvare le prenotazioni nel file JSON
def salva_prenotazioni(prenotazioni):
    try:
        with open(JSON_FILE, 'w') as file:
            json.dump(prenotazioni, file, indent=4)
        print(f'Dati salvati correttamente in {JSON_FILE}')
    except Exception as e:
        print(f'Errore nel salvataggio dei dati: {str(e)}')

# Funzione per prenotare un tavolo 
@app.route('/prenota', methods=['POST'])
def prenota():
    try:
        dati = request.json
        print(f'Dati ricevuti dal frontend: {dati}')

        nome = dati.get('nome')
        email = dati.get('email')
        data = dati.get('data')
        ora = dati.get('ora')
        persone = dati.get('persone')

        # Crea un nuovo dizionario per la prenotazione
        nuova_prenotazione = {
            'nome': nome,
            'email': email,
            'data': data,
            'ora': ora,
            'persone': persone
        }

        # Carica le prenotazioni esistenti
        prenotazioni = carica_prenotazioni()
        print(f'Prenotazioni caricate: {prenotazioni}')

        # Aggiungi la nuova prenotazione
        prenotazioni.append(nuova_prenotazione)
        print(f'Prenotazioni aggiornate: {prenotazioni}')

        # Salva tutte le prenotazioni
        salva_prenotazioni(prenotazioni)

        return jsonify({'success': True, 'message': 'Prenotazione effettuata con successo!'})
    
    except Exception as e:
        print(f"Errore nel salvataggio delle prenotazioni: {str(e)}")
        return jsonify({'success': False, 'message': 'Errore nel salvataggio delle prenotazioni.'}), 500

#Funzione per modificare la prenotazione
@app.route('/modifica', methods=['POST'])
def modifica():
    try:
        dati = request.json
        print(f'Dati ricevuti dal frontend per modifica: {dati}')

        nome = dati.get('nome')
        email = dati.get('email')
        nuova_data = dati.get('data')
        nuova_ora = dati.get('ora')
        nuove_persone = dati.get('persone')

        #carica le prenotazioni esistenti
        prenotazioni = carica_prenotazioni()
        print(f'Prenotazioni caricate: {prenotazioni}')
        
        #Trova la prenotazione da modificare
        prenotazione_trovata = False
        for prenotazione in prenotazioni:
            if prenotazione['nome'] == nome and prenotazione['email'] == email:
                prenotazione['data'] = nuova_data
                prenotazione['ora'] = nuova_ora
                prenotazione['persone'] = nuove_persone
                prenotazione_trovata = True
                break
        if prenotazione_trovata:
            #Salva tutte le prenotazioni
            salva_prenotazioni(prenotazioni)
            return jsonify({'success': True, 'message': 'Prenotazione modificata con successo!'})
        else:
            return jsonify({'success': False, 'message': 'Prenotazione non trovata.'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': 'Errore nella modifica delle prenotazioni!'}), 500

# Funzione per cancellare la prenotazione   
@app.route('/cancella', methods=['POST'])
def cancella():
    try:
        dati = request.json
        print(f'Dati ricevuti dal frontend per cancellazione: {dati}')

        nome = dati.get('nome')
        email = dati.get('email')

        prenotazioni = carica_prenotazioni()
        print(f'Prenotazioni caricate: {prenotazioni}')

        prenotazione_trovata = False
        prenotazioni_aggiornate = []
        for prenotazione in prenotazioni:
            if prenotazione['nome'] == nome and prenotazione['email'] == email:
                prenotazione_trovata = True
            else:
                prenotazioni_aggiornate.append(prenotazione)

        if prenotazione_trovata:
            salva_prenotazioni(prenotazioni_aggiornate)
            return jsonify({'success': True, 'message': 'Prenotazione cancellata con successo!'})
        else:
            return jsonify({'success': False, 'message': 'Prenotazione non trovata!'}), 404
    except Exception as e:
        print(f"Errore nella cancellazione delle prenotazioni: {str(e)}")
        return jsonify({'success': False, 'message': 'Errore nella cancellazione delle prenotazioni'}), 500   

# Serve i file statici
@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory(app.static_folder, path)

# Serve la home page
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
