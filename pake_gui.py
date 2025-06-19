#!/usr/bin/env python3
"""
Pake GUI - Interface graphique pour transformer des sites web en applications de bureau
Utilise l'outil Pake (https://github.com/tw93/Pake) pour créer des applications légères
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
import json
from pathlib import Path
import re
import shutil
import datetime

# Imports optionnels pour le téléchargement de favicon
try:
    import requests
    from urllib.parse import urljoin, urlparse
    from PIL import Image
    import tempfile
    FAVICON_SUPPORT = True
except ImportError:
    FAVICON_SUPPORT = False
    print("⚠️ Modules manquants pour le téléchargement de favicon.")
    print("💡 Installez avec: pip install requests pillow")
    print("📝 Le téléchargement automatique des favicons sera désactivé.")

class PakeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pake GUI - Transformateur de sites web en applications")
        self.root.geometry("1400x900")  # Fenêtre plus grande pour éviter les ascenseurs
        self.root.resizable(True, True)
          # Variables
        self.url_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.width_var = tk.StringVar(value="1200")
        self.height_var = tk.StringVar(value="800")
        self.icon_path_var = tk.StringVar()
        self.fullscreen_var = tk.BooleanVar()
        self.hide_title_var = tk.BooleanVar()
        self.always_on_top_var = tk.BooleanVar()
        self.auto_favicon_var = tk.BooleanVar(value=FAVICON_SUPPORT)  # Activer seulement si dépendances disponibles
        
        # Variables pour contrôle de processus
        self.current_process = None
        self.is_building = False
        
        # Configuration par défaut
        self.config_file = Path("pake_gui_config.json")
        self.pake_executable = None
        
        self.load_config()
        self.setup_ui()
        
        # Vérifier les prérequis au démarrage
        self.root.after(1000, self.check_prerequisites)
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Style moderne
        style = ttk.Style()
        try:
            style.theme_use('vista')  # Windows
        except:
            try:
                style.theme_use('clam')  # Fallback
            except:
                pass
          # Couleurs personnalisées
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), foreground='#2E86AB')
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
          # Frame principal direct sans scrollbar pour éviter les ascenseurs
        main_frame = ttk.Frame(self.root, padding="12")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuration du grid
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
          # Titre avec emoji et style
        title_label = ttk.Label(main_frame, text="🚀 Pake GUI - Créateur d'applications de bureau", 
                               style='Title.TLabel')
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 15))
        row += 1
          # Section URL et nom
        url_frame = ttk.LabelFrame(main_frame, text="📋 Configuration de base", padding="8")
        url_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 12))
        url_frame.columnconfigure(1, weight=1)
        row += 1
        
        ttk.Label(url_frame, text="URL du site:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 8))
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=120, font=('Arial', 14))
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(0, 8))
        
        ttk.Label(url_frame, text="Nom de l'app:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(8, 0))
        name_entry = ttk.Entry(url_frame, textvariable=self.name_var, width=120, font=('Arial', 14))
        name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(8, 0))
        
        # Section dimensions
        dim_frame = ttk.LabelFrame(main_frame, text="📐 Dimensions de la fenêtre", padding="10")
        dim_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        row += 1
        
        # Grid pour les dimensions
        dims_grid = ttk.Frame(dim_frame)
        dims_grid.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(dims_grid, text="Largeur:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 8))
        ttk.Entry(dims_grid, textvariable=self.width_var, width=25, font=('Arial', 14)).grid(
            row=0, column=1, padx=(0, 25))
        
        ttk.Label(dims_grid, text="Hauteur:", font=('Arial', 10, 'bold')).grid(
            row=0, column=2, sticky=tk.W, padx=(0, 8))
        ttk.Entry(dims_grid, textvariable=self.height_var, width=25, font=('Arial', 14)).grid(
            row=0, column=3, padx=0)
        
        # Section icône
        icon_frame = ttk.LabelFrame(main_frame, text="🎨 Icône personnalisée", padding="10")
        icon_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        icon_frame.columnconfigure(1, weight=1)
        row += 1
        ttk.Label(icon_frame, text="Fichier icône:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Entry(icon_frame, textvariable=self.icon_path_var, state="readonly", font=('Arial', 13), width=80).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        icon_buttons = ttk.Frame(icon_frame)
        icon_buttons.grid(row=0, column=2)
        ttk.Button(icon_buttons, text="📁 Parcourir", command=self.browse_icon).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(icon_buttons, text="🗑️ Effacer", command=self.clear_icon).pack(side=tk.LEFT)
          # Case à cocher pour le téléchargement automatique du favicon
        favicon_checkbox = ttk.Checkbutton(icon_frame, text="🌐 Télécharger automatiquement le favicon si aucune icône", 
                       variable=self.auto_favicon_var)
        favicon_checkbox.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(8, 0))
        
        # Désactiver si les dépendances ne sont pas disponibles
        if not FAVICON_SUPPORT:
            favicon_checkbox.config(state='disabled')
        
        # Section options
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Options avancées", padding="10")
        options_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        row += 1
        
        options_grid = ttk.Frame(options_frame)
        options_grid.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Checkbutton(options_grid, text="🖥️ Plein écran", variable=self.fullscreen_var).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 25))
        ttk.Checkbutton(options_grid, text="🎯 Masquer barre de titre", variable=self.hide_title_var).grid(
            row=0, column=1, sticky=tk.W, padx=(0, 25))
        ttk.Checkbutton(options_grid, text="📌 Toujours au premier plan", variable=self.always_on_top_var).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 25), pady=(8, 0))
        
        # Section presets
        presets_frame = ttk.LabelFrame(main_frame, text="🌟 Sites populaires", padding="10")
        presets_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        row += 1
        
        # Boutons presets en grille
        presets = [
            ("YouTube", "https://www.youtube.com", "🎥"),
            ("Gmail", "https://mail.google.com", "📧"),
            ("GitHub", "https://github.com", "🐙"),
            ("Twitter/X", "https://twitter.com", "🐦"),
            ("WhatsApp Web", "https://web.whatsapp.com", "💬"),
            ("ChatGPT", "https://chat.openai.com", "🤖"),
            ("Discord", "https://discord.com/app", "🎮"),
            ("Spotify", "https://open.spotify.com", "🎵"),
            ("Netflix", "https://www.netflix.com", "🎬")
        ]
        
        for i, (name, url, emoji) in enumerate(presets):
            btn = ttk.Button(presets_frame, text=f"{emoji} {name}", 
                           command=lambda n=name, u=url: self.load_preset(n, u))
            btn.grid(row=i//3, column=i%3, padx=5, pady=3, sticky=(tk.W, tk.E))
            presets_frame.columnconfigure(i%3, weight=1)
        
        # Boutons d'action principaux
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=row, column=0, columnspan=3, pady=(15, 10))
        row += 1
        
        ttk.Button(action_frame, text="🔍 Vérifier prérequis", 
                  command=self.check_prerequisites).pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_button = ttk.Button(action_frame, text="🚀 Créer l'application", 
                  command=self.create_app, style="Accent.TButton")
        self.create_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(action_frame, text="⏹️ Arrêter", 
                  command=self.stop_build, state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(action_frame, text="📋 Générer commande", 
                  command=self.show_command).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="💾 Sauvegarder config", 
                  command=self.save_config).pack(side=tk.LEFT)
        
        # Zone de log - réduite pour éviter les ascenseurs
        log_frame = ttk.LabelFrame(main_frame, text="📄 Journal d'activité", padding="8")
        log_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 8))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(row, weight=1)        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD, font=('Consolas', 11))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.log("✅ Interface initialisée avec succès")
        
    def load_preset(self, name, url):
        """Charge un preset de site populaire"""
        self.url_var.set(url)
        self.name_var.set(name)
        self.log(f"📝 Preset chargé: {name}")
        
    def browse_icon(self):
        """Ouvre un dialogue pour sélectionner une icône"""
        filetypes = [
            ("Fichiers icône", "*.ico *.png *.jpg *.jpeg *.gif *.bmp"),
            ("Tous les fichiers", "*.*")
        ]
        filename = filedialog.askopenfilename(title="Sélectionner une icône", filetypes=filetypes)
        if filename:
            self.icon_path_var.set(filename)
            self.log(f"🎨 Icône sélectionnée: {os.path.basename(filename)}")
            
    def clear_icon(self):
        """Efface le chemin de l'icône"""
        self.icon_path_var.set("")
        self.log("🗑️ Icône effacée")
        
    def log(self, message):
        """Ajoute un message au journal avec timestamp"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        self.log_text.insert(tk.END, f"{full_message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def find_pake_executable(self):
        """Trouve l'exécutable Pake sur le système avec détection avancée"""
        self.log("🔍 Recherche de l'exécutable Pake...")
        
        # 1. Essayer d'abord la commande directe dans le PATH
        try:
            result = subprocess.run(['pake', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log("✅ Pake trouvé dans le PATH système")
                return 'pake'
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # 2. Chercher avec shutil.which (plus fiable)
        pake_path = shutil.which('pake')
        if pake_path:
            self.log(f"✅ Pake trouvé via which: {pake_path}")
            return pake_path
          # 3. Obtenir le dossier global npm et chercher dedans
        try:
            result = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                npm_global = result.stdout.strip()
                self.log(f"📂 Dossier npm global: {npm_global}")
                
                # Chercher dans .bin avec toutes les variantes possibles
                bin_paths = [
                    os.path.join(npm_global, '.bin', 'pake.cmd'),
                    os.path.join(npm_global, '.bin', 'pake.CMD'),  # Windows majuscules
                    os.path.join(npm_global, '.bin', 'pake'),
                    os.path.join(npm_global, '.bin', 'pake.exe'),
                    os.path.join(npm_global, '.bin', 'pake.EXE'),
                ]
                
                for bin_path in bin_paths:
                    if os.path.exists(bin_path):
                        self.log(f"✅ Pake trouvé: {bin_path}")
                        return bin_path
                        
        except (FileNotFoundError, subprocess.TimeoutExpired):
            self.log("⚠️ npm non trouvé ou timeout")
          # 4. Chercher dans les chemins Windows typiques
        windows_paths = [
            os.path.expanduser('~\\AppData\\Roaming\\npm\\pake.cmd'),
            os.path.expanduser('~\\AppData\\Roaming\\npm\\pake.CMD'),  # Majuscules
            os.path.expanduser('~\\AppData\\Roaming\\npm\\pake.exe'),
            os.path.expanduser('~\\AppData\\Roaming\\npm\\pake.EXE'),
            os.path.expanduser('~\\AppData\\Roaming\\npm\\pake'),
            'C:\\Program Files\\nodejs\\pake.cmd',
            'C:\\Program Files\\nodejs\\pake.CMD',
            'C:\\Program Files\\nodejs\\pake.exe',
            'C:\\Program Files\\nodejs\\pake.EXE',
            'C:\\Program Files\\nodejs\\pake',
            'C:\\Program Files (x86)\\nodejs\\pake.cmd',
            'C:\\Program Files (x86)\\nodejs\\pake.CMD',
            'C:\\Program Files (x86)\\nodejs\\pake.exe',
            'C:\\Program Files (x86)\\nodejs\\pake.EXE',
            'C:\\Program Files (x86)\\nodejs\\pake',
        ]
        
        self.log("🔍 Recherche dans les chemins Windows...")
        for path in windows_paths:
            if os.path.exists(path):
                self.log(f"✅ Pake trouvé: {path}")
                return path
          # 5. Chercher dans le PATH étendu manuellement
        path_env = os.environ.get('PATH', '')
        for path_dir in path_env.split(os.pathsep):
            if path_dir.strip():
                for exe_name in ['pake.cmd', 'pake.CMD', 'pake.exe', 'pake.EXE', 'pake']:
                    full_path = os.path.join(path_dir.strip(), exe_name)
                    if os.path.exists(full_path):
                        self.log(f"✅ Pake trouvé dans PATH: {full_path}")
                        return full_path
                        
        self.log("❌ Pake non trouvé sur le système")
        return None
        
    def check_prerequisites(self):
        """Vérifie si Node.js, Rust et Pake sont installés"""
        self.log("🔍 === Vérification des prérequis ===")
        
        def check():
            all_ok = True
            
            # Vérifier Node.js
            try:
                result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.log(f"✅ Node.js installé: {version}")
                else:
                    self.log("❌ Node.js: commande échouée")
                    all_ok = False
            except (FileNotFoundError, subprocess.TimeoutExpired):
                self.log("❌ Node.js non installé ou non accessible")
                self.log("💡 Installez Node.js depuis: https://nodejs.org/")
                all_ok = False
                
            # Vérifier npm
            try:
                result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.log(f"✅ npm installé: {version}")
                else:
                    self.log("❌ npm: commande échouée")
                    all_ok = False
            except (FileNotFoundError, subprocess.TimeoutExpired):
                self.log("❌ npm non installé ou non accessible")
                all_ok = False
                
            # Vérifier Rust
            try:
                result = subprocess.run(['rustc', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.log(f"✅ Rust installé: {version}")
                else:
                    self.log("❌ Rust: commande échouée")
                    all_ok = False
            except (FileNotFoundError, subprocess.TimeoutExpired):
                self.log("❌ Rust non installé ou non accessible")
                self.log("💡 Installez Rust depuis: https://rustup.rs/")
                all_ok = False
                  
            # Vérifier Pake avec détection avancée
            pake_path = self.find_pake_executable()
            if pake_path:
                try:
                    # Tester la commande Pake
                    result = subprocess.run([pake_path, '--version'], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        version = result.stdout.strip()
                        self.log(f"✅ Pake installé: {version}")
                        self.log(f"📍 Chemin utilisé: {pake_path}")
                        self.pake_executable = pake_path
                    else:
                        self.log(f"❌ Pake: commande échouée (code: {result.returncode})")
                        if result.stderr:
                            self.log(f"❌ Erreur: {result.stderr.strip()}")
                        self.pake_executable = None
                        all_ok = False
                except (subprocess.TimeoutExpired, Exception) as e:
                    self.log(f"❌ Erreur lors du test de Pake: {e}")
                    self.pake_executable = None
                    all_ok = False
            else:
                self.log("❌ Pake non installé ou non trouvé")
                self.log("💡 Installez Pake avec: npm install -g pake-cli")
                self.log("💡 Ou redémarrez ce programme après installation")
                self.log("💡 Assurez-vous que le PATH npm global est configuré")
                self.pake_executable = None
                all_ok = False
                
            # Résumé final
            if all_ok:
                self.log("🎉 === Tous les prérequis sont installés! ===")
            else:
                self.log("⚠️ === Certains prérequis manquent ===")
                self.log("💡 Consultez HELP.md pour les instructions d'installation")
                
        # Lancer la vérification dans un thread
        threading.Thread(target=check, daemon=True).start()
        
    def generate_command(self):
        """Génère la commande Pake avec l'exécutable détecté"""
        if not self.url_var.get().strip():
            return None, "URL manquante"
            
        url = self.url_var.get().strip()
        name = self.name_var.get().strip() or "MonApp"
        
        # Nettoyer le nom (supprimer caractères spéciaux)
        name = re.sub(r'[^\w\s-]', '', name).strip()
        name = re.sub(r'\s+', '_', name)
        
        # Utiliser l'exécutable Pake détecté ou fallback
        pake_cmd = self.pake_executable or 'pake'
        cmd = [pake_cmd, url, '--name', name]
        
        # Ajouter les options
        if self.width_var.get() and self.width_var.get().isdigit():
            cmd.extend(['--width', self.width_var.get()])
            
        if self.height_var.get() and self.height_var.get().isdigit():
            cmd.extend(['--height', self.height_var.get()])        # Gestion de l'icône avec téléchargement automatique du favicon
        icon_path = self.icon_path_var.get()
        if icon_path and os.path.exists(icon_path):
            # Utiliser l'icône spécifiée par l'utilisateur
            cmd.extend(['--icon', icon_path])
        elif self.auto_favicon_var.get():
            # Tenter de télécharger le favicon automatiquement si l'option est activée
            self.log("🎨 Aucune icône spécifiée, tentative de téléchargement du favicon...")
            favicon_path = self.download_favicon(url)
            if favicon_path and os.path.exists(favicon_path):
                cmd.extend(['--icon', favicon_path])
                self.log(f"✅ Favicon utilisé comme icône: {os.path.basename(favicon_path)}")
            else:
                self.log("⚠️ Favicon non trouvé, icône par défaut de Pake utilisée")
        else:
            self.log("ℹ️ Téléchargement automatique du favicon désactivé, icône par défaut de Pake utilisée")
        if self.fullscreen_var.get():
            cmd.append('--fullscreen')
            
        if self.hide_title_var.get():
            cmd.append('--hide-title-bar')
            
        if self.always_on_top_var.get():
            cmd.append('--always-on-top')
            cmd.append('--always-on-top')
            
        return cmd, None
        
    def show_command(self):
        """Affiche la commande qui sera exécutée"""
        cmd, error = self.generate_command()
        if error:
            messagebox.showerror("Erreur", error)
            return
            
        if cmd:
            cmd_str = ' '.join(f'"{arg}"' if ' ' in str(arg) else str(arg) for arg in cmd)
            
            # Créer une fenêtre pour afficher la commande
            cmd_window = tk.Toplevel(self.root)
            cmd_window.title("Commande Pake générée")
            cmd_window.geometry("600x300")
            cmd_window.transient(self.root)
            
            ttk.Label(cmd_window, text="Commande qui sera exécutée:", font=('Arial', 10, 'bold')).pack(pady=10)
            
            # Zone de texte pour la commande
            cmd_text = scrolledtext.ScrolledText(cmd_window, height=8, wrap=tk.WORD, font=('Consolas', 9))
            cmd_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            cmd_text.insert('1.0', cmd_str)
            cmd_text.config(state='disabled')
              # Bouton pour copier
            def copy_command():
                cmd_window.clipboard_clear()
                cmd_window.clipboard_append(cmd_str)
                messagebox.showinfo("Copié", "Commande copiée dans le presse-papiers!")
                
            ttk.Button(cmd_window, text="📋 Copier dans le presse-papiers", 
                      command=copy_command).pack(pady=(0, 10))
            
            self.log(f"📋 Commande générée et affichée")
        else:
            messagebox.showerror("Erreur", "Impossible de générer la commande")
            
    def create_app(self):
        """Lance la création de l'application"""
        cmd, error = self.generate_command()
        if error:
            messagebox.showerror("Erreur", error)
            return
            
        if not self.pake_executable:
            messagebox.showerror("Erreur", "Pake n'est pas installé ou non trouvé!\nVeuillez vérifier les prérequis.")
            return
            
        # Activer l'état de construction
        self.is_building = True
        self.create_button.config(state='disabled')
        self.stop_button.config(state='normal')
            
        def run_pake():
            try:
                self.progress.start(10)
                self.log("🚀 === Démarrage de la création ===")
                cmd_str = ' '.join(f'"{arg}"' if ' ' in str(arg) else str(arg) for arg in cmd)
                self.log(f"📝 Commande: {cmd_str}")
                self.log(f"📍 Exécutable: {self.pake_executable}")
                
                # Changer vers le répertoire de travail si nécessaire
                cwd = os.getcwd()
                self.log(f"📂 Répertoire de travail: {cwd}")
                
                # Exécuter Pake
                self.current_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    universal_newlines=True,
                    cwd=cwd
                )                
                # Lire la sortie en temps réel
                output_lines = []
                for line in self.current_process.stdout:
                    if not self.is_building:  # Vérifier si l'arrêt a été demandé
                        break
                    line = line.strip()
                    if line:
                        output_lines.append(line)
                        self.log(f"📦 {line}")
                        
                self.current_process.wait()
                
                self.log(f"🏁 Processus terminé avec le code: {self.current_process.returncode}")
                
                if self.current_process.returncode == 0 and self.is_building:
                    self.log("🎉 === APPLICATION CRÉÉE AVEC SUCCÈS! ===")
                    self.log("📁 Vérifiez le dossier courant pour les fichiers générés")
                    messagebox.showinfo("Succès", 
                        "🎉 L'application a été créée avec succès!\n\n"
                        "Vérifiez le dossier courant pour:\n"
                        "• Le fichier d'installation (.msi, .deb, .dmg)\n"
                        "• Les fichiers de l'application")
                elif self.is_building:  # Seulement afficher l'erreur si pas d'arrêt manuel
                    self.log(f"❌ === ERREUR LORS DE LA CRÉATION ===")
                    error_msg = "Une erreur s'est produite lors de la création."
                    if output_lines:
                        error_msg += f"\n\nDernières lignes de sortie:\n" + "\n".join(output_lines[-5:])
                    messagebox.showerror("Erreur", error_msg)
                    
            except Exception as e:
                if self.is_building:  # Seulement afficher l'erreur si pas d'arrêt manuel
                    self.log(f"❌ Exception: {str(e)}")
                    messagebox.showerror("Erreur", f"Erreur lors de l'exécution:\n{str(e)}")
            finally:
                self.is_building = False
                self.current_process = None
                self.progress.stop()
                self.create_button.config(state='normal')
                self.stop_button.config(state='disabled')
                
        # Sauvegarder la config avant de commencer
        self.save_config()
        
        # Lancer dans un thread séparé
        threading.Thread(target=run_pake, daemon=True).start()
        
    def stop_build(self):
        """Arrête le processus de création en cours"""
        if self.current_process and self.is_building:
            try:
                self.current_process.terminate()
                self.log("⏹️ Arrêt du processus demandé...")
                
                # Attendre un peu pour la terminaison propre
                try:
                    self.current_process.wait(timeout=3)
                    self.log("✅ Processus arrêté proprement")
                except subprocess.TimeoutExpired:
                    # Forcer l'arrêt si nécessaire
                    self.current_process.kill()
                    self.log("🛑 Processus forcé à s'arrêter")
                    
            except Exception as e:
                self.log(f"⚠️ Erreur lors de l'arrêt: {e}")
            finally:
                self.is_building = False
                self.current_process = None
                self.progress.stop()
                self.create_button.config(state='normal')
                self.stop_button.config(state='disabled')
                self.log("🔄 Interface prête pour une nouvelle création")
        else:
            self.log("ℹ️ Aucun processus en cours à arrêter")
            
    def save_config(self):
        """Sauvegarde la configuration actuelle"""
        config = {
            'url': self.url_var.get(),
            'name': self.name_var.get(),
            'width': self.width_var.get(),
            'height': self.height_var.get(),
            'icon_path': self.icon_path_var.get(),
            'fullscreen': self.fullscreen_var.get(),
            'hide_title': self.hide_title_var.get(),
            'always_on_top': self.always_on_top_var.get(),
            'auto_favicon': self.auto_favicon_var.get()
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self.log("💾 Configuration sauvegardée")
        except Exception as e:
            self.log(f"⚠️ Impossible de sauvegarder la config: {e}")
            
    def load_config(self):
        """Charge la configuration sauvegardée"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)                # Charger les valeurs sauvegardées
                self.url_var.set(config.get('url', ''))
                self.name_var.set(config.get('name', ''))
                self.width_var.set(config.get('width', '1200'))
                self.height_var.set(config.get('height', '800'))
                self.icon_path_var.set(config.get('icon_path', ''))
                self.fullscreen_var.set(config.get('fullscreen', False))
                self.hide_title_var.set(config.get('hide_title', False))
                self.always_on_top_var.set(config.get('always_on_top', False))
                self.auto_favicon_var.set(config.get('auto_favicon', True))
                
                print("✅ Configuration chargée depuis pake_gui_config.json")
                
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement de la config: {e}")
                
    def download_favicon(self, url):
        """Télécharge automatiquement le favicon d'un site web"""
        if not FAVICON_SUPPORT:
            self.log("❌ Téléchargement de favicon non disponible - modules manquants")
            self.log("💡 Installez avec: pip install requests pillow")
            return None
            
        try:
            self.log(f"🔍 Recherche du favicon pour {url}")
            
            # Nettoyer et valider l'URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            # Liste des emplacements possibles du favicon
            favicon_urls = [
                urljoin(base_url, '/favicon.ico'),
                urljoin(base_url, '/apple-touch-icon.png'),
                urljoin(base_url, '/apple-touch-icon-precomposed.png'),
                urljoin(base_url, '/favicon.png'),
                urljoin(base_url, '/favicon.svg'),
            ]
            
            # Essayer de récupérer le favicon depuis la page HTML
            try:
                response = requests.get(url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                if response.status_code == 200:
                    html_content = response.text
                    # Chercher les balises link rel="icon" ou rel="shortcut icon"
                    import re
                    icon_patterns = [
                        r'<link[^>]*rel=["\'](?:shortcut )?icon["\'][^>]*href=["\']([^"\']+)["\'][^>]*>',
                        r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\'](?:shortcut )?icon["\'][^>]*>',
                        r'<link[^>]*rel=["\']apple-touch-icon["\'][^>]*href=["\']([^"\']+)["\'][^>]*>',
                    ]
                    
                    for pattern in icon_patterns:
                        matches = re.findall(pattern, html_content, re.IGNORECASE)
                        for match in matches:
                            favicon_url = urljoin(base_url, match)
                            if favicon_url not in favicon_urls:
                                favicon_urls.insert(0, favicon_url)
            except:
                pass
            
            # Essayer de télécharger le favicon
            for favicon_url in favicon_urls:
                try:
                    self.log(f"🔗 Tentative: {favicon_url}")
                    response = requests.get(favicon_url, timeout=10, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    })
                    
                    if response.status_code == 200 and len(response.content) > 100:
                        # Créer un dossier pour les favicons s'il n'existe pas
                        favicon_dir = Path("favicons")
                        favicon_dir.mkdir(exist_ok=True)
                        
                        # Déterminer l'extension du fichier
                        content_type = response.headers.get('content-type', '').lower()
                        if 'png' in content_type:
                            ext = '.png'
                        elif 'svg' in content_type:
                            ext = '.svg'
                        elif 'jpeg' in content_type or 'jpg' in content_type:
                            ext = '.jpg'
                        elif 'gif' in content_type:
                            ext = '.gif'
                        else:
                            ext = '.ico'
                        
                        # Nom du fichier basé sur le domaine
                        domain = parsed_url.netloc.replace('www.', '').replace(':', '_')
                        favicon_path = favicon_dir / f"{domain}_favicon{ext}"
                        
                        # Sauvegarder le favicon
                        with open(favicon_path, 'wb') as f:
                            f.write(response.content)
                        
                        # Vérifier que c'est bien une image valide
                        try:
                            if ext != '.svg':  # SVG n'est pas supporté par PIL
                                with Image.open(favicon_path) as img:
                                    # Convertir en PNG si nécessaire
                                    if ext != '.png':
                                        png_path = favicon_path.with_suffix('.png')
                                        img.save(png_path, 'PNG')
                                        favicon_path.unlink()  # Supprimer l'original
                                        favicon_path = png_path
                        except Exception as img_error:
                            self.log(f"⚠️ Erreur de validation image: {img_error}")
                            if favicon_path.exists():
                                favicon_path.unlink()
                            continue
                        
                        self.log(f"✅ Favicon téléchargé: {favicon_path}")
                        return str(favicon_path.absolute())
                        
                except requests.RequestException as e:
                    self.log(f"⚠️ Échec {favicon_url}: {e}")
                    continue
                except Exception as e:
                    self.log(f"⚠️ Erreur inattendue: {e}")
                    continue
            
            self.log("❌ Aucun favicon trouvé")
            return None
            
        except Exception as e:
            self.log(f"❌ Erreur lors du téléchargement du favicon: {e}")
            return None

def main():
    """Point d'entrée principal de l'application"""
    # Configuration de l'application
    root = tk.Tk()
    
    # Améliorer le rendu sur Windows avec mise à l'échelle
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
        
    try:
        root.tk.call('tk', 'scaling', 1.0)
    except:
        pass
    
    # Icône de l'application (si disponible)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # Créer l'application
    app = PakeGUI(root)
    
    # Gérer la fermeture propre
    def on_closing():
        try:
            app.save_config()
        except:
            pass
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Message de démarrage
    print("🚀 Pake GUI démarré")
    print("📂 Répertoire de travail:", os.getcwd())
    
    # Lancer l'interface graphique
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        
    print("👋 Pake GUI fermé")

if __name__ == "__main__":
    main()
