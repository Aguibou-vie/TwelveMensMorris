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


pions_a_poser = {
    "noir": 12,
    "blanc": 12
}

# les 24 ptites positions du plateau (c les ronds ou on clic)

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

def verifier_victoire():
    joueurs= ["noir" , "blanc"]
    for joueur in joueurs:
        nb_pions = sum(1 for pos in positions_occupees if positions_occupees[pos]== joueur)
        if nb_pions < 3:
            print(f"{joueur} n'a plus que {nb_pions}pions....Il perd la partie")
            gagnant=" blanc " if joueur == "noir " else " noir"
            print(f"{gagnant.upper()} a gagné la partie !")
            canvas.unbind("<Button-1>") #desactive les clics
            return True
    return False

def joueur_peut_sauter(joueur):
    nb_pions = sum(1 for p in positions_occupees if positions_occupees[p]==joueur)
    return nb_pions == 3

#fonction qui verifie si un joueur peu bouger
def joueur_peut_bouger(joueur):
    #on parcour toute les list du pleateau
    for pos in positions_occupees:
        #si le pion de cette possition appatien au joueur 
        if positions_occupees== joueur:
            #on regarde toute les position posible
            for a, b in connexions:
                if a == pos and b not in positions_occupees:
                    return True
                if b == pos and a not in positions_occupees:
                    return True
    return False

def pion_in_moulin(pos, joueur):
    for moulin in moulins:
        if pos in moulin:
            if all(positions_occupees.get(p) == joueur for p in moulin):
                return True
    return False

# ici c la fct ki s’active kan on clic sur un point
def clic_souris(event):
    global joueur_actuel, mode_suppresion, phase_mouvement , pion_selectionne, joueur_en_suppression , suppression_effectuee
    x, y = event.x, event.y
    rayon = 10
    
    if mode_suppresion :
        #verifie si un joueur peu suppr un pion 
        pion_adverse = "noir" if joueur_en_suppression== "blanc" else "blanc"
        #si tous les pions adverse sont dans un moulin
        tous_dans_moulin= all (pion_in_moulin(pos, pion_adverse) for pos in positions_occupees if positions_occupees[pos]== pion_adverse)
        for i, (px,py) in enumerate(points):
            distance= ((px - event.x) ** 2 + (py - event.y) ** 2) ** 0.5
            if distance <= 10:
                #verifie si ya un pion 
                adversaire= "noir" if joueur_en_suppression =="blanc" else "blanc"
                if not suppression_effectuee and i in positions_occupees and positions_occupees[i] == pion_adverse:
                    if not pion_in_moulin(i, pion_adverse) or tous_dans_moulin:

                        #on elimine un. pion adverse 
                        canvas.create_oval(px-10 , py-10 , px + 10 , py +10, fill="beige")
                        # on l'elimine du dictionnaire 
                        del positions_occupees[i]
                        print(f"pion adverse retirer en {i}")
                        
                        if verifier_victoire():
                            return
                        suppression_effectuee = True
                        mode_suppresion = False
                        joueur_actuel = "blanc" if joueur_en_suppression == "noir" else "noir"
                        joueur_en_suppression = None
                        return 
                    else:
                        print("tu peux pas retirer un pion dans un moulin sauf si y'a pas d'autre dispo")

                else:
                    print("Suppression IMPOSIBLE!")           
                    return    
    if phase_mouvement:
        if not joueur_peut_bouger(joueur_actuel):
            print(f"{joueur_actuel} ne peut plus bouger ...Il perd la partie")
            gagnant = "blanc" if joueur_actuel== "noir" else "noir"
            print(f"{gagnant.upper()} A GAGNÈ !")
            canvas.unbind("<button-1>")
            return
        for i, (px,py) in enumerate(points):
            distance= ((px - x) ** 2 ) ** 0.5
            if distance <= rayon:
                #si pas de pion selectionner , on selectionne un
                if pion_selectionne is None:
                    if i in positions_occupees and positions_occupees[i] == joueur_actuel:
                        pion_selectionne = i
                        print(f"pion du {joueur_actuel} selectioner en posstion {i}")
                    else:
                        print("tu peux selectionner que tes propre pion")
                else:
                    #verifie que la case est vide
                    if i not in positions_occupees:
                        #verifie sa voisinage du pion selectionner
                        if joueur_peut_sauter(joueur_actuel) or (pion_selectionne, i) in connexions or (i, pion_selectionne) in connexions:
                            print("{joueur_actuel} en Phase de SAUT!")
                            #effancer ancien pions
                            x1, y1 = points[pion_selectionne]
                            canvas.create_oval(x1 - rayon, y1 - rayon, x1 + rayon, y1 + rayon, fill="lightgray")
                            
                            #designer nouveau pion
                            x2, y2 = points[i]
                            couleur= "black" if joueur_actuel== "noir" else "white" 
                            canvas.create_oval(x2 - rayon , y2 - rayon , x2 + rayon , y2 + rayon , fill = couleur)
                            #mettre a jour le dictionnaire 
                            del positions_occupees[pion_selectionne]
                            positions_occupees[i]= joueur_actuel
                            print(f"pion deplace de {pion_selectionne}")
                            
                            if verifier_victoire():
                                return
                            
                            pion_selectionne= None
                            
                            #verifie moulin
                            if verifier_moulin(i, joueur_actuel):
                                print(f"MOULIN ! {joueur_actuel} peut retirer un pion Adverse")
                                mode_suppresion = True
                                joueur_en_suppression = joueur_actuel
                                return
                            #changement de joueur 
                            joueur_actuel= "blanc" if joueur_actuel == "noir" else "noir"
                            print(f"c'est au tour du {joueur_actuel}")
                        else:
                            print("Cette case n'est pas voisin")
                    else:
                        print("Cette case est deja prise")
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
            # on retire un pion dispo a ce joueur
            pions_a_poser[joueur_actuel] -= 1 

            # on check si le joueur a fait un moulin 
            if verifier_moulin(i, joueur_actuel):
                print(f" MOULIN ! {joueur_actuel} peut retirer un pion adverse")
                mode_suppresion = True # active mode suppresion
                return
                
            #passer au deplacement if 24pions
            if pions_a_poser["noir"] == 0 and pions_a_poser["blanc"] == 0:
                """if not joueur_peut_bouger("noir") and not joueur_peut_bouger("blanc"):
                    print("Plus aucun mouvement possible... MATCH NUL !")
                    canvas.unbind("<Button-1>")
                else:"""
                print("Phase deplacement active")
                phase_mouvement = True


            # on change de joueur (genre c au tour de l'autre)
            joueur_actuel = "blanc" if joueur_actuel == "noir" else "noir"
            print(f"c au tour de {joueur_actuel}")
            break
        
    suppression_effectuee = False


# on dessine le plateau et on lance le jeu
dessiner_plateau()
canvas.bind("<Button-1>", clic_souris)
root.mainloop()
