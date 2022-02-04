# coding: utf-8

import socket
from datetime import datetime
import mysql.connector
import time

# #Bluetooth receiving message
# hostMACAddress = 'e4:70:B8:09:df:ed'#'e4:42:1a:3f:5c:27' #            #The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
# #hostname=socket.gethostname()
# port = 5 # 3 is an arbitrary choice. However, it must match the port used by the client.
# backlog = 1
# size = 1024
#
# s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
# s.bind((hostMACAddress,port))
# s.listen(backlog)
#
# ok=0
# while ok==0:
#     try:
#         print("En écoute...")
#         time.sleep(20)
#         client, address = s.accept()
#         ok=1
#         while 1:
#             data = client.recv(size)
#             if data:
#                 #print(data)
#                 #Récupération des deux numéros du message
#                 new_data = data.decode("utf-8")     #data:bytes --> Il faut décoder les bytes en string
#                 x = new_data.split(";")             #récupération du numéro étudiant et de l'identifiant du téléphone dans deux variable
#                 print(x[0], x[1])                   #x[0]: n° étudiant ; x[1]:n°téléphone
#
#                 #Récupération de la date et l'heure de réception du message
#                 date_recept = datetime.now()
#                 formatted_date = date_recept.strftime('%Y-%m-%d %H:%M:%S')
#                 print(formatted_date)
#
#                 #Connexion et envois des infos à la base de données
#                 db = mysql.connector.connect(host="localhost", user="root", password="", database="gphy_presence")#user="gphypresence",password="kjnfkvn-456123-ibsfdbv"
#                 with mysql.connector.connect(host="localhost", user="root", password="", database="gphy_presence") as db :
#                     with db.cursor() as c:
#                         c.execute("select count(*) from identite where num_etu=%s ", (x[0],)) #Vérif si le numéro étudiant existe dans la base
#                         resultat = c.fetchall()
#                         print(resultat)
#                         if resultat[0] == (0,):
#                             try:
#                                 print("ajout...")
#                                 c.execute("INSERT INTO Identite ( num_etu, num_IMEI)  VALUES(%s, %s)", x) #Insert l'étudiant dans la base si il n'y est pas déjà
#                                 c.execute("INSERT INTO presence (num_capteur, num_ident, tag_horaire)  VALUES( %s, %s, %s)", (1, x[0], formatted_date)) #Insert le tag horaire de présence dans la base
#                                 db.commit()
#                             except mysql.connector.errors.IntegrityError:
#                                 print("Etudiant déjà inscrit dans la base de données")
#                         else:
#                             c.execute("INSERT INTO presence (num_capteur, num_ident, tag_horaire)  VALUES( %s, %s, %s)", (1, x[0], formatted_date)) #Insert le tag horaire de présence dans la base
#                             db.commit()
#                 db.close()
#
#                 #Générer la date et l'heure à laquelle le message a été reçu et l'envoyer à l'app
#                 date_retour = formatted_date.encode("utf-8")
#                 print(date_retour)
#                 client.send(date_retour)
#                 client.close()
#                 s.close()
#                 ok=0
#     except:
#         print("Closing socket")
#         client.close()
#         s.close()
        #ok=0

new_data="21911504;5727972890"
date_recept = datetime.now()
formatted_date = date_recept.strftime('%Y-%m-%d %H:%M:%S')

#Récupération des deux numéros
x = new_data.split(";")
user = (x[0], x[1])
etu=x[0]


#print(x[0], x[1]) #x[0]: n° étudiant ; x[1]:n°téléphone

#Connexion et envois des infos à la base de données
db = mysql.connector.connect(host="localhost", user="root", password="", database="gphy_presence")#user="gphypresence",password="kjnfkvn-456123-ibsfdbv"
with mysql.connector.connect(host="localhost", user="root", password="", database="gphy_presence") as db :
    with db.cursor() as c:
        c.execute("select count(*) from identite where num_etu=%s ", (x[0],))
        resultat = c.fetchall()
        print(resultat)
        if resultat[0] == (0,):
            c.execute("select count(*) from liste_etu where num_etu=%s ", (x[0],))
            resultat2 = c.fetchall()
            if resultat2[0] == (1,):
                c.execute("select nom_etu from liste_etu where num_etu=%s ", (x[0],))
                nom=c.fetchall()
                print(nom)
                c.execute("select prenom_etu from liste_etu where num_etu=%s ", (x[0],))
                prenom=c.fetchall()
                print(prenom)
                envoi_nom="ok"
            else:
                try:
                    c.execute("INSERT INTO identite (num_etu, num_IMEI)  VALUES(%s, %s)", user)
                    c.execute("INSERT INTO presence (num_capteur, num_ident, tag_horaire)  VALUES( %s, %s, %s)", (1, x[0], formatted_date))
                    db.commit()
                except mysql.connector.errors.IntegrityError:
                    print("Etudiant déjà inscrit dans la base de données")
        else:
            print("ok")
            print(x[0], formatted_date)
            c.execute("INSERT INTO presence (num_capteur, num_ident, tag_horaire)  VALUES( %s, %s, %s)", (1, x[0], formatted_date))
            db.commit()
db.close()