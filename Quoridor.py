import random


class SaveGame:

    def __init__(self, joueur1=None, joueur2=None, partie=None, filename="SauvePartie.txt"):
        self.p1 = joueur1
        self.p2 = joueur2
        self.game = partie
        self.filename = filename

    def sauvegarde(self, joueur1, game, joueur2):

        txtWalls = ""
        for i in game.wall:
            for j in i:
                txtWalls += str(j)
            txtWalls += " "

        posJ1 = str(joueur1.position[0]) + str(joueur1.position[1])
        posJ2 = str(joueur2.position[0]) + str(joueur2.position[1])

        couleurJ1 = ""
        if "\u001b[31m" == joueur1.couleur:
            couleurJ1 = "red"
        elif "\u001b[32m" == joueur1.couleur:
            couleurJ1 = "green"
        elif "\u001b[34;1m" == joueur1.couleur:
            couleurJ1 = "blue"
        elif "\u001b[35m" == joueur1.couleur:
            couleurJ1 = "magenta"

        couleurJ2 = ""

        if "\u001b[31m" == joueur2.couleur:
            couleurJ2 = "red"
        elif "\u001b[32m" == joueur2.couleur:
            couleurJ2 = "green"
        elif "\u001b[34;1m" == joueur2.couleur:
            couleurJ2 = "blue"
        elif "\u001b[35m" == joueur2.couleur:
            couleurJ2 = "magenta"

        contenuFichierTexte = txtWalls + "\n" + joueur1.name + "\n" + posJ1 + "\n" + str(
            joueur1.nombre_mur) + "\n" + couleurJ1 + "\n" + joueur2.name + "\n" + posJ2 + "\n" + str(
            joueur2.nombre_mur) + "\n" + couleurJ2 + "\n" + str(game.tour) + "\n"
        return contenuFichierTexte

    def ecriture(self, text):
        try:
            f = open(self.filename, "w")
            f.write(text)
            f.close()
            return True
        except Exception as exc:
            print("Écriture de la sauvegarde échouée: " + str(exc))
            return False

    def lecture(self):
        try:
            f = open(self.filename, "r")
            sauvegarde = f.readlines()
        except Exception as exc:
            print("La lecture du fichier à échouée: " + str(exc))
            return None

        sauvegarde = [x[0:-1] for x in sauvegarde]

        infoJoueur1 = []
        infoJoueur2 = []

        compteurLigne = 0

        walls = sauvegarde[compteurLigne].split(" ")
        wallsPos = []
        for i in walls:
            wallsPos.append(tuple(int(x) for x in i))

        compteurLigne += 1
        for i in range(compteurLigne, compteurLigne + 8):
            if i <= 4:
                infoJoueur1.append(sauvegarde[i])
            else:
                infoJoueur2.append(sauvegarde[i])

        infoJoueur1[1] = tuple(int(x) for x in infoJoueur1[1])
        infoJoueur2[1] = tuple(int(x) for x in infoJoueur2[1])

        partie = Game(10)
        if sauvegarde[9] == "True":
            partie.tour = True
        else:
            partie.tour = False

        wallsPos = [x for x in wallsPos if x != ()]
        if wallsPos != []:
            for i in wallsPos:
                partie.add_wall(i)

        joueur1 = Player(infoJoueur1[0], infoJoueur1[1], partie)
        joueur2 = Player(infoJoueur2[0], infoJoueur2[1], partie)

        joueur1.nombre_mur = int(infoJoueur1[2])
        joueur2.nombre_mur = int(infoJoueur2[2])

        couleurJ1 = ""
        if "red" == infoJoueur1[3]:
            couleurJ1 = "\u001b[31m"
        elif "green" == infoJoueur1[3]:
            couleurJ1 = "\u001b[32m"
        elif "blue" == infoJoueur1[3]:
            couleurJ1 = "\u001b[34;1m"
        elif "magenta" == infoJoueur1[3]:
            couleurJ1 = "\u001b[35m"

        couleurJ2 = ""

        if "red" == infoJoueur2[3]:
            couleurJ2 = "\u001b[31m"
        elif "green" == infoJoueur2[3]:
            couleurJ2 = "\u001b[32m"
        elif "blue" == infoJoueur2[3]:
            couleurJ2 = "\u001b[34;1m"
        elif "magenta" == infoJoueur2[3]:
            couleurJ2 = "\u001b[35m"

        joueur1.couleur = couleurJ1
        joueur2.couleur = couleurJ2

        joueur1.joue.plateau[joueur1.position[0]][joueur1.position[1]] = joueur1.couleur + joueur1.name[
            0] + joueur1.joue.fin_couleur
        joueur2.joue.plateau[joueur2.position[0]][joueur2.position[1]] = joueur2.couleur + joueur2.name[
            0] + joueur2.joue.fin_couleur

        return [partie, joueur1, joueur2]


