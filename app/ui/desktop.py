import os
import threading
from pathlib import Path
from typing import Optional

import customtkinter as ctk
from tkinter import END
from PIL import Image
from langchain_core.documents import Document

from app.rag.rag_pipeline import RAGPipeline

# Jetons de couleur (MD3 : pas de hex brut dans les widgets)
COLOR_PRIMARY = "#FF7A00"
COLOR_PRIMARY_HOVER = "#E86800"
COLOR_SURFACE = "#FFFFFF"
COLOR_SURFACE_VARIANT = "#F5F5F5"
COLOR_ON_SURFACE = "#333333"
COLOR_ON_SURFACE_VARIANT = "#888888"
COLOR_ERROR = "#C62828"

ICON_DIR = Path(__file__).parent / "assets" / "icons"
SPINNER_FRAME_COUNT = 12
SPINNER_INTERVAL_MS = 80


class RAGDesktopApp:
    """Interface desktop : capture les requêtes et affiche les réponses du RAG."""

    def __init__(self, rag_pipeline: Optional[RAGPipeline] = None):
        ctk.set_appearance_mode("light")

        # Injection de dépendance : on instancie le pipeline uniquement si rien n'est fourni
        self.rag = rag_pipeline or RAGPipeline()

        self.app = ctk.CTk()
        self.app.title("Assistant RAG")
        self.app.geometry("950x650")
        self.app.configure(fg_color=COLOR_SURFACE)

        self._setup_ui_components()
        
        self._spinner_job = None
        self._spinner_frame = 0

    def _setup_ui_components(self) -> None:
        """Initialise et dispose tous les composants graphiques."""
        self.header = ctk.CTkFrame(self.app, height=70, fg_color=COLOR_PRIMARY, corner_radius=0)
        self.header.pack(fill="x")

        self.title = ctk.CTkLabel(
            self.header,
            text="Assistant IA -- RAG",
            text_color=COLOR_SURFACE,
            font=("Segoe UI", 24, "bold"),
        )
        self.title.place(x=20, y=15)

        self.output_box = ctk.CTkTextbox(
            self.app,
            width=880,
            height=420,
            corner_radius=15,
            fg_color=COLOR_SURFACE_VARIANT,
            text_color=COLOR_ON_SURFACE,
            font=("Segoe UI", 14),
        )
        self.output_box.pack(pady=20)

        input_frame = ctk.CTkFrame(self.app, fg_color=COLOR_SURFACE)
        input_frame.pack(fill="x", pady=(10, 0))

        self.input_field = ctk.CTkEntry(
            input_frame,
            width=700,
            height=45,
            corner_radius=15,
            fg_color=COLOR_SURFACE,
            border_color=COLOR_PRIMARY,
            border_width=2,
            text_color=COLOR_ON_SURFACE,
            placeholder_text="Pose ta question ici...",
            placeholder_text_color=COLOR_ON_SURFACE_VARIANT,
            font=("Segoe UI", 14),
        )
        self.input_field.pack(side="left", padx=15, pady=10)
        self.input_field.bind("<Return>", lambda _event: self.ask_question())

        self.send_icon = self._load_icon("send.png")
        self.spinner_frames = [self._load_icon(f"spinner_{i:02d}.png") for i in range(SPINNER_FRAME_COUNT)]

        self.ask_button = ctk.CTkButton(
            input_frame,
            image=self.send_icon,
            text="",
            width=45,
            height=45,
            corner_radius=15,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            command=self.ask_question,
        )
        self.ask_button.pack(side="left", padx=10)

        self.error_label = ctk.CTkLabel(
            self.app,
            text="",
            text_color=COLOR_ERROR,
            font=("Segoe UI", 12),
        )
        self.error_label.pack(pady=(0, 10))

    def _load_icon(self, filename: str) -> ctk.CTkImage:
        """Charge une icône depuis le dossier assets."""
        image = Image.open(ICON_DIR / filename)
        return ctk.CTkImage(light_image=image, dark_image=image, size=(20, 20))

    def ask_question(self) -> None:
        """Capture l'entrée utilisateur et lance le traitement asynchrone."""
        query = self.input_field.get().strip()
        if not query:
            return

        self._clear_input()
        self._display_user_message(query)
        self._set_loading(True)

        def worker() -> None:
            try:
                # Le pipeline retourne désormais un tuple (réponse, documents)
                response, docs = self.rag.ask(query)
                self.app.after(0, lambda: self._on_response(response, docs))
            except Exception as exc:
                self.app.after(0, lambda: self._on_error(exc))

        threading.Thread(target=worker, daemon=True).start()

    def _clear_input(self) -> None:
        """Réinitialise le champ de saisie et les erreurs."""
        self.error_label.configure(text="")
        self.input_field.delete(0, END)

    def _display_user_message(self, query: str) -> None:
        """Affiche le message de l'utilisateur dans la boîte de sortie."""
        self.output_box.insert(END, f"\nVous : {query}\n")
        self.output_box.see(END)

    def _format_sources(self, docs: list[Document]) -> str:
        """Formate les métadonnées des documents pour l'affichage (Logique de présentation pure)."""
        if not docs:
            return ""
        
        sources_str = "\n--- SOURCES UTILISEES ---\n"
        for i, doc in enumerate(docs):
            source_path = doc.metadata.get("source", "Inconnu")
            source_file = os.path.basename(source_path)
            text_preview = doc.page_content.replace('\n', ' ')[:100] + "..."
            sources_str += f"  > [{i+1}] {source_file} -- {text_preview}\n"
        
        sources_str += "-" * 40 + "\n"
        return sources_str

    def _display_assistant_message(self, response: str, docs: list[Document]) -> None:
        """Affiche la réponse de l'assistant et ses sources."""
        self.output_box.insert(END, f"Assistant : {response}\n")
        self.output_box.insert(END, self._format_sources(docs))
        self.output_box.see(END)

    def _set_loading(self, loading: bool) -> None:
        """Gère l'état de chargement de l'interface (désactivation inputs + spinner)."""
        state = "disabled" if loading else "normal"
        self.input_field.configure(state=state)
        self.ask_button.configure(state=state)

        if loading:
            self._spinner_frame = 0
            self._animate_spinner()
        else:
            if self._spinner_job is not None:
                self.app.after_cancel(self._spinner_job)
                self._spinner_job = None
            self.ask_button.configure(image=self.send_icon)

    def _animate_spinner(self) -> None:
        """Gère l'animation du bouton de chargement."""
        self.ask_button.configure(image=self.spinner_frames[self._spinner_frame])
        self._spinner_frame = (self._spinner_frame + 1) % SPINNER_FRAME_COUNT
        self._spinner_job = self.app.after(SPINNER_INTERVAL_MS, self._animate_spinner)

    def _on_response(self, response: str, docs: list[Document]) -> None:
        """Callback de succès : arrête le chargement et affiche le résultat."""
        self._set_loading(False)
        self._display_assistant_message(response, docs)

    def _on_error(self, exc: Exception) -> None:
        """Callback d'erreur : arrête le chargement et affiche l'erreur."""
        self._set_loading(False)
        self.error_label.configure(
            text=f"Erreur : {exc}. Vérifie qu'Ollama est lancé, puis réessaie."
        )

    def run(self) -> None:
        """Lance la boucle principale de l'application."""
        self.app.mainloop()