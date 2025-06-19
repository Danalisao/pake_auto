# 🚀 Pake GUI - Interface graphique pour créer des applications de bureau

Une interface graphique conviviale pour utiliser [Pake](https://github.com/tw93/Pake), l'outil qui transforme des sites web en applications de bureau légères et rapides.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-green)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)

## ✨ Fonctionnalités

- 🖥️ **Interface graphique intuitive** - Plus besoin de ligne de commande
- 🎯 **Presets de sites populaires** - YouTube, Gmail, GitHub, Twitter, etc.
- 🎨 **Personnalisation avancée** - Icônes, dimensions, options d'affichage
- 📱 **Cross-plateforme** - Windows, macOS, Linux
- 📝 **Configuration sauvegardée** - Vos paramètres sont conservés
- 📋 **Génération de commandes** - Visualisez la commande Pake générée
- 📊 **Journal d'activité** - Suivez le processus de création en temps réel
- ✅ **Vérification automatique** - Contrôle des prérequis

## 📋 Prérequis

Avant d'utiliser Pake GUI, vous devez installer :

### 1. Python 3.7+
- **Windows** : [Télécharger Python](https://python.org/downloads/)
- **macOS** : `brew install python3` ou depuis le site officiel
- **Linux** : `sudo apt install python3 python3-tk` (Ubuntu/Debian)

### 2. Node.js (version 18+)
- [Télécharger Node.js](https://nodejs.org/)

### 3. Rust
- **Windows** : [Télécharger Rust](https://www.rust-lang.org/tools/install)
- **macOS/Linux** : `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

### 4. Pake CLI
```bash
npm install -g pake-cli
```

**Note Windows** : Si vous avez une erreur d'exécution de scripts, exécutez dans PowerShell :
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🚀 Installation

1. **Cloner ou télécharger** ce projet
2. **Naviguer** vers le dossier du projet
3. **Lancer** l'application :

### Windows
```cmd
launch_pake_gui.bat
```
ou
```cmd
python pake_gui.py
```

### macOS/Linux
```bash
chmod +x launch_pake_gui.sh
./launch_pake_gui.sh
```
ou
```bash
python3 pake_gui.py
```

## 🎯 Utilisation

### Interface principale

1. **URL du site** : Entrez l'URL du site web à transformer
2. **Nom de l'app** : Donnez un nom à votre application
3. **Dimensions** : Définissez la taille de la fenêtre (largeur/hauteur)
4. **Icône** : Sélectionnez une icône personnalisée (optionnel)
5. **Options** : Cochez les options souhaitées (plein écran, masquer titre, etc.)

### Presets disponibles

L'interface propose des boutons pour les sites populaires :
- 🎬 **YouTube** - Plateforme vidéo
- 📧 **Gmail** - Client email
- 🐙 **GitHub** - Plateforme de développement
- 🐦 **Twitter/X** - Réseau social
- 💬 **WhatsApp Web** - Messagerie
- 🤖 **ChatGPT** - IA conversationnelle

### Création d'une application

1. **Remplissez** les champs obligatoires (URL minimum)
2. **Cliquez** sur "🚀 Créer l'application"
3. **Suivez** le processus dans le journal d'activité
4. **Récupérez** le fichier d'installation généré dans le dossier courant

### Types de fichiers générés

- **Windows** : `.msi` - Installateur Windows
- **macOS** : `.dmg` - Image disque macOS
- **Linux** : `.deb` - Package Debian/Ubuntu

## 🛠️ Options avancées

### Paramètres de fenêtre
- **Largeur/Hauteur** : Dimensions par défaut (1200x800)
- **Plein écran** : Lance l'app en mode plein écran
- **Masquer barre de titre** : Interface plus épurée

### Icônes personnalisées
- Formats supportés : `.ico`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`
- Taille recommandée : 256x256 pixels
- L'icône sera convertie automatiquement par Pake

## 🔧 Dépannage

### "Pake non installé"
```bash
npm install -g pake-cli
```

### "Node.js non trouvé"
- Vérifiez l'installation : `node --version`
- Redémarrez votre terminal après installation

### "Rust non trouvé"
- Vérifiez l'installation : `rustc --version`
- Sourcez votre profil : `source ~/.bashrc` (Linux/macOS)

### Erreur de permissions Windows
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Interface qui ne s'affiche pas (Linux)
```bash
sudo apt install python3-tk
```

## 📁 Structure du projet

```
pake_auto/
├── pake_gui.py              # Application principale
├── requirements.txt         # Dépendances Python
├── launch_pake_gui.bat     # Lanceur Windows
├── launch_pake_gui.sh      # Lanceur Linux/macOS
├── README.md               # Documentation
└── pake_gui_config.json    # Configuration (créé automatiquement)
```

## 🎨 Captures d'écran

L'interface propose :
- ✅ Vérification automatique des prérequis
- 📝 Formulaire de configuration intuitif
- 🎯 Boutons presets pour sites populaires
- 📊 Journal d'activité en temps réel
- 💾 Sauvegarde automatique des paramètres

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Signaler des bugs
- 💡 Proposer des améliorations
- 🔧 Ajouter des fonctionnalités
- 📖 Améliorer la documentation

## 📜 Licence

Ce projet est sous licence libre. Pake est développé par [tw93](https://github.com/tw93/Pake).

## 🔗 Liens utiles

- [Pake sur GitHub](https://github.com/tw93/Pake)
- [Documentation Pake](https://github.com/tw93/Pake/blob/main/bin/README.md)
- [Tauri Framework](https://tauri.app/)
- [Node.js](https://nodejs.org/)
- [Rust](https://www.rust-lang.org/)

## 🎉 Remerciements

- **tw93** pour l'excellent outil Pake
- La communauté **Tauri** pour le framework
- Tous les contributeurs et utilisateurs

---

**Astuce** : Utilisez le bouton "📋 Générer commande" pour voir la commande Pake qui sera exécutée avant de créer l'application !
