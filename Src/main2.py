# Site web du code utilisé: https://python.developpez.com/cours/TutoSwinnen/?page=page_20
#
# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.

HOST = '04:42:1a:3f:5c:27' #adaptateur: '04:42:1a:3f:5c:27''e4:70:B8:09:df:ed'
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
                print (message)

                #Récupération de la date et l'heure de réception du message
                date_recept = datetime.now()
                formatted_date = date_recept.strftime('%Y-%m-%d %H:%M:%S'+';')
                nom_e=""
                prenom_e=""
                envoi_nom=""
                #print(formatted_date)

                #Connexion et envois des infos à la base de données
                db = mysql.connector.connect(host="localhost", user="root", password="", database="gphy_presence")#user="gphypresence",password="kjnfkvn-456123-ibsfdbv"
                with mysql.connector.connect(host="localhost", user="root", password="", database="gphy_presence") as db :
                    with db.cursor() as c:
                        c.execute("select count(*) from identite where num_etu=%s ", (x[0],)) #Vérif si le numéro étudiant existe dans la table identite
                        resultat = c.fetchall()
                        #print(resultat)
                        if resultat[0] == (0,): #Si le numéro étudiant n'existe pas dans la table identite
                            c.execute("select count(*) from liste_etu where num_etu=%s ", (x[0],))
                            resultat2 = c.fetchall()
                            if resultat2[0] == (1,): #Si le numéro est dans la liste des étudiants
                                c.execute("select nom_etu from liste_etu where num_etu=%s ", (x[0],))
                                nom_e=c.fetchall()
                                #print(nom_e)
                                c.execute("select prenom_etu from liste_etu where num_etu=%s ", (x[0],))
                                prenom_e=c.fetchall()
                                #print(prenom_e)
                                #if nom_e[0] != "" and prenom_e[0] != "":
                                envoi_nom="ok"
                                #else:
                                    #envoi_nom="pas ok"
                            else: #Si le numéro n'est pas dans la liste des étudiants
                                envoi_nom="pas ok"
                            #Si le numéro etudiant n'existe pas dans identité
                            try:
                                #print("ajout...")
                                c.execute("INSERT INTO Identite ( num_etu, num_IMEI)  VALUES(%s, %s)", x) #Insert l'étudiant dans la base si il n'y est pas déjà
                                db.commit()
                                #c.execute("INSERT INTO presence (num_capteur, num_ident, tag_horaire)  VALUES( %s, %s, %s)", (1, x[0], formatted_date)) #Insert le tag horaire de présence dans la base
                                #db.commit()
                            except mysql.connector.errors.IntegrityError:
                                print("Etudiant déjà inscrit dans la base de données")
                        else:
                            c.execute("select count(*) from identite where num_IMEI=%s ", (x[1],))
                            id_tel=c.fetchall()
                            print(id_tel[0])
                            if id_tel[0] != (0,):
                                c.execute("INSERT INTO presence (num_capteur, num_ident, tag_horaire)  VALUES( %s, %s, %s)", (1, x[0], formatted_date)) #Insert le tag horaire de présence dans la base
                                db.commit()
                            else:
                                envoi_nom="mauvais identifiant telephone"
                db.close()


                if envoi_nom == "ok" :
                    nom_prenom="".join(nom_e[0]) + " " + "".join(prenom_e[0]) + ";"
                    #print(nom_prenom)
                    self.connexion.send(nom_prenom.encode())
                    #newmsg=self.connexion.recv(1024)
                    #if newmsg:
                    #    new_message=newmsg.decode("utf-8")
                    #    print(new_message)
                elif envoi_nom == "pas ok":
                    self.connexion.send("Numéro étudiant inconnu;".encode())
                elif envoi_nom == "mauvais identifiant telephone":
                    self.connexion.send("Mauvais identifiant de téléphone;".encode())
                else:
                    date_retour=formatted_date.encode("utf-8")
                    print(date_retour)
                    self.connexion.send(date_retour)

        # Fermeture de la connexion :
        self.connexion.close()      # couper la connexion côté serveur
        del conn_client[nom]        # supprimer son entrée dans le dictionnaire
        print ("Client %s déconnecté." % nom)
        # Le thread se termine ici
        return true;


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
        #date_recept = datetime.now();
        #formatted_date = date_recept.strftime('%Y-%m-%d %H:%M:%S'+';');
        #date_retour=formatted_date.encode("utf-8");
        #connexion.send(date_retour);
        #connexion.send(date_retour).encode())
    except:
        mySocket.close()