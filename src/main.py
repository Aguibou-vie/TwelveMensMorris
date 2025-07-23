# on importe tkinter (c la bibli pr dessiner le jeu)
import tkinter as tk

# les 24 ptites positions du plateau (c les ronds ou on clic)
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

# le joueur ki commence (on met noir d’abord) et les cases dja joues
joueur_actuel = "noir"
positions_occupees = {}
mode_suppresion = False # si c True , on supprime le pion
phase_mouvement = False # si true pasons a la phase deplacement

# la liste des combinaisons ki font un moulin (3 pions alignés)
moulins = [
    [0, 1, 2], [2, 3, 4], [4, 5, 6], [6, 7, 0],
    [8, 9, 10], [10, 11, 12], [12, 13, 14], [14, 15, 8],
    [16, 17, 18], [18, 19, 20], [20, 21, 22], [22, 23, 16],
    [1, 9, 17], [3, 11, 19], [5, 13, 21], [7, 15, 23]
]

# on crée la fenetre du jeu
root = tk.Tk()
root.title("Twelve Men's Morris")
root.geometry("800x800")

# on crée le canvas pr dessiner (c genre une feuille blanche)
canvas = tk.Canvas(root, width=800, height=800, bg="beige")
canvas.pack()

# fonction pr dessiner le plateau (c les carré + lignes + points)
def dessiner_plateau():
    marges = [100, 200, 300]
    taille = 800

    # les 3 carré imbriqu
    for marge in marges:
        canvas.create_rectangle(marge, marge, taille - marge, taille - marge, width=2)

    # lignes qui relie les carree au centre
    centre = taille // 2
    canvas.create_line(centre, marges[0], centre, marges[1], width=2)
    canvas.create_line(centre, taille - marges[0], centre, taille - marges[1], width=2)
    canvas.create_line(marges[0], centre, marges[1], centre, width=2)
    canvas.create_line(taille - marges[0], centre, taille - marges[1], centre, width=2)

    # on dessine les lignes entre les points
    lignes = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
        (6, 7), (7, 0),
        (8, 9), (9, 10), (10, 11), (11, 12), (12, 13),
        (13, 14), (14, 15), (15, 8),
        (16, 17), (17, 18), (18, 19), (19, 20), (20, 21),
        (21, 22), (22, 23), (23, 16),
        (1, 9), (9, 17), (3, 11), (11, 19),
        (5, 13), (13, 21), (7, 15), (15, 23)
    ]
    for (i, j) in lignes:
        x1, y1 = points[i]
        x2, y2 = points[j]
        canvas.create_line(x1, y1, x2, y2, width=2)

    # on met les 24 pts du plateau (petit cercle noir)
    for (x, y) in points:
        r = 10
        canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightgray", outline= "black")

# fct ki vérifie si le joueur a fait un moulin ou pas
def verifier_moulin(position, joueur):
    for moulin in moulins:
        if position in moulin:
            if all(positions_occupees.get(p) == joueur for p in moulin):
                return True
    return False

# ici c la fct ki s’active kan on clic sur un point
def clic_souris(event):
    global joueur_actuel, mode_suppresion, phase_mouvement
    x, y = event.x, event.y
    rayon = 10
    
    if mode_suppresion :
        for i, (px,py) in enumerate(points):
            distance= ((px - event.x) ** 2 + (py - event.y) ** 2) ** 0.5
            if distance <= 10:
                #verifie si ya un pion 
                if i in positions_occupees and positions_occupees[i] != joueur_actuel:
                    #on elimine un. pion adverse 
                    canvas.create_oval(px-10 , py-10 , px + 10 , py +10, fill="beige")
                    # on l'elimine du dictionnaire 
                    del positions_occupees[i]
                    print(f"pion adverse retirer en {i}")
                    mode_suppresion = False #on retourne en mode normal
                    return
                else:
                    print("Suppression IMPOSIBLE!")           
        return     
    # on vérifie si le clic est sur un des 24 pts
    for i, (px, py) in enumerate(points):
        distance = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
        if distance <= rayon:
            if i in positions_occupees:
                print(f"c mort frérot, position {i} déjà prise par {positions_occupees[i]}")
                return

            # on dessine le pion du joueur actuel
            couleur = "black" if joueur_actuel == "noir" else "white"
            canvas.create_oval(px - rayon, py - rayon, px + rayon, py + rayon, fill=couleur)

            # on marque la position comme joue
            positions_occupees[i] = joueur_actuel
            print(f"{joueur_actuel} a mis un pion en {i}")

            # on check si le joueur a fait un moulin 
            if verifier_moulin(i, joueur_actuel):
                print(f" MOULIN ! {joueur_actuel} peut retirer un pion adverse")
                mode_suppresion = True # active mode suppresion
                
            #passer au deplacement if 24pions
            if len(positions_occupees) == 24:
                print("Phase deplacement active")
                phase_mouvement = True

            # on change de joueur (genre c au tour de l'autre)
            joueur_actuel = "blanc" if joueur_actuel == "noir" else "noir"
            print(f"c au tour de {joueur_actuel}")
            break

def pion_in_moulin(pos, joueur):
    for moulin in moulins:
        if pos in moulin:
            if all(positions_occupees.get(p) == joueur for p in moulin):
                return True
    return False
# on dessine le plateau et on lance le jeu
dessiner_plateau()
canvas.bind("<Button-1>", clic_souris)
root.mainloop()
