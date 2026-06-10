# Stream PDF 🇫🇷

Ce projet est un script Python conçu pour analyser et extraire des données à partir de fichiers PDF, en mettant l'accent sur le digital forensic, la stéganographie et les défis CTF (Capture The Flag). J'ai développé ce script moi-même dans le but de résoudre un challenge RootMe [PDF-Embedded](https://www.root-me.org/fr/Challenges/Steganographie/PDF-Embedded).

Les principales caractéristiques du script incluent :

1. **Afficher les listes d'objets/stream :** Les utilisateurs peuvent accéder à des listes d'objets et de stream à l'intérieur d'un fichier PDF désigné, ce qui leur permet de mieux comprendre la structure du document.

2. **Extraire tous les objets/stream :** Cette fonctionnalité facilite l'extraction de tous les objets et stream à partir d'un fichier PDF, les enregistrant dans un fichier généré. (Note : Cette fonctionnalité n'est pas recommandée pour les fichiers PDF volumineux, car elle peut provoquer un plantage du script.)

3. **Extraire un objet/stream spécifique :** Cette fonctionnalité permet aux utilisateurs d'extraire un objet ou un stream particulier d'un PDF en spécifiant son numéro.

4. **Extraire FlateDecode :** Le script est capable d'extraire des objets/stream FlateDecode du PDF. De plus, les utilisateurs ont la possibilité de décoder le contenu au format base64, ce qui est utile pour révéler des informations cachées.

Ce projet a été développé pour répondre aux besoins de ceux qui travaillent dans la cybercriminalité numérique, la stéganographie, les passionés de CTF et qui utilisent des fichiers PDF, nécessitant un outil polyvalent pour l'analyse détaillée et l'extraction de données.

English version [here](EN/README.md) 🇬🇧

## Démonstration
![](fr_demo.gif)

## Installation

Vous pouvez installer le projet en exécutant la commande suivante :
    
```
git clone https://github.com/CalValmar/Stream-pdf.git
```
N'oubliez pas d'installer les dépendances :    
```
pip install -r requirements.txt
```
Si `colorama` n'est pas installé, le script fonctionne quand même sans couleurs.

## Utilisation

Pour utiliser le script, exécutez la commande suivante :    

```
python3 stream-pdf.py
```

⚠️  Avant d'exécuter le script, placez le fichier PDF à analyser dans le dossier du script. Vous pouvez aussi adapter la variable `default_pdf_file` si vous voulez changer le fichier utilisé par défaut.
    
```
default_pdf_file = 'your_pdf_file.pdf'
```

⚠️  Le document `bac2004.pdf` est un exemple de fichier PDF fourni avec le projet pour tester le script. Vous pouvez le supprimer si vous le souhaitez.

## Licence

Ce projet est sous licence GNU General Public License v3.0 - consultez le fichier [LICENSE](LICENSE) pour plus de détails.

GNU General Public License v3.0 © [CalValmar](https://github.com/CalValmar)

## Inspirations et informations supplémentaires

- [FlateDecode](https://gist.github.com/averagesecurityguy/ba8d9ed3c59c1deffbd1390dafa5a3c2)
- [peepdf](https://eternal-todo.com/tools/peepdf-pdf-analysis-tool/)
