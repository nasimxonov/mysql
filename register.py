from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QRadioButton, QComboBox, QVBoxLayout, QHBoxLayout, QLabel)
from PyQt5.QtGui import QIcon
import mysql.connector
import sys
import re

class RegisterWindow(QWidget):
    regions = ["Toshkent shahri", "Andijon viloyati", "Namangan viloyati", "Farg'ona viloyati", "Sirdaryo viloyati",
               "Jizzax viloyati", "Samarqand viloyati", "Navoiy viloyati", "Buxoro viloyati", "Xorazm viloyati",
               "Qashqadaryo viloyati", "Surxondaryo viloyati"]

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ro'yxatdan o'tish")
        self.setGeometry(600, 300, 400, 600)
        self.setWindowOpacity(0.95)
        self.createWidgets()
        self.setStyleSheet("""
            QWidget {background-color: #f2f2f2;}
            QLineEdit {border: 2px solid #8c8c8c; border-radius: 10px; padding: 8px;}
            QPushButton {background-color: #5F6AE1; border: 2px solid #0400E1; border-radius: 10px; padding: 10px;}
            QLabel {font-size: 14px; font-weight: bold;}
        """)
        self.show()

    def createWidgets(self):
        self.ism_yozish = QLineEdit(self)
        self.ism_yozish.setPlaceholderText('Ismingizni kiriting')

        self.fam_yozish = QLineEdit(self)
        self.fam_yozish.setPlaceholderText('Familiyangizni kiriting')

        self.age_kiritish = QLineEdit(self)
        self.age_kiritish.setPlaceholderText('Yoshingizni kiriting')

        self.tel_raqam = QLineEdit(self)
        self.tel_raqam.setPlaceholderText("+998 ")

        self.email_kiritish = QLineEdit(self)
        self.email_kiritish.setPlaceholderText('Emailingizni kiriting')

        self.parol_kiritish = QLineEdit(self)
        self.parol_kiritish.setPlaceholderText('Parolingizni kiriting')
        self.parol_kiritish.setEchoMode(QLineEdit.Password)

        self.jins_erkak = QRadioButton("Erkak", self)
        self.jins_ayol = QRadioButton("Ayol", self)

        self.region_combo = QComboBox(self)
        self.region_combo.addItems(self.regions)

        self.saqlash_button = QPushButton("Ro'yxatdan o'tish", self)
        self.saqlash_button.clicked.connect(self.saqla)

        self.login_button = QPushButton("Login oynasiga o'tish", self)
        self.login_button.clicked.connect(self.open_login_window)

        self.setupLayout()

    def setupLayout(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        layout.addWidget(QLabel("Ismingiz:"))
        layout.addWidget(self.ism_yozish)

        layout.addWidget(QLabel("Familiyangiz:"))
        layout.addWidget(self.fam_yozish)

        layout.addWidget(QLabel("Yoshingiz:"))
        layout.addWidget(self.age_kiritish)

        layout.addWidget(QLabel("Telefon raqamingiz:"))
        layout.addWidget(self.tel_raqam)

        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_kiritish)

        layout.addWidget(QLabel("Parol:"))
        layout.addWidget(self.parol_kiritish)

        jins_layout = QHBoxLayout()
        jins_layout.addWidget(self.jins_erkak)
        jins_layout.addWidget(self.jins_ayol)
        layout.addWidget(QLabel("Jinsingiz:"))
        layout.addLayout(jins_layout)

        layout.addWidget(QLabel("Viloyatingiz:"))
        layout.addWidget(self.region_combo)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.saqlash_button)
        button_layout.addWidget(self.login_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def saqla(self):
        if not self.ism_yozish.text():
            self.ism_yozish.setPlaceholderText('Ismingizni kiriting!')
            return
        if not self.fam_yozish.text():
            self.fam_yozish.setPlaceholderText('Familiyangizni kiriting!')
            return
        if not self.age_kiritish.text().isdigit():
            self.age_kiritish.setPlaceholderText('Yoshingizni togri kiriting!')
            return
        if not self.tel_raqam.text()[1:].isdigit() or not self.tel_raqam.text().startswith("+998"):
            self.tel_raqam.setPlaceholderText('Telefon raqam notogri!')
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email_kiritish.text()):
            self.email_kiritish.setPlaceholderText('Emailni togri kiriting!')
            return
        if not self.parol_kiritish.text():
            self.parol_kiritish.setPlaceholderText('Parolingizni kiriting!')
            return
        if not self.jins_erkak.isChecked() and not self.jins_ayol.isChecked():
            QMessageBox.warning(self, "Warning", "Jinsingizni tanlang!")
            return

        user_info = {
            "ism": self.ism_yozish.text(),
            "familiya": self.fam_yozish.text(),
            "yosh": int(self.age_kiritish.text()),
            "tel_raqam": self.tel_raqam.text(),
            "email": self.email_kiritish.text(),
            "parol": self.parol_kiritish.text(),
            "jins": "Erkak" if self.jins_erkak.isChecked() else "Ayol",
            "viloyat": self.region_combo.currentText()
        }

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="admin",
                password="admin",
                database="register"
            )
            cursor = connection.cursor()
            query = """
                INSERT INTO users (ism, familiya, yosh, tel_raqam, email, parol, jins, viloyat)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, tuple(user_info.values()))
            connection.commit()
            QMessageBox.information(self, "Success", "Ro'yxatdan o'tdingiz!")
            self.clear_fields()
        except mysql.connector.Error as err:
            QMessageBox.warning(self, "Error", f"Ro'yxatdan o'tishda xatolik: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def clear_fields(self):
        self.ism_yozish.clear()
        self.fam_yozish.clear()
        self.age_kiritish.clear()
        self.tel_raqam.clear()
        self.email_kiritish.clear()
        self.parol_kiritish.clear()
        self.jins_erkak.setChecked(False)
        self.jins_ayol.setChecked(False)
        self.region_combo.setCurrentIndex(0)

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(600, 300, 400, 300)
        self.setWindowOpacity(0.95)
        self.createWidgets()
        self.setStyleSheet("""
            QWidget {background-color: #f2f2f2;}
            QLineEdit {border: 2px solid #8c8c8c; border-radius: 10px; padding: 8px;}
            QPushButton {background-color: #5F6AE1; border: 2px solid #0400E1; border-radius: 10px; padding: 10px;}
            QLabel {font-size: 14px; font-weight: bold;}
        """)
        self.show()

    def createWidgets(self):
        self.email_login = QLineEdit(self)
        self.email_login.setPlaceholderText('Emailingizni kiriting')

        self.parol_login = QLineEdit(self)
        self.parol_login.setPlaceholderText('Parolingizni kiriting')
        self.parol_login.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Kirish", self)
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_login)
        layout.addWidget(QLabel("Parol:"))
        layout.addWidget(self.parol_login)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def login(self):
        email = self.email_login.text()
        parol = self.parol_login.text()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="admin",
                password="admin",
                database="register"
            )
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE email=%s AND parol=%s"
            cursor.execute(query, (email, parol))
            result = cursor.fetchone()
            if result:
                QMessageBox.information(self, "Success", "Tizimga kirdingiz!")
            else:
                QMessageBox.warning(self, "Error", "Noto'g'ri email yoki parol!")
        except mysql.connector.Error as err:
            QMessageBox.warning(self, "Error", f"Kirishda xatolik: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    sys.exit(app.exec_())
