import numpy as np
import sys #module python pour initialiser une valeur maximale/minimal possible

EMPTY = "[ ]" 	#case vide
PLAYER1 = "[O]" #case du joueur 1
PLAYER2 = "[X]" #case du joueur 2
MAX_ROUNDS = 2


# état initial du jeu 
def etat_initial():
	etat = []
	for i in range(15):
		etat.append([EMPTY for j in range(15)]) #j'ajoute une ligne qui contient 15 éléments EMPTY
	return etat


# on verifie si la position est vide 
def si_position_disponible(etat, pos):
	return etat[pos[0]][pos[1]] == EMPTY # ici on prend pas pos[0] et pos[0] car sinon on verifie toujours la même valeur

# en fonction de l'état et de moves, la fonction retourne une liste de position possible
def get_positions_possibles(etat, moves):
	positions = []
	for move in moves:
		move_x = move[0]
		move_y = move[1]
		for i in range(5):
			for j in range(5):
				# On calcule les nouvelles coordonnées en fonction du mouvement et de l'offset i,j
				new_x = move_x + (i - 2)
				new_y = move_y + (j - 2)
				# On vérifie si la position est dans les limites du plateau
				if (new_x >= 0) and (new_y >= 0) and (new_x < 15) and (new_y < 15):
					# On vérifie si la position est vide
					if ([new_x, new_y] not in positions) and (etat[new_x][new_y] == EMPTY):
						# On ajoute la position à la liste des positions possibles
						positions.append([new_x, new_y])
	# On retourne la liste des positions possibles
	return positions


# user = PLAYER1 ou PLAYER2
def make_move(etat, pos, user):
	"""
	Fonction pour jouer un coup sur l'état actuel du plateau.

	:param etat: une liste de listes représentant le plateau de jeu.
	:param pos: une liste représentant la position du coup à jouer.
	:param user: un entier représentant le joueur qui joue le coup (PLAYER1 ou PLAYER2).
	:return: un booléen indiquant si le coup a été joué avec succès.
	"""
	# On vérifie si la position est disponible pour jouer le coup
	if si_position_disponible(etat, pos):
		# On met à jour l'état avec le coup joué par le joueur
		etat[pos[0]][pos[1]] = user
		return True
	# Si la position n'est pas disponible, le coup ne peut pas être joué
	return False

def unmake_move(etat, move):
	etat[move[0]][move[1]] = EMPTY

def get_vertical_from_position(etat, pos):
	"""
	Fonction pour récupérer la colonne verticale d'une position donnée sur le plateau.
	:param etat: une liste de listes représentant le plateau de jeu.
	:param pos: une liste représentant la position dont on veut récupérer la colonne verticale.
	:return: une liste représentant la colonne verticale de la position donnée.
	"""
	# On transforme le plateau en un tableau numpy pour pouvoir récupérer la colonne verticale plus facilement
	a = np.array(etat)
	# On retourne la colonne correspondant à la position donnée
	return a[:,pos[1]]


def get_horizontal_from_position(etat, pos):
	"""
	Fonction pour récupérer la ligne horizontale d'une position donnée sur le plateau.

	:param etat: une liste de listes représentant le plateau de jeu.
	:param pos: une liste représentant la position dont on veut récupérer la ligne horizontale.
	:return: une liste représentant la ligne horizontale de la position donnée.
	"""
	# On transforme le plateau en un tableau numpy pour pouvoir récupérer la ligne horizontale plus facilement
	a = np.array(etat)
	# On retourne la ligne correspondant à la position donnée
	return a[pos[0],:]



def get_sequences_from_positions(etat, moves):
	# Initialisation des listes pour stocker les séquences et les positions visitées
	sequences = []
	visited = []

	# Boucle pour traiter chaque position de coup récent
	for move in moves:
		# Vérification si la colonne n'a pas déjà été visitée
		if move[1] not in visited:
			# Obtention de la colonne verticale contenant la position
			vertical = get_vertical_from_position(etat,move)
			# Recherche de séquences dans la colonne verticale
			sequence = obtenir_sequences_dans_tableau(vertical)
			# Ajout de la colonne à la liste des positions visitées
			visited.append(move[1])
			# Si des séquences ont été trouvées, elles sont ajoutées à la liste des séquences
			if len(sequence) > 0:
				sequences.extend(sequence)

		# Vérification si la rangée n'a pas déjà été visitée
		if move[0]+15 not in visited:
			# Obtention de la rangée horizontale contenant la position
			horizontal = get_horizontal_from_position(etat,move)
			# Recherche de séquences dans la rangée horizontale
			sequence = obtenir_sequences_dans_tableau(horizontal)
			# Ajout de la rangée à la liste des positions visitées
			visited.append(move[0]+15)
			# Si des séquences ont été trouvées, elles sont ajoutées à la liste des séquences
			if len(sequence) > 0:
				sequences.extend(sequence)

	# Retourne la liste de toutes les séquences trouvées
	return sequences



