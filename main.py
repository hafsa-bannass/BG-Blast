import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMessageBox
from PyQt6 import QtCore
import sys
from mainwindow_ui import Ui_MainWindow
from login import Ui_LoginWindow
from PyQt6.QtGui import QIcon
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import subprocess
from PyQt6.QtWidgets import QFileDialog

import shutil
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter




class Login(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.usernameLineEdit.setText("")
        self.ui.passwordLineEdit.setText("")
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
    
    def show_Information(self, title, text):
        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        icon = QIcon("./images/icon.png")  
        message_box.setWindowIcon(icon)
        message_box.exec()   

    def login(self):
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()

        # Connect to the SQLite database
        connection = sqlite3.connect('bgblast.db')  # Replace with your actual database file
        cursor = connection.cursor()

        # Query the database for the username and password
        cursor.execute("SELECT username, password FROM user WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()  # Fetch the first matching row

        # Close the database connection
        connection.close()

        if result is not None:
            self.login_successful = True
            # Close the login window when login is successful
            self.close()  # Close the login window

            # Create and show the main window
            main_window = my_app()
            main_window.set_username_password(username, password)  # Pass the username and password
            self.usernameLineEdit.setText("")
            self.passwordLineEdit.setText("")

            main_window.show()
        else:
            self.show_warning("Login", "Nom d'utilisateur ou mot de passe incorrect")




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
                    ligne_tir DOUBLE,
                    A_E_I DOUBLE,
                    metrage_fore DOUBLE,
                    raccords_17 DOUBLE,
                    raccords_25 DOUBLE,
                    raccords_42 DOUBLE,
                    raccords_65 DOUBLE,
                    raccords_100 DOUBLE,
                    repartition DOUBLE,
                    C_I DOUBLE,
                    detos_450 DOUBLE,
                    detos_500 DOUBLE,
                    bourage_final DOUBLE,
                    rendu_prevu DOUBLE,
                    FOREIGN KEY (id_commande) REFERENCES commande(id_C))''')
   
    # Create the "stock" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock 
                   (id_ST INTEGER PRIMARY KEY,
                    id_Commande INTEGER,
                    date DATE,
                    type VARCHAR(50),
                    stock_global DOUBLE,
                    stock_actuel DOUBLE,
                    stock_consome DOUBLE,
                    FOREIGN KEY (id_Commande) REFERENCES resultat(id_R))''')
    
    # Create the "cout" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS cout
                   (id_CT INTEGER PRIMARY KEY,
                    id_Commande INTEGER,
                    date DATE,
                    type VARCHAR(50),
                    cout_global Double,
                    cout_actuel Double,
                    cout_consome DOUBLE,
                    FOREIGN KEY (id_Commande) REFERENCES resultat(id_R))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS apres_sautage 
                   (id_AS INTEGER PRIMARY KEY,
                    date Date,
                    heure1 VARCHAR(50),
                    heure2 VARCHAR(50),
                    blf_ammonix VARCHAR(50),
                    blf_tovex VARCHAR(50),
                    blf_artifice VARCHAR(50),
                    bs_ammonix VARCHAR(50),
                    bs_tovex_artifice VARCHAR(50),
                    type VARCHAR(50),
                    effectif VARCHAR(50),
                    vitesse VARCHAR(50),
                    son VARCHAR(50),
                    frequence VARCHAR(50),
                    observation VARCHAR(100))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS avanc_decap 
                   (id_AD INTEGER PRIMARY KEY,
                    avanc_Foration VARCHAR(50),
                    avanc_decap VARCHAR(50),
                    machine_decap VARCHAR(50))''')

    # Create the "user" table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user 
                   (id_user INTEGER PRIMARY KEY,
                    username VARCHAR(50) ,
                    password VARCHAR(50),
                    name VARCHAR(50),
                    Profession VARCHAR(50),
                    role VARCHAR(50),
                    direction VARCHAR(50),
                    entite VARCHAR(50),
                    organusme VARCHAR(50))''')
    # Insert initial users (if not already inserted)
    cursor.execute('SELECT id_user FROM user')
    existing_users = cursor.fetchall()

    if not existing_users:
        initial_users = [
            ('username1', 'password1', 'User 1', 'Agent Ocp', 'Admin', 'Mines Gantour', 'Sautage de Ben Guerir', 'Ocp'),
            ('username2', 'password2', 'User 2', 'Agent Ocp', 'Admin', 'Mines Gantour', 'Sautage de Ben Guerir', 'Ocp'),
            ('username3', 'password3', 'User 3', 'Agent Ocp', 'User', 'Mines Gantour', 'Sautage de Ben Guerir', 'Ocp'),
            ('username4', 'password4', 'User 4', 'Agent Ocp', 'Admin', 'Mines Gantour', 'Sautage de Ben Guerir', 'Ocp'),
            ('username5', 'password5', 'User 5', 'Agent Ocp', 'Admin', 'Mines Gantour', 'Sautage de Ben Guerir', 'Ocp'),
            ('username6', 'password6', 'User 6', 'Agent Ocp', 'Admin', 'Mines Gantour', 'Sautage de Ben Guerir', 'Ocp'),
            # Add more users as needed
        ]

        cursor.executemany('''
            INSERT INTO user (username, password, name, Profession, role, direction, entite, organusme)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', initial_users)
    
    connection.commit()
    connection.close()
    
    # Create the "client" table
   

   

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


        self.ui.TbBtn.clicked.connect(self.tableauBord)



        self.ui.GesComBtn.clicked.connect(self.show_Options)   

        self.ui.calculBtn.clicked.connect(self.calculations)   
        self.ui.resetBtnFs.clicked.connect(self.resetCommande)

        self.ui.valResBtn.clicked.connect(self.saveResultats)
        self.ui.valResBtn.clicked.connect(self.showButtons)
        self.ui.genResBtn.clicked.connect(self.fetch_data)
        # self.ui.suppResBtn.clicked.connect(self.deleteCommandeResultat)
        self.ui.retourResBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Commandes_calcul),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Commande_Calcul)
        ))


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
        #Gestion du stock 
        self.ui.ajouStockBtn.clicked.connect(self.stockStorage)
        self.ui.stockAllBtn.clicked.connect(self.stockAffichage)    
        self.ui.stockDateBtn.clicked.connect(self.stockAffichageDate)    
        self.ui.stockArtBtn.clicked.connect(self.stockAffichageType)



        self.ui.GesCoutBtN.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Cout),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Cout)
        ))
        self.ui.GesCoutBtN.clicked.connect(self.show_Options)     
        self.ui.GesCoutBtN.clicked.connect(self.coutAffichage)   
        self.ui.ajouCoutBtn.clicked.connect(self.coutStorage)
        self.ui.coutAllBtn.clicked.connect(self.coutAffichage)
        self.ui.coutDateBtn.clicked.connect(self.coutAffichageDate)    
        self.ui.coutArtBtn.clicked.connect(self.coutAffichageType)



        self.ui.GesASBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Apres_Sautage),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Apres_Sautage)
        ))
        self.ui.GesASBtn.clicked.connect(self.show_Options)  
        

        self.ui.saveApresSautageBtn.clicked.connect(self.saveApresSautage)
        self.ui.saveApresSautageBtn.clicked.connect(self.showBtns)

        self.ui.resetApresSautageBtn.clicked.connect(self.resetApresSautage)
        self.ui.deleteApresSautageBtn.clicked.connect(self.deleteApresSautage)
        self.ui.pushButton_13.clicked.connect(self.createPdfAS)


        self.ui.GesADBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Avan_Decapage),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Avan_decapage)
        ))
        self.ui.GesADBtn.clicked.connect(self.show_Options)  
        self.ui.GesADBtn.clicked.connect(self.showAvancDecap)  

        self.ui.ajouterBtn.clicked.connect(self.saveAvancDecap)
        self.ui.avDecForBtn.clicked.connect(self.showAvancFD)    
        self.ui.avdecAllBtn.clicked.connect(self.showAvancDecap)    
        self.ui.avdecArtBtn.clicked.connect(self.showAvancMach)    

        '''self.ui.documBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Documentation),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Docummentation)
        ))
        self.ui.documBtn.clicked.connect(self.show_Options)  ''' 


        self.ui.archiveBtn.clicked.connect(self.show_Options)     
        self.ui.archiveBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives)
        ))
        
        
            

        self.ui.historiqueCommandeBtn.clicked.connect(self.show_Options) 
        self.ui.historiqueCommandeBtn.clicked.connect(self.hisCommandeResulat)  
        self.ui.historiqueCommandeBtn.clicked.connect(lambda:(
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Com_Avan),
            self.ui.Title.setText("Historique des Commandes")
        ))

        self.ui.historiqueStockBtn.clicked.connect(self.show_Options)  
        self.ui.historiqueStockBtn.clicked.connect(self.hisStock)           
        self.ui.historiqueStockBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Stock),
            self.ui.Title.setText("Historique Gestin des Stocks")
        ))
    

        self.ui.historiqueCoutBtn.clicked.connect(self.show_Options)   
        self.ui.historiqueCoutBtn.clicked.connect(self.hisCout)       
        self.ui.historiqueCoutBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Cout),
            self.ui.Title.setText("Historique Gestion des Couts")
        ))

        self.ui.historiqueAvDcpBtn.clicked.connect(self.show_Options)     
        self.ui.historiqueAvDcpBtn.clicked.connect(self.hisAD)       
        self.ui.historiqueAvDcpBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Avan_decapage),
            self.ui.Title.setText("Historique Avant Décapage")
        ))

        self.ui.historiqueApSautBtn.clicked.connect(self.show_Options)     
        self.ui.historiqueApSautBtn.clicked.connect(self.hisAs)     
        self.ui.historiqueApSautBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_AS),
            self.ui.Title.setText("Historique Après Sautage")
        ))
        self.ui.logoutBtn.clicked.connect(self.logout)


    def set_username_password(self, username, password):
        
        # Connect to the SQLite database
        connection = sqlite3.connect('bgblast.db')  # Replace with your actual database file
        cursor = connection.cursor()

        # Query the database for user information based on the provided username and password
        cursor.execute("SELECT name, Profession, role, direction, entite, organusme FROM user WHERE username = ? AND password = ?", (username, password))
        user_info = cursor.fetchone()  # Fetch the first matching row

        # Close the database connection
        connection.close()

        # Display user information in your UI (replace with actual UI elements)
        name, profession, role, direction, entite, organisme = user_info
        self.ui.o22.setText(name)
        self.ui.o23.setText(profession)
        self.ui.o24.setText(role)
        self.ui.o25.setText(direction)
        self.ui.o26.setText(entite)
        self.ui.o27.setText(organisme)
       


    def showButtons(self):
        self.ui.genResBtn.show()

        self.ui.retourResBtn.show()     
    def showBtns(self):
        self.ui.deleteApresSautageBtn.show()
        self.ui.pushButton_13.show()

    def tableauBord(self):
        #types=["Ammonix","Tovex","A.E.I","Detos450ms","Detos500ms","Raccords17ms","Raccords25ms","Raccords42ms","Raccords65ms","Raccords100ms","Ligne de tir"]

        try:
            connection = sqlite3.connect('bgblast.db')  
            cursor = connection.cursor()
            
            # Use placeholders for the selected types in the query
            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("Ammonix",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_70.setText(str(rows[0]))
                self.ui.label_71.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_70.setText("0")
                self.ui.label_71.setText("0")
            

            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("Tovex",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_60.setText(str(rows[0]))
                self.ui.label_61.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_60.setText("0")
                self.ui.label_61.setText("0")



            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("aei",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_65.setText(str(rows[0]))
                self.ui.label_66.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_65.setText("0")
                self.ui.label_66.setText("0")


            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("Ligne de tir",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_81.setText(str(rows[0]))
                self.ui.label_82.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_81.setText("0")
                self.ui.label_82.setText("0")


            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("Raccords17ms",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_76.setText(str(rows[0]))
                self.ui.label_77.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_76.setText("0")
                self.ui.label_77.setText("0")


            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("Raccords25ms",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_84.setText(str(rows[0]))
                self.ui.label_85.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_84.setText("0")
                self.ui.label_85.setText("0")


            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("Raccords42ms",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_871.setText(str(rows[0]))
                self.ui.label_861.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_871.setText("0")
                self.ui.label_861.setText("0")
            

            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("Raccords65ms",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_90.setText(str(rows[0]))
                self.ui.label_91.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_90.setText("0")
                self.ui.label_91.setText("0")


            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("Raccords100ms",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_93.setText(str(rows[0]))
                self.ui.label_94.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_93.setText("0")
                self.ui.label_94.setText("0")
            
            
            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("Detos450ms",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_96.setText(str(rows[0]))
                self.ui.label_97.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_96.setText("0")
                self.ui.label_97.setText("0")

            query = 'SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1'
            cursor.execute(query, ("Detos500ms",))
    
            # Fetch the results for the current type
            rows = cursor.fetchone()
            print(rows)
            if rows:
                self.ui.label_99.setText(str(rows[0]))
                self.ui.label_100.setText(str(rows[1]))
                connection.commit()
            else:
                self.ui.label_99.setText("0")
                self.ui.label_100.setText("0")
            connection.commit()
        except sqlite3.Error as e:
            self.show_warning("SQLite Error", f"Error: {str(e)}")
        except Exception as e:
            self.show_warning("Stock", f"Unexpected Error: {str(e)}")



    def resetCommande (self):
        # Reset the first QComboBox
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
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

        # Connect the warning message outside of the loop
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

                # Database operations
                # Connect to the SQLite database
                connection = sqlite3.connect('bgblast.db')
                cursor = connection.cursor()
                cursor.execute('''SELECT date, type_tir, mode_tir, schema_tir, mode_chargement, machine_foration,
                                machine_decappage, panneau, tranche, niveau, profondeur, nombre_trous, nombre_rangs, nombre_trousrang,
                                maille, dosage_prevu FROM commande ORDER BY id_C DESC LIMIT 1''')
                result=cursor.fetchone()
                # Insert data into the "commande" table
                if result is None:
                
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
                    print("result saved ")
            
                    connection.commit()
                    connection.close() 
#str(result[0]) == date
                elif result[0]==date and result[1]== zoneTir and result[2]== modeTir and result[3]== schemaTir and result[4]== modeCharg and result[5]== machineForation and result[6]== machineDecapage and result[7]==panneau and result[8]==tranche and result[9]== niveau and result[10]== profondeur and result[11]== nbrTrous and result[12]== nbrRang and result[13]== nbrTrousRange and result[14]==maille_combined and result[15]== dosagePrevu:   
                    print("result not saved ")
                    self.show_warning("Fiche des saisie", "Cette commanede est déjà faite!")
                    return 
                elif result !=[date, zoneTir, modeTir, schemaTir, modeCharg, machineForation, machineDecapage, panneau,
                    tranche, niveau, profondeur, nbrTrous, nbrRang, nbrTrousRange,maille_combined, dosagePrevu]:
                
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
                    print("result saved ")

                    connection.commit()
                    connection.close() 
            except ValueError:
                # Show a warning message only once                
        
                self.show_warning("Fiche de saisie", " Tous les champs doivent être remplis et valides, réssayez ")       
                return
            self.valid_inputs= True
   
        #proceed with calculations
        if self.valid_inputs == True:        
            #operations 
            longueur= maille1*nbrTrousRange
            largeur= maille2*nbrRang
            surface = longueur*largeur
            volume = surface*profondeur
            #Quantité Ammonix
            ammonix = dosagePrevu*profondeur * maille1 * maille2 * nbrTrous # 
            ammonix = ammonix if ammonix % 25 == 0 else (int( ammonix / 25) + 1) * 25
            #Quantité tovex
            tovex = nbrTrous/2
            tovex = tovex if tovex % 25 == 0 else (int(tovex / 25) + 1) * 25
            cordeau = 0
            ligneTir = 500
            aei = 1
            metrageFore = nbrTrous*profondeur
            repartition = (ammonix/nbrTrous)*25 
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
                raccords17 = (nbrTrous - ( nbrRang +2))+2
                raccords25 = nbrRang + 2
                raccords42 = nbrRang + 2
                raccords65 = 0
                raccords100 = 0
            elif schemaTir=="17ms,25ms,42ms,65ms":
                raccords17 = (nbrTrous - ( nbrRang +2) )+2
                raccords25 = nbrRang + 2
                raccords42 = nbrRang + 2
                raccords65 = nbrRang + 2
                raccords100 = 0
            elif schemaTir=="17ms,25ms":
                raccords17 = (nbrTrous - ( nbrRang +2) )+2
                raccords25 = nbrRang + 2
                raccords42 = 0
                raccords65 = 0
                raccords100 = 0
            elif schemaTir=="17ms,100ms":
                raccords17 = (nbrTrous - ( nbrRang +2) )+2
                raccords25 = 0
                raccords42 = 0
                raccords65 = 0
                raccords100 = nbrTrousRange
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
            self.ui.o11.setText(str(raccords25))
            self.ui.o12.setText(str(raccords42))
            self.ui.o13.setText(str(raccords65))
            self.ui.o14.setText(str(raccords17))
            self.ui.o15.setText(str(repartition))
            self.ui.o16.setText(str(renduPrevu))
            self.ui.o19.setText(str(bourrageFinal))
            self.ui.o20.setText(str(ci)) 
            self.ui.o21.setText(str(raccords100))
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Commandes_resultats)
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Commande_Resultats)
                
# fonction d'enregistrement des resultats dans la db
    def saveResultats (self):
        longueur = self.ui.o1.text()
        largeur = self.ui.o2.text()
        surface = self.ui.o3.text()
        volume=self.ui.o4.text()
        Ammonix =self.ui.o5.text()
        Tovex=self.ui.o6.text()
        cordeau=self.ui.o7.text()
        Ligne_de_tir=self.ui.o8.text()
        aei=self.ui.o9.text()
        metrageFore=self.ui.o10.text()
        Detos450ms=self.ui.o17.text()
        Detos500ms=self.ui.o18.text()
        Raccords25ms=self.ui.o11.text()
        Raccords42ms=self.ui.o12.text()
        Raccords65ms=self.ui.o13.text()
        Raccords17ms=self.ui.o14.text()
        repartition=self.ui.o15.text()
        renduPrevu=self.ui.o16.text()
        bourrageFinal=self.ui.o19.text()
        ci=self.ui.o20.text() 
        Raccords100ms=self.ui.o21.text()
        
        try :   
            # Connect to the SQLite database
            connection = sqlite3.connect('bgblast.db')
            cursor = connection.cursor()
            # Execute the SELECT query to get the last id_C
            cursor.execute('''SELECT id_C, date FROM commande ORDER BY id_C DESC LIMIT 1''')
            # Fetch the result of the query
            Com = cursor.fetchone()

            # Check if a result was obtained
            if Com:
                cursor.execute('''SELECT id_commande FROM resultat ORDER BY id_commande DESC LIMIT 1''')
                # Fetch the result of the query
                id_comm = cursor.fetchone()

                if id_comm is not None and id_comm[0]==Com[0]:
                    self.show_warning("Fiche des résultats", "Ces résultats sont déjà enregistrés!")
                else:
                # Extract the id_C value from the result
                    id_commande = Com[0]
                    # Insert data into the "resultat" table with the corresponding id_commande
                    cursor.execute('''
                        INSERT INTO resultat (id_commande, longueur, largeur, surface, volume, ammonix, tovex, cordeau12g, 
                                            ligne_tir, A_E_I, metrage_fore, raccords_17, raccords_25, raccords_42, raccords_65, 
                                            raccords_100, repartition, C_I, detos_450, detos_500, bourage_final, rendu_prevu)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        id_commande, longueur, largeur, surface, volume, Ammonix, Tovex, cordeau, Ligne_de_tir, aei, metrageFore,
                        Raccords17ms, Raccords25ms, Raccords42ms, Raccords65ms, Raccords100ms, repartition, ci, Detos450ms, Detos500ms,
                        bourrageFinal, renduPrevu
                    ))

                    try:
                        # updates stock after a commmande  
                        date = Com[1] 
                        values = [ Ammonix, Tovex, aei, Detos450ms, Detos500ms, Raccords17ms, Raccords25ms, Raccords42ms, Raccords65ms, Raccords100ms, Ligne_de_tir]
                        types = ["Ammonix", "Tovex", "aei", "Detos450ms", "Detos500ms", "Raccords17ms", "Raccords25ms", "Raccords42ms", "Raccords65ms", "Raccords100ms", "Ligne de tir"]
                        for typename in types:
                            cursor.execute('''
                                SELECT stock_global, stock_actuel, stock_consome FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1
                            ''', (typename,))
                            # Fetch the result of the query
                            result= cursor.fetchone()
                            SG = float(result[0])
                            SA= float(result[1]) - float(values[types.index(typename)])
                            SC= float(values[types.index(typename)])
                            cursor.execute(''' INSERT INTO stock(id_Commande, date, type, stock_global, stock_actuel, stock_consome) 
                                VALUES(?, ?, ?, ?, ?, ?)''', (id_commande, date, typename, SG, SA, SC))  
                                   
                    except sqlite3.Error as e:
                        print("SQLite Error:", str(e))
                        self.show_warning("Fiche des résultats", "Une erreur s'est produite lors de l'enregistrement des données.")
                    except Exception as e:
                        print("Unexpected Error:", str(e))
                                # Commit the changes to the database
                    
                    try:
                        # Updates cout after a commmande
                        print ("Ss")
                        date = Com[1]
                        values = [Ammonix, Tovex, aei, Detos450ms, Detos500ms, Raccords17ms, Raccords25ms, Raccords42ms, Raccords65ms, Raccords100ms, Ligne_de_tir]
                        types = ["Ammonix", "Tovex", "aei", "Detos450ms", "Detos500ms", "Raccords17ms", "Raccords25ms", "Raccords42ms", "Raccords65ms", "Raccords100ms", "Ligne de tir"]
                        sommeG= 0 #Somme des couts globals 
                        sommeA= 0 #Somme des couts restantes 
                        sommeC= 0 #Somme des couts consomés 
                        print ("pp")
                        for typename in types:
                            print ( "DEbut " ," ", sommeG ," ", sommeA ," ", sommeC)
                            cursor.execute('''
                                SELECT cout_global, cout_actuel FROM cout WHERE type = ? ORDER BY id_CT DESC LIMIT 1
                            ''', (typename,))
                            # Fetch the result of the query
                            result = cursor.fetchone()
                             # Calculate the adjustment factor based on the typename
                            if typename is not None and ( typename == "Ammonix" or typename == "Tovex"):
                                adjustment_factor = 11
                            elif typename == "aei":
                                adjustment_factor = 0.8
                            elif typename == "Detos450ms" or typename == "Detos500ms":
                                adjustment_factor = 79
                            elif typename in ["Raccords17ms", "Raccords25ms", "Raccords42ms", "Raccords65ms", "Raccords100ms"]:
                                adjustment_factor = 73
                            elif typename == "Ligne de tir":
                                adjustment_factor = 0.5
                            else:
                                adjustment_factor = 0  # Handle cases where typename doesn't match any condition

                            # Perform the calculation and update the database
                            CG = float(result[0])
                            CA = float(result[1]) - (adjustment_factor * float(values[types.index(typename)]))
                            CC= (adjustment_factor * float(values[types.index(typename)]))
                            sommeG= sommeG+ CG #Somme des couts initials
                            sommeA= sommeA+ CA #Somme des couts restantes 
                            sommeC= sommeC + CC #Somme des couts consomé
                            print ("calcul"," ", sommeG ," ", sommeA ," ", sommeC)
                            cursor.execute(''' INSERT INTO cout(id_Commande, date, type, cout_global, cout_actuel, cout_consome )
                                VALUES(?, ?, ?, ?, ?, ?)''', (id_commande, date, typename, CG, CA, CC))
                        cursor.execute(''' INSERT INTO cout(id_Commande, date, type, cout_global, cout_actuel, cout_consome )
                                VALUES(?, ?, ?, ?, ?, ?)''', (id_commande, date, "Somme", sommeG, sommeA, sommeC))
                        print (" fin", " ",sommeG ," ", sommeA ," ", sommeC)
                    except sqlite3.Error as e:
                        print("SQLite Error:", str(e))
                        self.show_warning("Cout", "Une erreur s'est produite lors de l'enregistrement des données.")
                    except Exception as e:
                        print(" cout Error:", str(e))

                    connection.commit()
                    connection.close()
                    self.show_Information("Fiche des résultats", "Résultats bien enregistrées ")
        except sqlite3.Error as e:
            # Print the specific error message
            print("SQLite error:", e)
            self.show_warning("Fiche des résultats", "Une erreur s'est produite lors de l'enregistrement des données.")
        except Exception as e:
            # Print any other unexpected exceptions
            print("Unexpected error:", e)
            self.show_warning("Fiche des résultats", "Une erreur inattendue s'est produite.")

