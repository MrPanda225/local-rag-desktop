import customtkinter as ctk
from tkinter import END
from app.rag.rag_pipeline import RAGPipeline


class RAGDesktopApp:
    def __init__(self):
        # Mode clair
        ctk.set_appearance_mode("light")

        # Fenêtre principale
        self.app = ctk.CTk()
        self.app.title("")
        self.app.geometry("950x650")
        self.app.configure(fg_color="#FFFFFF")  # Fond blanc

        # HEADER ORANGE
        self.header = ctk.CTkFrame(
            self.app,
            height=70,
            fg_color="#FF7A00",  # Orange dynamique
            corner_radius=0
        )
        self.header.pack(fill="x")

        # Titre du header
        self.title = ctk.CTkLabel(
            self.header,
            text="🤖 Assistant IA – RAG Test",
            text_color="white",
            font=("Segoe UI", 24, "bold")
        )
        self.title.place(x=20, y=15)

        # ZONE DE CHAT (gris clair)
        self.output_box = ctk.CTkTextbox(
            self.app,
            width=880,
            height=420,
            corner_radius=15,
            fg_color="#F5F5F5",   # gris clair
            text_color="#333333",  # texte gris foncé
            font=("Segoe UI", 14)
        )
        self.output_box.pack(pady=20)

        # FRAME INPUT
        input_frame = ctk.CTkFrame(
            self.app,
            fg_color="#FFFFFF"  # fond blanc
        )
        input_frame.pack(fill="x", pady=10)

        # Champ d’entrée blanc + bord orange
        self.input_field = ctk.CTkEntry(
            input_frame,
            width=700,
            height=45,
            corner_radius=15,
            fg_color="#FFFFFF",
            border_color="#FF7A00",  # Bord orange
            border_width=2,
            text_color="#333333",
            placeholder_text="Pose ta question ici...",
            placeholder_text_color="#888888",
            font=("Segoe UI", 14)
        )
        self.input_field.pack(side="left", padx=15, pady=10)

        # Bouton ORANGE dynamique
        self.ask_button = ctk.CTkButton(
            input_frame,
            text="Demander 💬",
            width=180,
            height=45,
            corner_radius=15,
            fg_color="#FF7A00",      # orange
            hover_color="#E86800",   # orange plus foncé
            text_color="white",
            font=("Segoe UI", 15, "bold"),
            command=self.ask_question
        )
        self.ask_button.pack(side="left", padx=10)

    def ask_question(self):
        query = self.input_field.get().strip()
        if not query:
            return

        self.output_box.insert(END, f"\n🟧 Vous : {query}\n")
        self.output_box.see(END)

        response = self.rag.ask(query)

        self.output_box.insert(END, f"🟦 IA : {response}\n")
        self.output_box.see(END)

        self.input_field.delete(0, END)

    def run(self):
        self.rag = RAGPipeline()
        self.app.mainloop()
