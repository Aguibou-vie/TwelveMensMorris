# Import de la bibliothèque tkinter
import tkinter as tk

# Liste des 24 positions sur le plateau
points = [
    (100, 100), (400, 100), (700, 100),
    (700, 400), (700, 700), (400, 700),
    (100, 700), (100, 400),

    (200, 200), (400, 200), (600, 200),
    (600, 400), (600, 600), (400, 600),
    (200, 600), (200, 400),

    (300, 300), (400, 300), (500, 300),
    (500, 400), (500, 500), (400, 500),
    (300, 500), (300, 400)
]

# Variables globales
joueur_actuel = "noir"             # Le joueur qui commence
positions_occupees = {}            # Dictionnaire pour suivre les cases déjà jouées

# Création de la fenêtre principale
root = tk.Tk()
root.title("Twelve Men's Morris")  # Titre de la fenêtre
root.geometry("800x800")           # Taille de la fenêtre

# Canvas de dessin (zone graphique)
canvas = tk.Canvas(root, width=800, height=800, bg="beige")
canvas.pack()

# Fonction qui dessine le plateau
def dessiner_plateau():
    # On définit les marges pour les 3 carrés imbriqués
    marges = [100, 200, 300]
    taille = 800

    # On dessine les 3 carrés
    for marge in marges:
        canvas.create_rectangle(marge, marge, taille - marge, taille - marge, width=2)

    # On relie les carrés au centre
    centre = taille // 2
    canvas.create_line(centre, marges[0], centre, marges[1], width=2)
    canvas.create_line(centre, taille - marges[0], centre, taille - marges[1], width=2)
    canvas.create_line(marges[0], centre, marges[1], centre, width=2)
    canvas.create_line(taille - marges[0], centre, taille - marges[1], centre, width=2)

    # Connexions entre les points (lignes)
    lignes = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
        (5, 6), (6, 7), (7, 0),

        (8, 9), (9,10), (10,11), (11,12), (12,13),
        (13,14), (14,15), (15,8),

        (16,17), (17,18), (18,19), (19,20), (20,21),
        (21,22), (22,23), (23,16),

        (1,9), (9,17),
        (3,11), (11,19),
        (5,13), (13,21),
        (7,15), (15,23)
    ]

    # On dessine chaque ligne entre deux points
    for (i, j) in lignes:
        x1, y1 = points[i]
        x2, y2 = points[j]
        canvas.create_line(x1, y1, x2, y2, width=2)

    # On dessine les 24 points sous forme de petits cercles noirs
    for (x, y) in points:
        r = 10  # rayon
        canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")

# Fonction appelée quand on clique avec la souris
def clic_souris(event):
    global joueur_actuel

    x, y = event.x, event.y  # Coordonnées du clic
    rayon = 10  # rayon des cercles

    # On vérifie si on a cliqué sur un des 24 points
    for i, (px, py) in enumerate(points):
        distance = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
        if distance <= rayon:
            if i in positions_occupees:
                print(f"Position {i} déjà occupée par {positions_occupees[i]}")
                return  # on ne fait rien si la case est déjà prise

            # On dessine un pion de la couleur du joueur actuel
            couleur = "black" if joueur_actuel == "noir" else "white"
            canvas.create_oval(px - rayon, py - rayon, px + rayon, py + rayon, fill=couleur)

            # On enregistre que la position est occupée
            positions_occupees[i] = joueur_actuel

            print(f"{joueur_actuel} a joué en position {i}")

            # On change de joueur pour le prochain tour
            joueur_actuel = "blanc" if joueur_actuel == "noir" else "noir"
            print(f"C'est au tour du joueur {joueur_actuel}")
            break

# Dessiner le plateau au lancement
dessiner_plateau()

# Lier le clic souris au canvas (très important : Button avec B majuscule)
canvas.bind("<Button-1>", clic_souris)

# Lancer la boucle graphique Tkinter
root.mainloop()
