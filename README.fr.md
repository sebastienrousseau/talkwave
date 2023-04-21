<!-- markdownlint-disable MD033 MD041 -->

<img src="https://kura.pro/talkwave/images/logos/talkwave.svg" alt="talkwave logo" width="261" align="right" />

<!-- markdownlint-enable MD033 MD041 -->

# Python TalkWave

![talkwave banner](https://kura.pro/talkwave/images/titles/title-talkwave.svg)

## Aperçu 📖

TalkWave est un chatbot d'IA pour les développeurs écrit en Python. Il dispose d'une interface HTML simple et est conçu pour être accessible sur différents navigateurs et appareils. TalkWave prend en charge les opérations asynchrones et peut gérer plusieurs demandes simultanément.

## Fonctionnalités ✨

- [x] Accepte une gamme de paramètres pour personnaliser la réponse, tels que le nombre maximal de jetons, la température et les conditions d'arrêt.
- [x] Conception accessible pour une compatibilité inter-navigateurs et inter-appareils (Chrome, Firefox, Safari, Edge et mobile).
- [x] Limite précisément la facturation avec des limites et une liaison d'ID pour éviter de dépasser les limites de l'API et de supporter des frais.
- [x] Implémente une fonctionnalité de limitation de taux pour éviter de dépasser les limites de l'API et de supporter des frais.
- [x] Implémentation Python simple avec un nombre limité de dépendances pour une installation et une utilisation faciles.
- [x] Stocke les réponses dans des fichiers journaux, des formats JSON et Markdown pour une analyse et un partage faciles.
- [x] Prend en charge plusieurs modèles GPT pour la génération de réponses, notamment "gpt-3.5-turbo", "text-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001".

## Exigences 📋

- Python 3.6 ou supérieur
- Les packages `openai`, `tabulate` et `python-dotenv`
- Une clé d'API OpenAI (en obtenir une [ici](https://openai.com/))

## Installation 🛠

1. Installer les packages requis:

```bash
pip install openai tabulate python-dotenv
```

1. Clonez le référentiel TalkWave:

```bash
git clone https://github.com/yourusername/talkwave.git
```

1. Ajoutez votre clé d'API OpenAI à un fichier `.env` dans le répertoire du projet:

```bash
OPENAI_API_KEY="your_api_key_here"
```

## Utilisation 🚀

### Interface de ligne de commande

Pour utiliser TalkWave, accédez au répertoire du projet dans votre terminal et exécutez la commande suivante:

```bash
python talkwave -p "Votre prompt ici"
```

Vous pouvez également spécifier des options supplémentaires, telles que le modèle GPT, le nombre maximal de jetons, la température et l'ID utilisateur:

```bash
python talkwave -m 1 -p "Dis-moi une blague" -t 50 -T 0.5 -u "test@test.com" -r 5 -s -o "json"
```

Pour plus d'informations sur les options disponibles, exécutez:

```bash
python talkwave --help
```

### Interface Web

Pour utiliser l'interface web, accédez au répertoire du projet dans
votre terminal et exécutez la commande suivante :

```bash
python talkwave/frontend.py
```

Ensuite, ouvrez votre navigateur et rendez-vous sur
<http://127.0.0.1:5000>. Cela ouvrira l'interface web de TalkWave, que
vous pourrez utiliser pour générer des réponses.

## Structure des fichiers 📁

```bash
.
├── talkwave
│   ├── data
│   ├── templates
│   │   ├── 404.html
│   │   └── index.html
│   ├── utils
│   │   ├── curl.py
│   │   └── dir.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── core.py
│   └── frontend.py
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE-APACHE
├── LICENSE-MIT
├── MANIFEST.in
├── README.md
├── README_fr.md
├── TEMPLATE.md
├── pylintrc
├── pyproject.toml
├── requirements.txt
├── setup.cfg
└── setup.py
```

## License 📜

Le projet est sous licence des termes de la licence MIT et de la Licence Apache (Version 2.0).

- [Licence Apache, Version 2.0](https://opensource.org/licenses/apache-2.0/)
- [Licence MIT](https://opensource.org/licenses/MIT)
