# 🚀 Pake GUI - Interface Graphique pour Pake

Une interface graphique moderne et intuitive pour transformer n'importe quel site web en application de bureau native avec [Pake](https://github.com/tw93/Pake).

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-green)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)

## ✨ Fonctionnalités

### 🎯 Interface Moderne
- **Design moderne** avec emojis et couleurs attractives
- **Interface responsive** qui s'adapte à la taille de l'écran
- **Sections organisées** pour une navigation intuitive
- **Journal d'activité en temps réel** avec timestamps
- **Barres de progression** pour suivre l'avancement

### 🌟 Sites Populaires (Presets)
Boutons rapides pour créer des applications pour :
- 🎥 YouTube
- 📧 Gmail  
- 🐙 GitHub
- 🐦 Twitter/X
- 💬 WhatsApp Web
- 🤖 ChatGPT
- 🎮 Discord
- 🎵 Spotify
- 🎬 Netflix

### ⚙️ Configuration Avancée
- **Dimensions personnalisées** (largeur × hauteur)
- **Icône personnalisée** (tous formats supportés)
- **Options avancées** :
  - 🖥️ Mode plein écran
  - 🎯 Masquer la barre de titre
  - 📌 Toujours au premier plan
  - 👻 Mode transparent

### 🔧 Détection Intelligente
- **Auto-détection de Pake** même si pas dans le PATH
- **Vérification des prérequis** (Node.js, npm, Rust, Pake)
- **Messages d'aide contextuelle** pour l'installation
- **Support multi-plateforme** (Windows, Linux, macOS)

### 💾 Gestion de Configuration
- **Sauvegarde automatique** des paramètres
- **Chargement automatique** au démarrage
- **Export des commandes** générées
- **Copie vers le presse-papiers**

## 🚀 Installation Rapide

### Prérequis
```bash
# 1. Node.js (depuis https://nodejs.org/)
node --version

# 2. Rust (depuis https://rustup.rs/)  
rustc --version

# 3. Pake via npm
npm install -g pake-cli
```

### Lancement
```bash
# Méthode 1: Python direct
python pake_gui.py

# Méthode 2: Script batch (Windows)
launch_pake_gui.bat

# Méthode 3: Script shell (Linux/macOS)
./launch_pake_gui.sh
```

## 🎯 Guide d'Utilisation

### 1. Vérification des Prérequis
Cliquez sur **"🔍 Vérifier prérequis"** au premier lancement :
- ✅ Node.js installé
- ✅ npm installé  
- ✅ Rust installé
- ✅ Pake installé et détecté

### 2. Configuration de Base
- **URL du site** : L'adresse complète (ex: https://github.com)
- **Nom de l'app** : Le nom de votre application (ex: GitHub)

### 3. Personnalisation
- **Dimensions** : Largeur × Hauteur en pixels
- **Icône** : Fichier .ico, .png, .jpg (optionnel)
- **Options** : Plein écran, masquer titre, etc.

### 4. Création
- **"📋 Générer commande"** : Voir la commande qui sera exécutée
- **"🚀 Créer l'application"** : Lancer la création
- **Suivre le journal** : Messages en temps réel

### 5. Résultat
L'application créée sera dans le dossier courant :
- Fichier d'installation (`.msi`, `.deb`, `.dmg`)
- Dossier avec les sources de l'application

## 🛠️ Dépannage

### Pake non trouvé
Si l'interface ne trouve pas Pake après installation :

1. **Redémarrer** le terminal/invite de commande
2. **Vérifier l'installation** : `npm list -g pake-cli`
3. **Réinstaller si nécessaire** : `npm uninstall -g pake-cli && npm install -g pake-cli`
4. **Vérifier le PATH npm** : `npm root -g`

### Erreurs de création
- **Vérifier l'URL** : Doit commencer par `http://` ou `https://`
- **Nom valide** : Éviter les caractères spéciaux
- **Icône accessible** : Fichier existant et lisible
- **Connexion internet** : Nécessaire pour télécharger les dépendances

### Performance
- **Première création** : Plus lente (téléchargement des dépendances)
- **Créations suivantes** : Plus rapides (cache local)
- **Gros sites** : Peuvent prendre plusieurs minutes

## 📁 Structure des Fichiers

```
pake_auto/
├── 📄 pake_gui.py              # Interface principale
├── 📄 requirements.txt         # Dépendances Python
├── 📄 launch_pake_gui.bat     # Lanceur Windows
├── 📄 launch_pake_gui.sh      # Lanceur Linux/macOS
├── 📄 README.md               # Cette documentation
├── 📄 HELP.md                 # Aide détaillée
├── 📄 .gitignore              # Fichiers à ignorer
├── 📄 pake_gui_config.json    # Configuration sauvegardée
└── 📁 generated_apps/         # Applications créées (auto)
```

## 🚀 Fonctionnalités Avancées

### Détection Automatique de Pake
L'interface recherche Pake dans :
1. PATH système standard
2. Dossier npm global (`npm root -g`)  
3. Chemins Windows typiques (`%APPDATA%\npm\`)
4. Dossiers Node.js système
5. PATH étendu manuel

### Gestion des Erreurs
- **Messages détaillés** dans le journal
- **Suggestions de solutions** automatiques
- **Timeouts intelligents** pour éviter les blocages
- **Gestion des interruptions** utilisateur

### Configuration Persistante
- **Sauvegarde automatique** à chaque création
- **Chargement au démarrage** des derniers paramètres
- **Format JSON lisible** pour édition manuelle
- **Encodage UTF-8** pour les caractères spéciaux

## 🎨 Interface Moderne

L'interface comprend :
- **En-tête stylé** avec titre et emoji
- **Sections colorées** avec icônes pour chaque fonctionnalité  
- **Boutons presets** avec emojis pour les sites populaires
- **Journal d'activité** avec scrolling automatique et timestamps
- **Barre de progression** animée pendant la création
- **Fenêtres popup** pour l'affichage des commandes
- **Gestion du scroll** avec molette de souris

## 📞 Support et Documentation

- **Documentation Pake** : https://github.com/tw93/Pake
- **HELP.md** : Guide détaillé d'installation et dépannage
- **Journal intégré** : Messages détaillés dans l'interface
- **Logs** : Consultez le journal d'activité en bas de l'interface

## 🔄 Changelog v2.0.0

### 🆕 Nouvelles fonctionnalités
- Interface graphique complètement redessinée
- Détection automatique avancée de Pake
- 9 presets de sites populaires avec emojis
- Journal d'activité avec timestamps
- Options avancées (transparence, toujours au premier plan)
- Fenêtre de visualisation des commandes avec copie
- Gestion du scroll avec molette
- Configuration UTF-8 pour les caractères spéciaux

### 🔧 Améliorations techniques
- Code complètement refactorisé et documenté
- Gestion d'erreurs robuste avec timeouts
- Threading pour éviter le gel de l'interface
- Auto-sauvegarde de la configuration
- Messages d'aide contextuelle
- Support multi-plateforme amélioré

### 🐛 Corrections
- Problème de détection de Pake sur Windows
- Erreurs d'import et d'indentation
- Gestion des chemins avec espaces
- Encodage des caractères spéciaux
- Interface responsive sur différentes résolutions

---

*Interface créée avec ❤️ pour simplifier l'utilisation de Pake*
