# Local RAG Desktop

Application desktop 100% locale pour interroger des documents avec une IA embarquée, sans envoyer de données vers le cloud.

Local RAG Desktop transforme une collection de PDF en base de connaissances consultable sur votre machine. L'objectif est simple : obtenir des réponses fiables, sourcées et rapides, tout en gardant vos documents et vos échanges en local.

## Pourquoi ce projet

La plupart des assistants documentaires promettent de la précision, mais reposent souvent sur des API externes ou sur des réponses trop générales. Ce projet prend le contre-pied : il privilégie la confidentialité, la traçabilité et la pertinence.

Il est conçu pour les cas d'usage où la maîtrise des données n'est pas négociable : documentation interne, notes de recherche, corpus métier, rapports PDF ou bases de connaissances personnelles.

## Ce que l'application apporte

- Exécution 100% locale via Ollama.
- Aucune clé API requise.
- Aucune donnée transmise à un service tiers.
- Réponses appuyées sur des extraits réellement retrouvés dans les documents.
- Gestion des questions de suivi grâce au contexte conversationnel.
- Pipeline RAG enrichi avec recherche hybride, reranking et récupération parent-child.

## Fonctionnement

L'application suit une chaîne de traitement pensée pour limiter les hallucinations et améliorer la précision des réponses.

### 1. Ingestion des documents

Les fichiers PDF déposés dans `documents/` sont lus, nettoyés et découpés en segments exploitables. Le système génère ensuite des embeddings et stocke les représentations dans une base vectorielle locale.

### 2. Recherche hybride

Lorsqu'une question est posée, le moteur combine deux approches complémentaires :

- La recherche sémantique pour retrouver les passages proches du sens de la question.
- La recherche lexicale BM25 pour capter les mots-clés exacts, noms propres et expressions spécifiques.

Cette combinaison améliore le rappel sans sacrifier la précision.

### 3. Reranking

Les premiers résultats récupérés ne sont pas tous aussi utiles. Un reranker réévalue les extraits en fonction de la requête et conserve uniquement les plus pertinents pour la génération finale.

### 4. Parent-child chunking

Le système indexe de petits segments pour retrouver l'information avec finesse, mais transmet à l'IA un bloc plus large lors de la réponse. Cela permet de préserver le contexte sans diluer la pertinence.

### 5. Reformulation des requêtes

Pour les questions de suivi, une reformulation transforme une requête implicite en question autonome. Le moteur comprend ainsi plus facilement les références contextuelles et maintient une conversation naturelle.

### 6. Génération contrainte

Le modèle de génération répond uniquement à partir du contexte fourni. Si l'information n'apparaît pas dans les documents récupérés, l'application doit l'indiquer explicitement au lieu d'inventer une réponse.

## Fonctionnalités

- Réponses sourcées à partir des documents chargés.
- Mémoire conversationnelle pour les relances.
- Fonctionnement hors ligne sur poste local.
- Interface desktop en CustomTkinter.
- Stockage local de la base vectorielle avec ChromaDB.
- Support d'un pipeline RAG avancé prêt à être étendu.

## Architecture du projet

```text
local-rag-desktop/
│
├── app/
│   ├── config.py              # Configuration des modèles (LLM et embeddings)
│   ├── ingestion/
│   │   ├── document_loader.py # Extraction PDF avec PyMuPDF
│   │   ├── text_splitter.py   # Logique de découpage parent-child
│   │   ├── embedder.py        # Génération des embeddings via Ollama
│   │   ├── vector_store.py    # Gestion de ChromaDB
│   │   └── ingest.py          # Pipeline d'ingestion
│   │
│   ├── rag/
│   │   ├── retriever.py       # Recherche hybride, reranking et expansion parent
│   │   ├── generator.py       # Génération et reformulation des requêtes
│   │   └── rag_pipeline.py    # Orchestration et garde-fous anti-hallucination
│   │
│   └── ui/
│       └── desktop.py         # Interface desktop CustomTkinter
│
├── documents/                 # Déposez vos PDF ici
├── db/                        # Base vectorielle locale générée automatiquement
│
├── main_ingest.py             # Étape 1 : ingestion des documents
├── main.py                    # Étape 2 : lancement de l'application
├── requirements.txt
└── README.md
```

## Stack technique

| Couche | Technologie | Rôle |
|--------|-------------|------|
| Langage | Python 3.10+ | Logique applicative |
| Orchestration RAG | LangChain | Construction du pipeline |
| Base vectorielle | ChromaDB | Stockage et recherche vectorielle |
| Recherche lexicale | BM25 (`rank-bm25`) | Correspondance exacte de mots-clés |
| Reranking | FlashRank | Tri des extraits par pertinence |
| Runtime LLM | Ollama | Exécution locale des modèles |
| Modèle de génération | Qwen 2.5 7B | Réponses et reformulation |
| Modèle d'embeddings | Nomic Embed Text | Vectorisation des textes |
| Traitement PDF | PyMuPDF | Extraction de texte |
| Interface | CustomTkinter | Application desktop |

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/MrPanda225/local-rag-desktop.git
cd local-rag-desktop
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Configuration d'Ollama

Installez [Ollama](https://ollama.com/download), puis téléchargez les modèles nécessaires.

```bash
ollama pull qwen2.5:7b-instruct-q4_K_M
ollama pull nomic-embed-text
```

## Démarrage rapide

### 1. Ajouter des documents

Placez vos fichiers PDF dans le dossier `documents/`.

### 2. Lancer l'ingestion

```bash
python main_ingest.py
```

Cette étape extrait le texte, construit les segments parent-child, calcule les embeddings et alimente la base locale `db/`.

### 3. Ouvrir l'application

```bash
python main.py
```

Vous pouvez ensuite poser une question, demander une précision ou enchaîner avec une relance. Les réponses s'appuient sur les passages réellement trouvés dans vos documents.

## Cas d'usage

- Interroger une base de PDF métier sans dépendre d'un service cloud.
- Explorer une documentation technique locale avec citations de sources.
- Construire un assistant documentaire privé pour la recherche ou l'entreprise.
- Valider rapidement des informations dans un corpus spécialisé.

## Roadmap

- [ ] Ajouter un mode sombre et un mode clair.
- [ ] Améliorer l'affichage des conversations avec des bulles de chat.
- [ ] Permettre l'import de PDF directement depuis l'interface.
- [ ] Ajouter le streaming des réponses.
- [ ] Intégrer un pipeline OCR pour les PDF scannés.
- [ ] Exposer une API FastAPI pour une intégration web.