# fonction de ajout de stock
    def hisCommandeResulat(self):
        
        connection = sqlite3.connect('bgblast.db')
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
                r.raccords_17, r.raccords_25, r.raccords_42, r.raccords_65,
                r.raccords_100, r.repartition, r.C_I, r.detos_450, r.detos_500,
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

    """ def deleteCommandeResultat(self):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('bgblast.db')
            cursor = connection.cursor()

            cursor.execute('''
                SELECT id_C FROM commande ORDER BY id_C DESC LIMIT 1  ''')
            row_id = cursor.fetchone()
            # Delete the row from the "commande" table
            cursor.execute('DELETE FROM commande WHERE id_C = ?', (row_id[0],))
            # Check if the row exists based on input values in the "resultat" table
            cursor.execute('SELECT id_commande FROM resultat WHERE id_commande = ?', (row_id[0],))
            id= cursor.fetchone()
            if id is not None: 
                # Delete the corresponding row from the "resultat" table
                cursor.execute('DELETE FROM resultat WHERE id_commande = ?', (row_id[0],))
                self.show_Information("Suppression de ligne", "La ligne a été supprimée avec succès.")

            connection.commit()
            self.show_Information("Suppression de ligne", "La ligne a été supprimée avec succès.")
            
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Commandes_calcul)
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Commande_Calcul)

        except sqlite3.Error as e:
            # Handle any database-related errors here
            self.show_warning("Suppression de ligne", "Une erreur s'est produite lors de la suppression : " + str(e))

        finally:
            if connection:
                connection.close()
    """
    
    def fetch_data(self):
        # Replace with your database connection code
        connection = sqlite3.connect('bgblast.db')
        cursor = connection.cursor()

        
        filename = "commande.pdf"  # Provide the desired filename
        title = "Gestion des commandes: Fiche de saisie"  # Specify the title
        title2 = "Gestion des commandes: Fiche des résultats"  # Specify the title
        conteur= 0
        
        cursor.execute('''SELECT date, type_tir, mode_tir, schema_tir, mode_chargement, machine_foration,
                                machine_decappage, panneau, tranche, niveau, profondeur, nombre_trous, nombre_rangs, nombre_trousrang,
                                maille, dosage_prevu FROM commande ORDER BY id_C DESC LIMIT 1''')
        result=cursor.fetchone()
        
        
        data = {
            "Date:": result[0],
            "Type de tir:": result[1],
            "Mode de tir:": result[2],
            "Schéma de tir:": result[3],
            "Mode de chargement:": result[4],
            "Machine de foration:": result[5],
            "Machine de décapage:": result[6],
            "Panneau:": result[7],
            "Tranche:": result[8],
            "Niveau:": result[9],
            "Profondeur": result[10],
            "Nombre de trous:": result[11],
            "Nombre de rangs:": result[12],
            "Nombre de trous par rang:": result[13],
            "Maille:": result[14],
            "Dosage prévu:": result[15],
            "Longueur/m:": self.ui.o1.text(),
            "Largeur:": self.ui.o2.text(),
            "Surface:": self.ui.o3.text(),
            "Volume:": self.ui.o4.text(),
            "Ammonix/kg:": self.ui.o5.text(),
            "Tovex/kg:": self.ui.o6.text(),
            "Cordeau:": self.ui.o7.text(),
            "Ligne de tir:": self.ui.o8.text(),
            "Aei/U:": self.ui.o9.text(),
            "Métrage Fore:": self.ui.o10.text(),
            "Detos 450ms/U:": self.ui.o17.text(),
            "Detos 500ms/U:": self.ui.o18.text(),
            "Raccords 17ms/U:": self.ui.o14.text(),
            "Raccords 25ms/U:": self.ui.o11.text(),
            "Raccords 42ms/U:": self.ui.o12.text(),
            "Raccords 65ms/U:": self.ui.o13.text(),
            "Raccords 100ms/U:": self.ui.o21.text(),
            "Répartition:": self.ui.o15.text(),
            "Rendu Prévu:": self.ui.o16.text(),
            "Bourrage Final:": self.ui.o19.text(),
            "Ci:": self.ui.o20.text() 
        }

        c = canvas.Canvas(filename, pagesize=letter)

        def start_new_page():
            c.showPage()  # Start a new page
            # Add page-specific content (e.g., header or footer) here

        # Draw the first picture (replace 'path_to_picture1' with the actual file path)
        c.drawImage('./images/logosautage.png', 500, 680, width=72, height=80)

        # Draw the second picture (replace 'path_to_picture2' with the actual file path)
        c.drawImage('./images/ocp.jpg', 100, 680, width=63, height=80)

        # Set the font to bold (Helvetica-Bold) and specify the font size for the title
        c.setFont("Helvetica-Bold", 14)
        c.drawString(190, 650, title)
        # Add the specified text
        c.setFont("Helvetica-Bold", 10)
        c.drawString(180, 750, "DIRECTION INDUSTRIELLES MINES GANTOUR")
        c.drawString(180, 735, "SAUTAGE DE BENGUERIR")
        c.drawString(180, 720, "GROUP OCP")


        # Initialize y-coordinate for data
        y = 600

        # Iterate over the data and labels to display them in the PDF
        label_x = 100  # x-coordinate for labels
        data_x = 300  # x-coordinate for data

        for label, value in data.items():
            c.setFont("Helvetica-Bold", 12)
            c.drawString(label_x, y, label)
            c.setFont("Helvetica", 12)
            value_str = str(value) 
            c.drawString(data_x, y, value_str) # Convert value to string
            y -= 25
            conteur = conteur +1
            # Check if there is enough space for the text, start a new page if not
            if conteur == 16:
                start_new_page()
                # Draw the first picture (replace 'path_to_picture1' with the actual file path)
                c.drawImage('./images/logosautage.png', 500, 680, width=72, height=80)

                # Draw the second picture (replace 'path_to_picture2' with the actual file path)
                c.drawImage('./images/ocp.jpg', 100, 680, width=63, height=80)

                # Set the font to bold (Helvetica-Bold) and specify the font size for the title
                c.setFont("Helvetica-Bold", 14)
                c.drawString(190, 650, title2)
                # Add the specified text
                c.setFont("Helvetica-Bold", 10)
                c.drawString(180, 750, "DIRECTION INDUSTRIELLES MINES GANTOUR")
                c.drawString(180, 735, "SAUTAGE DE BENGUERIR")
                c.drawString(180, 720, "GROUP OCP")
                

                y = 600  # Reset y-coordinate for the new page
                label_x = 100  # x-coordinate for labels
                data_x = 300  # x-coordinate for data

        
        # Save the PDF file
        c.save()

        # Prompt the user to choose the save path for the PDF file
        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")

        if save_path:
            shutil.move(filename, save_path)  # Move the generated PDF to the chosen location
            self.show_Information("PDF Generated","Votre PDF a été généré et enregistré à l'emplacement choisi avec succès!")

        

