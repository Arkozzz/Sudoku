# Partie algébrique du résolveur du sudoku principe de Back-Tracking : Il consiste à faire des retours en arrière afin de tester toutes les possibilités et de 
# trouver la solution qui permet de remplir la grille sans erreur. Cette technique permet donc de ne pas s’arrêter à la première erreur, 
# et donc de repartir un peu en arrière pour tester d’autres possibilités

import numpy as np
from random import randrange, random

def affichage(grille):   # Fonction qui affiche la grille comme un sudoku réel dans la console
    print(grille)
nm=0
#k=chiffre a placer , grille=grille qu'on va changer, l= ligne concernée, c= colonne concernée
def absentsurligne(k, grille, l):   # Fonction qui vérifie si le chiffre 'k' est deja présent sur la ligne
    for c in range(9):
        if grille[l][c] == k:
            return False
    return True

def absentsurcolonne(k, grille, c):   # Fonction qui vérifie si le chiffre 'k' est deja présent sur la colonne
    for l in range(9):
        if grille[l][c] == k:
            return False
    return True

def absentsurbloc(k , grille , l , c):  # Fonction qui vérifie si le chiffre 'k' est deja présent sur le bloc
    _l = l-(l%3)
    _c = c-(c%3)
    for c in range(_c,_c+3):
        for l in range(_l,_l+3):
            if grille[l][c] == k:
                return False
    return True

def solve(grille , position):  # Fonction qui vérifie si on doit modifier la case, la case est défini avec le paramètre position qui s'agrémente de 1 à chaque fois
    global nm
    if position == 9*9:
        nm+=1
        return True

    l = position//9
    c = position%9

    if grille[l][c] != 0:
        nm+=1
        return solve(grille , position+1)
    else:
        nm+=1
        for k in range(1,10):
            nm+=1
            if absentsurligne(k,grille,l) and absentsurcolonne(k,grille,c) and absentsurbloc(k,grille,l,c):
                grille[l][c] = k
                if solve(grille,position+1):
                    return True
                

    grille[l][c] = 0 #Si l ou c invalide on recommence (en mettant 0)
    return False

def check_cells(cells):
    #cells.sort(key=lambda v: v[10])
    maxval = len_of_cells = len(cells)
    changeds = [False] * len_of_cells
    modified = False

    while True:
        changed = False

        # Check for no possibility on cell
        for cell in cells:
            if len(cell) == 0:
                return False, modified, changeds

        # Check for one possibility on cell
        for cell in cells:
            if len(cell) == 1:
                val = cell[0]
                # Remove the possibility to have v on other cell
                for i in range(len_of_cells):
                    if cells[i] is not cell and val in cells[i]:
                        cells[i].remove(val)
                        changed = True
                        changeds[i] = True

        if changed:
            modified = True
            continue

        # Check if all number are available
        occs = [ 0] * (maxval + 1) # Occurence of values (histograme)
        poss = [-1] * (maxval + 1) # Last know position of a value

        for i in range(len_of_cells):
            for val in cells[i]:
                occs[val] += 1
                poss[val] = i

        for val in range(1, maxval + 1):
            if occs[val] == 0:
                return False, modified, changeds
            elif occs[val] == 1:
                cell = cells[poss[val]]
                if len(cell) > 1:
                    cell.clear()
                    cell.append(val)
                    changed = True
                    changeds[poss[val]] = True
                    break

        if changed:
            modified = True
            continue

        return True, modified, changeds


def is_valid(grid):
    cols_to_check    = [False] * 9 
    lines_to_check   = [False] * 9
    squares_to_check = [False] * 9
    need_to_check = False

    working_table = [[val for val in range(1, 10)] for _ in range(9 * 9)]   #toute cette partie check pour crée un tableau qui représente les valeurs possible pr le sudoku
    cols    = [[working_table[c + 9 * l] for l in range(9)] for c in range(9)] #compliqué à expliquer : tableau de tableau de tableau (tableau de colonnes...)
    lines   = [[working_table[c + 9 * l] for c in range(9)] for l in range(9)] 
    squares = []

    for l1 in range(0, 9, 3):
        for c1 in range(0, 9, 3):
            square = []
            for l2 in range(l1, l1 + 3, 1):
                for c2 in range(c1, c1 + 3, 1):
                    square.append(working_table[l2 * 9 + c2])
            squares.append(square) #fin de création de l'espace de travail

    for l in range(9): #remplit avec les valeurs de grilles émises
        for c in range(9):
            val = grid[l][c]
            if val != 0:
                cell = working_table[l * 9 + c]
                cell.clear()
                cell.append(val)
                cols_to_check[c] = True
                lines_to_check[l] = True
                squares_to_check[(c // 3) + (l // 3) * 3] = True
                need_to_check = True 

    while need_to_check: #on résout (check de validité)
        need_to_check = False

        next_lines_to_check   = [False] * 9
        next_cols_to_check    = [False] * 9
        next_squares_to_check = [False] * 9

        for i in range(9):
            if cols_to_check[i]:
                valid, changed, changeds = check_cells(cols[i])

                if not valid:
                    return False

                if changed:
                    need_to_check = True
                    for j in range(9):
                        next_lines_to_check[j] |= changeds[j]
                        next_squares_to_check[(i // 3) + (j // 3) * 3] |= changeds[j]

            if lines_to_check[i]:
                valid, changed, changeds = check_cells(lines[i])

                if not valid:
                    return False

                if changed:
                    need_to_check = True
                    for j in range(9):
                        next_cols_to_check[j] |= changeds[j]
                        next_squares_to_check[(i // 3) * 3 + (j // 3)] |= changeds[j]

            if squares_to_check[i]:
                valid, changed, changeds = check_cells(squares[i])

                if not valid:
                    return False

                if changed:
                    need_to_check = True
                    offset_c = (i % 3) * 3
                    offset_l = (i // 3) * 3
                    for l in range(3):
                        for c in range(3):
                            next_cols_to_check[offset_c + c] |= changeds[l * 3 + c]
                            next_lines_to_check[offset_l + l] |= changeds[l * 3 + c]

        lines_to_check   = next_lines_to_check
        cols_to_check    = next_cols_to_check
        squares_to_check = next_squares_to_check

    return True

#Programme permettant de crée une grille à résoudre

def randomgrid(filling_rate):
    grille2=np.zeros((9,9), dtype=int)
    for l in range(0,9):
        for c in range(0,9):
            if random()<filling_rate: #on remplit un certain pourcentage de la grille (plus c'est haut plus le remplissage de la grille est élévé)
                AvailableNumber=[] #liste qui prends les valeurs possible pour un élément de la grille
                for k in range(1,10):
                    grille2[l][c]=k #on modifie la case spécifique puis on continue
                    if is_valid(grille2): #on vérifie la validité de cette grille
                        AvailableNumber.append(k) #on ajoute la valeur possible à la liste définie précédemment
                if len(AvailableNumber) == 0:
                    #print("Error len(AvailableNumber) = 0")
                    return randomgrid(filling_rate)
                else:
                    grille2[l][c]=AvailableNumber[randrange(len(AvailableNumber))] #on ajoute a la grille une des valeurs possible
            else:
                grille2[l][c]=0 #on met 0 a l'élément de la grille

    return grille2
