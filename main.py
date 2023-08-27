import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMessageBox
import sys
from mainwindow_ui import Ui_MainWindow
from login import Ui_LoginWindow
from PyQt6.QtGui import QIcon
import sqlite3


class Login(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.login_successful = False
        icon = QIcon("./images/icon.png")  
        self.setWindowIcon(icon)
        self.ui.loginButton.clicked.connect(self.login)
    
    def show_warning(self, title, text):
        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        icon = QIcon("./images/icon.png")  
        message_box.setWindowIcon(icon)
        message_box.exec()


    def login(self):
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        if username == "admin" and password == "password":
            self.login_successful = True
            # quit the login wndow when login in if login is successful
            #login_window.close()
            if username != "admin":
                self.show_warning( "Login", " Nom d'utilisateur Incorrect ")
            elif password != "password":
                self.show_warning( "Login", "  Mot de passe Incorrect ")
            else:
                self.show_warning( "Login", " Nom d'utilisateur et Mot de passe Incorrect ")

def create_database():
    connection = sqlite3.connect('bgblast.db')  # Replace 'bgblast.db' with your desired database name
    cursor = connection.cursor()
    
    # Create the "commande" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS commande 
                   (id_C INTEGER PRIMARY KEY,
                    date VARCHAR(50),
                    type_tir VARCHAR(50),
                    mode_tir VARCHAR(50),
                    schema_tir VARCHAR(50),
                    mode_chargement VARCHAR(50),
                    machine_foration VARCHAR(50),
                    machine_decappage VARCHAR(50),
                    panneau VARCHAR(50),
                    tranche VARCHAR(50),
                    niveau VARCHAR(50),
                    profondeur DOUBLE,
                    nombre_trous INTEGER,
                    nombre_rangs INTEGER,
                    nombre_trousrang INTEGER,
                    maille VARCHAR(50),
                    dosage_prevu  DOUBLE )''')
    
    # Create the "resultat" table with a foreign key reference
    cursor.execute('''CREATE TABLE IF NOT EXISTS resultat 
                   (id_R INTEGER PRIMARY KEY,
                    id_commande INTEGER,
                    longueur INTEGER,
                    largeur INTEGER,
                    surface INTEGER,
                    volume DOUBLE,
                    ammonix INTEGER,
                    tovex INTEGER,
                    cordeau12g INTEGER,
                    ligne_tir VARCHAR(50),
                    A_E_I INTEGER,
                    metrage_fore DOUBLE,
                    reccords_17 INTEGER,
                    reccords_25 INTEGER,
                    reccords_42 INTEGER,
                    reccords_65 INTEGER,
                    reccords_100 INTEGER,
                    repartition DOUBLE,
                    C_I DOUBLE,
                    detos_450 INTEGER,
                    detos_500 INTEGER,
                    bourage_final DOUBLE,
                    rendu_prevu DOUBLE,
                    FOREIGN KEY (id_commande) REFERENCES commande(id_C))''')
   
    # Create the "stock" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock 
                   (id_st INTEGER PRIMARY KEY,
                    id_Commande INTEGER,
                    date DATE,
                    type VARCHAR(50),
                    stock_global DOUBLE,
                    stock_actuel Double,
                    FOREIGN KEY (id_Commande) REFERENCES resultat(id_commande))''')
    connection.commit()
    connection.close()
    """
     # Create the "cout" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS cout 
                   (id_ct INTEGER PRIMARY KEY,
                    cout_initial INTEGER,
                    cout_actuel INTEGER,
                    type VARCHAR(50),
                    numero INTEGER)''')
    
    # Create the "user" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user 
                   (id_user INTEGER PRIMARY KEY,
                    name VARCHAR(50),
                    role VARCHAR(50),
                    Profession VARCHAR(50),
                    username VARCHAR(50) ,
                    password VARCHAR(50))''')
    
    # Create the "client" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS client 
                   (id_d INTEGER PRIMARY KEY,
                    id_commande INTEGER,
                    machine VARCHAR(50),
                    pa,
                    FOREIGN KEY (id_commande) REFERENCES commande(id_C))''')"""

   