# Retourne des séquences dans un tableau
def obtenir_sequences_dans_tableau(tableau):
	sequences = [] # Initialise la liste des séquences
	seq_temp = [] # Initialise une liste temporaire pour enregistrer chaque séquence
	ouverture_temp = 0 # Initialise une variable temporaire pour enregistrer si la séquence est une séquence d'ouverture ou de fermeture
	
	# Boucle pour parcourir chaque élément du tableau
	for i, element in enumerate(tableau):
		if i > 0:
			dernier_element = tableau[i-1]
			if element != EMPTY:
				if dernier_element != element:
					if dernier_element == EMPTY:
						ouverture_temp = 1
						seq_temp.append(element)
					else:
						if(len(seq_temp) > 1):
							sequences.append([seq_temp[0], ouverture_temp, len(seq_temp)])
						seq_temp = []
						ouverture_temp = 0
				else:
					if(len(seq_temp) < 1):
						seq_temp.append(dernier_element)
					seq_temp.append(element)
			elif dernier_element != element:
				if len(seq_temp) > 1:
					sequences.append([seq_temp[0], ouverture_temp+1, len(seq_temp)])
				seq_temp = []
				ouverture_temp = 0
	if len(seq_temp) > 1:
		sequences.append([seq_temp[0], ouverture_temp, len(seq_temp)])
	return sequences




def get_diagonal_sequences(etat):
	sequences = []
	x,y = 15,15
	a = np.array(etat)
	diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
	diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
	diagonals = [n.tolist() for n in diags]
	for diagonal in diagonals:
		sequences += obtenir_sequences_dans_tableau(diagonal)
	return sequences


# attribut des scores pour chaque longueur 
def get_sequence_score(length):
	if length == 2:
		return 1
	elif length == 3:
		return 1000
	elif length == 4:
		return 10000000
	elif length == 5:
		return 10000000000


def get_all_sequences(etat, moves):
	all_sequences = (get_sequences_from_positions(etat,moves))
	for sequence in get_diagonal_sequences(etat):
		all_sequences.append(sequence)
	return all_sequences


def exists_winner(etat, moves):
	all_sequences = get_all_sequences(etat, moves)
	for sequence in all_sequences:
		if len(sequence) > 0:
			if sequence[2] == 5:
				return sequence[0]
	return EMPTY


def get_heuristique(etat, round_number, moves):
	all_sequences = get_all_sequences(etat, moves)
	score = 0
	for sequence in all_sequences:
		if len(sequence) > 0:
			for i in range(2, 5):
				if sequence[2] == i:
					score = score + get_sequence_score(i)*sequence[1] if sequence[0] == PLAYER2 else score - get_sequence_score(i)*sequence[1]
					break;
			if sequence[2] >= 5:
				score = score + get_sequence_score(5) if sequence[0] == PLAYER2 else score - get_sequence_score(5)
	return (score*225)/round_number


def get_heuristique_for_game_IA(etat,round_number, moves):
	all_sequences = get_all_sequences(etat, moves)
	score = 0
	for sequence in all_sequences:
		if len(sequence) > 0:
			for i in range(2, 5):
				if sequence[2] == i:
					score = score + get_sequence_score(i)*sequence[1] if sequence[0] == PLAYER1 else score - get_sequence_score(i)*sequence[1]
					break;
			if sequence[2] >= 5:
				score = score + get_sequence_score(5) if sequence[0] == PLAYER1 else score - get_sequence_score(5)
	return (score*225)/round_number


def alpha_beta(player, etat, alpha, beta, rounds, round_number, moves, depth):
    possible_moves = get_positions_possibles(etat, moves)
    bestMove = [-1,-1]
    maximum = MAX_ROUNDS
    
    if (player == PLAYER2 and (len(possible_moves) == 0) or (rounds >= maximum) or (depth == 0)):
        score = get_heuristique(etat, round_number+rounds, moves)
        return [score, bestMove]
    elif (player == PLAYER1 and (len(possible_moves) == 0) or (rounds >= maximum) or (depth == 0)):
        score = get_heuristique_for_game_IA(etat, round_number+rounds, moves)
        return [score, bestMove]
    else:
        for move in possible_moves:
            make_move(etat, move, player)
            moves.append(move)
            score = alpha_beta(PLAYER2 if player==PLAYER1 else PLAYER1, etat, alpha,beta, rounds + 1, round_number, moves, depth-1)[0]
            unmake_move(etat, move)
            moves.remove(move)
            if(player == PLAYER2):
                if score > alpha:
                    alpha = score
                    bestMove = move
            else:
                if score < beta:
                    beta = score
                    bestMove = move
            if alpha >= beta:
                return [alpha if player==PLAYER2 else beta, bestMove]
        return [alpha if player==PLAYER2 else beta, bestMove]




# retourne le meilleur move pour l'IA
def get_IA_move_for_game_IA(etat, round_number, moves, depth):
    return alpha_beta(PLAYER1, etat, -sys.maxsize-1, sys.maxsize, 0, round_number, moves, depth)[1]

def get_IA_move(etat, round_number, moves, depth):
    return alpha_beta(PLAYER2, etat, -sys.maxsize-1, sys.maxsize, 0, round_number, moves, depth)[1]


