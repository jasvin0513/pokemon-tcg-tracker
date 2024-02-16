import sys
from PySide6 import QtCore, QtWidgets, QtGui

# Create the search table
class SearchTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize the search table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(9)
        self.table.setRowCount(20)
        
        # Set the columns
        column_names = ["Supertype", "Name", "National No.", "Set", "Set No.", "Pokemon Type", "Pokemon Subtype", "Rarity", "Worth"]
        self.table.setHorizontalHeaderLabels(column_names)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        

# Create the search page
class SearchPage(QtWidgets.QWidget):
    def __init__(self, width, height):
        super().__init__()
        
        # Initialize home page size
        self.width = width
        self.height = height
        
        # Create the page title
        title = QtWidgets.QLabel("Card Search", 
                                    alignment=QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(18)
        title.setFont(font)
        
        # Create a vertical layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(60)
        self.layout.addWidget(title)
        
        # Add the table to the layout
        table = SearchTable()
        self.layout.addWidget(table)
        table_height = int(self.height * 0.8)
        table.setMaximumHeight(table_height)
        
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    search = SearchPage(1000, 600)
    search.resize(search.width, search.height)
    search.show()
    
    sys.exit(app.exec())