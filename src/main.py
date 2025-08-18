# on importe tkinter (c la bibli pr dessiner le jeu)
import tkinter as tk
import pygame # pour l'ajout de la musiqu

# le joueur ki commence (on met noir d’abord) et les cases dja joues
joueur_actuel = "noir"
positions_occupees = {}
mode_suppresion = False                      # si c True , on supprime le pion
phase_mouvement = False                       # si true pasons a la phase deplacement
pion_selectionne= None                         #pas de pion selectionner au debutç
joueur_en_suppression = None                            # le joueur ki a fait le moulin
suppression_effectuee = False
phase_pose = True                                       #on active la phase de pose

pygame.mixer.init()                                               #init pygame mixer
pygame.mixer.music.load("assets/music/background-music.mp3")   #charger une musique
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)    #jouer en boucl
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


voisins = {
    0: [1, 7],
    1: [0, 2, 9],
    2: [1, 3],
    3: [2, 4, 11],
    4: [3, 5],
    5: [4, 6, 13],
    6: [5, 7],
    7: [0, 6, 15],
    8: [9, 15],
    9: [1, 8, 10, 17],
    10: [9, 11],
    11: [3, 10, 12, 19],
    12: [11, 13],
    13: [5, 12, 14, 21],
    14: [13, 15],
    15: [7, 8, 14, 23],
    16: [17, 23],
    17: [9, 16, 18],
    18: [17, 19],
    19: [11, 18, 20],
    20: [19, 21],
    21: [13, 20, 22],
    22: [21, 23],
    23: [15, 16, 22]
}

def cases_voisines(pos1, pos2):
    return pos2 in voisins.get(pos1, [])


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

# la liste des combinaisons ki font un moulin (3 pions alignés)
moulins = [
    [0, 1, 2], [2, 3, 4], [4, 5, 6], [6, 7, 0],
    [8, 9, 10], [10, 11, 12], [12, 13, 14], [14, 15, 8],
    [16, 17, 18], [18, 19, 20], [20, 21, 22], [22, 23, 16],
    [1, 9, 17], [3, 11, 19], [5, 13, 21], [7, 15, 23]
]

# fct ki donne le joueur adverse
def joueur_adverse(joueur):
    return "noir" if joueur == "blanc" else "blanc"



def reset_game():
    # remet tout a zero pr une nouvelle parti
    global joueur_actuel, positions_occupees, mode_suppresion
    global phase_mouvement, pion_selectionne, joueur_en_suppression
    global suppression_effectuee, phase_pose, pions_a_poser

    joueur_actuel = "noir"  # on recommence tjr par noir (comm avant)
    positions_occupees = {}  # plateau vide
    mode_suppresion = False
    phase_mouvement = False
    pion_selectionne = None
    joueur_en_suppression = None
    suppression_effectuee = False
    phase_pose = True
    pions_a_poser = {"noir": 12, "blanc": 12}

    # on nettoie et on redessine
    canvas.delete("all")
    dessiner_plateau()

    # on reactive le clic
    canvas.bind("<Button-1>", clic_souris)
    label_tour.config(text="Tour : noir (Phase: Pose)")


    # on reactive le bouton rejouer (il reste dispo) et on log
    print("nouvelle partie demarree")



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



def nb_pions(joueur):
    return sum(1 for _, j in positions_occupees.items() if j == joueur)

def mettre_a_jour_phase():
    global phase_pose, phase_mouvement
    if pions_a_poser["noir"] == 0 and pions_a_poser["blanc"] == 0:
        phase_pose = False
        phase_mouvement = True
        print("Phase de déplacement activée")
        label_tour.config(
            text=f"Tour : {joueur_actuel} (Phase: Mouvement) | Restants N/B : {pions_a_poser['noir']} / {pions_a_poser['blanc']}"
        )


def verifier_victoire():
    # 1) Victoire "moins de 3 pions
    for joueur in ["noir", "blanc"]:
        pions_joueur = [pos for pos, j in positions_occupees.items() if j == joueur]
        if len(pions_joueur) < 3:
            gagnant = joueur_adverse(joueur)
            print(f"Victoire de {gagnant} ! (l'adversaire n'a plus que {len(pions_joueur)} pions)")
            label_tour.config(text=f"Gagnant : {gagnant}")
            canvas.unbind("<Button-1>")
            return True

    # 2) Victoire par "blocage" 
    if not phase_pose:
        # On test le blocage uniquement pour le joueur qui va jouer (joueur_actuel)
        joueur = joueur_actuel
        pions_joueur = [pos for pos, j in positions_occupees.items() if j == joueur]

        # avec 3 pions, il peut sauter => pas de blocage possible
        if len(pions_joueur) >= 4:
            a_un_coup = any(
                any((v not in positions_occupees) and cases_voisines(pos, v) for v in range(24))
                for pos in pions_joueur
            )
            if not a_un_coup:
                gagnant = joueur_adverse(joueur)
                print(f"Victoire de {gagnant} ! (joueur {joueur} bloqué)")
                label_tour.config(text=f"Gagnant : {gagnant}")
                canvas.unbind("<Button-1>")
                return True

    return False