def start_game_IA(depth1, depth2):
    round_number = 1
    moves = []
    etat = etat_initial()
    turn = get_initial_player_for_game_IA()
    winner = EMPTY
    affiche_etat(etat)
    
    while winner == EMPTY:
        print("====================== Tour numéro : "+ str(round_number) + " ======================")
        print("\n")
        if len(moves) == 225:
            break
        if (turn == PLAYER1):
            move = get_IA_move_for_game_IA(etat, round_number, moves, depth1)
        else:
            move = get_IA_move(etat, round_number, moves, depth2)
        make_move(etat, move, turn)
        moves.append(move)
        round_number += 1
        winner = exists_winner(etat, moves)
        turn = PLAYER2 if turn==PLAYER1 else PLAYER1
        affiche_etat(etat)
    game_over(winner)

def start_game_Humain(depth):
	round_number = 1
	moves = []
	etat = etat_initial()
	turn = get_initial_player()
	winner = EMPTY
	affiche_etat(etat)
	while winner == EMPTY:
		print("====================== Tour numéro : "+ str(round_number) + " ======================")
		print("\n")
		if len(moves) == 225:
			break
		if (turn == PLAYER2) and (len(moves) == 0):
			make_move(etat, [7,7], turn)
		else:
			move = input_position(turn, etat) if turn==PLAYER1 else get_IA_move(etat, round_number, moves,depth)
			make_move(etat, move, turn)
			moves.append(move)
		round_number += 1
		winner = exists_winner(etat, moves)
		turn = PLAYER2 if turn==PLAYER1 else PLAYER1
		affiche_etat(etat)
	game_over(winner)


def affiche_menu():
    print("===========================  ")
    print("          MENU               ")
    print("    1. Regarder IA contre IA ")
    print("    2. Joueur contre IA      ")
    print("    3. Quitter le jeu        ")
    print("===========================  ")
    exit = False
    while not exit:
        user_input = input("Sélectionnez une option : ")
        if user_input == "1":
            level_IA1 = input("Insérer le niveau du premier IA (1, 2 ou 3) : ")
            level_IA2 = input("Insérer le niveau du deuxième IA (1, 2 ou 3) : ")
            if level_IA1 not in ["1", "2", "3"] or level_IA2 not in ["1", "2", "3"]:
                print("Niveau invalide. Veuillez choisir un nombre entre 1 et 3.")
            start_game_IA(int(level_IA1), int(level_IA2))
        elif user_input == "2":
            level = input("Insérer le niveau de l'IA (1, 2 ou 3) : ")
            if level not in ["1", "2", "3"]:
                print("Niveau invalide. Veuillez choisir un nombre entre 1 et 3.")
            else:
                start_game_Humain(int(level)+1)
        elif user_input == "3":
            exit = True
            print("À bientôt !")
            sys.exit(0)
        else:
            print("Option invalide.")


def get_initial_player():
	while(True):
		user_input = input("Entrez 1 pour HUMAIN [O] joue en premier, ou 2 pour l'IA [X] joue en premier : ")
		if user_input == "1":
			return PLAYER1
		elif user_input == "2":
			return PLAYER2
		print("Entrée invalide")


def get_initial_player_for_game_IA():
	while(True):
		user_input = input("Entrez 1 pour l'IA [O] joue en premier, ou 2 pour l'IA [X] joue en premier : ")
		if user_input == "1":
			return PLAYER1
		elif user_input == "2":
			return PLAYER2
		print("Entrée invalide")



def game_over(winner):
    print("FIN DU JEU")
    print("\nLE JOUEUR " + str(winner) + " GAGNE" if winner != EMPTY else "Plus de positions disponibles. C'est une égalité!")
    print("Jouer à nouveau ? [y/n]")
    exit = False
    while not exit:
        user_input = input("")
        if user_input == "y":
            affiche_menu()
        elif user_input == "n":
            exit = True
            print("À bientôt !")
            sys.exit(0)
        else:
            print("Option invalide")

# recupere les inputs du joueur
def input_position(turn, etat):
	while True:
		try:
			print("C'est au tour du joueur " + turn + " :")
			row = int(input("ligne : "))
			col = int(input("colonne : "))
			if (row > 14 or col > 14):
				print("Veuillez saisir des valeurs entre 0 et 14.")
			elif not si_position_disponible(etat, [row, col]):
				print("La position est occupée.")
			else:
				return [row, col]
		except IndexError:
			print("Veuillez saisir des valeurs entre 0 et 14.")
		except ValueError:
			print("Veuillez saisir des valeurs entre 0 et 14.")
	return []


# affiche l'etat du jeu
def affiche_etat(etat):
	s = " "
	for j in range(15):
		s += "  " + str(j).zfill(2) #remplir des 0 à gauche
	print(s)
	i=0;
	for row in etat:
		string = ""
		for column in row:
			string += column + " "
		print(str(i).zfill(2) + " " + string)
		i+=1

def main():
	affiche_menu()

if __name__ == "__main__":
	main()