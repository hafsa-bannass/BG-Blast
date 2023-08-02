import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QIODevice, QFile
from PyQt6.QtWidgets import QApplication
import os
import sys
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
        self.calcul = self.ui.frame_10.findChild(QtWidgets.QPushButton, "pushButton_7")
        self.calcul.clicked.connect(lambda:(
            self.ui.stackedWidget.setCurrentWidget(self.ui.Ges_Commandes_resultats),
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.Options_Commande_Resultats)
        ))
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

            #operations 
            longueur= maille1*nbrRang
            largeur= maille2*nbrRang
            """surface = longueur*largeur
            volume = surface*profondeur
            ammonix = profondeur*maille1*nbrTrous # 
            tovex = nbrTrous/2
            cordeau = 0
            ligneTir = "500m"
            aei ="01"
            metrageFore = nbrTrous*profondeur
            repartition =1/nbrTrous #
            renduPrevu = volume/2 #
            bourrageFinal = profondeur-(renduPrevu*0,75)
            ci = repartition*25

            #ewccords17
            reccords25 = nbrRang + 2
            reccords42 = nbrRang + 2
            reccords65 = nbrRang + 2
            reccords100 = nbrTrousRange
            detos450 = nbrTrous+2
            detos500 = nbrTrous+2

"""
        except ValueError:
            output = "Invalid input"
        #output 
        self.ui.o1.setText(str(longueur))
        self.ui.o2.setText(str(largeur))
        """
        self.ui.o3.setText(str(surface))
        self.ui.o4.setText(str(volume))
        self.ui.o5.setText(str(ammonix))
        self.ui.o6.setText(str(tovex))
        self.ui.o7.setText(str(cordeau))
        self.ui.o8.setText(str(ligneTir))
        self.ui.o9.setText(str(aei))
        self.ui.o10.setText(str(metrageFore))
        self.ui.o11.setText(str(reccords25))
        self.ui.o12.setText(str(reccords42))
        self.ui.o13.setText(str(reccords65))
        self.ui.o14.setText(str(reccords100))
        self.ui.o15.setText(str(repartition))
        self.ui.o16.setText(str(renduPrevu))
        self.ui.o17.setText(str(detos450))
        self.ui.o18.setText(str(detos500))
        self.ui.o19.setText(str(bourrageFinal))
        self.ui.o20.setText(str(ci)) """


        
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


# Create the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Flask backend!"

# Start the Flask application in a separate thread
def start_flask_app():
    app.run(host='localhost')

if __name__ == '__main__':
    # Start the Flask application in a separate thread
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.start()

    # Create the Qt application
    app = QApplication(sys.argv)

    # Create the main window
    window = my_app()

    # Show the main window
    window.show()

    # Start the Qt application event loop
    sys.exit(app.exec())
