import sys
from PySide6 import QtCore, QtWidgets, QtGui
import search_api

# Create the selection page
class SearchSelection(QtWidgets.QTableWidget):
    def __init__(self, width, height):
        super().__init__()
        
        # Initialize home page size
        self.width = width
        self.height = height
        
        # Align each search criteria vertically and add them to the list of filters
        filters = []
        layout = QtWidgets.QVBoxLayout(self)
        
        # Create a filter for Pokemon names
        name_filter = NameFilter()
        layout.addWidget(name_filter)
        filters.append(name_filter)
        
        #Create a filter for the national Pokedex numbers
        national_filter = NationalNoFilter()
        layout.addWidget(national_filter)
        filters.append(national_filter)
        
        # Create a filter for sets
        
        
        # Create a button that searches the API using each filter
        search_button = QtWidgets.QPushButton("Search", self)
        search_button.clicked.connect(lambda: self.search_cards(filters))
        layout.addWidget(search_button)

        
    def search_cards(self, filters):
        parameters = ''
        for filter in filters:
            if filter.get_content().strip():
                parameters += (f" {filter.type}:{filter.get_content()} ")
        
        search_api.search_cards(parameters)

# Create the Pokemon name filter
class NameFilter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Create the filter
        self.type = 'name'
        title = QtWidgets.QLabel("Name:", self)
        self.filter = QtWidgets.QLineEdit(self)
        
        # Align elements horizontally
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.filter)
        
    def get_content(self):
        return self.filter.text()

# Create the Pokemon name filter
class NationalNoFilter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Create the filter
        self.type = 'nationalPokedexNumbers'
        title = QtWidgets.QLabel("National No.:", self)
        self.filter = QtWidgets.QLineEdit(self)
        
        # Align elements horizontally
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.filter)
        
    def get_content(self):
        return self.filter.text()
        
class SetFilter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Create the filter
        self.type = 'id'
        title = QtWidgets.QLabel("Set:", self)
        
        # Align elements horizontally
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(title)
        
    def get_content(self):
        return self.filter.text()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    # table = SearchTable()
    # table.resize(1000, 600)
    # table.show()
    
    selection = SearchSelection(600, 100)
    selection.resize(selection.width, selection.height)
    selection.show()
    
    sys.exit(app.exec())