class my_app(QtWidgets.QMainWindow):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
        icon = QIcon("./images/icon.png")  
        self.setWindowIcon(icon)

        #show L'Acceuil
        self.ui.stackedWidget_2.hide()
        self.ui.stackedWidget.setCurrentWidget(self.ui.Acceuil)
        #self.options= self.ui.stackedWidget_2
        self.ui.pushButton_4.clicked.connect(self.menu_show)
        self.ui.AccBtn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.Acceuil))
        self.ui.AccBtn.clicked.connect(self.hide_Options)     
        self.ui.TbBtn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.Tablaeu_de_bord))
        self.ui.TbBtn.clicked.connect(self.hide_Options)     
        self.ui.GesComBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Commandes_calcul),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Commande_Calcul)
        ))
        self.ui.GesComBtn.clicked.connect(self.show_Options)     

        self.ui.pushButton.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Users),
            self.ui.stackedWidget_2.hide()
        ))
       # self.ui.pushButton.clicked.connect(self.hide_Options)

        self.ui.GesStockBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Stock),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Stock)
        ))
        self.ui.GesStockBtn.clicked.connect(self.show_Options)  
        self.ui.GesStockBtn.clicked.connect(self.stockAffichage)       

        self.ui.GesCoutBtN.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Cout),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Cout)
        ))
        self.ui.GesCoutBtN.clicked.connect(self.show_Options)     

        self.ui.GesASBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Apres_Sautage),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Apres_Sautage)
        ))
        self.ui.GesASBtn.clicked.connect(self.show_Options)     

        self.ui.GesADBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Aven_Decappage),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Avan_Decappage)
        ))
        self.ui.GesADBtn.clicked.connect(self.show_Options)     

        self.ui.documBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Documentation),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Docummentation)
        ))
        self.ui.documBtn.clicked.connect(self.show_Options)   


        self.ui.archiveBtn.clicked.connect(self.show_Options)     
        self.ui.archiveBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives)
        ))
        
        self.valid_inputs=False
        #self.option= self.ui.stackedWidget_2
        #boutton calcul fiche de saisie 
        self.calcul = self.ui.frame_10.findChild(QtWidgets.QPushButton, "pushButton_7")
        self.calcul.clicked.connect(self.calculations) 
        

        self.ui.valResBtn.clicked.connect(self.resetValues)
        self.ui.valResBtn.clicked.connect(self.calculations)
        self.ui.valResBtn.clicked.connect(self.saveResultats)

        self.ui.resetBtnFs.clicked.connect(self.resetValues)

        self.ui.ajouStockBtn.clicked.connect(self.stockStorage)
        
        self.ui.stockAllBtn.clicked.connect(self.stockAffichage)
        
        self.ui.stockPerDateBtn.clicked.connect(self.stockAffichageDate)
        
        self.ui.stockArtBtn.clicked.connect(self.stockAffichageType)
        

        self.ui.historiqueCommandeBtn.clicked.connect(self.show_Options) 
        self.ui.historiqueCommandeBtn.clicked.connect(self.hisCommandeResulat)  
        self.ui.historiqueCommandeBtn.clicked.connect(lambda:(
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Com_Avan)
        ))

        self.ui.historiqueStockBtn.clicked.connect(self.show_Options)     
        self.ui.historiqueStockBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Stock)
        ))
    

        self.ui.historiqueCoutBtn.clicked.connect(self.show_Options)     
        self.ui.historiqueCoutBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Cout)
        ))

        self.ui.historiqueAvDcpBtn.clicked.connect(self.show_Options)     
        self.ui.historiqueAvDcpBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Avan_Decappage)
        ))

        self.ui.pushButton_38.clicked.connect(self.show_Options)     
        self.ui.pushButton_38.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Acces)
        ))
       # self.ui.pushButton_10.clicked.connect(self.exit)
    
    def resetValues (self):
        # Reset the first QComboBox
        self.ui.comboBox.setCurrentIndex(-1)
        self.ui.comboBox_2.setCurrentIndex(-1)
        self.ui.comboBox_3.setCurrentIndex(-1)
        self.ui.comboBox_4.setCurrentIndex(-1)
        self.ui.comboBox_5.setCurrentIndex(-1)
        self.ui.comboBox_5.setCurrentIndex(-1)
        self.ui.comboBox_7.setCurrentIndex(-1)
        self.ui.comboBox_9.setCurrentIndex(-1)
        self.ui.comboBox_10.setCurrentIndex(-1)
        self.ui.comboBox_11.setCurrentIndex(-1)
        # Reset the first QLineEdit
        
        self.ui.line8.setText("")
        self.ui.line1.setText("")
        self.ui.line2.setText("")
        self.ui.line3.setText("")
        self.ui.line4.setText("")
        self.ui.line6.setText("")


    def calculations(self): 
        self.valid_inputs=False
        self.warning_shown = False
        # Connect the warning message outside of the loop
        self.calcul.clicked.connect(lambda: self.show_warning("Fiche de saisie", "Entrées invalides, ressayez "))
        while self.valid_inputs==False:
            try:
                #input Data
                date= str(self.ui.dateEdit.date().toPyDate())
                zoneTir = self.ui.comboBox.currentText()
                modeTir = self.ui.comboBox_2.currentText()
                modeCharg = self.ui.comboBox_3.currentText()
                machineForation= self.ui.comboBox_4.currentText()
                machineDecapage= self.ui.comboBox_5.currentText()
                schemaTir=self.ui.comboBox_6.currentText()
                panneau= self.ui.comboBox_7.currentText()
                tranche= str(self.ui.line8.text())
                niveau= self.ui.comboBox_9.currentText()
                profondeur= int(self.ui.line1.text())
                nbrTrous = int(self.ui.line2.text())
                nbrRang = int(self.ui.line3.text())
                nbrTrousRange= int(self.ui.line4.text())
                maille1 = int(self.ui.comboBox_10.currentText())
                maille2 = int(self.ui.comboBox_11.currentText())
                maille_combined = f"{maille1},{maille2}"
                dosagePrevu= float(self.ui.line6.text())
                self.valid_inputs= True

                # Database operations
                # Connect to the SQLite database
                connection = sqlite3.connect('bgblast.db')
                cursor = connection.cursor()
                # Insert data into the "commande" table
                cursor.execute('''
                    INSERT INTO commande (date, type_tir, mode_tir, schema_tir, mode_chargement, machine_foration,
                                        machine_decappage, panneau, tranche, niveau, profondeur, nombre_trous, nombre_rangs, nombre_trousrang,
                                maille,   dosage_prevu)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    date, zoneTir, modeTir, schemaTir, modeCharg, machineForation, machineDecapage, panneau,
                    tranche, niveau, profondeur, nbrTrous, nbrRang, nbrTrousRange,maille_combined, dosagePrevu
                ))
                # Commit the changes to the database
                connection.commit()
            
                connection.close()                
            except ValueError:
                 # Show a warning message only once                
                if not self.warning_shown:
                    self.adjustSizewarning_shown = True
                    self.show_warning("Fiche de saisie", "Entrées invalides, ressayez ")
                        
                return
                
        #proceed with calculations
        if self.valid_inputs == True:        
            self.calcul.clicked.connect(lambda:(
            
                self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Commandes_resultats),
                self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Commande_Resultats)
            ))    
            self.calcul.clicked.connect(self.show_Options) 
            
            #operations 
            longueur= maille1*nbrRang
            largeur= maille2*nbrRang
            surface = longueur*largeur
            volume = surface*profondeur
            #Quantité Ammonix
            ammonix = dosagePrevu/(profondeur * maille1 * maille2 * nbrTrous) # 
            ammonix = ammonix if ammonix % 25 == 0 else (int( ammonix / 25) + 1) * 25
            #Quantité tovex
            tovex = nbrTrous/2
            tovex = tovex if tovex % 25 == 0 else (int(tovex / 25) + 1) * 25
            cordeau = 0
            ligneTir = "500m"
            aei = 1
            metrageFore = nbrTrous*profondeur
            repartition = ammonix/nbrTrous 
            renduPrevu = volume/21 # 21 heures de marche 
            bourrageFinal = profondeur - (repartition*0.75)
            ci = repartition*25    

            if modeCharg=="Unique":
                detos500 = nbrTrous+2
                detos450 =0
            else:
                detos500 = 0
                detos450 = nbrTrous+2
                
            if schemaTir=="17ms,25ms,42ms":
                reccords17 = (nbrTrous - ( nbrRang +2))+2
                reccords25 = nbrRang + 2
                reccords42 = nbrRang + 2
                reccords65 = 0
                reccords100 = 0
            elif schemaTir=="17ms,25ms,42ms,65ms":
                reccords17 = (nbrTrous - ( nbrRang +2) )+2
                reccords25 = nbrRang + 2
                reccords42 = nbrRang + 2
                reccords65 = nbrRang + 2
                reccords100 = 0
            elif schemaTir=="17ms,25ms":
                reccords17 = (nbrTrous - ( nbrRang +2) )+2
                reccords25 = nbrRang + 2
                reccords42 = 0
                reccords65 = 0
                reccords100 = 0
            elif schemaTir=="17ms,100ms":
                reccords17 = (nbrTrous - ( nbrRang +2) )+2
                reccords25 = 0
                reccords42 = 0
                reccords65 = 0
                reccords100 = nbrTrousRange
            #output 
            self.ui.o1.setText(str(longueur))
            self.ui.o2.setText(str(largeur))
            self.ui.o3.setText(str(surface))
            self.ui.o4.setText(str(volume))
            self.ui.o5.setText(str(ammonix))
            self.ui.o6.setText(str(tovex))
            self.ui.o7.setText(str(cordeau))
            self.ui.o8.setText(str(ligneTir))
            self.ui.o9.setText(str(aei))
            self.ui.o10.setText(str(metrageFore))
            self.ui.o17.setText(str(detos450))
            self.ui.o18.setText(str(detos500))
            self.ui.o11.setText(str(reccords25))
            self.ui.o12.setText(str(reccords42))
            self.ui.o13.setText(str(reccords65))
            self.ui.o14.setText(str(reccords17))
            self.ui.o15.setText(str(repartition))
            self.ui.o16.setText(str(renduPrevu))
            self.ui.o19.setText(str(bourrageFinal))
            self.ui.o20.setText(str(ci)) 
            self.ui.o21.setText(str(reccords100))

# fonction d'enregistrement des resultats dans la db

    def saveResultats (self):
        longueur = self.ui.o1.text()
        largeur = self.ui.o2.text()
        surface = self.ui.o3.text()
        volume=self.ui.o4.text()
        ammonix =self.ui.o5.text()
        tovex=self.ui.o6.text()
        cordeau=self.ui.o7.text()
        ligneTir=self.ui.o8.text()
        aei=self.ui.o9.text()
        metrageFore=self.ui.o10.text()
        detos450=self.ui.o17.text()
        detos500=self.ui.o18.text()
        reccords25=self.ui.o11.text()
        reccords42=self.ui.o12.text()
        reccords65=self.ui.o13.text()
        reccords17=self.ui.o14.text()
        repartition=self.ui.o15.text()
        renduPrevu=self.ui.o16.text()
        bourrageFinal=self.ui.o19.text()
        ci=self.ui.o20.text() 
        reccords100=self.ui.o21.text()
        
        try :   
            # Connect to the SQLite database
            connection = sqlite3.connect('bgblast.db')
            cursor = connection.cursor()

                    
                    # Execute the SELECT query to get the last id_C
            cursor.execute('''SELECT id_C FROM commande ORDER BY id_C DESC LIMIT 1''')
            
            # Fetch the result of the query
            result = cursor.fetchone()

            # Check if a result was obtained
            if result:
                # Extract the id_C value from the result
                id_commande = result[0]

                # Insert data into the "resultat" table with the corresponding id_commande
                cursor.execute('''
                    INSERT INTO resultat (id_commande, longueur, largeur, surface, volume, ammonix, tovex, cordeau12g, 
                                        ligne_tir, A_E_I, metrage_fore, reccords_17, reccords_25, reccords_42, reccords_65, 
                                        reccords_100, repartition, C_I, detos_450, detos_500, bourage_final, rendu_prevu)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    id_commande, longueur, largeur, surface, volume, ammonix, tovex, cordeau, ligneTir, aei, metrageFore,
                    reccords17, reccords25, reccords42, reccords65, reccords100, repartition, ci, detos450, detos500,
                    bourrageFinal, renduPrevu
                ))

                # Commit the changes to the database
                connection.commit()

                # Close the connection
                connection.close()
                
                self.updateStock

                self.show_Information("Fiche de saisie", "Résultats bien enregistrées ")
        except sqlite3.Error as e:
            # Print the specific error message
            print("SQLite error:", e)
            self.show_warning("SQLite Error", "Une erreur s'est produite lors de l'enregistrement des données.")
        except Exception as e:
            # Print any other unexpected exceptions
            print("Unexpected error:", e)
            self.show_warning("Unexpected Error", "Une erreur inattendue s'est produite.")