# fonction de ajout de stock
    def stockStorage(self):
        try:
            # Get data from your widgets
            id_Commande = 0
            date = self.ui.dateEdit_2.date().toPyDate()
            type = self.ui.typeLine.currentText()
            stockglobal = float(self.ui.stockInitialLine.text())
            
            connection = sqlite3.connect('bgblast.db')
            cursor = connection.cursor()
            cursor.execute('''
                SELECT stock_global, stock_actuel FROM stock WHERE type = ? ORDER BY id_ST DESC LIMIT 1
            ''', (type,))
            # Fetch the result of the query
            result = cursor.fetchone()

            if result:
                # If there's a result, use it to insert a new record
                cursor.execute('''
                    INSERT INTO stock (id_Commande, date, type, stock_global, stock_actuel, stock_consome)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (id_Commande, date, type, result[0]+stockglobal, result[1]+stockglobal, 0))  # Assuming result[0] contains the stock_actuel value
            else:
                # If there's no result, insert with a default value
                cursor.execute('''
                    INSERT INTO stock (id_Commande, date, type, stock_global, stock_actuel, stock_consome)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (id_Commande, date, type, stockglobal, stockglobal, 0))
            # Commit the changes to the database
            connection.commit()            
            self.show_Information("Ajout de stock", "Votre stock a été ajouté avec succès.")
            self.stockAffichage()
            connection.close()
                
        except sqlite3.Error as e:
            print("SQLite Error:", str(e))
        except Exception as e:
            if str(e) == "could not convert string to float: ''":
                self.show_warning("Ajout de stock", "Veuillez vérifier les données que vous avez saisit.")
            print("Unexpected Error:", str(e))
    #fonction qui affiche tout les statistiques du stock
    def stockAffichage(self):
        connection = sqlite3.connect('bgblast.db')
