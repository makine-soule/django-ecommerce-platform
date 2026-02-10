# Plateforme E-Commerce

Application web e-commerce complète construite avec Django, intégrant l'authentification utilisateur avec double authentification (2FA), un panier d'achat basé sur les sessions, le paiement via PayPal et le stockage cloud AWS S3 pour les fichiers media.

## Fonctionnalites

- **Catalogue Produits** -- Navigation par catégorie, pages produits détaillées avec images et descriptions
- **Panier d'Achat** -- Panier basé sur les sessions avec ajout, modification et suppression
- **Comptes Utilisateurs** -- Inscription avec vérification par email, gestion de profil, suppression de compte
- **Double Authentification (2FA)** -- Authentification TOTP via `django-two-factor-auth`
- **Gestion des Commandes** -- Tunnel de commande, suivi et historique des commandes
- **Paiement en Ligne** -- Intégration PayPal pour des paiements sécurisés
- **Stockage Cloud** -- AWS S3 pour les fichiers statiques et les uploads media
- **Notifications Email** -- Emails de vérification et réinitialisation de mot de passe via Gmail SMTP
- **Gestion des Adresses de Livraison** -- Enregistrement et gestion de plusieurs adresses

## Stack Technique

| Couche      | Technologie                    |
|-------------|--------------------------------|
| Backend     | Python 3.10, Django 4.2        |
| Base de donnees | PostgreSQL (SQLite en dev) |
| Stockage    | AWS S3 via `django-storages`   |
| Auth        | Django Auth + `django-otp`     |
| Paiement    | PayPal                         |
| Serveur     | Gunicorn                       |
| Frontend    | Django Templates, CSS, JS      |

## Structure du Projet

```
EcommerceProject/
├── src/
│   ├── manage.py
│   ├── ecommerce/          # Configuration du projet (settings, urls, wsgi)
│   ├── Store/              # Application catalogue produits
│   ├── Cart/               # Application panier (basé sur les sessions)
│   ├── account/            # Authentification et gestion des profils
│   ├── payment/            # Commandes, paiement et intégration PayPal
│   └── media/              # Fichiers uploadés par les utilisateurs
├── requirements.txt
├── .gitignore
└── README.md
```

## Demarrage

### Prerequis

- Python 3.10+
- PostgreSQL (ou SQLite pour le développement local)
- Bucket AWS S3 (pour le stockage media/statique)
- Compte Gmail avec [Mot de passe d'application](https://support.google.com/accounts/answer/185833) (pour les emails)

### Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/your-username/EcommerceProject.git
   cd EcommerceProject
   ```

2. **Créer et activer un environnement virtuel**

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**

   ```bash
   cp src/.env.example src/.env
   ```

   Modifiez `src/.env` et renseignez vos valeurs (voir [Configuration](#configuration)).

5. **Appliquer les migrations**

   ```bash
   cd src
   python manage.py migrate
   ```

6. **Créer un superutilisateur**

   ```bash
   python manage.py createsuperuser
   ```

7. **Lancer le serveur de développement**

   ```bash
   python manage.py runserver
   ```

   L'application sera accessible sur `http://127.0.0.1:8000/`.

## Configuration

Toute la configuration sensible est gérée via des variables d'environnement dans le fichier `src/.env`. Copiez `src/.env.example` vers `src/.env` et configurez les valeurs suivantes :

| Variable                  | Description                              |
|---------------------------|------------------------------------------|
| `SECRET_KEY`              | Clé secrète Django                       |
| `DEBUG`                   | Mode debug (`True` / `False`)            |
| `ENGINE`                  | Moteur de base de données                |
| `NAME`                    | Nom de la base de données                |
| `USER`                    | Utilisateur de la base de données        |
| `PASSWORD`                | Mot de passe de la base de données       |
| `HOST`                    | Hôte de la base de données               |
| `PORT`                    | Port de la base de données               |
| `EMAIL_BACKEND`           | Classe du backend email                  |
| `EMAIL_HOST`              | Serveur SMTP                             |
| `EMAIL_PORT`              | Port SMTP                                |
| `EMAIL_USE_TLS`           | Activer TLS (`True` / `False`)           |
| `EMAIL_HOST_USER`         | Adresse email SMTP                       |
| `EMAIL_HOST_PASSWORD`     | Mot de passe SMTP / mot de passe d'app   |
| `DEFAULT_FROM_EMAIL`      | Adresse email d'expédition par défaut    |
| `AWS_STORAGE_BUCKET_NAME` | Nom du bucket AWS S3                     |

## Applications

### Store
Catalogue produits avec catégories. Supporte l'upload d'images, les URLs slugifiées et le filtrage par catégorie.

### Cart
Panier d'achat basé sur les sessions. Aucune surcharge base de données -- les données du panier sont stockées dans la session utilisateur avec des opérations CRUD complètes.

### Account
Inscription avec vérification par email, gestion de profil, gestion des adresses de livraison, suivi des commandes et configuration de la double authentification.

### Payment
Tunnel de commande avec formulaire d'adresse de livraison, intégration PayPal, création de commande et gestion des succès/échecs de paiement.

## Deploiement

Pour un déploiement en production avec Gunicorn :

```bash
cd src
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
```

Assurez-vous que `DEBUG=False` et configurez `ALLOWED_HOSTS` dans `settings.py` avec votre nom de domaine.

## Licence

Ce projet est à vocation éducative et de portfolio.
