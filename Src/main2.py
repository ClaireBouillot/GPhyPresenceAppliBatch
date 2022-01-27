# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.
# site du code utilisé: https://python.developpez.com/cours/TutoSwinnen/?page=page_20

HOST = 'e4:70:B8:09:df:ed'
PORT = 5
import socket, sys, threading
from datetime import datetime
import mysql.connector
import time

class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def run(self):
        # Dialogue avec le client :
        nom = self.getName()        # Chaque thread possède un nom
        while 1:
            msgClient = self.connexion.recv(1024)
            if msgClient:
                message=msgClient.decode("utf-8")
                x = message.split(";")             #récupération du numéro étudiant et de l'identifiant du téléphone dans deux variable
                print(x[0], x[1])                   #x[0]: n° étudiant ; x[1]:n°téléphone
                #print (message)

                #Récupération de la date et l'heure de réception du message
                date_recept = datetime.now()
                formatted_date = date_recept.strftime('%Y-%m-%d %H:%M:%S')
                print(formatted_date)

                #Connexion et envois des infos à la base de données
                db = mysql.connector.connect(host="localhost", user="root", password="", database="gphy_presence")#user="gphypresence",password="kjnfkvn-456123-ibsfdbv"
                with mysql.connector.connect(host="localhost", user="root", password="", database="gphy_presence") as db :
                    with db.cursor() as c:
                        c.execute("select count(*) from identite where num_etu=%s ", (x[0],)) #Vérif si le numéro étudiant existe dans la base
                        resultat = c.fetchall()
                        print(resultat)
                        if resultat[0] == (0,):
                            try:
                                print("ajout...")
                                c.execute("INSERT INTO Identite ( num_etu, num_IMEI)  VALUES(%s, %s)", x) #Insert l'étudiant dans la base si il n'y est pas déjà
                                db.commit()
                                c.execute("INSERT INTO presence (num_capteur, num_ident, tag_horaire)  VALUES( %s, %s, %s)", (1, x[0], formatted_date)) #Insert le tag horaire de présence dans la base
                                db.commit()
                            except mysql.connector.errors.IntegrityError:
                                print("Etudiant déjà inscrit dans la base de données")
                        else:
                            c.execute("INSERT INTO presence (num_capteur, num_ident, tag_horaire)  VALUES( %s, %s, %s)", (1, x[0], formatted_date)) #Insert le tag horaire de présence dans la base
                            db.commit()
                db.close()

        # Fermeture de la connexion :
        date_retour=formatted_date.encode("utf-8")
        print(date_retour)
        self.connexion.send(date_retour)
        self.connexion.close()      # couper la connexion côté serveur
        del conn_client[nom]        # supprimer son entrée dans le dictionnaire
        print ("Client %s déconnecté." % nom)
        # Le thread se termine ici

# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
try:
   mySocket.bind((HOST, PORT))
except socket.error:
   print ("La liaison du socket à l'adresse choisie a échoué.")
   sys.exit()
print ("Serveur prêt, en attente de requêtes ...")
mySocket.listen(1)

# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}                # dictionnaire des connexions clients
while 1:
    try:
        connexion, adresse = mySocket.accept()
    # Créer un nouvel objet thread pour gérer la connexion :
        th = ThreadClient(connexion)
        th.start()
    # Mémoriser la connexion dans le dictionnaire :
        it = th.getName()        # identifiant du thread
        conn_client[it] = connexion
        print ("Client %s connecté, adresse IP %s, port %s." % \
            (it, adresse[0], adresse[1]))
    # Dialogue avec le client :
        connexion.send(("Vous êtes connecté. Envoyez vos messages.").encode())
    except:
        mySocket.close()