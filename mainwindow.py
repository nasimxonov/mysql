import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QToolBar, \
    QVBoxLayout, QAction, QDialog, QLabel, QPushButton, QFormLayout


def get_connection():
    return mysql.connector.connect(
        user='admin',
        host='localhost',
        password='admin',
        database='mainwindow'
    )


def fetch_users():
    connection = get_connection()
    connection.autocommit = True
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
    
    connection.close()
    return users


class AddProductDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mahsulot qo'shish")
        self.setGeometry(650, 350, 300, 200)

        self.layout = QFormLayout()

        self.name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.color_input = QLineEdit()
        self.description_input = QLineEdit()
        self.date_input = QLineEdit()

        self.layout.addRow("Nomi:", self.name_input)
        self.layout.addRow("Soni:", self.quantity_input)
        self.layout.addRow("Rangi:", self.color_input)
        self.layout.addRow("Haqida:", self.description_input)
        self.layout.addRow("Sanasi:", self.date_input)

        self.submit_button = QPushButton("Qo'shish")
        self.submit_button.clicked.connect(self.add_product)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def add_product(self):
        conn = get_connection()
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Product (name, quantity, color, description, date) VALUES (%s, %s, %s, %s, %s)",
                (
                    self.name_input.text(),
                    self.quantity_input.text(),
                    self.color_input.text(),
                    self.description_input.text(),
                    self.date_input.text()
                )
            )
        self.accept()  


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(600, 300, 750, 600)
        self.setWindowTitle("Product app")

        vertical_layout = QVBoxLayout()

        self.add_button = QAction("Qo'shish", self)
        self.edit_button = QAction("Tahrirlash", self)
        self.delete_button = QAction("O'chirish", self)

        self.add_button.triggered.connect(self.show_add_dialog)
        self.delete_button.triggered.connect(self.delete_item)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.add_button)
        self.toolbar.addAction(self.edit_button)
        self.toolbar.addAction(self.delete_button)

        self.table = QTableWidget()
        self.load_data()

        vertical_layout.addWidget(self.table)

        widget = QWidget()
        widget.setLayout(vertical_layout)

        self.setCentralWidget(widget)

        self.show_users()  

    def load_data(self):
        conn = get_connection()
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Product")
            result = cursor.fetchall()

        self.table.setColumnCount(6)
        self.table.setRowCount(len(result))

        self.table.setHorizontalHeaderLabels(["ID", "Nomi", "Soni", "Rangi", "Haqida", "Sanasi"])

        for row_index, data in enumerate(result):
            for column_index, item in enumerate(data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(item)))

    def show_add_dialog(self):
        dialog = AddProductDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()  

    def delete_item(self):
        current = self.table.currentRow()
        item = self.table.item(current, 0)

        conn = get_connection()
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(f"DELETE FROM Product WHERE id={item.text()}")

        self.load_data()

    def show_users(self):
        users = fetch_users()  
        print("Foydalanuvchilar:", users) 


app = QApplication([])
window = MainWindow()
window.show()

app.exec_()