# Assuming you have a database connection established as 'connection'
        cursor = connection.cursor()
        
        # Execute a query to fetch data from the 'commande' and 'resultat' tables
        cursor.execute('''
            SELECT id_Commande, date, type, stock_global, stock_actuel, stock_consome FROM stock ''')

        # Fetch all rows from the query result
        data = cursor.fetchall()
        if data : 
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
        else :
            self.show_Information(" Gestion du Stock ", "Aucune donnée à afficher!")

        connection.commit
#fonction qui affiche les statistiques du stock en specifiant la date
    def stockAffichageDate(self):
        date1 = self.ui.stockDate1.date().toPyDate()
        date2 = self.ui.stockDate2.date().toPyDate()

        connection = sqlite3.connect('bgblast.db')  # Replace 'bgblast.db' with your desired database name
        cursor = connection.cursor()

        cursor.execute('''
            SELECT id_Commande, date, type, stock_global, stock_actuel, stock_consome FROM stock WHERE date BETWEEN strftime('%Y-%m-%d', ?) AND strftime('%Y-%m-%d', ?) ORDER BY date
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
            self.show_warning("Affichage du stock",  " Aucune donnée trouvée pour la plage de dates spécifiée, réssayez! ")
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
            query = 'SELECT id_Commande, date, type, stock_global, stock_actuel, stock_consome FROM stock WHERE type IN ({})'.format(','.join('?' * len(selected_types)))

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
                self.show_warning("Affichage du stock", "Aucune donnée trouvée pour les types sélectionnés")

        except sqlite3.Error as e:
            self.show_warning("SQLite Error", f"Error: {str(e)}")
        except Exception as e:
            self.show_warning("Stock", f"Unexpected Error: {str(e)}")

    def hisStock (self):
        
        connection = sqlite3.connect('bgblast.db')
          # Assuming you have a database connection established as 'connection'
        cursor = connection.cursor()
        
        # Execute a query to fetch data from the 'commande' and 'resultat' tables
        cursor.execute('''
            SELECT id_Commande, date, type, stock_global, stock_actuel, stock_consome FROM stock ''')

        # Fetch all rows from the query result
        data = cursor.fetchall()
        if data : 
            # Clear the existing table content
            self.ui.tableWidget_2.clearContents()

            # Set the number of rows in the table
            self.ui.tableWidget_2.setRowCount(len(data))

            # Iterate through the data and populate the table
            for row_num, row_data in enumerate(data):
                for col_num, col_value in enumerate(row_data):
                    # Create a QTableWidgetItem and set its text to the database value
                    item = QtWidgets.QTableWidgetItem(str(col_value))
                    # Set the item in the appropriate cell of the table
                    self.ui.tableWidget_2.setItem(row_num, col_num, item)
        else :
            self.show_Information(" Gestion du Stock ", "Aucune donnée à afficher!")

        connection.commit()
        connection.close()  



    def coutStorage(self):
        try:
            # Get data from your widgets
            id_Commande = 0
            date = self.ui.dateEditC.date().toPyDate()
            type = self.ui.typeLineC.currentText()
            coutglobal = float(self.ui.coutInitialLine.text())
            
            connection = sqlite3.connect('bgblast.db')
            cursor = connection.cursor()
            
            # Attempt to insert the cout record
            cursor.execute('''
                INSERT INTO cout (id_Commande, date, type, cout_global, cout_actuel, cout_consome)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id_Commande, date, type, coutglobal, coutglobal, 0))
            
            # Commit the changes to the database
            connection.commit()
            
            self.show_Information("Ajout de cout", "Vos cout a été ajouté avec succès.")
            self.coutAffichage()
            
        except sqlite3.Error as e:
            print("SQLite Error:", str(e))
        except Exception as e:
            print("Unexpected Error:", str(e))
        finally:
            connection.close()

    def coutAffichage(self):
        connection = sqlite3.connect('bgblast.db')
        # Assuming you have a database connection established as 'connection'
        cursor = connection.cursor()
        
        # Execute a query to fetch data from the 'cout' table
        cursor.execute('''
            SELECT id_Commande, date, type, cout_global, cout_actuel, cout_consome FROM cout ''')

        # Fetch all rows from the query result
        data = cursor.fetchall()
        if data:
            # Clear the existing table content
            self.ui.Tableau_Cout.clearContents()

            # Set the number of rows in the table
            self.ui.Tableau_Cout.setRowCount(len(data))

            # Iterate through the data and populate the table
            for row_num, row_data in enumerate(data):
                for col_num, col_value in enumerate(row_data):
                    # Create a QTableWidgetItem and set its text to the database value
                    item = QtWidgets.QTableWidgetItem(str(col_value))
                    # Set the item in the appropriate cell of the table
                    self.ui.Tableau_Cout.setItem(row_num, col_num, item)
        else: 
            self.show_Information(" Gestion du cout" ,"Aucune donnée à afficher!")

        connection.commit    
