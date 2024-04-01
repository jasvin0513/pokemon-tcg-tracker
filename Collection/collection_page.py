"""
This is the main collection file that displays all cards currently in the database
"""
import sys, sqlite3, functools
from PySide6 import QtCore, QtWidgets, QtSql

# Create a dialog for displaying additional information
class RowDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=None, record=None):
        # Create the dialog
        super().__init__(parent)
        self.setWindowTitle("Row Information")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel()
        self.layout.addWidget(self.label)
        
        # Breakdown the record into usable fields
        self.card_id = record.value(0)
        self.supertype = record.value(1)
        self.name = record.value(2)
        self.nationalNum = record.value(3)
        self.set = record.value(4)
        self.setNum = record.value(5)
        self.type = record.value(6)
        self.subtype = record.value(7)
        self.rarity = record.value(8)
        self.worth = record.value(9)
        self.card_details = (self.supertype, self.name, self.nationalNum, self.set, self.setNum, self.type, self.subtype, self.rarity, self.worth)

        # Print the card's details
        self.set_text()
        
        # Add a 'add copy' button
        self.addCopyButton = QtWidgets.QPushButton("Add a copy")
        self.layout.addWidget(self.addCopyButton)
        self.addCopyButton.clicked.connect(functools.partial(self.addCard))
        
        # Add a 'delete card' button
        self.deleteButton = QtWidgets.QPushButton("Delete Card")
        self.layout.addWidget(self.deleteButton)
        self.deleteButton.clicked.connect(functools.partial(self.deleteCard))
        
        # Delete the dialog once a button is clicked
        self.rejected.connect(self.deleteLater())
        
    def set_text(self):
        card_details_message = (
            f"Supertype: {self.supertype}\n"
            f"Name: {self.name}\n"
            f"National #: {self.nationalNum}\n"
            f"Set: {self.set}\n"
            f"Set #: {self.setNum}\n"
            f"Type: {self.type}\n"
            f"Subtype: {self.subtype}\n"
            f"Rarity: {self.rarity}\n"
            f"Worth: {self.worth}\n"
        )

        self.label.setText(card_details_message)
        self.label.setAlignment(QtCore.Qt.AlignLeft)

    def deleteCard(self):
        # Connect to the database
        conn = sqlite3.connect('Database/card_collection.db')
        cursor = conn.cursor()
        
        cursor.execute(f'''DELETE FROM card_collection WHERE ID = {self.card_id}''')
        
        # Commit changes to the database
        conn.commit()
        conn.close()
                
        # Refresh the table after deleting
        print("Card deleted from collection")
        self.parent().refreshTable()
        self.hide()
        self.reject()
    
    def addCard(self):
        # Connect to the database
        conn = sqlite3.connect('Database/card_collection.db')
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO card_collection ("Supertype", "Name", "National #", "Set", "Set #", "Type", "Subtype", "Rarity", "Worth")
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', self.card_details)
        
        # Commit changes to the database
        conn.commit()
        conn.close()
        
        # Refresh the table after adding a card
        print("Card added to collection")
        self.parent().refreshTable()
        self.hide()
        self.reject()

# Create the collection page
class CollectionPage(QtWidgets.QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        # Create the table view
        self.table_view = QtWidgets.QTableView()
        
        # Load the table
        self.model = QtSql.QSqlTableModel()
        if self.connect_database():
            self.load_table()
            
        # Add the table to horizontal layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.table_view)
        
        # Connect the clicked signal of the table view to open_dialog slot
        self.table_view.clicked.connect(self.open_dialog)
        

        
    def connect_database(self):
        # Accesses the database and grants read/write permissions
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db_path = "Database/card_collection.db"
        db.setDatabaseName(db_path)
        
        if not db.open():
            print("Could not open the database: ", db.lastError().text())
            return False
        else:
            print("Database connected successfully")
            return True
        
    def load_table(self):
        query = QtSql.QSqlQuery()
        query.exec("""  SELECT CC.[ID],
                            CC.[Supertype], 
                            CC.[Name], 
                            CC.[National #], 
                            CC.[Set], 
                            CC.[Set #], 
                            CC.[Type], 
                            CC.[Subtype], 
                            CC.[Rarity], 
                            CC.[Worth], 
                            Copies_Count.[Copies Owned]
                        FROM card_collection CC
                        JOIN (
                            SELECT [Set], 
                                [Set #], 
                                COUNT(*) AS [Copies Owned] 
                            FROM card_collection 
                            GROUP BY 
                                    [Set], 
                                    [Set #]
                        ) Copies_Count
                        ON CC.[Set] = Copies_Count.[Set]
                        AND CC.[Set #] = Copies_Count.[Set #]
                        ORDER BY CC.[Set], CC.[Set #]""")
        
        # Populate table with data
        self.model.setQuery(query)
        self.table_view.setModel(self.model)
            
    def open_dialog(self, index):
        row = index.row()
        
        # Get row data
        record = self.model.record(row)
        
        # Create a dialog for the card
        dialog = RowDialog(self, record)
        dialog.exec()
        
    def refreshTable(self):
        self.load_table()
        print("Collection reloaded")
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    collection = CollectionPage(1150, 700)
    collection.resize(collection.width, collection.height)
    collection.show()
    
    sys.exit(app.exec())