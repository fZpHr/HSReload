# HSReload - Auto Firewall Control

HSReload est une application Windows permettant de contrôler automatiquement les règles du pare-feu en fonction de la détection d'images à l'écran.

## 🚀 Fonctionnalités

- **Détection d'images** : Surveillance automatique de l'écran pour détecter des images spécifiques
- **Contrôle du pare-feu** : Gestion automatique des règles du pare-feu Windows
- **Modes de fonctionnement** :
  - Mode "Full Auto" pour une surveillance continue
  - Mode "Semi Auto" pour des actions manuelles
- **Interface graphique** intuitive avec Tkinter
- **Système de logs** pour suivre les actions de l'application
- **Musique d'ambiance** optionnelle en arrière-plan

## 📋 Prérequis

- Python 3.x
- Bibliothèques Python :
  - tkinter
  - pygame
  - numpy
  - opencv-python
  - pyautogui

## 💻 Installation

### Version .exe (Recommandée pour Windows)

1. Téléchargez `HSReload.exe` depuis la section releases
2. Double-cliquez sur le fichier pour lancer l'application

### Installation depuis les sources

```bash
# Cloner le repository
git clone https://github.com/fZpHr/HSReload.git
cd HSReload

# Installer les dépendances
pip install -r requirements.txt
```

## 🔧 Utilisation

### Lancement

- **Version .exe** : Double-cliquez sur `HSReload.exe`
- **Version Python** : Exécutez `python HS_Reload.py`

### Modes de fonctionnement

- **Full Auto** : Surveillance continue et actions automatiques
- **Semi Auto** : Actions déclenchées manuellement sur détection
- **Manuel** : Contrôle direct des règles du pare-feu

### Paramètres disponibles

- Activation/désactivation des logs
- Conservation des règles après fermeture
- Contrôle de la musique d'ambiance

## 🛠 Compilation en .exe

Pour créer votre propre version exécutable :

```bash
pyinstaller --onefile --noconsole \
  --add-data "combat.png;." \
  --add-data "tavern.png;." \
  --add-data "music.mp3;." \
  --icon="icon.ico" \
  HS_Reload.py
```

📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

