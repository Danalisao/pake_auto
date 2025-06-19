#!/bin/bash

echo "===================================="
echo "       Pake GUI - Lanceur"
echo "===================================="
echo

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python 3 n'est pas installé"
    echo "Veuillez installer Python 3"
    exit 1
fi

# Vérifier si le fichier principal existe
if [[ ! -f "pake_gui.py" ]]; then
    echo "ERREUR: pake_gui.py non trouvé"
    echo "Assurez-vous d'être dans le bon répertoire"
    exit 1
fi

# Lancer l'application
echo "Lancement de Pake GUI..."
python3 pake_gui.py