class Game:

    def __init__(self, board_size: int):
        self.board_size = board_size
        self.wall = []
        self.plateau = [["|" for x in range(self.board_size)] for y in range(self.board_size)]
        self.red = "\u001b[31m"
        self.green = "\u001b[32m"
        self.blue = "\u001b[34;1m"
        self.magenta = "\u001b[35m"
        self.brown = "\033[0;33m"
        self.light_blue = "\033[1;34m"
        self.LIGHT_PURPLE = "\033[1;35m"
        self.fin_couleur = '\x1B[0m'
        self.pose_mur = "m"
        self.bouger = "b"
        self.monter = "z"
        self.descendre = "s"
        self.droite = "d"
        self.gauche = "q"
        self.nbplayer = 0
        self.tour = True
        self.arret = False
        self.nb_mur = 6

    def draw(self):
        number = 0
        print("  " + " ".join(str(i) for i in range(0, 10)))
        for i in self.plateau:
            print(number, end=" ")
            print(" ".join(i))

            number += 1

    def add_player(self, player):
        position = player.position
        nom = player.name
        self.nbplayer += 1
        self.plateau[position[0]][position[1]] = nom[0]

    def add_wall(self, place: tuple):
        self.wall.append(place)
        self.plateau[place[0]][place[1]] = self.brown + "X" + self.fin_couleur

    def is_wall(self, place: tuple):

        if place in self.wall:
            return True

    def is_joueur(self, pos, joueur1, joueur2):

        if joueur1.position == pos or joueur2.position == pos:
            return True
        return False

    def description(self):

        print(self.LIGHT_PURPLE + "\n"
                                  "░██████╗░██╗░░░██╗░█████╗░██████╗░██╗██████╗░░█████╗░██████╗░\n"
                                  "██╔═══██╗██║░░░██║██╔══██╗██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗\n"
                                  "██║██╗██║██║░░░██║██║░░██║██████╔╝██║██║░░██║██║░░██║██████╔╝\n"
                                  "╚██████╔╝██║░░░██║██║░░██║██╔══██╗██║██║░░██║██║░░██║██╔══██╗\n"
                                  "░╚═██╔═╝░╚██████╔╝╚█████╔╝██║░░██║██║██████╔╝╚█████╔╝██║░░██║\n"
                                  "░░░╚═╝░░░░╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝\n" + self.fin_couleur)

        print("Bienvenue sur Quoridor")

        choix = input("Veuillez choisir une option\n"
                      "1. Règle\n"
                      "2. Afficher et modifier les commandes\n"
                      "3. Nombre de mur\n"
                      "4. Lancer la partie\n"
                      "> ")

        while choix != "1" and choix != "2" and choix != "3" and choix != "4":
            choix = input("Mauvaise entrée! Réessayez. > ")

        while choix == "1" or choix == "2" or choix == "3":

            if choix == "1":
                print(
                    "Votre but : atteindre le premier la ligne opposée.Votre problème : l'adversaire pose des barrières pour vous ralentir ! Rassurez-vous : il doit vous laisser au moins un passage libre. Mais qui aura le chemin le plus court ?\n"
                    "Vous aurez maximum 6 barrière pour empècher les joueurs d'arriver à sa fin. Ou vous avez une options qui vous permettra de modifier ce nombre.\n"
                    "Vous aurez une possibilité de sauvegarder une partie à tout moment pour recommencer plus tard!")

            if choix == "2":

                print(
                    "Il y aura deux manières de jouer, si vous voulez poser un mur il faudra appuyer sur [M], apres ça vous allez avoir 2 coordonées à placer dans le X et le Y\n"
                    "Puis si vous voulez pas placer un mur, vous pouvez vous déplacer, il faudra appuyer sur [B), après si vous voulez aller vers le haut press [Z], vers le bas [S], vers la gauche [Q] et pour finir vers la droite [D]")

                choix_commande = input(
                    "Voulez-vous changer les commandes ou garder celle de base ? [g]arder ou [c]hanger\n> ").lower()

                while choix_commande != "c" and choix_commande != "g":
                    choix_commande = input("Mauvaise entrée! Réessayez. > ").lower()

                if choix_commande == "c":
                    print("Écrivez une nouvelle commande pour...")
                    choix_m = input("... poser un mur : ").lower()
                    while choix_m == "p" or len(choix_m) != 1:
                        print(
                            "Mauvaise entrée! Vous ne pouvez pas utiliser la touche [P] car il est déjà utiliser pour la sauvegarde ou vous avez entré 2 ou plusieurs caractères")
                        choix_m = input("... poser un mur : ").lower()

                    choix_b = input("... se déplacer : ").lower()
                    while choix_b == "p" or len(choix_b) != 1 or choix_b == choix_m:
                        print(
                            "Mauvaise entrée! Vous ne pouvez pas utiliser la touche [P] car il est déjà utiliser pour la sauvegarde ou vous avez entré 2 ou plusieurs caractères ou vous avez déja utilisé cette touche pour une autre commande")
                        choix_b = input("... se déplacer : ").lower()

                    choix_z = input("... monter : ").lower()
                    while choix_z == "p" or len(choix_z) != 1 or choix_z in[choix_m, choix_b]:
                        print(
                            "Mauvaise entrée! Vous ne pouvez pas utiliser la touche [P] car il est déjà utiliser pour la sauvegarde ou vous avez entré 2 ou plusieurs caractères ou vous avez déja utilisé cette touche pour une autre commande")
                        choix_z = input("... monter : ").lower()

                    choix_s = input("... descendre : ").lower()
                    while choix_s == "p" or len(choix_s) != 1 or choix_s in[choix_m, choix_b, choix_z]:
                        print(
                            "Mauvaise entrée! Vous ne pouvez pas utiliser la touche [P] car il est déjà utiliser pour la sauvegarde ou vous avez entré 2 ou plusieurs caractères ou vous avez déja utilisé cette touche pour une autre commande")
                        choix_s = input("... descendre : ").lower()

                    choix_q = input("... aller à gauche : ").lower()
                    while choix_q == "p" or len(choix_q) != 1 or choix_q in[choix_m, choix_b, choix_z, choix_s]:
                        print(
                            "Mauvaise entrée! Vous ne pouvez pas utiliser la touche [P] car il est déjà utiliser pour la sauvegarde ou vous avez entré 2 ou plusieurs caractères ou vous avez déja utilisé cette touche pour une autre commande")
                        choix_q = input("... aller à gauche : ").lower()

                    choix_d = input("... aller à droite : ").lower()
                    while choix_d == "p" or len(choix_d) != 1 or choix_d in[choix_m, choix_b, choix_z, choix_s, choix_q]:
                        print(
                            "Mauvaise entrée! Vous ne pouvez pas utiliser la touche [P] car il est déjà utiliser pour la sauvegarde ou vous avez entré 2 ou plusieurs caractères ou vous avez déja utilisé cette touche pour une autre commande")
                        choix_d = input("... aller à droite : ").lower()

                    self.pose_mur = choix_m
                    self.bouger = choix_b
                    self.monter = choix_z
                    self.descendre = choix_s
                    self.droite = choix_d
                    self.gauche = choix_q

                    print("Voici les nouvelles commendes:\nSe déplacer : " + self.bouger + ",\nPoser un mur : " + self.pose_mur + ",\nDroite : " + self.droite + " ,\nGauche : " + self.gauche + ",\nDescendre : " + self.descendre + ",\nMonter : " + self.monter)

                elif choix_commande == "garder":
                    print("Les commandes n'ont pas été modifiées")

            if choix == "3":

                print("Les nombres de murs sont initialisés à 6 par joueur.")

                choix_nbmur = input("Voulez-vous garder le nombre de mur initial? [g]arder ou [c]hanger\n> ").lower()

                while choix_nbmur != "g" and choix_nbmur != "c":
                    choix_nbmur = input("Mauvaise entrée! Réessayez. > ")

                if choix_nbmur == "g":
                    print("Vous avez gardé les paramètres de base")

                elif choix_nbmur == "c":
                    correct = False
                    while not correct:
                        try:
                            nombre_mur = int(input("Combien de mur voulez-vous que chaque joueur possède? Entre 5 et 12"))
                            if 5 <= nombre_mur <= 12:
                                correct = True
                                self.nb_mur = nombre_mur
                            else:
                                print("Le chiffre n'est pas compris entre 5 et 12")
                        except ValueError:
                            print("Votre entrée n'est pas un nombre")

            choix = input("\n\nVeuillez choisir une option\n"
                          "1. Règle\n"
                          "2. Commandes ou Changement de commande\n"
                          "3. Nombre de mur\n"
                          "4. Lancer la partie\n"
                          "> ")
            while choix != "1" and choix != "2" and choix != "3" and choix != "4":
                choix = input("Mauvaise entrée! Réessayez. > ")

        if choix == "4":
            print("la partie va commencer")

    def lancement_des(self, joueur1, joueur2):

        des = input("voulez-vous lancer les dés pour déterminer qui jouera le premier ? oui ou non.\n"
                    "> ").lower()
        while des != "oui" and des != "non":
            des = input("Mauvaise entrée! Réessayez. > ").lower()
        if des == "oui":
            des1 = random.randint(1, 6)
            des2 = random.randint(1, 6)
            while des1 == des2:
                des1 = random.randint(1, 6)
                des2 = random.randint(1, 6)
            print("des du joueur1 :", des1)
            print("des du joueur2 :", des2)
            if des2 > des1:
                self.tour = False
                print("c'est", joueur2.name, "qui commence")
            else:
                print("c'est", joueur1.name, "qui commence")

    def play(self, joueur1, joueur2):

        while not joueur1.is_winner() and not self.arret:
            if not self.tour:
                a.draw()
                joueur2.play()
                self.changerTour()
                if joueur2.is_winner() == "j2":
                    print("Le gagnant est", joueur2.name + "!")
                elif not self.arret:
                    a.draw()
                    joueur1.play()
                    self.changerTour()
                    if joueur1.is_winner() == "j1":
                        print("Le gagnant est", joueur1.name + "!")
            else:
                a.draw()
                joueur1.play()
                self.changerTour()
                if joueur1.is_winner() == "j1":
                    print("Le gagnant est", joueur1.name + "!")
                elif not self.arret:
                    a.draw()
                    joueur2.play()
                    self.changerTour()
                    if joueur2.is_winner() == "j2":
                        print("Le gagnant est", joueur2.name + "!")

    def changerTour(self):

        if self.tour:
            self.tour = False
        else:
            self.tour = True


