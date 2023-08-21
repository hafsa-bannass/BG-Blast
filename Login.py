from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor


class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Login")
        MainWindow.resize(822, 460)
        MainWindow.setStyleSheet("*{\n"
"    background-color: rgb(0, 79, 116);\n"
"   border:none;\n"
"   background-color: transparent;\n"
"   background: transparent;\n"
"   padding: 0;\n"
"   margin:0;\n"
"   color:#fff;\n"
"}\n"
"#centralwidget, #mainBodyContent, #AccBtn{\n"
"background-color: #003f5c;\n"
"}\n"
"\n"
"#loginButton{\n"
"background-color: #2fc692 ;\n"
"color: #003f5c;\n"
"border-radius: 10px 10px 10px 10px;\n"
"padding: 3px 5px;\n"
"}\n"
"QLineEdit{\n"
"background-color: transparent;\n"
"color: #ffffff;\n"
"border-radius: 10px ;\n"
"border: 2px solid #2fc692;\n"
"padding: 4px 8px;\n"
"}")
     
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.rightPart = QtWidgets.QWidget(parent=self.centralwidget)
        self.rightPart.setObjectName("rightPart")     
        
        self.label = QtWidgets.QLabel(self.rightPart)
        self.label.setGeometry(QtCore.QRect(50, -120, 150, 40))
        font = QtGui.QFont()
        font.setFamily("Gabriola")
        font.setPointSize(34)
        font.setBold(True)
        self.label.setStyleSheet("color: #2fc692;")
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.usernameLineEdit = QtWidgets.QLineEdit(parent=self.rightPart)
        self.usernameLineEdit.setGeometry(QtCore.QRect(70, 165, 165, 36))
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        
        self.passwordLineEdit = QtWidgets.QLineEdit(parent=self.rightPart)
        self.passwordLineEdit.setGeometry(QtCore.QRect(70, 210, 165, 36))
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        
        self.loginButton = QtWidgets.QPushButton(parent=self.rightPart)
        self.loginButton.setObjectName("loginButton")
        self.loginButton.setGeometry(QtCore.QRect(80, 290, 146, 26))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(8)
        font.setBold(True)
        self.loginButton.setFont(font)
        # Set the cursor to a pointing hand when hovering over the login button
        self.loginButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.guestLabel = QtWidgets.QLabel(self.rightPart)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.guestLabel.setGeometry(QtCore.QRect(70, 250, 170, 30))
        font.setUnderline(True)
        self.guestLabel.setFont(font)
        self.guestLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.guestLabel.setObjectName("guestLabel")
        self.guestLabel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.label_1 = QtWidgets.QLabel(parent=self.rightPart)
        self.label_1.setGeometry(QtCore.QRect(70, 130, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(410, 40, 358, 381))
        self.label.setFixedSize(400, 400)  # Set the width and height
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("./images/LogoSautage1.png"))
        self.label_3.setObjectName("label_3")

        self.horizontalLayout.addWidget(self.rightPart)
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Login"))
        self.label.setText(_translate("MainWindow", "Bienvenue sur BG Blast!"))
        self.usernameLineEdit.setPlaceholderText(_translate("MainWindow", "Nom d'utilisateur"))
        self.passwordLineEdit.setPlaceholderText(_translate("MainWindow", "Mot de passe"))
        self.loginButton.setText(_translate("MainWindow", "Se Connecter"))
        self.guestLabel.setText(_translate("MainWindow", "Continuer autant que visiteur?"))        
        self.label_1.setText(_translate("MainWindow", "Connectez-vous à votre compte"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
