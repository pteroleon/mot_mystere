import customtkinter as ctk
import pandas as pd
import os
import mot_mystere as mm


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mot Mystère")
        self.geometry("1280x720")
        self.minsize(960, 540)
        ctk.set_appearance_mode("dark")

        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=2)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.liste_mots = mm.liste_mots

        self.pseudo = None

        # Initialisation des zones
        # Barre gauche
        self.sidebar_gauche = SidebarGauche(self)
        self.sidebar_gauche.grid(row=1, column=0, sticky="nsew")

        # Zone centrale
        self.zone_centrale = ZoneCentrale(self)
        self.zone_centrale.grid(row=1, column=1, sticky="nsew")

        # Barre droite
        self.sidebar_droite = SidebarDroite(self)
        self.sidebar_droite.grid(row=1, column=2, sticky="nsew")

        # Demande le pseudo
        self.after(500, self.demander_pseudo)

    def demander_pseudo(self):
        """Demande le pseudo : Anonyme si rien est rentrer"""
        dialog = ctk.CTkInputDialog(text="Bienvenue ! Entrez votre pseudo pour jouer :", title="Identification")
        pseudo = dialog.get_input()
        self.pseudo = pseudo if pseudo and pseudo.strip() != "" else "Anonyme"
        self.nouvelle_partie()

    def nouvelle_partie(self):
        self.partie_finie = False
        self.mode = self.sidebar_gauche.box_mode.get()
        difficulte = self.sidebar_gauche.box_dif.get()

        # Réinitialisation des scores (mort subite)
        self.score_total = 0
        self.mots_trouves = 0

        # Paramétrage de la difficulté Initiale
        if self.mode == "Mort Subite":
            self.cible_rating_min = 0.0
            self.cible_rating_max = 3.0
            self.vies_max = 4  # 4 erreurs max par mot en mort subite
        else:
            if difficulte == "Facile":
                self.cible_rating_min = 0.0
                self.cible_rating_max = 4.0
                self.vies_max = 10
            elif difficulte == "Normal":
                self.cible_rating_min = 4.0
                self.cible_rating_max = 7.0
                self.vies_max = 7
            elif difficulte == "Expert":
                self.cible_rating_min = 7.0
                self.cible_rating_max = 10.0
                self.vies_max = 4

        self.lancer_manche()

    def lancer_manche(self):
        self.partie_finie = False
        self.vies = self.vies_max

        # Choix du mot filtré avec rating ciblé
        self.mot_actuel = mm.choix_mot_filtre(self.liste_mots, self.cible_rating_min, self.cible_rating_max)
        self.mystere = mm.mot_mystere(self.mot_actuel)
        self.lettres_proposees = []

        # Mise à jour de l'interface
        self.zone_centrale.lbl_mot.configure(text=self.mystere)
        # Nombre de vie restante
        self.zone_centrale.lbl_vies.configure(text=f"❤️ Vies : {self.vies}")

        # Mode actuel
        info_diff = f"Mort Subite ({self.mots_trouves} trouvés)" if self.mode == "Mort Subite" else f"Normal ({self.sidebar_gauche.box_dif.get()})"
        self.zone_centrale.lbl_difficulte.configure(text=info_diff)

        # Lettre déjà proposés et qui ne sont pas dans le mot
        self.zone_centrale.lbl_fausses.configure(text="Lettres absentes : aucune")
        self.zone_centrale.lbl_message.configure(text=f"Bonne chance {self.pseudo} !", text_color="white")

        self.zone_centrale.entree_lettre.delete(0, 'end')
        self.zone_centrale.entree_lettre.focus()


