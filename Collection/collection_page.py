"""
This is the main collection file that displays all cards currently
"""
import sys
from PySide6 import QtCore, QtWidgets, QtGui, QtSql

# Create the collection page
class CollectionPage(QtWidgets.QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        # Load the table
        self.model = QtSql.QSqlTableModel()
        self.table_view.setModel(self.model)
        self.connect_database()
        self.load_table("card_collection")
        
        # Add the table to the layout
        layout = QtWidgets.QVBoxLayout(self)
        self.table_view = QtWidgets.QTableView()
        layout.addWidget(self.table_view)
        
    def connect_database(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("../Database/card_collection.db")
        
        if not db.open():
            print("Could not open the database")
            return False
        else:
            print("Database connected successfully")
            return True
        
    def load_table(self, table_name):
        self.model.setTable(table_name)
        if not self.model.select():
            print("Error loading table:", self.model.lastError().text())
        else:
            print("Table loaded successfully.")

        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    collection = CollectionPage(1150, 700)
    collection.resize(collection.width, collection.height)
    collection.show()
    
    sys.exit(app.exec())