# ici c la fonction ki s’active quan on clic sur un point
def clic_souris(event):
    global joueur_actuel, mode_suppresion, pion_selectionne, joueur_en_suppression, suppression_effectuee, phase_mouvement, phase_pose
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
                        if verifier_victoire():
                            return
                        
                        joueur_actuel = joueur_adverse(joueur_en_suppression)
                        joueur_en_suppression = None
                        label_tour.config(
                            text=f"Tour : {joueur_actuel} "
                                 f"{'(Phase: Mouvement)' if not phase_pose else '(Phase: Pose)'} | "
                                 f"Restants N/B : {pions_a_poser['noir']} / {pions_a_poser['blanc']}"
                        )
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
            if not phase_pose :
                if pion_selectionne is None:
                    #choisit un pion a bouger
                    if i in positions_occupees and positions_occupees[i] == joueur_actuel:
                        pion_selectionne= i
                        print(f"{joueur_actuel} a selectionne le pion en {i}")
                    else:
                        print("selection invalide, faut choisir un de tes pion")
                else:
                    #on a deja choisi donc on bouge
                    if i not in positions_occupees:
                        if len([p for p, j in positions_occupees.items() if j == joueur_actuel]) == 3 or cases_voisines(pion_selectionne, i):
                        #on deplace le pion
                            positions_occupees[i]= joueur_actuel
                            del positions_occupees[pion_selectionne]
                            
                            #on efface l'ancien case
                            old_x, old_y = points[pion_selectionne]
                            canvas.create_oval(old_x - rayon, old_y - rayon, old_x + rayon, old_y + rayon, fill="lightgray", outline="black")
                            #on designe le nouveau pion
                            new_couleur = "black" if joueur_actuel == "noir" else "white"
                            new_x, new_y =points[i]
                            canvas.create_oval(new_x -rayon, new_y - rayon, new_x + rayon,new_y + rayon, fill=new_couleur )
                            print(f"{joueur_actuel} a bouger son pion de {pion_selectionne} vers {i}")
                            pion_selectionne = None
                            
                            #check moulin
                            if pion_in_moulin(i, joueur_actuel):
                                print(f"MOULIN {joueur_actuel} PEUT RETIRER UN PION ADVERSE")
                                mode_suppresion= True
                                joueur_en_suppression = joueur_actuel
                                suppression_effectuee = False
                                label_tour.config(text=f"{joueur_actuel} : retire un pion adverse")
                            if verifier_victoire():
                                return
                            else:
                                joueur_actuel = joueur_adverse(joueur_actuel)
                                label_tour.config(text=f"Tour : {joueur_actuel} (Phase: Mouvement)")
                                verifier_victoire()
                        else:
                            print("deplacement invalide, tu dois choisir un case voisin")
                            pion_selectionne = None
                    else:
                        print("case deja occupee!")
                        pion_selectionne = None
                return
            #si le joueur n'a plus de pions
            if phase_pose and pions_a_poser[joueur_actuel] == 0:
                autre = joueur_adverse(joueur_actuel)
                if pions_a_poser[autre] > 0 :
                    print(f"{joueur_actuel} a fini de poser. tour auto passe a {autre}.")
                    joueur_actuel = autre
                    label_tour.config(text=f"Tour : {joueur_actuel} (Phase: Pose)")
                    return
                else:
                    mettre_a_jour_phase() # les 2 ont fini de poser
            if i in positions_occupees:
                print(f"c mort frérot, position {i} déjà prise par {positions_occupees[i]}")
                return
            if pions_a_poser[joueur_actuel] <= 0 :
                print(f"{joueur_actuel} n'a plus de pions a poser")
                return
            couleur = "black" if joueur_actuel == "noir" else "white"
            canvas.create_oval(px - rayon, py - rayon, px + rayon, py + rayon, fill=couleur)
            positions_occupees[i] = joueur_actuel
            print(f"{joueur_actuel} a mis un pion en {i}")
            print(f"Nombre total de pion actifs: {len(positions_occupees)}")
            pions_a_poser[joueur_actuel] -= 1
            if pion_in_moulin(i, joueur_actuel):
                print(f" MOULIN ! {joueur_actuel} peut retirer un pion adverse")
                mode_suppresion = True
                joueur_en_suppression = joueur_actuel
                suppression_effectuee = False
                label_tour.config(text=f"{joueur_actuel} : retire un pion adverse")
                return
            mettre_a_jour_phase()
            joueur_actuel = joueur_adverse(joueur_actuel) #changement de joueur
            label_tour.config(
                text=f"Tour : {joueur_actuel} "
                    f"{'(Phase: Mouvement)' if not phase_pose else '(Phase: Pose)'} | "
                    f"Restants N/B : {pions_a_poser['noir']} / {pions_a_poser['blanc']}"
            )
            if not phase_pose:
                verifier_victoire()
            break
        
# on cree la fenetre du jeu
root = tk.Tk()
root.title("Twelve Men's Morris")

# taille de la fenetre
root.geometry("800x860")
canvas = tk.Canvas(root, width=800, height=760, bg="beige")
canvas.pack(side="top")

control_frame = tk.Frame(root, bg="#e6e6e6")
control_frame.pack(side="bottom", fill="x", pady=8)
#rejouer
btn_rejouer = tk.Button(control_frame, text="Rejouer", command=reset_game)
btn_rejouer.pack(side="left", padx=6)


# bouton quitter pour fermer le jeu
btn_quitter = tk.Button(control_frame, text="Quitter", command=root.destroy)
btn_quitter.pack(side="left", padx=6)

label_tour = tk.Label(control_frame, text="Tour : noir")
label_tour.pack(side="left", padx=12)

# on dessine le plateau et on lance le jeu
dessiner_plateau()
canvas.bind("<Button-1>", clic_souris)
root.mainloop()
