import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QIODevice, QFile
from PyQt6.QtWidgets import QApplication
import os
import sys
import sqlite3
from mainwindow_ui import Ui_MainWindow
import threading
from flask import Flask
from Login import Ui_LoginWindow

class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        # Connect the login button to the login function
        self.ui.loginButton.clicked.connect(self.login)

    def login(self):
        
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        if username == "admin" and password == "password":
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Login", " Login Invalid ")

"""
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
                    longueur DOUBLE,
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

class my_app(QtWidgets.QMainWindow):
    def __init__(self, parent= None):
        super().__init__(parent)
        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
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

        self.ui.GesStockBtn.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Stock),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Stock)
        ))
        self.ui.GesStockBtn.clicked.connect(self.show_Options)     

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

        self.ui.pushButton_8.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Documentation),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Docummentation)
        ))
        self.ui.pushButton_8.clicked.connect(self.show_Options)     

        self.ui.pushButton_9.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives)
        ))
        #self.option= self.ui.stackedWidget_2
        #boutton calcul fiche de saisie 
        self.calcul = self.ui.frame_10.findChild(QtWidgets.QPushButton, "pushButton_7")
        self.calcul.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Commandes_resultats),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Commande_Resultats)
        ))    
        #self.calcul.clicked.connect(create_database)
        self.calcul.clicked.connect(self.show_Options) 
        self.calcul.clicked.connect(self.calculations) 


        self.ui.pushButton_33.clicked.connect(self.show_Options)     
        self.ui.pushButton_33.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Com_Avan)
        ))

        self.ui.pushButton_34.clicked.connect(self.show_Options)     
        self.ui.pushButton_34.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Stock)
        ))

        self.ui.pushButton_35.clicked.connect(self.show_Options)     
        self.ui.pushButton_35.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Archives),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Archives),
            self.ui.Historiques.setCurrentWidget(self.ui.Historique_Cout)
        ))

        self.ui.pushButton_37.clicked.connect(self.show_Options)     
        self.ui.pushButton_37.clicked.connect(lambda:(
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

    def calculations(self):
        try:
            #input Data
            #date= self.ui.dateEdit_3.data()
            zoneTir = self.ui.comboBox.currentText()
            modeTir = self.ui.comboBox_2.currentText()
            modeCharg = self.ui.comboBox_3.currentText()
            machineForation= self.ui.comboBox_4.currentText()
            machineDecapage= self.ui.comboBox_5.currentText()
            schemaTir=self.ui.comboBox_6.currentText()
            panneau= self.ui.comboBox_7.currentText()
            tranche= self.ui.line8.text()
            niveau= self.ui.comboBox_9.currentText()
            profondeur= float(self.ui.line1.text())
            nbrTrous = float(self.ui.line2.text())
            nbrRang = float(self.ui.line3.text())
            nbrTrousRange= float(self.ui.line4.text())
            maille1 = float(self.ui.comboBox_10.currentText())
            maille2 = float(self.ui.comboBox_11.currentText())
            dosagePrevu= float(self.ui.line6.text())

           

        except ValueError:
            output = "Invalid input"


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
        aei ="01"
        metrageFore = nbrTrous*profondeur
        repartition = ammonix/nbrTrous 
        renduPrevu = volume/21 # 21 heures de marche 
        bourrageFinal = profondeur - (repartition*0.75)
        ci = repartition*25
        
        if modeCharg=="Unique":
            detos500 = nbrTrous+2
            detos450 ="0"
        elif modeCharg== "Deux Etages":
            detos500 = "0"
            detos450 = nbrTrous+2
            
        if schemaTir=="17ms,25ms,42ms":
            reccords17 = (nbrTrous - ( nbrRang +2))+2
            reccords25 = nbrRang + 2
            reccords42 = nbrRang + 2
            reccords65 = 'none'
            reccords100 = nbrTrousRange
        elif schemaTir=="17ms,25ms,42ms,65ms":
            reccords17 = (nbrTrous - ( nbrRang +2) )+2
            reccords25 = nbrRang + 2
            reccords42 = nbrRang + 2
            reccords65 = nbrRang + 2
            reccords100 = 'none'
        elif schemaTir=="17ms,25ms":
            reccords17 = (nbrTrous - ( nbrRang +2) )+2
            reccords25 = nbrRang + 2
            reccords42 = 'none'
            reccords65 = 'none'
            reccords100 = 'none'
        elif schemaTir=="17ms,100ms":
            reccords17 = (nbrTrous - ( nbrRang +2) )+2
            reccords25 = 'none'
            reccords42 = 'none'
            reccords65 = 'none'
            reccords100 = nbrTrousRange
            
        """ else:
            reccords25 = nbrRang + 2
            reccords42 = nbrRang + 2
            reccords65 = nbrRang + 2
            reccords100 = nbrTrousRange
            
        self.ui.o17.setText(str(detos450))
        self.ui.o18.setText(str(detos500))
        """

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



# Start the Flask application in a separate thread
def start_flask_app():
    app.run(host='localhost')

if __name__ == '__main__':
    
    # Create the Qt application
    app = QApplication(sys.argv)

    # Create the main window
    window = LoginDialog()

    # Show the main window
    window.show()

    # Start the Qt application event loop
    sys.exit(app.exec())