# fonction de ajout de stock
    def hisCommandeResulat(self):
        # Assuming you have a database connection established as 'connection'
        cursor = connection.cursor()
        
        # Execute a query to fetch data from the 'commande' and 'resultat' tables
        cursor.execute('''
            SELECT r.id_R, c.date, c.type_tir, c.mode_tir, c.mode_chargement,
                c.machine_foration, c.machine_decappage, c.schema_tir,
                c.panneau, c.tranche, c.niveau, c.profondeur, c.nombre_trous, c.nombre_rangs,
                c.nombre_trousrang, c.maille, c.dosage_prevu,
                r.longueur, r.largeur, r.surface, r.volume, r.ammonix,
                r.tovex, r.cordeau12g, r.ligne_tir, r.A_E_I, r.metrage_fore,
                r.reccords_17, r.reccords_25, r.reccords_42, r.reccords_65,
                r.reccords_100, r.repartition, r.C_I, r.detos_450, r.detos_500,
                r.bourage_final, r.rendu_prevu
            FROM commande c
            INNER JOIN resultat r ON c.id_C = r.id_commande
        ''')

        # Fetch all rows from the query result
        data = cursor.fetchall()

        # Clear the existing table content
        self.ui.tableWidget.clearContents()

        # Set the number of rows in the table
        self.ui.tableWidget.setRowCount(len(data))

        # Iterate through the data and populate the table
        for row_num, row_data in enumerate(data):
            for col_num, col_value in enumerate(row_data):
                # Create a QTableWidgetItem and set its text to the database value
                item = QtWidgets.QTableWidgetItem(str(col_value))
                # Set the item in the appropriate cell of the table
                self.ui.tableWidget.setItem(row_num, col_num, item)

