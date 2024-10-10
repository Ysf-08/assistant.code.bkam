from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .model import db, User
import openai

# Créez un blueprint nommé 'main' pour organiser les routes de l'application
main = Blueprint('main', __name__)

# Configurez OpenAI API avec votre clé API


# Fonction pour appeler l'API OpenAI Chat avec un prompt spécifique
def call_openai_api(prompt):
    try:
        # Générer du texte en utilisant OpenAI GPT-3.5 Turbo ou GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou utilisez "gpt-4" pour GPT-4
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        generated_text = response['choices'][0]['message']['content'].strip()
        return generated_text
    except Exception as e:
        # Gérer les erreurs en affichant un message d'erreur
        print(f"Erreur lors de la génération de texte : {e}")
        return f"Erreur : échec de la requête API avec l'erreur {str(e)}."

# Fonction pour ajouter les entrées utilisateur et les réponses générées à l'historique de session
def add_to_history(user_input, generated_output):
    if 'history' not in session:
        session['history'] = []
    session['history'].append({'user': user_input, 'output': generated_output})

# Route pour l'inscription des utilisateurs
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Récupérer les informations d'inscription depuis le formulaire
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Vérifier si l'utilisateur ou l'email existe déjà
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return render_template('signup.html', error_message="Le nom d'utilisateur ou l'email est déjà pris.")

        # Créer un nouvel utilisateur et enregistrer dans la base de données
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Rediriger l'utilisateur vers la page de connexion après l'inscription
        return redirect(url_for('main.login'))
    
    return render_template('signup.html')

# Route pour la connexion des utilisateurs
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Récupérer les informations de connexion depuis le formulaire
        username = request.form['username']
        password = request.form['password']

        # Vérifier si l'utilisateur existe et si le mot de passe est correct
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username  # Ajouter le nom d'utilisateur à la session
            return redirect(url_for('main.index'))

        else:
            return render_template('login.html', error_message="Nom d'utilisateur ou mot de passe incorrect.")
    
    return render_template('login.html')

# Route pour la page d'accueil, redirige vers la page de connexion par défaut
@main.route('/')
def home():
    return redirect(url_for('main.login'))


# Route pour déconnecter l'utilisateur
@main.route('/logout')
def logout():
    # Supprimer les informations de l'utilisateur de la session
    session.pop('user_id', None)
    return redirect(url_for('main.login'))

# Route pour afficher la page d'accueil après la connexion de l'utilisateur
@main.route('/index')
def index():
    if 'user_id' in session:
        # Récupérer le nom d'utilisateur de la session et afficher un message de bienvenue
        username = session.get('username', 'Utilisateur').split('@')[0]
        return render_template('index.html', username=username)
    else:
        return redirect(url_for('main.login'))

# Route pour générer des tests unitaires pour le code fourni
@main.route('/generate-tests', methods=['POST'])
def generate_tests():
    code = request.form.get('code')
    if not code:
        return jsonify({'success': False, 'message': "Erreur : Aucun code fourni. Veuillez coller le code que vous souhaitez tester."})
    
    prompt = f"Voici un extrait de code :\n\n{code}\n\nGénérez des tests unitaires appropriés en utilisant le module unittest ."
    tests = call_openai_api(prompt)
    add_to_history(code, tests)
    
    return jsonify({'success': True, 'tests': tests}) if tests else jsonify({'success': False, 'message': "Erreur : Impossible de générer des tests."})

# Route pour générer la documentation du code fourni
@main.route('/generate-docs', methods=['POST'])
def generate_docs():
    code = request.form.get('code')
    if not code:
        return jsonify({'success': False, 'message': "Erreur : Aucun code fourni. Veuillez coller le code pour lequel vous souhaitez générer de la documentation."})
    
    prompt = f"Voici un extrait de code:\n\n{code}\n\nGénérez une documentation complète pour ce code."
    docs = call_openai_api(prompt)
    add_to_history(code, docs)
    
    return jsonify({'success': True, 'docs': docs}) if docs else jsonify({'success': False, 'message': "Erreur : Impossible de générer la documentation."})

# Route pour optimiser le code fourni
@main.route('/optimize-code', methods=['POST'])
def optimize_code():
    code = request.form.get('code')
    if not code:
        return jsonify({'success': False, 'message': "Erreur : Aucun code fourni. Veuillez coller le code que vous souhaitez optimiser."})
    
    prompt = f"Voici un extrait de code :\n\n{code}\n\nOptimisez ce code pour améliorer ses performances, sa lisibilité et sa maintenabilité."
    optimized_code = call_openai_api(prompt)
    add_to_history(code, optimized_code)
    
    if optimized_code.startswith("Erreur"):
        return jsonify({'success': False, 'message': optimized_code})

    return jsonify({'success': True, 'optimized_code': optimized_code})

# Route pour générer du code Python à partir d'une description
@main.route('/generate-code', methods=['POST'])
def generate_code():
    description = request.form.get('description')
    if not description:
        return jsonify({'success': False, 'message': "Erreur : Aucune description fournie. Veuillez fournir une description de la tâche que vous souhaitez automatiser par le code."})
    
    prompt = (
        f"Veuillez générer du code  pour accomplir la tâche suivante :\n\n{description}\n\n"
        "Fournissez le code  complet et correct qui répond à cette demande."
    )
    generated_code = call_openai_api(prompt)
    add_to_history(description, generated_code)
    
    return jsonify({'success': True, 'generated_code': generated_code}) if generated_code else jsonify({'success': False, 'message': "Erreur : Impossible de générer le code."})

# Route pour récupérer l'historique des interactions utilisateur avec le système
@main.route('/chat-history', methods=['GET'])
def chat_history():
    return jsonify(session.get('history', []))