class SidebarGauche(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=280, corner_radius=0, border_width=1, **kwargs)

        #Titre
        self.lbl_titre = ctk.CTkLabel(self, text="Créer une partie", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titre.pack(pady=(30, 10))

        # Mode de jeu
        self.frame_mode = ctk.CTkFrame(self)
        self.frame_mode.pack(fill="x", padx=10, pady=(5, 0))
        self.frame_titre2 = ctk.CTkFrame(self.frame_mode, fg_color=("#cccccc", "#454547"))
        self.frame_titre2.pack(fill="x", padx=15, pady=(10, 12))
        ctk.CTkLabel(self.frame_titre2, text="Mode de Jeu :", font=ctk.CTkFont(weight="bold", size=16)).pack(padx=5,
                                                                                                             pady=5)
        # Bouton segmentés Mode de Jeu
        self.box_mode = ctk.CTkSegmentedButton(self.frame_mode, values=["Normal", "Mort Subite"])
        self.box_mode.pack(pady=10, padx=10, fill="x")
        self.box_mode.set("Normal")

        # Difficulté
        self.frame_difficulte = ctk.CTkFrame(self)
        self.frame_difficulte.pack(fill="x", padx=10, pady=(10, 0))
        self.frame_titre1 = ctk.CTkFrame(self.frame_difficulte, fg_color=("#cccccc", "#454547"))
        self.frame_titre1.pack(fill="x", padx=15, pady=(10, 12))
        ctk.CTkLabel(self.frame_titre1, text="Difficulté :", font=ctk.CTkFont(weight="bold", size=16)).pack(padx=5,
                                                                                                            pady=5)
        # Bouton segmentés Difficulté
        self.box_dif = ctk.CTkSegmentedButton(self.frame_difficulte, values=["Facile", "Normal", "Expert"])
        self.box_dif.pack(pady=10, padx=10, fill="x")
        self.box_dif.set("Facile")

        # Bouton Lancer
        self.btn_nouvelle = ctk.CTkButton(self, text="Nouvelle Partie", font=ctk.CTkFont(size=18, weight="bold"),
                                          height=40, command=self.lancer_partie)
        self.btn_nouvelle.pack(pady=30, padx=20, fill="x")

    def lancer_partie(self):
        if self.master.pseudo:
            self.master.nouvelle_partie()


class ZoneCentrale(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, border_width=1, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # titre
        self.lbl_titre = ctk.CTkLabel(self, text="Trouvez le Mot Mystère", font=ctk.CTkFont(size=26, weight="bold"))
        self.lbl_titre.pack(pady=(30, 10))

        self.lbl_mot = ctk.CTkLabel(self, text="", font=ctk.CTkFont(family="Courier", size=42, weight="bold"))
        self.lbl_mot.pack(pady=30)

        self.cadre_info = ctk.CTkFrame(self, fg_color="transparent")
        self.cadre_info.pack(pady=10)

        # Affichage des vies
        self.lbl_vies = ctk.CTkLabel(self.cadre_info, text="❤️ Vies : -", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_vies.pack(side="left", padx=30)

        #affichage du Mode
        self.lbl_difficulte = ctk.CTkLabel(self.cadre_info, text="Mode : -", font=ctk.CTkFont(size=16))
        self.lbl_difficulte.pack(side="right", padx=30)

        # Affichage de la listes des lettres déjà proposées et fausses
        self.lbl_fausses = ctk.CTkLabel(self, text="Lettres absentes : aucune",
                                        font=ctk.CTkFont(size=14))
        self.lbl_fausses.pack(pady=(10, 10))

        # Input pour proposer une lettre
        self.entree_lettre = ctk.CTkEntry(self, placeholder_text="Tapez une lettre...", width=180, height=40,
                                          font=ctk.CTkFont(size=18), justify="center")
        self.entree_lettre.pack(pady=15)
        self.entree_lettre.bind('<Return>', self.valider_lettre)

        self.btn_valider = ctk.CTkButton(self, text="Valider", height=40, command=self.valider_lettre)
        self.btn_valider.pack(pady=10)

        self.lbl_message = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_message.pack(pady=20)

    def valider_lettre(self, event=None):
        app = self.master
        if app.partie_finie: return

        lettre = self.entree_lettre.get().lower().strip()
        self.entree_lettre.delete(0, 'end')

        #Cheatcode si on rentre "NSI"
        if lettre == "nsi":
            app.mystere = " ".join(app.mot_actuel)
            self.lbl_mot.configure(text=app.mystere)
            app.partie_finie = True
            self.verifier_fin_partie()
            return

        #Cheatcode si on rentre "HAINAUT"
        elif lettre == "hainaut":
            self.lbl_mot.configure(text=app.mystere)
            self.lbl_message.configure(text=f"Triche activée... Le mot est {app.mot_actuel}", text_color="yellow")
            return

        # Vérifiaction si l'utilisateur donne bien une seule lettre
        elif len(lettre) != 1 or not lettre.isalpha():
            self.lbl_message.configure(text="⚠️ Veuillez saisir une seule lettre !", text_color="orange")
            return

        # Vérifiaction si l'utilisateur donne une lettre déjà proposée
        elif lettre in app.mystere or lettre in app.lettres_proposees:
            self.lbl_message.configure(text="🔄 Vous avez déjà proposé cette lettre !", text_color="orange")
            return

        # Lettre présente dans le mot
        elif mm.verification(lettre, app.mot_actuel):
            self.lbl_message.configure(text="✅ Bien joué !", text_color="#2ecc71")
            app.mystere = mm.completer_mot(lettre, app.mot_actuel, app.mystere)
            self.lbl_mot.configure(text=app.mystere)

        # Sinon il perd une vie
        else:
            self.lbl_message.configure(text="❌ Raté...", text_color="#e74c3c")
            app.lettres_proposees.append(lettre)
            app.vies -= 1
            self.lbl_vies.configure(text=f"❤️ Vies : {app.vies}")
            self.lbl_fausses.configure(text=f"Lettres absentes : {', '.join(app.lettres_proposees)}")

        self.verifier_fin_partie()

    def verifier_fin_partie(self):
        app = self.master

        # Si le mot a été trouvé
        if "_" not in app.mystere:
            app.partie_finie = True
            note_mot = mm.rating(app.mot_actuel)
            app.score_total += note_mot
            app.mots_trouves += 1

            # Si en mode mort subite
            if app.mode == "Mort Subite":
                self.lbl_message.configure(
                    text=f"✅ GAGNÉ ! Score de ce mot : {note_mot:.1f}\nPréparez-vous pour le suivant...",
                    text_color="#2ecc71")
                # Augmentation progressive de la difficulté
                app.cible_rating_min = min(9.0, app.cible_rating_min + 0.5)
                app.cible_rating_max = min(10.0, app.cible_rating_max + 0.5)
                # On relance automatiquement après 3 secondes
                self.after(3000, app.lancer_manche)
            else:
                # Message de victoire
                self.lbl_message.configure(
                    text=f"🎉 GAGNÉ !\nLe mot était : {app.mot_actuel.upper()}\nScore de ce mot : {note_mot:.1f}/10",
                    text_color="#2ecc71")

                # Ajout du score dans le tableau
                mm.ajouter_tableau(app.pseudo, round(app.score_total, 1), app.mot_actuel)
                app.sidebar_droite.maj_classement()

        elif app.vies <= 0:
            app.partie_finie = True
            mot_entier = " ".join(app.mot_actuel).upper()
            self.lbl_mot.configure(text=mot_entier)

            if app.mode == "Mort Subite":
                # Message de fin
                self.lbl_message.configure(
                    text=f"💀 PERDU !\nFin de la mort subite.\nMots trouvés : {app.mots_trouves} | Score Final : {app.score_total:.1f}\nLe mot était : {app.mot_actuel.upper()}",
                    text_color="#e74c3c")
                if app.mots_trouves > 0:
                    # Ajout du score dans le tableau
                    mm.ajouter_tableau(app.pseudo, round(app.score_total, 1), f"{app.mots_trouves} mots (MS)")
            else:
                # Message de défaite
                self.lbl_message.configure(text=f"💀 PERDU !\nLe mot était : {app.mot_actuel.upper()}",
                                           text_color="#e74c3c")

            # mis à jour du classement
            app.sidebar_droite.maj_classement()


class SidebarDroite(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=280, corner_radius=0, border_width=1, **kwargs)

        # Titre
        self.lbl_titre = ctk.CTkLabel(self, text="Statistiques", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titre.pack(pady=(30, 10))

        # Graphique
        self.frame_graphe = ctk.CTkFrame(self)
        self.frame_graphe.pack(fill="x", padx=10, pady=(5, 0))
        self.btn_graphe = ctk.CTkButton(self.frame_graphe, text="Graphique des notes", font=("Arial", 16, "bold"),
                                        command=self.afficher_graphe)
        self.btn_graphe.pack(padx=5, pady=15, fill="x")

        # Classement
        self.frame_classement = ctk.CTkFrame(self)
        self.frame_classement.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        self.frame_titre3 = ctk.CTkFrame(self.frame_classement, fg_color=("#cccccc", "#454547"))
        self.frame_titre3.pack(fill="x", padx=15, pady=(10, 12))
        ctk.CTkLabel(self.frame_titre3, text="Classement :", font=ctk.CTkFont(weight="bold", size=16)).pack(padx=5,
                                                                                                            pady=5)

        self.textbox_classement = ctk.CTkTextbox(self.frame_classement, font=("Courier", 13), activate_scrollbars=False)
        self.textbox_classement.pack(fill="both", expand=True, padx=10, pady=10)

        self.maj_classement()

    def afficher_graphe(self):
        mm.generer_graphique_notes(self.master.liste_mots)

    def maj_classement(self):
        self.textbox_classement.configure(state="normal")
        self.textbox_classement.delete("1.0", "end")

        if os.path.exists("tableau_score.csv"):

            df = pd.read_csv("tableau_score.csv")
            if df.empty:
                self.textbox_classement.insert("1.0", "Aucun score.")
            else:
                # Affichage du tableau
                df = df.sort_values(by=["Note"], ascending=False).head(15)
                en_tete = f"{'Nom':<9} | {'Score':<5} | {'Mot/Mode'}\n"
                separation = "-" * 30 + "\n"
                texte_final = en_tete + separation

                for _, row in df.iterrows():
                    nom = str(row.get('Nom', 'Inconnu'))[:9].ljust(9)
                    note = f"{float(row.get('Note', 0)):.1f}".ljust(5)
                    mot = str(row.get('Mot', ''))
                    texte_final += f"{nom} | {note} | {mot}\n"

                self.textbox_classement.insert("1.0", texte_final)

        else:
            mm.reset_tableau()

        self.textbox_classement.configure(state="disabled")


if __name__ == '__main__':
    app = App()
    app.mainloop()