# fonction de ajout de stock
    def stockStorage(self):
        try:# Get data from your widgets
            id_Commande = 0
            date = self.ui.dateEdit_2.date().toPyDate()
            type = self.ui.typeLine.currentText()
            stockglobal = float(self.ui.stockInitialLine.text())         
            connection = sqlite3.connect('bgblast.db')  
            cursor = connection.cursor()
            # Execute the SELECT query to get the last commande from the 'stock' table with the type that you wanna add stock to
            cursor.execute('''
                SELECT id_Commande,stock_global,stock_actuel from stock WHERE type = ?  ORDER BY id_Commande DESC LIMIT 1''',
                (type))
                # Fetch the result of the query
            result= cursor.fetchone()

            # Check if there was a commande was obtained
            if result[0]:
                cursor.execute('''
                    INSERT INTO stock (id_Commande, date, type, stock_global, stock_actuel)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (id_Commande, date, type, stockglobal+result[1], result[2]))
                self.show_Information("Ajout de stock", "Votre stock a été ajouté avec succés.")
                self.stockAffichage
            else:  
                cursor.execute('''
                INSERT INTO stock (id_Commande, date, type, stock_global, stock_actuel)
                VALUES (?, ?, ?, ?, ?)
                ''', (id_Commande, date, type, stockglobal, stockglobal))
                
                self.show_Information("Ajout de stock", "Votre stock a été ajouté avec succés.")
                self.stockAffichage
        except sqlite3.Error as e:
            print("SQLite Error:", str(e))
        except Exception as e:
            print("Unexpected Error:", str(e))
        finally: 
            connection.commit()
            connection.close()

                
    
            
# updates stock after a commmande  
    def updateStock(self):
        try:
            connection = sqlite3.connect('bgblast.db')  # Replace 'bgblast.db' with your desired database name
            cursor = connection.cursor()

            # Execute the SELECT query to get the last Commande done from the 'resultat' table
            cursor.execute(
                '''SELECT id_R, ammonix, tovex, A_E_I, detos_450, detos_500, reccords_17, reccords_25, reccords_42,
                reccords_65, reccords_100, ligne_tir FROM resultat ORDER BY id_R DESC LIMIT 1''')
            
            # Fetch the result of the query
            result = cursor.fetchone()
            
            # Extract the id_Commande from the result
            id_Commande = result[0]
            
            # Extract the date from the commande of those result
            cursor.execute(
                '''SELECT date FROM commande WHERE id_C = ?''', (id_Commande,))
            
            date = cursor.fetchone()[0]
            
            # Define the types
            types = ["Ammonix", "Tovex", "A.E.I", "Detos450ms", "Detos500ms", "Reccords17ms", "Reccords25ms", "Reccords42ms", "Reccords65ms", "Reccords100ms", "Ligne de tir"]
            
            for type_name in types:
                # Calculate the value to update stock_actuel based on the corresponding result column
                consomme = result[types.index(type_name) + 1]  # Skip the id_R column
                
                # Update the stock_actuel in the stock table for the specific type and id_Commande
                cursor.execute('''
                    INSERT INTO stock (id_Commande, date, type, stock_global, stock_actuel)
                    SELECT ?, ?, ?, stock_global, stock_actuel - ?
                    FROM stock
                    WHERE type = ? AND id_Commande = ?
                ''', (id_Commande, date, type_name, consomme, type_name, id_Commande))

            # Commit the changes to the database
            connection.commit()

        except sqlite3.Error as e:
            print("SQLite Error:", str(e))
        except Exception as e:
            print("Unexpected Error:", str(e))
        finally:
            connection.close()

                # Update the stock_actuel in the stock table for the specific type
        
    """ except sqlite3.Error as e:
            self.show_warning("SQLite Error", f"Error: {str(e)}")
        except Exception as e:
            self.show_warning( "Error", f"Unexpected Error: {str(e)}") """

    #fonction qui affiche tout les statistiques du stock
    def stockAffichage(self):
        # Assuming you have a database connection established as 'connection'
        cursor = connection.cursor()
        
        # Execute a query to fetch data from the 'commande' and 'resultat' tables
        cursor.execute('''
            SELECT id_Commande, date, type, stock_global, stock_actuel FROM stock ''')

        # Fetch all rows from the query result
        data = cursor.fetchall()

        # Clear the existing table content
        self.ui.Tableau_Stock.clearContents()


        # Set the number of rows in the table
        self.ui.Tableau_Stock.setRowCount(len(data))

        # Iterate through the data and populate the table
        for row_num, row_data in enumerate(data):
            for col_num, col_value in enumerate(row_data):
                # Create a QTableWidgetItem and set its text to the database value
                item = QtWidgets.QTableWidgetItem(str(col_value))
                # Set the item in the appropriate cell of the table
                self.ui.Tableau_Stock.setItem(row_num, col_num, item)
        connection.commit
#fonction qui affiche les statistiques du stock en specifiant la date
    def stockAffichageDate(self):
        date1 = self.ui.stockDate1.date().toPyDate()
        date2 = self.ui.stockDate2.date().toPyDate()

        connection = sqlite3.connect('bgblast.db')  # Replace 'bgblast.db' with your desired database name
        cursor = connection.cursor()

        cursor.execute('''
            SELECT id_Commande, date, type, stock_global, stock_actuel FROM stock WHERE date BETWEEN strftime('%Y-%m-%d', ?) AND strftime('%Y-%m-%d', ?) ORDER BY date
        ''', (date1, date2))

        # Fetch all rows that match the date range
        data = cursor.fetchall()

        if data:
            try:
                self.ui.Tableau_Stock.clearContents()
                self.ui.Tableau_Stock.setRowCount(len(data))

                for row_num, row_data in enumerate(data):
                    for col_num, col_value in enumerate(row_data):
                        item = QtWidgets.QTableWidgetItem(str(col_value))
                        self.ui.Tableau_Stock.setItem(row_num, col_num, item)

                connection.commit()

            except sqlite3.Error as e:
                self.show_warning("SQLite Error", f"Error: {str(e)}")
            except Exception as e:
                self.show_warning("Stock", f"Unexpected Error: {str(e)}")
        else:
            self.show_warning("Stock",  f"Unexpected Error: Aucune donnée trouvée pour la plage de dates spécifiée, réssayez! ")
#fonction qui affiche les statistiques du stock par spécifications des types
    def stockAffichageType(self):
        
        selected_types = []
        # Check which checkboxes are selected
        if self.ui.checkBox.isChecked():
            selected_types.append("Ammonix")
        if self.ui.checkBox_2.isChecked():
            selected_types.append("Tovex")
        if self.ui.checkBox_3.isChecked():
            selected_types.append("A.E.I")
        if self.ui.checkBox_4.isChecked():
            selected_types.append("Detos450ms")
        if self.ui.checkBox_5.isChecked():
            selected_types.append("Detos500ms")
        if self.ui.checkBox_7.isChecked():
            selected_types.append("Raccords17ms")
        if self.ui.checkBox_8.isChecked():
            selected_types.append("Raccords25ms")
        if self.ui.checkBox_9.isChecked():
            selected_types.append("Raccords42ms")
        if self.ui.checkBox_1.isChecked():
            selected_types.append("Raccords65ms")
        if self.ui.checkBox_10.isChecked():
            selected_types.append("Raccords100ms")
        if self.ui.checkBox_101.isChecked():
            selected_types.append("Ligne de tir")

        if not selected_types:
            self.show_warning("Stock", f" Filter Error : Veuillez sélectionner au moins un type.")
            return

        try:
            connection = sqlite3.connect('bgblast.db')  
            cursor = connection.cursor()
            
            # Use placeholders for the selected types in the query
            query = 'SELECT id_Commande, date, type, stock_global, stock_actuel FROM stock WHERE type IN ({})'.format(','.join('?' * len(selected_types)))

            # Execute the query with selected types
            cursor.execute(query, selected_types)

            data = cursor.fetchall()
            
            if data:
                self.ui.Tableau_Stock.clearContents()
                self.ui.Tableau_Stock.setRowCount(len(data))

                for row_num, row_data in enumerate(data):
                    for col_num, col_value in enumerate(row_data):
                        item = QtWidgets.QTableWidgetItem(str(col_value))
                        self.ui.Tableau_Stock.setItem(row_num, col_num, item)

                connection.commit()
            else:
                self.show_warning("Stock", f"Aucune donnée trouvée pour les types sélectionnés")

        except sqlite3.Error as e:
            self.show_warning("SQLite Error", f"Error: {str(e)}")
        except Exception as e:
            self.show_warning("Stock", f"Unexpected Error: {str(e)}")


    def show_warning(self, title, text):
        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        icon = QIcon("./images/icon.png")  
        message_box.setWindowIcon(icon)
        message_box.exec()
    
    def show_Information(self, title, text):
        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        icon = QIcon("./images/icon.png")  
        message_box.setWindowIcon(icon)
        message_box.exec()

    def menu_show(self):
        if self.ui.leftMenu.isHidden():
            self.ui.leftMenu.show()
        else:
                self.ui.leftMenu.hide()

    def hide_Options(self):
        if self.ui.stackedWidget_2.isVisible():
            self.ui.stackedWidget_2.hide()

    def show_Options(self):
        if self.ui.stackedWidget_2.isHidden():
            self.ui.stackedWidget_2.show() 

if __name__ == "__main__":
    connection = sqlite3.connect('bgblast.db')
    create_database()
    # Create the Qt application
    app = QApplication(sys.argv)
    # Create the main window
    main_window = my_app()

    # Show the main window
    main_window.show()

    sys.exit(app.exec())
    

       
   


"""

if __name__ == "__main__":
    # Call the function to create the database and table
    create_database()

    # Create the Qt application
    app = QApplication(sys.argv)

    # Create the login window
    login_window = Login()

    # Show the login window
    login_window.show()
    
    # Start the application event loop
    app.exec()

    # After the event loop ends (user logs in or closes the window), check if login was successful
    if login_window.login_successful== True:
        # quit the login wndow when login in if login is successful    

        # Create the main window
        main_window = my_app()

        # Show the main window
        main_window.show()

        sys.exit(app.exec())
   


def create_database():
    connection = sqlite3.connect('bgblast.db')  # Replace 'bgblast.db' with your desired database name
    cursor = connection.cursor()
    # Create the "user" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user 
                   (id_user INTEGER PRIMARY KEY,
                    name VARCHAR(50),
                    role VARCHAR(50),
                    username VARCHAR(50) ,
                    password VARCHAR(50))''')
    
    connection.commit()
    connection.close()


