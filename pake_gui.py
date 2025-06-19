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

class PakeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pake GUI - Transformateur de sites web en applications")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.url_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.width_var = tk.StringVar(value="1200")
        self.height_var = tk.StringVar(value="800")
        self.icon_path_var = tk.StringVar()
        self.fullscreen_var = tk.BooleanVar()
        self.hide_title_var = tk.BooleanVar()
        self.transparent_var = tk.BooleanVar()
        self.always_on_top_var = tk.BooleanVar()
        
        # Configuration par défaut
        self.config_file = Path("pake_gui_config.json")
        self.load_config()
        
        self.setup_ui()
        self.check_prerequisites()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Titre
        title_label = ttk.Label(main_frame, text="🚀 Pake GUI - Créateur d'applications de bureau", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        row += 1
        
        # Section URL et nom
        url_frame = ttk.LabelFrame(main_frame, text="Configuration de base", padding="5")
        url_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        row += 1
        
        ttk.Label(url_frame, text="URL du site:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Label(url_frame, text="Nom de l'app:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        name_entry = ttk.Entry(url_frame, textvariable=self.name_var, width=50)
        name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        
        # Section dimensions
        dim_frame = ttk.LabelFrame(main_frame, text="Dimensions de la fenêtre", padding="5")
        dim_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1
        
        ttk.Label(dim_frame, text="Largeur:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(dim_frame, textvariable=self.width_var, width=10).grid(row=0, column=1, padx=(5, 15))
        
        ttk.Label(dim_frame, text="Hauteur:").grid(row=0, column=2, sticky=tk.W)
        ttk.Entry(dim_frame, textvariable=self.height_var, width=10).grid(row=0, column=3, padx=(5, 0))
        
        # Section icône
        icon_frame = ttk.LabelFrame(main_frame, text="Icône personnalisée", padding="5")
        icon_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        icon_frame.columnconfigure(1, weight=1)
        row += 1
        
        ttk.Label(icon_frame, text="Fichier icône:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(icon_frame, textvariable=self.icon_path_var, state="readonly").grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(icon_frame, text="Parcourir", command=self.browse_icon).grid(row=0, column=2)
        ttk.Button(icon_frame, text="Effacer", command=self.clear_icon).grid(row=0, column=3, padx=(5, 0))
        
        # Section options
        options_frame = ttk.LabelFrame(main_frame, text="Options avancées", padding="5")
        options_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1
        
        ttk.Checkbutton(options_frame, text="Plein écran", variable=self.fullscreen_var).grid(
            row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Masquer barre de titre", variable=self.hide_title_var).grid(
            row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Section presets
        presets_frame = ttk.LabelFrame(main_frame, text="Sites populaires", padding="5")
        presets_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1
        
        # Boutons presets
        presets = [
            ("YouTube", "https://www.youtube.com"),
            ("Gmail", "https://mail.google.com"),
            ("GitHub", "https://github.com"),
            ("Twitter/X", "https://twitter.com"),
            ("WhatsApp Web", "https://web.whatsapp.com"),
            ("ChatGPT", "https://chat.openai.com")
        ]
        
        for i, (name, url) in enumerate(presets):
            btn = ttk.Button(presets_frame, text=name, 
                           command=lambda n=name, u=url: self.load_preset(n, u))
            btn.grid(row=i//3, column=i%3, padx=5, pady=2, sticky=(tk.W, tk.E))
            presets_frame.columnconfigure(i%3, weight=1)
        
        # Boutons d'action
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=row, column=0, columnspan=3, pady=(10, 0))
        row += 1
        
        ttk.Button(action_frame, text="🔍 Vérifier prérequis", 
                  command=self.check_prerequisites).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="🚀 Créer l'application", 
                  command=self.create_app, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="📋 Générer commande", 
                  command=self.show_command).pack(side=tk.LEFT)
        
        # Zone de log
        log_frame = ttk.LabelFrame(main_frame, text="Journal d'activité", padding="5")
        log_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(row, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=row+1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.log("✅ Interface initialisée")
        
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
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.icon_path_var.set(filename)
            self.log(f"🎨 Icône sélectionnée: {os.path.basename(filename)}")
            
    def clear_icon(self):
        """Efface le chemin de l'icône"""
        self.icon_path_var.set("")
        self.log("🗑️ Icône effacée")
        
    def log(self, message):
        """Ajoute un message au journal"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def check_prerequisites(self):
        """Vérifie si Node.js, Rust et Pake sont installés"""
        self.log("🔍 Vérification des prérequis...")
        
        def check():
            # Vérifier Node.js
            try:
                result = subprocess.run(['node', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.log(f"✅ Node.js installé: {version}")
                else:
                    self.log("❌ Node.js non trouvé")
                    return False
            except FileNotFoundError:
                self.log("❌ Node.js non installé")
                return False
                
            # Vérifier Rust
            try:
                result = subprocess.run(['rustc', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.log(f"✅ Rust installé: {version}")
                else:
                    self.log("❌ Rust non trouvé")
                    return False
            except FileNotFoundError:
                self.log("❌ Rust non installé")
                return False
                
            # Vérifier Pake
            try:
                result = subprocess.run(['pake', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.log(f"✅ Pake installé: {version}")
                    return True
                else:
                    self.log("❌ Pake non trouvé")
                    return False
            except FileNotFoundError:
                self.log("❌ Pake non installé")
                self.log("💡 Installez Pake avec: npm install -g pake-cli")
                return False
                
        threading.Thread(target=check, daemon=True).start()
        
    def generate_command(self):
        """Génère la commande Pake"""
        if not self.url_var.get().strip():
            return None
            
        url = self.url_var.get().strip()
        name = self.name_var.get().strip() or "MonApp"
        
        # Nettoyer le nom (supprimer caractères spéciaux)
        name = re.sub(r'[^\w\s-]', '', name).strip()
        name = re.sub(r'\s+', '_', name)
        
        cmd = ['pake', url, '--name', name]
        
        # Ajouter les options
        if self.width_var.get() and self.width_var.get().isdigit():
            cmd.extend(['--width', self.width_var.get()])
            
        if self.height_var.get() and self.height_var.get().isdigit():
            cmd.extend(['--height', self.height_var.get()])
            
        if self.icon_path_var.get():
            cmd.extend(['--icon', self.icon_path_var.get()])
            
        if self.fullscreen_var.get():
            cmd.append('--fullscreen')
            
        if self.hide_title_var.get():
            cmd.append('--hide-title-bar')
            
        return cmd
        
    def show_command(self):
        """Affiche la commande qui sera exécutée"""
        cmd = self.generate_command()
        if cmd:
            cmd_str = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in cmd)
            messagebox.showinfo("Commande Pake", f"Commande à exécuter:\n\n{cmd_str}")
            self.log(f"📋 Commande générée: {cmd_str}")
        else:
            messagebox.showerror("Erreur", "Veuillez renseigner au moins l'URL du site")
            
    def create_app(self):
        """Lance la création de l'application"""
        cmd = self.generate_command()
        if not cmd:
            messagebox.showerror("Erreur", "Veuillez renseigner au moins l'URL du site")
            return
            
        def run_pake():
            try:
                self.progress.start(10)
                self.log(f"🚀 Démarrage de la création de l'application...")
                cmd_str = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in cmd)
                self.log(f"📝 Commande: {cmd_str}")
                
                # Exécuter Pake
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    universal_newlines=True
                )
                
                # Lire la sortie en temps réel
                for line in process.stdout:
                    line = line.strip()
                    if line:
                        self.log(f"📦 {line}")
                        
                process.wait()
                
                if process.returncode == 0:
                    self.log("🎉 Application créée avec succès!")
                    messagebox.showinfo("Succès", "L'application a été créée avec succès!\nVérifiez le dossier courant pour le fichier d'installation.")
                else:
                    self.log(f"❌ Erreur lors de la création (code: {process.returncode})")
                    messagebox.showerror("Erreur", "Une erreur s'est produite lors de la création de l'application.")
                    
            except Exception as e:
                self.log(f"❌ Erreur: {str(e)}")
                messagebox.showerror("Erreur", f"Erreur lors de l'exécution: {str(e)}")
            finally:
                self.progress.stop()
                
        # Sauvegarder la config
        self.save_config()
        
        # Lancer dans un thread séparé
        threading.Thread(target=run_pake, daemon=True).start()
        
    def save_config(self):
        """Sauvegarde la configuration"""
        config = {
            'url': self.url_var.get(),
            'name': self.name_var.get(),
            'width': self.width_var.get(),
            'height': self.height_var.get(),
            'icon_path': self.icon_path_var.get(),
            'fullscreen': self.fullscreen_var.get(),
            'hide_title': self.hide_title_var.get()
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.log(f"⚠️ Impossible de sauvegarder la config: {e}")
            
    def load_config(self):
        """Charge la configuration sauvegardée"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    
                self.url_var.set(config.get('url', ''))
                self.name_var.set(config.get('name', ''))
                self.width_var.set(config.get('width', '1200'))
                self.height_var.set(config.get('height', '800'))
                self.icon_path_var.set(config.get('icon_path', ''))
                self.fullscreen_var.set(config.get('fullscreen', False))
                self.hide_title_var.set(config.get('hide_title', False))
                
            except Exception as e:
                print(f"Erreur lors du chargement de la config: {e}")

def main():
    """Point d'entrée principal"""
    root = tk.Tk()
    
    # Configuration pour un meilleur rendu sur Windows
    try:
        root.tk.call('tk', 'scaling', 1.2)
    except:
        pass
        
    app = PakeGUI(root)
    
    # Gérer la fermeture
    def on_closing():
        app.save_config()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Lancer l'application
    root.mainloop()

if __name__ == "__main__":
    main()
