"""
This is the main search file that displays all cards captured by a search
"""
import sys
from PySide6 import QtCore, QtWidgets, QtGui

# Create the search table
class SearchTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize the search table
        self.setColumnCount(9)
        self.setRowCount(20)
        
        # Set the columns
        self.column_names = ["Supertype", "Name", "National No.", "Set", "Set No.", "Pokemon Type", "Pokemon Subtype", "Rarity", "Worth"]
        self.setHorizontalHeaderLabels(self.column_names)
        
        # Resize the columns and add a scroll bar
        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        
        # Set a context menu for the header
        header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.showHeaderContextMenu)
    
    # Triggers the filter button when right clicking a column header
    def showHeaderContextMenu(self, pos):
        header = self.horizontalHeader()
        column = header.logicalIndexAt(pos)

        context_menu = QtWidgets.QMenu(self)

        # Create filter action for each column
        filter_action = context_menu.addAction("Filter")
        filter_action.triggered.connect(lambda: self.showFilterBox(column))

        context_menu.exec_(header.mapToGlobal(pos))
    
    # Displays the filter box
    def showFilterBox(self, column):
        filter_text, ok = QtWidgets.QInputDialog.getText(self, "Filter", f"Enter filter text for column {self.column_names[column]}:")
        if ok:
            self.applyFilter(column, filter_text)
    
    # Applies the filter   
    def applyFilter(self, column, filter_text):
        for row in range(self.rowCount()):
            item = self.item(row, column)
            if item is not None:
                item.setHidden(filter_text.lower() not in item.text().lower())
              
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
        self.table = SearchTable()
        self.layout.addWidget(self.table)
    
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    # table = SearchTable()
    # table.resize(1000, 600)
    # table.show()
    
    search = SearchPage(1150, 700)
    search.resize(search.width, search.height)
    search.show()
    
    sys.exit(app.exec())