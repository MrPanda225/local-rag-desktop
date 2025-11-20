
---

# 🤖 Assistant IA – RAG Test

Application Desktop locale qui utilise un modèle Ollama + un pipeline RAG pour interroger vos documents hors-ligne.

---

## 🚀 Présentation

Ce projet permet de :

* Charger un document PDF
* L’ingérer en base vectorielle localement (Chroma)
* Utiliser Ollama pour générer des réponses pertinentes
* Poser des questions via une interface graphique moderne
* Fonctionner **100% hors-ligne**, sans envoyer aucune donnée sur Internet

---

## 🧠 Fonctionnalités principales

* 🔍 **RAG (Retrieval Augmented Generation)**
* 📄 Ingestion automatique de PDF
* 💬 Interface Desktop claire moderne (CustomTkinter)
* ⚡ Moteur IA local (Ollama – Mistral, Llama3, etc.)
* 🔒 Respect de la vie privée (tout reste en local)
* 🧱 Architecture propre (KISS, DRY, Clean Code)

---

## 📁 Structure du projet

```
RAG_TEST/
│
├── app/
│   ├── ingestion/        # Ingestion PDF, splitting, embeddings, vectorstore
│   ├── rag/              # Retriever, Generator, Pipeline RAG
│   └── ui/               # Interface Desktop (CustomTkinter)
│
├── documents/            # Contient vos PDF (non versionné)
├── db/                   # Base Chroma (non versionnée)
│
├── main_ingest.py        # Script qui ingère le PDF
├── main.py               # Lance l’interface graphique
├── requirements.txt
└── README.md
```

---

## 🔧 Installation

### 1. Cloner le projet

```bash
git clone <TON_REPO_GITHUB>
cd RAG_TEST
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv
```

* Windows :

  ```bash
  venv\Scripts\activate
  ```

* Linux/macOS :

  ```bash
  source venv/bin/activate
  ```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🤖 Installation d’Ollama

Télécharger Ollama :
👉 [https://ollama.com/download](https://ollama.com/download)

Puis installer les modèles utilisés :

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

---

## 📄 Ajouter vos documents

Placez vos fichiers dans le dossier :

```
documents/
```

Exemple :
`documents/mon_document.pdf`

---

## 🧪 Étape 1 — Lancer l’ingestion

```bash
python main_ingest.py
```

Cela :

* charge le PDF
* découpe en chunks
* génère les embeddings
* enregistre la base vectorielle

---

## 💬 Étape 2 — Lancer l’application IA

```bash
python main.py
```

Vous pourrez poser des questions sur votre document.

---

## 🎨 Interface

Interface moderne, claire, avec :

* fond blanc
* header orange dynamique
* champ de saisie et bouton stylés
* zone de chat avec réponses IA

---

## 🛠️ Technologies utilisées

* Python 3.10+
* LangChain
* ChromaDB
* Ollama
* CustomTkinter
* PyPDF
* Nomic Embeddings
* Mistral / Llama3

---

## 📌 Améliorations possibles

* Import PDF depuis l’UI
* Historique des conversations
* Mode sombre / clair
* Choix du modèle dans l’interface
* Bulles de chat
* Export des réponses
* Version API (FastAPI)

---

## 📄 Licence

Libre d'utilisation.

---
