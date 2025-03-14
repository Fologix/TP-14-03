import tkinter as tk
import time
import hashlib

from PIL import ImageGrab

class EntropyCollector:
    def __init__(self, root):
        self.root = root
        self.root.title("Générateur d'entropie - Bouge la souris !")

        # Liste pour stocker toutes nos données (coordonnées, timings, pixels)
        self.random_data = []

        # Label d'informations
        self.label_info = tk.Label(root, text="Bouge la souris pour accumuler de l'entropie.\n"
                                             "Quand tu es prêt, clique sur le bouton.")
        self.label_info.pack(pady=10)

        # Bouton de génération
        self.generate_button = tk.Button(root, text="Générer la donnée aléatoire", command=self.generate_random)
        self.generate_button.pack(pady=10)

        # Label pour afficher le résultat
        self.label_result = tk.Label(root, text="", fg="blue")
        self.label_result.pack(pady=10)

        # Liaison de l'événement de mouvement de souris
        self.root.bind("<Motion>", self.on_mouse_move)

    def on_mouse_move(self, event):
        """
        Capturer les mouvements de la souris + un échantillon de pixels autour du pointeur
        pour accumuler plus d'entropie.
        """
        x, y = event.x, event.y
        t = time.time_ns()  # horodatage en nanosecondes

        # Récupération d'un échantillon de pixels autour du curseur
        pixel_data_str = self.capture_pixels(x, y, size=20)

        # On stocke tout dans la liste random_data
        # Le but est juste de "mélanger" toutes ces infos dans le futur hachage
        self.random_data.append(f"{x}-{y}-{t}-{pixel_data_str}")

    def capture_pixels(self, x, y, size=20):
        """
        Capture un carré de `size x size` pixels autour du curseur.
        Convertit ensuite les valeurs en string pour les mélanger à l'entropie.
        """
        # Calcul des bords : on centre le carré sur (x, y).
        # On s'assure aussi de ne pas demander une zone négative (cas proche du bord).
        left   = max(x - size//2, 0)
        top    = max(y - size//2, 0)
        right  = left + size
        bottom = top + size

        # On prend l'écran complet comme référence (0,0) tout en tenant compte
        # que tk se base sur la fenêtre, pas la position absolue écran.
        # -> Il se peut qu'il faille ajuster offsetX, offsetY si la fenêtre
        #    n'est pas au (0,0) en haut à gauche. Mais pour l’exemple, ça marche
        #    souvent directement.
        try:
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            # On récupère tous les pixels -> list de tuples (R, G, B)
            pixels = list(screenshot.getdata())
            # Conversion en chaîne brut (attention, c'est potentiellement volumineux).
            # Pour un usage plus costaud, on peut hacher localement les pixels
            # et renvoyer déjà un hash intermédiaire.
            return str(pixels)
        except Exception as e:
            # En cas d’erreur (permissions, coords hors écran, etc.), on renvoie juste ""
            return ""

    def generate_random(self):
        """
        Concatène tout ce qu'on a collecté et génère un SHA-256.
        """
        if not self.random_data:
            self.label_result.config(text="Pas assez d'entropie collectée. Bouge la souris avant !")
            return

        # Concatène les données
        combined_data = "".join(self.random_data)
        # Hache le tout
        random_hash = hashlib.sha256(combined_data.encode("utf-8")).hexdigest()

        # Affiche le résultat
        self.label_result.config(text=f"Donnée générée (SHA-256) :\n{random_hash}")

        # Réinitialise la liste de données si tu veux relancer
        self.random_data = []

# --- Programme principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = EntropyCollector(root)
    root.mainloop()
