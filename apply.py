import tkinter as tk
import time
import hashlib

class EntropyCollector:
    def __init__(self, root):
        self.root = root
        self.root.title("Générateur d'entropie - Bouge la souris !")

        # On stocke ici toutes nos données issues des mouvements de souris
        self.random_data = []

        # Label indicatif
        self.label_info = tk.Label(root, text="Bouge la souris pour accumuler de l'entropie.\n"
                                             "Quand tu es prêt, clique sur le bouton.")
        self.label_info.pack(pady=10)

        # Bouton pour générer la donnée aléatoire
        self.generate_button = tk.Button(root, text="Générer la donnée aléatoire", command=self.generate_random)
        self.generate_button.pack(pady=10)

        # Label pour afficher la sortie
        self.label_result = tk.Label(root, text="", fg="blue")
        self.label_result.pack(pady=10)

        # On lie l'événement <Motion> (mouvement de la souris) à la fonction de callback
        self.root.bind("<Motion>", self.on_mouse_move)

    def on_mouse_move(self, event):
        """
        À chaque mouvement de souris, on capture la position x,y
        ainsi que l'heure précise pour accumuler un maximum d'entropie.
        """
        x, y = event.x, event.y
        t = time.time_ns()  # heure en nanosecondes
        # On stocke tout ça dans une liste
        self.random_data.append(f"{x}-{y}-{t}")

    def generate_random(self):
        """
        On prend tout ce qu’on a collecté, on le passe dans un SHA-256
        pour obtenir une valeur pseudo-aléatoire finale.
        """
        if not self.random_data:
            self.label_result.config(text="Pas assez d'entropie collectée. Bouge la souris avant !")
            return

        # Concatène toutes les valeurs en une seule grande chaîne
        combined_data = "".join(self.random_data)
        # Hache la chaîne
        random_hash = hashlib.sha256(combined_data.encode("utf-8")).hexdigest()

        # Affiche le résultat
        self.label_result.config(text=f"Donnée générée (SHA-256) :\n{random_hash}")

        # Réinitialise éventuellement la liste de données si tu veux recommencer
        self.random_data = []

# --- Programme principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = EntropyCollector(root)
    root.mainloop()