class Player:

    def __init__(self, name: str, position, joue):
        self.name = name
        self.position = position
        self.couleur = ""
        self.joue = joue
        joue.add_player(self)
        self.commence = False
        self.nombre_mur = self.joue.nb_mur

    def place_wall(self, place: tuple, joueur1, joueur2):

        if not self.joue.is_joueur(place, joueur1, joueur2) and self.nombre_mur > 0 and not (self.joue.is_wall(place)):
            self.joue.add_wall(place)
            return True
        else:
            print("Il n'est pas possible de placer un mur à la position", place[0], ";", place[1])
            return False

    def choix_couleur1(self):

        print("Choississez une couleur pour le pion du joueur1")
        choix = input("Rouge ou Vert\n"
                      "> ").lower()
        while choix != "rouge" and choix != "vert":
            choix = input("Mauvaise entrée! Réessayez. > ").lower()

        if choix.lower() == "rouge":
            self.couleur = self.joue.red
        elif choix.lower() == "vert":
            self.couleur = self.joue.green

        self.joue.plateau[self.position[0]][self.position[1]] = self.couleur + self.name[0] + self.joue.fin_couleur

    def choix_couleur2(self):

        print("Choississez une couleur pour le pion du joueur2")
        choix2 = input("Bleu ou Violet.\n"
                      "> ").lower()
        while choix2 != "bleu" and choix2 != "violet":
            choix2 = input("Mauvaise entrée! Réessayez. > ").lower()

        if choix2.lower() == "bleu":
            self.couleur = self.joue.blue
        elif choix2.lower() == "violet":
            self.couleur = self.joue.magenta

        self.joue.plateau[self.position[0]][self.position[1]] = self.couleur + self.name[0] + self.joue.fin_couleur

    def move(self, mouvement: tuple):

        self.joue.plateau[self.position[0]][self.position[1]] = "|"
        self.joue.plateau[mouvement[0]][mouvement[1]] = self.couleur + self.name[0] + self.joue.fin_couleur

    def play(self):

        listeMouvements = [self.joue.monter, self.joue.descendre, self.joue.gauche,
                           self.joue.droite]  # 0=haut, 1=bas, 2=gauche, 3=droite

        print("C'est au tour de", self.name)
        deplacement = input(
            "Que voulez-vous faire ?\n" + self.joue.bouger.upper() + " = bouger,\n" + self.joue.pose_mur.upper() + " = poser un mur,\n" + "P = sauvegarder la partie\n> ").lower()

        while deplacement not in [self.joue.bouger, self.joue.pose_mur, "p"]:
            deplacement = input("Mauvaise entrée! Réessayez. > ").lower()

        if deplacement == "p":
            sauvegardePartie = SaveGame(joueur1, joueur2, self.joue)
            text = sauvegardePartie.sauvegarde(joueur1, self.joue, joueur2)
            if sauvegardePartie.ecriture(text):
                print("Partie sauvegardée")
                self.joue.arret = True

        if deplacement == self.joue.bouger:
            mvmt = input(self.joue.monter.upper() + " = déplacer vers le haut \n" +
                         self.joue.descendre.upper() + " = déplacer vers le bas \n" +
                         self.joue.gauche.upper() + " = déplacer vers la gauche \n" +
                         self.joue.droite.upper() + " = déplacer vers la droite \n"
                                                    "> ").lower()
            while mvmt not in listeMouvements:
                mvmt = input("Mauvaise entrée! Réessayez. > ").lower()

            x = self.position[0]
            y = self.position[1]

            if mvmt == listeMouvements[0]:
                x -= 1
            elif mvmt == listeMouvements[1]:
                x += 1
            elif mvmt == listeMouvements[2]:
                y -= 1
            elif mvmt == listeMouvements[3]:
                y += 1

            if x > 9 or y > 9 or x < 0 or y < 0:
                print("Vous ne pouvez pas aller dans cette direction")
                print("Recommencer")
                self.play()
            elif (x, y) == joueur1.position or (x, y) == joueur2.position:
                print("Un joueur se trouve à la position", x, ";", y)
                print("Recommencer")
                self.play()
            elif self.joue.is_wall((x, y)):
                print("Un mur se trouve à la position", x, ";", y)
                print("Recommencer")
                self.play()
            else:
                self.move((x, y))
                self.position = x, y

        elif deplacement == self.joue.pose_mur:

            print("Où voulez-vous placez votre mur ?")

            correct = False
            while not correct:
                try:
                    abscisse = int(input("l'axe des x : "))
                    ordonnee = int(input("l'axe des y : "))
                    if 0 <= abscisse <= 9 and 0 <= ordonnee <= 9:
                        if self.place_wall((abscisse, ordonnee), joueur1, joueur2):
                            self.nombre_mur -= 1
                            print("Il ne vous reste plus que", self.nombre_mur, "murs à poser")
                        else:
                            self.play()
                        correct = True
                    else:
                        print("Les coordonées ne sont pas dans le plateau")
                except ValueError:
                    print("Votre entrée n'est pas un nombre")

    def is_winner(self):

        if joueur1.position[0] == 9:
            return "j1"

        elif joueur2.position[0] == 0:
            return "j2"

        else:
            return False

if __name__ == "__main__":
    charger = input("Voulez-vous charger une partie? oui/non:\n> ")
    while charger != "oui" and charger != "non":
        charger = input("Mauvaise entrée! Réessayez. > ").lower()
    if charger.lower() == "oui":
        infoPartie = SaveGame()
        a, joueur1, joueur2 = infoPartie.lecture()
        a.play(joueur1, joueur2)
    else:
        a = Game(10)
        a.description()
        nom_joueur1 = input("Comment vous appelez-vous? [J1] : ")
        while len(nom_joueur1) ==0:
            nom_joueur1 = input("Comment vous appelez-vous? [J1] : ")
        nom_joueur2 = input("Comment vous appelez-vous? [J2] : ")
        while len(nom_joueur2) ==0:
            nom_joueur2 = input("Comment vous appelez-vous? [J2] : ")
        joueur1 = Player(nom_joueur1, (0, 4), a,)
        joueur2 = Player(nom_joueur2, (9, 4), a,)
        joueur1.choix_couleur1()
        joueur2.choix_couleur2()
        a.lancement_des(joueur1, joueur2)
        a.play(joueur1, joueur2)