#def login :

         # Connect to the SQLite database
        connection = sqlite3.connect("bgblast.db")
        cursor = connection.cursor()

        # Retrieve user data from the database based on the entered username
        cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()

        if user_data is None:
            self.show_warning_message("Login", "Nom d'utilisateur Incorrect")
        elif user_data[1] != password:
            self.show_warning_message("Login", "Mot de passe Incorrect")
        else:
            self.login_successful = True
            login_window.close()

        # Close the database connection
        connection.close()

        import sqlite3

def register_user(username, password, name):
    # Connect to the SQLite database
    connection = sqlite3.connect("your_database.db")
    cursor = connection.cursor()

    # Define the data for the new user
    new_user = (username, password, name)

    try:
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", new_user)

        # Commit the changes
        connection.commit()
    except sqlite3.IntegrityError:
        # Handle the case where the username is already taken
        print("Username already exists!")

    # Close the database connection
    connection.close()



#Creation of the database
def create_database():
    connection = sqlite3.connect('bgblast.db')  # Replace 'bgblast.db' with your desired database name
    cursor = connection.cursor()
    
    # Create the "commande" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS commande 
                   (id_C INTEGER PRIMARY KEY,
                    date DATE,
                    type_tir VARCHAR(50),
                    mode_tir VARCHAR(50),
                    schema_tir VARCHAR(50),
                    mode_chargement VARCHAR(50),
                    machine_foration VARCHAR(50),
                    machine_decappage VARCHAR(50),
                    panneau VARCHAR(50),
                    tranche VARCHAR(50),
                    niveau VARCHAR(50),
                    nombre_trous INTEGER,
                    nombre_rangs INTEGER,
                    dosage_prevu REAL,
                    maille VARCHAR(50))''')
    
    # Create the "resultat" table with a foreign key reference
    cursor.execute('''CREATE TABLE IF NOT EXISTS resultat 
                   (id_R INTEGER PRIMARY KEY,
                    id_commande INTEGER,
                    longueur VARCHAR(50),
                    largeur DOUBLE,
                    surface DOUBLE,
                    volume DOUBLE,
                    ammonix DOUBLE,
                    tovex DOUBLE,
                    cordeau12g DOUBLE,
                    ligne_tir DOUBLE,
                    A_E_I DOUBLE,
                    metrage_fore DOUBLE,
                    reccords_17 DOUBLE,
                    reccords_25 DOUBLE,
                    reccords_42 DOUBLE,
                    reccords_65 DOUBLE,
                    reccords_100 DOUBLE,
                    repartition DOUBLE,
                    C_I DOUBLE,
                    detos_450 DOUBLE,
                    detos_500 DOUBLE,
                    bourage_final DOUBLE,
                    rendu_prevu DOUBLE,
                    FOREIGN KEY (id_commande) REFERENCES commande(id_C))''')
   
    # Create the "cout" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS cout 
                   (id_ct INTEGER PRIMARY KEY,
                    cout_initial INTEGER,
                    cout_actuel INTEGER,
                    type VARCHAR(50),
                   numero INTEGER)''')
    
    # Create the "user" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user 
                   (id_user INTEGER PRIMARY KEY,
                    name VARCHAR(50),
                    username VARCHAR(50) ,
                    password VARCHAR(50),
                    role VARCHAR(50))''')
    
    # Create the "client" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS client 
                   (id_d INTEGER PRIMARY KEY,
                    id_commande INTEGER,
                    machine VARCHAR(50),
                    pa,
                    FOREIGN KEY (id_commande) REFERENCES commande(id_C))''')

    connection.commit()
    connection.close()

# Call the function to create the tables
create_database()
"""