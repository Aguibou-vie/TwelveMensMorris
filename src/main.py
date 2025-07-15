import tkinter as tk

# Création de la fenêtre principale
root = tk.Tk()
root.title("Twelve Men's Morris")
root.geometry("800x800")

# Canvas de dessin
canvas = tk.Canvas(root, width=800, height=800, bg="beige")
canvas.pack()

# Coordonnées des carrés
marges = [100, 200, 300]
taille = 800

# Fonction pour dessiner le plateau
def dessiner_plateau():
    # 3 carrés imbriqués
    for marge in marges:
        canvas.create_rectangle(marge, marge, taille - marge, taille - marge, width=2)

    # Lignes entre les carrés
    centre = taille // 2
    canvas.create_line(centre, marges[0], centre, marges[1], width=2)
    canvas.create_line(centre, taille - marges[0], centre, taille - marges[1], width=2)
    canvas.create_line(marges[0], centre, marges[1], centre, width=2)
    canvas.create_line(taille - marges[0], centre, taille - marges[1], centre, width=2)

    # Positions des 24 points
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

    # Connexions entre les points
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

    for (i, j) in lignes:
        x1, y1 = points[i]
        x2, y2 = points[j]
        canvas.create_line(x1, y1, x2, y2, width=2)

    # Dessiner les positions (cercles noirs)
    for (x, y) in points:
        r = 10
        canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")

# Appel de la fonction de dessin
dessiner_plateau()

# Boucle Tkinter à la fin
root.mainloop()
