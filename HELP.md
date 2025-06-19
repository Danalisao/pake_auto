# 🚀 Aide rapide - Pake GUI

## Démarrage rapide

1. **Première utilisation** :
   - Exécutez `install_prerequisites.bat` (Windows)
   - Ou installez manuellement : Node.js, Rust, puis `npm install -g pake-cli`

2. **Lancer l'application** :
   - Windows : Double-cliquez sur `launch_pake_gui.bat`
   - Linux/macOS : `./launch_pake_gui.sh`

## Utilisation

### Étapes simples :
1. **URL** : Entrez l'URL du site (ex: https://youtube.com)
2. **Nom** : Donnez un nom à votre app (ex: YouTube)
3. **Cliquez** sur "🚀 Créer l'application"
4. **Attendez** la fin du processus
5. **Installez** le fichier généré (.msi sur Windows)

### Boutons presets :
- Cliquez sur YouTube, Gmail, etc. pour remplir automatiquement

### Options avancées :
- **Dimensions** : Changez la taille de la fenêtre
- **Icône** : Parcourir pour une icône personnalisée (.ico, .png)
- **Plein écran** : L'app s'ouvrira en plein écran
- **Masquer titre** : Interface plus épurée

## Raccourcis dans les apps créées

| Windows | Action |
|---------|--------|
| Ctrl + ← | Page précédente |
| Ctrl + → | Page suivante |
| Ctrl + R | Actualiser |
| Ctrl + W | Masquer fenêtre |
| Ctrl + +/- | Zoom |

## Problèmes courants

### "Pake non installé"
```cmd
npm install -g pake-cli
```

### Erreur PowerShell
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### App ne se lance pas
- Vérifiez que tous les prérequis sont installés
- Regardez le journal d'activité pour les erreurs

## Fichiers générés

- **Windows** : `NomApp.msi` - Installateur
- **macOS** : `NomApp.dmg` - Image disque  
- **Linux** : `NomApp.deb` - Package Debian

## Support

- Documentation complète : `README.md`
- Issues/Bugs : Créez une issue sur le dépôt
- Pake officiel : https://github.com/tw93/Pake

---
**Astuce** : Utilisez "📋 Générer commande" pour voir la commande avant exécution !
