# on importe tkinter (c la bibli pr dessiner le jeu)
import tkinter as tk

# le joueur ki commence (on met noir d’abord) et les cases dja joues
joueur_actuel = "noir"
positions_occupees = {}
mode_suppresion = False # si c True , on supprime le pion
phase_mouvement = False # si true pasons a la phase deplacement
pion_selectionne= None  #pas de pion selectionner au debutç
joueur_en_suppression = None  # le joueur ki a fait le moulin
suppression_effectuee = False

#dictionnaire des pions
pions_a_poser = {
    "noir": 12,
    "blanc": 12
}

# les 24 ptite positions du plateau (c les rond ou on clic)
connexions = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0),
    (8, 9), (9,10), (10,11), (11,12), (12,13), (13,14), (14,15), (15,8),
    (16,17), (17,18), (18,19), (19,20), (20,21), (21,22), (22,23), (23,16),
    (1, 9), (9,17),
    (3,11), (11,19),
    (5,13), (13,21),
    (7,15), (15,23)
]

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

# la liste des combinaisons ki font un moulin (3 pions alignes)
moulins = [
    [0, 1, 2], [2, 3, 4], [4, 5, 6], [6, 7, 0],
    [8, 9, 10], [10, 11, 12], [12, 13, 14], [14, 15, 8],
    [16, 17, 18], [18, 19, 20], [20, 21, 22], [22, 23, 16],
    [1, 9, 17], [3, 11, 19], [5, 13, 21], [7, 15, 23]
]

# fct ki donne le joueur adverse
def joueur_adverse(joueur):
    return "noir" if joueur == "blanc" else "blanc"

# on cree la fenetre du jeu
root = tk.Tk()
root.title("Twelve Men's Morris")
root.geometry("800x800")

# on cree le canvas pr dessiner (c genre une feuille blanche)
canvas = tk.Canvas(root, width=800, height=800, bg="beige")
canvas.pack()

# fonction pr dessiner le plateau (c les carre + lignes + points)
def dessiner_plateau():
    marges = [100, 200, 300]
    taille = 800
    for marge in marges:
        canvas.create_rectangle(marge, marge, taille - marge, taille - marge, width=2)
    centre = taille // 2
    canvas.create_line(centre, marges[0], centre, marges[1], width=2)
    canvas.create_line(centre, taille - marges[0], centre, taille - marges[1], width=2)
    canvas.create_line(marges[0], centre, marges[1], centre, width=2)
    canvas.create_line(taille - marges[0], centre, taille - marges[1], centre, width=2)
    for (i, j) in connexions:
        x1, y1 = points[i]
        x2, y2 = points[j]
        canvas.create_line(x1, y1, x2, y2, width=2)
    for (x, y) in points:
        r = 10
        canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightgray", outline= "black")

def pion_in_moulin(pos, joueur):
    for moulin in moulins:
        if pos in moulin:
            if all(positions_occupees.get(p) == joueur for p in moulin):
                return True
    return False

# ici c la fct ki s’active kan on clic sur un point
def clic_souris(event):
    global joueur_actuel, mode_suppresion, pion_selectionne, joueur_en_suppression, suppression_effectuee
    x, y = event.x, event.y
    rayon = 10

    if mode_suppresion:
        pion_adverse = joueur_adverse(joueur_en_suppression)
        tous_dans_moulin = all(pion_in_moulin(pos, pion_adverse) for pos in positions_occupees if positions_occupees[pos] == pion_adverse)
        for i, (px, py) in enumerate(points):
            distance = ((px - event.x) ** 2 + (py - event.y) ** 2) ** 0.5
            if distance <= 10:
                if (
                    not suppression_effectuee
                    and i in positions_occupees
                    and positions_occupees[i] == pion_adverse
                ):
                    if not pion_in_moulin(i, pion_adverse) or tous_dans_moulin:
                        canvas.create_oval(px - 10, py - 10, px + 10, py + 10, fill="lightgray", outline="black")
                        del positions_occupees[i]
                        print(f"pion adverse retiré en {i}")
                        suppression_effectuee = True
                        mode_suppresion = False
                        joueur_actuel = joueur_adverse(joueur_en_suppression)
                        joueur_en_suppression = None
                        return
                    else:
                        print("tu peux pas retirer un pion dans un moulin sauf si y'a pas d'autre dispo")
                        return
                else:
                    print("Suppression IMPOSIBLE!")
                    return

    for i, (px, py) in enumerate(points):
        distance = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
        if distance <= rayon:
            if i in positions_occupees:
                print(f"c mort frérot, position {i} déjà prise par {positions_occupees[i]}")
                return
            couleur = "black" if joueur_actuel == "noir" else "white"
            canvas.create_oval(px - rayon, py - rayon, px + rayon, py + rayon, fill=couleur)
            positions_occupees[i] = joueur_actuel
            print(f"{joueur_actuel} a mis un pion en {i}")
            print(f"Nombre total de pion actifs: {len(positions_occupees)}")
            pions_a_poser[joueur_actuel] -= 1
            if verifier_moulin(i, joueur_actuel):
                print(f" MOULIN ! {joueur_actuel} peut retirer un pion adverse")
                mode_suppresion = True
                joueur_en_suppression = joueur_actuel
                suppression_effectuee = False
                return
            if pions_a_poser["noir"] == 0 and pions_a_poser["blanc"] == 0:
                print("Phase de deplacement activee")
                # phase_mouvement = True (pas encore gere ici)
            joueur_actuel = joueur_adverse(joueur_actuel)
            print(f"c au tour de {joueur_actuel}")
            break

# fct ki check les moulins

def verifier_moulin(position, joueur):
    for moulin in moulins:
        if position in moulin:
            if all(positions_occupees.get(p) == joueur for p in moulin):
                return True
    return False

# on dessine le plateau et on lance le jeu
dessiner_plateau()
canvas.bind("<Button-1>", clic_souris)
root.mainloop()