#fonction qui affiche les statistiques du cout en specifiant la date
    def coutAffichageDate(self):
        date1 = self.ui.coutDate1.date().toPyDate()
        date2 = self.ui.coutDate2.date().toPyDate()

        connection = sqlite3.connect('bgblast.db')  # Replace 'bgblast.db' with your desired database name
        cursor = connection.cursor()

        cursor.execute('''
            SELECT id_Commande, date, type, cout_global, cout_actuel, cout_consome FROM cout WHERE date BETWEEN strftime('%Y-%m-%d', ?) AND strftime('%Y-%m-%d', ?) ORDER BY date
        ''', (date1, date2))

        # Fetch all rows that match the date range
        data = cursor.fetchall()

        if data:
            try:
                # Clear the existing table content
                self.ui.Tableau_Cout.clearContents()
                # Set the number of rows in the table
                self.ui.Tableau_Cout.setRowCount(len(data))

                for row_num, row_data in enumerate(data):
                    for col_num, col_value in enumerate(row_data):
                        item = QtWidgets.QTableWidgetItem(str(col_value))
                        self.ui.Tableau_Cout.setItem(row_num, col_num, item)

                connection.commit()

            except sqlite3.Error as e:
                self.show_warning("SQLite Error", f"Error: {str(e)}")
            except Exception as e:
                self.show_warning("Cout", f"Unexpected Error: {str(e)}")
        else:
            self.show_warning("Cout",  "Aucune donnée trouvée pour la plage de dates spécifiée, réssayez! ")
        connection.close()  
