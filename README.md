# HSReload - Hearthstone Turn Skipper

HSReload est une application Windows qui vous permet de skip des tours sur Hearthstone en manipulant temporairement la connexion via le pare-feu Windows.

## 🎮 Comment ça marche

L'application crée et gère une règle de pare-feu qui, une fois activée, coupe brièvement la connexion d'Hearthstone pour skip le tour en cours. Plusieurs modes de fonctionnement sont disponibles selon vos besoins.

## 🚀 Modes de fonctionnement

- **Full Auto** : Skip automatiquement tous les tours
- **Semi Auto** : Skip uniquement le prochain tour
- **Manuel** : Activation/désactivation manuelle de la règle de pare-feu

## 📋 Prérequis

- Windows 10/11
- Python 3.x (si installation depuis les sources)
- Hearthstone installé
- Droits administrateur (pour la gestion du pare-feu)

## 💻 Installation

### Version Simple (Recommandée)
1. Téléchargez `HSReload.exe` depuis les releases
2. Lancez en tant qu'administrateur

### Version Développeur
```bash
# Cloner le projet
git clone https://github.com/fZpHr/HSReload.git
cd HSReload

# Installer les dépendances
pip install -r requirements.txt
```

## 🎯 Fonctionnalités

- **Interface simple** avec trois modes de skip
- **Détection d'images** pour le fonctionnement automatique
- **Gestion du pare-feu** Windows intégrée
- **Logs** pour suivre les actions effectuées
- **Musique** optionnelle en arrière-plan

## ⚙️ Options

- Activation/désactivation des logs
- Conservation des règles après fermeture
- Contrôle de la musique d'ambiance

## 🛠️ Compilation

Pour créer votre propre version :
```bash
pyinstaller --onefile --noconsole \
  --add-data "combat.png;." \
  --add-data "tavern.png;." \
  --add-data "music.mp3;." \
  --icon="icon.ico" \
  HS_Reload.py
```