#fonction qui affiche les statistiques du cout par spécifications des types    
    def coutAffichageType(self):
        
        selected_types = []
        # Check which checkboxes are selected
        if self.ui.checkBox_11.isChecked():
            selected_types.append("Ammonix")
        if self.ui.checkBox_12.isChecked():
            selected_types.append("Tovex")
        if self.ui.checkBox_13.isChecked():
            selected_types.append("A.E.I")
        if self.ui.checkBox_14.isChecked():
            selected_types.append("Detos450ms")
        if self.ui.checkBox_15.isChecked():
            selected_types.append("Detos500ms")
        if self.ui.checkBox_17.isChecked():
            selected_types.append("Raccords17ms")
        if self.ui.checkBox_18.isChecked():
            selected_types.append("Raccords25ms")
        if self.ui.checkBox_19.isChecked():
            selected_types.append("Raccords42ms")
        if self.ui.checkBox_20.isChecked():
            selected_types.append("Raccords65ms")
        if self.ui.checkBox_21.isChecked():
            selected_types.append("Raccords100ms")
        if self.ui.checkBox_22.isChecked():
            selected_types.append("Ligne de tir")

        if not selected_types:
            self.show_warning("Cout", "Veuillez sélectionner au moins un type.")
            return

        try:
            connection = sqlite3.connect('bgblast.db')  
            cursor = connection.cursor()
            
            # Use placeholders for the selected types in the query
            query = 'SELECT id_Commande, date, type, cout_global, cout_actuel, cout_consome FROM cout WHERE type IN ({})'.format(','.join('?' * len(selected_types)))

            # Execute the query with selected types
            cursor.execute(query, selected_types)

            data = cursor.fetchall()
            
            if data:
                self.ui.Tableau_Cout.clearContents()
                self.ui.Tableau_Cout.setRowCount(len(data))

                for row_num, row_data in enumerate(data):
                    for col_num, col_value in enumerate(row_data):
                        item = QtWidgets.QTableWidgetItem(str(col_value))
                        self.ui.Tableau_Cout.setItem(row_num, col_num, item)

                connection.commit()
                connection.close()  
            else:
                self.show_warning("Cout", "Aucune donnée trouvée pour les types sélectionnés")

        except sqlite3.Error as e:
            self.show_warning("SQLite Error", f"Error: {str(e)}")
        except Exception as e:
            self.show_warning("Cout", f"Unexpected Error: {str(e)}") 

    def hisCout(self):
        connection = sqlite3.connect('bgblast.db')
        # Assuming you have a database connection established as 'connection'
        cursor = connection.cursor()
        
        # Execute a query to fetch data from the 'cout' table
        cursor.execute('''
            SELECT id_Commande, date, type, cout_global, cout_actuel, cout_consome FROM cout ''')

        # Fetch all rows from the query result
        data = cursor.fetchall()
        if data:
            # Clear the existing table content
            self.ui.tableWidget_3.clearContents()

            # Set the number of rows in the table
            self.ui.tableWidget_3.setRowCount(len(data))

            # Iterate through the data and populate the table
            for row_num, row_data in enumerate(data):
                for col_num, col_value in enumerate(row_data):
                    # Create a QTableWidgetItem and set its text to the database value
                    item = QtWidgets.QTableWidgetItem(str(col_value))
                    # Set the item in the appropriate cell of the table
                    self.ui.tableWidget_3.setItem(row_num, col_num, item)
        else: 
            self.show_Information(" Gestion du cout" ,"Aucune donnée à affiche")
        
        connection.commit()
        connection.close()    



    def saveApresSautage(self):
        # Retrieve the text from QLineEdit widgets
        date = self.ui.dateEdit_3.date().toPyDate()
        heure1 = self.ui.timeEdit_3.time().toString()
        heure2 = self.ui.timeEdit_4.time().toString()
        blf_ammonix = self.ui.lineEdit_16.text()
        blf_tovex = self.ui.lineEdit_7.text()
        blf_artifice = self.ui.lineEdit_8.text()
        bs_ammonix = self.ui.lineEdit_9.text()
        bs_tovex_artifice = self.ui.lineEdit_10.text()
        type = self.ui.lineEdit_22.text()
        effectif = self.ui.lineEdit_12.text()
        vitesse = self.ui.lineEdit_13.text()
        son = self.ui.lineEdit_14.text()
        frequence = self.ui.lineEdit_11.text()
        observation = self.ui.lineEdit_15.text()

        # Check if any QLineEdit widget is empty
        if (not date or not heure1 or not heure2 or not blf_ammonix or not blf_tovex or
            not blf_artifice or not bs_ammonix or not bs_tovex_artifice or not type or
            not effectif or not vitesse or not son or not frequence or not observation):
            self.show_warning("Après Sautage", "Tous les champs doivent être remplis.")
            return  # Exit the function if any field is empty
        try:
            connection = sqlite3.connect('bgblast.db')
            cursor = connection.cursor()
            cursor.execute(''' 
                INSERT INTO apres_sautage (date, heure1, heure2, blf_ammonix, blf_tovex, blf_artifice, bs_ammonix, bs_tovex_artifice, type, effectif, vitesse, son, frequence, observation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (date, heure1, heure2, blf_ammonix, blf_tovex, blf_artifice, bs_ammonix, bs_tovex_artifice, type, effectif, vitesse, son, frequence, observation))
            connection.commit()
            connection.close()
            self.show_Information("Après Sautage", "Données enregistrées avec succès")
        except Exception as e:
            # Handle any exceptions (e.g., database errors)
            self.show_warning("Après Sautage", "Une erreur s'est produite lors de l'enregistrement : " + str(e))

    def resetApresSautage(self):
        # Reset the values of QLineEdit widgets
        self.ui.dateEdit_3.setDate(QtCore.QDate.currentDate())
        self.ui.timeEdit_3.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.timeEdit_4.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.lineEdit_16.setText("")
        self.ui.lineEdit_7.setText("")
        self.ui.lineEdit_8.setText("")
        self.ui.lineEdit_9.setText("")
        self.ui.lineEdit_10.setText("")
        self.ui.lineEdit_22.setText("")
        self.ui.lineEdit_12.setText("")
        self.ui.lineEdit_13.setText("")
        self.ui.lineEdit_14.setText("")
        self.ui.lineEdit_11.setText("")
        self.ui.lineEdit_15.setText("")

    def deleteApresSautage(self):
        # Retrieve input values
        date = self.ui.dateEdit_3.date().toPyDate()
        heure1 = self.ui.timeEdit_3.dateTime().toPyDateTime()
        heure2 = self.ui.timeEdit_4.dateTime().toPyDateTime()
        blf_ammonix = self.ui.lineEdit_16.text()
        blf_tovex = self.ui.lineEdit_7.text()
        blf_artifice = self.ui.lineEdit_8.text()
        bs_ammonix = self.ui.lineEdit_9.text()
        bs_tovex_artifice = self.ui.lineEdit_10.text()
        type = self.ui.lineEdit_22.text()
        effectif = self.ui.lineEdit_12.text()
        vitesse = self.ui.lineEdit_13.text()
        son = self.ui.lineEdit_14.text()
        frequence = self.ui.lineEdit_11.text()
        observation = self.ui.lineEdit_15.text()

        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('bgblast.db')
            cursor = connection.cursor()

            # Check if the row exists based on input values
            cursor.execute('''
                SELECT * FROM apres_sautage
                WHERE date = ? AND heure1 = ? AND heure2 = ? AND blf_ammonix = ? 
                    AND blf_tovex = ? AND blf_artifice = ? AND bs_ammonix = ?
                    AND bs_tovex_artifice = ? AND type = ? AND effectif = ?
                    AND vitesse = ? AND son = ? AND frequence = ? AND observation = ?
            ''', (date, heure1, heure2, blf_ammonix, blf_tovex, blf_artifice,
                bs_ammonix, bs_tovex_artifice, type, effectif, vitesse, son,
                frequence, observation))

            row = cursor.fetchone()

            if row is None:
                # If the row doesn't exist, display a message
                self.show_warning("Suppression de ligne", "La ligne n'existe pas dans la base de données.")
            else:
                # If the row exists, delete it from the database
                cursor.execute('''
                    DELETE FROM your_table_name
                    WHERE date = ? AND heure1 = ? AND heure2 = ? AND blf_ammonix = ? 
                        AND blf_tovex = ? AND blf_artifice = ? AND bs_ammonix = ?
                        AND bs_tovex_artifice = ? AND type = ? AND effectif = ?
                        AND vitesse = ? AND son = ? AND frequence = ? AND observation = ?
                ''', (date, heure1, heure2, blf_ammonix, blf_tovex, blf_artifice,
                    bs_ammonix, bs_tovex_artifice, type, effectif, vitesse, son,
                    frequence, observation))
                connection.commit()
                self.show_Information("Suppression de ligne", "La ligne a été supprimée avec succès.")

        except sqlite3.Error as e:
            # Handle any database-related errors here
            self.show_warning("Suppression de ligne", "Une erreur s'est produite lors de la suppression : " + str(e))

        finally:
            if connection:
                connection.close()

    def hisAs(self):
        connection = sqlite3.connect('bgblast.db')
        # Assuming you have a database connection established as 'connection'
        cursor = connection.cursor()
        
        # Execute a query to fetch data from the 'cout' table
        cursor.execute('''
            SELECT  date, heure1, heure2, blf_ammonix, blf_tovex, blf_artifice, bs_ammonix, bs_tovex_artifice, type, effectif, vitesse, son, frequence, observation FROM apres_sautage ''')

        # Fetch all rows from the query result
        data = cursor.fetchall()
        if data:
            # Clear the existing table content
            self.ui.tableWidget_4.clearContents()

            # Set the number of rows in the table
            self.ui.tableWidget_4.setRowCount(len(data))

            # Iterate through the data and populate the table
            for row_num, row_data in enumerate(data):
                for col_num, col_value in enumerate(row_data):
                    # Create a QTableWidgetItem and set its text to the database value
                    item = QtWidgets.QTableWidgetItem(str(col_value))
                    # Set the item in the appropriate cell of the table
                    self.ui.tableWidget_4.setItem(row_num, col_num, item)
        else: 
            self.show_Information("Après Sautage" ,"Aucune donnée à affiché")
        
        connection.commit()
        connection.close()    



    def saveAvancDecap(self):
        avancForation = self.ui.avancForationLine.text()
        machineDecap = self.ui.machineDecapLine.currentText()
        avancDecap = self.ui.avancDecapLine.text()

        if not avancForation or not machineDecap or not avancDecap:
            self.show_warning("Avancement décapage", "Tous les champs doivent être remplis.")
            return
        try:
            # Connectez-vous à la base de données SQLite
            connection = sqlite3.connect('bgblast.db')
            cursor = connection.cursor()

            # Insérez les données dans la table "avanc_decap"
            cursor.execute('''
                INSERT INTO avanc_decap (avanc_Foration, avanc_decap, machine_decap)
                VALUES (?, ?, ?)
            ''', (avancForation, avancDecap, machineDecap))

            # Committez les modifications dans la base de données
            connection.commit()
            print("Données enregistrées avec succès ")
            self.showAvancDecap()
            self.show_Information("Avancement Décapage","Données enregistrées avec succès!")

        except sqlite3.Error as e:
            # Gérez les erreurs liées à la base de données ici
            print("Une erreur s'est produite :", str(e))
            

        finally:
            if connection:
                connection.close()

    def showAvancDecap(self): 
        # Connectez-vous à la base de données SQLite
        connection = sqlite3.connect('bgblast.db')
        cursor = connection.cursor()

        # Exécutez la commande PRAGMA pour obtenir des informations sur les colonnes de la table "avanc_decap"
        cursor.execute(" select avanc_Foration, avanc_decap, machine_decap from avanc_decap")

        # Récupérez les informations sur les colonnes
        data = cursor.fetchall()
        if data:
            self.ui.Tableau_Avancement.clearContents()

            # Set the number of rows in the table
            self.ui.Tableau_Avancement.setRowCount(len(data))

            # Mettez à jour les en-têtes du tableau avec les noms des colonnes
            for row_num, row_data in enumerate(data):
                for col_num, col_value in enumerate(row_data):
                    # Create a QTableWidgetItem and set its text to the database value
                    item = QtWidgets.QTableWidgetItem(str(col_value))
                    # Set the item in the appropriate cell of the table
                    self.ui.Tableau_Avancement.setItem(row_num, col_num, item)
            
        else:
            self.show_Information("Avancement décapage","Aucune donnée à afficher!")

        connection.commit()
        connection.close()

    def showAvancMach(self):
        selected_types = []
        # Check which checkboxes are selected
        if self.ui.checkBox_42.isChecked():
            selected_types.append("7500M1")
        if self.ui.checkBox_43.isChecked():
            selected_types.append("7500M2")
        if self.ui.checkBox_44.isChecked():
            selected_types.append("PH1")
        if self.ui.checkBox_45.isChecked():
            selected_types.append("PH2")
        if self.ui.checkBox_46.isChecked():
            selected_types.append("ZD11")
        if self.ui.checkBox_48.isChecked():
            selected_types.append("EE")
        if not selected_types:
            self.show_warning("Avancement décapage","Aucune donnée à afficher!")
            return
        connection = sqlite3.connect('bgblast.db')  
        cursor = connection.cursor()
        
        # Use placeholders for the selected types in the query
        query = 'select avanc_Foration, avanc_decap, machine_decap from avanc_decap WHERE machine_decap IN ({})'.format(','.join('?' * len(selected_types)))

        # Execute the query with selected types
        cursor.execute(query, selected_types)

        data = cursor.fetchall()
        
        if data:
            self.ui.Tableau_Avancement.clearContents()
            self.ui.Tableau_Avancement.setRowCount(len(data))

            for row_num, row_data in enumerate(data):
                for col_num, col_value in enumerate(row_data):
                    item = QtWidgets.QTableWidgetItem(str(col_value))
                    self.ui.Tableau_Avancement.setItem(row_num, col_num, item)

            connection.commit()
        else:
            self.show_warning("Avancement décapage","Aucune donnée à afficher!")

    def showAvancFD(self):
    
        s1 = self.ui.avDecForBox.currentText()
        s2 = self.ui.avDecForLine.text()
        if not s1 or not s2:
            self.show_warning("Avancement décapage", "Veuillez spécifier un des paramètres")
            return
        elif s1 == "Avancement décapage":
            try:
                connection = sqlite3.connect('bgblast.db')
                cursor = connection.cursor()
                cursor.execute("SELECT avanc_Foration, avanc_decap, machine_decap FROM avanc_decap WHERE avanc_decap = ?", (s2,))
                data = cursor.fetchall()

                if data:
                    self.ui.Tableau_Avancement.clearContents()
                    self.ui.Tableau_Avancement.setRowCount(len(data))

                    for row_num, row_data in enumerate(data):
                        for col_num, col_value in enumerate(row_data):
                            item = QtWidgets.QTableWidgetItem(str(col_value))
                            self.ui.Tableau_Avancement.setItem(row_num, col_num, item)

                else:
                    self.show_warning("Avancement décapage", "Aucune donnée à afficher!")

                connection.commit()
                connection.close()

            except sqlite3.Error as e:
                self.show_warning("Erreur base de données", f"Erreur SQLite : {str(e)}")

        else:
            try:
                connection = sqlite3.connect('bgblast.db')
                cursor = connection.cursor()
                cursor.execute("SELECT avanc_Foration, avanc_decap, machine_decap FROM avanc_decap WHERE avanc_Foration = ?", (s2,))
                data = cursor.fetchall()

                if data:
                    self.ui.Tableau_Avancement.clearContents()
                    self.ui.Tableau_Avancement.setRowCount(len(data))

                    for row_num, row_data in enumerate(data):
                        for col_num, col_value in enumerate(row_data):
                            item = QtWidgets.QTableWidgetItem(str(col_value))
                            self.ui.Tableau_Avancement.setItem(row_num, col_num, item)

                else:
                    self.show_warning("Avancement décapage", "Aucune donnée à afficher!")

                connection.commit()
                connection.close()

            except sqlite3.Error as e:
                self.show_warning("Erreur base de données", f"Erreur SQLite : {str(e)}")

    def hisAD (self):
        # Connectez-vous à la base de données SQLite
        connection = sqlite3.connect('bgblast.db')
        cursor = connection.cursor()

        # Exécutez la commande PRAGMA pour obtenir des informations sur les colonnes de la table "avanc_decap"
        cursor.execute(" select avanc_Foration, avanc_decap, machine_decap from avanc_decap")

        # Récupérez les informations sur les colonnes
        data = cursor.fetchall()
        if data:
            self.ui.tableWidget_5.clearContents()

            # Set the number of rows in the table
            self.ui.tableWidget_5.setRowCount(len(data))

            # Mettez à jour les en-têtes du tableau avec les noms des colonnes
            for row_num, row_data in enumerate(data):
                for col_num, col_value in enumerate(row_data):
                    # Create a QTableWidgetItem and set its text to the database value
                    item = QtWidgets.QTableWidgetItem(str(col_value))
                    # Set the item in the appropriate cell of the table
                    self.ui.tableWidget_5.setItem(row_num, col_num, item)
            
        else:
            self.show_Information("Avancement décapage","Aucune donnée à afficher!")

        connection.commit()
        connection.close()





    def createPdfAS(self):
        filename = "Apres_Sautage.pdf"  # Provide the desired filename
        title = "Gestion Après Sautage"  # Specify the title

        # Collect user-entered data
        data = {
            "Date:": str(self.ui.dateEdit_3.date().toPyDate()),
            "Heure arrivée camion:": self.ui.timeEdit_3.time().toString(),
            "Heure de tir:": self.ui.timeEdit_4.time().toString(),
            "BLF Ammonix:": self.ui.lineEdit_16.text(),
            "BLF Tovex:": self.ui.lineEdit_7.text(),
            "BLF Artifice:": self.ui.lineEdit_8.text(),
            "BS Ammonix:": self.ui.lineEdit_9.text(),
            "BS Tovex Artifice:": self.ui.lineEdit_10.text(),
            "Type:": self.ui.lineEdit_22.text(),
            "Effectif:": self.ui.lineEdit_12.text(),
            "Vitesse(mm/s):": self.ui.lineEdit_13.text(),
            "Son(db):": self.ui.lineEdit_14.text(),
            "Fréquence:": self.ui.lineEdit_11.text(),
            "Observation:": self.ui.lineEdit_15.text(),
        }

        # Generate the PDF
        self.generate_pdf_with_data(filename, title, data)

    def generate_pdf_with_data(self, filename, title, data):
        try:
            c = canvas.Canvas(filename, pagesize=letter)
        
            # Draw the first picture (replace 'path_to_picture1' with the actual file path)
            c.drawImage('./images/logosautage.png', 500, 680, width=72, height=80)

            # Draw the second picture (replace 'path_to_picture2' with the actual file path)
            c.drawImage('./images/ocp.jpg', 100, 680, width=63, height=80)

            # Set the font to bold (Helvetica-Bold) and specify the font size for the title
            c.setFont("Helvetica-Bold", 14)
            c.drawString(230, 650, title)

            # Iterate over the data and labels to display them in the PDF
            y = 600  # Starting y-coordinate for data
            label_x = 100  # x-coordinate for labels
            data_x = 300  # x-coordinate for data
              # Set the font to bold (Helvetica-Bold) and specify the font size
            for label, value in data.items():
                c.setFont("Helvetica-Bold", 12)
                c.drawString(label_x, y, label)
                c.setFont("Helvetica", 12)
                c.drawString(data_x, y, value)
                y -= 25

            # Add the specified text
            c.setFont("Helvetica-Bold", 10)
            c.drawString(180, 750, "DIRECTION INDUSTRIELLES MINES GANTOUR")
            c.drawString(180, 735, "SAUTAGE DE BENGUERIR")
            c.drawString(180, 720, "GROUP OCP")
            c.showPage()
            c.save()

            # Prompt the user to choose the save path for the PDF file
            # Prompt the user to choose the save path for the PDF file

            save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")

            if save_path:
                shutil.move(filename, save_path)  # Move the generated PDF to the chosen location
                self.show_Information(self, "PDF Generated", f"PDF '{filename}' has been generated successfully and saved to the chosen location!")
        except Exception as e:
            print("generate_pdf_with_data", e)
            self.show_warning(self, "Error", f"An error occurred while generating the PDF: {str(e)}")



    def logout(self):
        confirm_logout = self.show_question("Confirmation", "Êtes-vous sûr de vouloir vous déconnecter ?")

        if confirm_logout == QMessageBox.StandardButton.Yes:
            # Clear user data and perform logout actions
            # For example:
            self.close()  # Close the main window
            login_window.show()  # Show the login window



    def show_question(self, title, text):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Question)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        icon = QIcon("./images/icon.png")
        message_box.setWindowIcon(icon)
        message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return message_box.exec()

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

    def user_show(self):
        if self.ui.Ges_Users.isHidden():
            self.ui.Ges_Users.show()
        else:
            self.ui.Ges_Users.hide()


    def hide_Options(self):
        if self.ui.stackedWidget_2.isVisible():
            self.ui.stackedWidget_2.hide()

    def show_Options(self):
        if self.ui.stackedWidget_2.isHidden():
            self.ui.stackedWidget_2.show() 



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






"""
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
    connection = sqlite3.connect("bgblast.db")
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


"""