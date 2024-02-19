import sys, warnings, requests
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
        # Suppress libpng warning
        warnings.simplefilter("ignore")
        sets = search_api.get_sets()
        set_filter = SetFilter(sets)
        layout.addWidget(set_filter)
        filters.append(set_filter)
        warnings.resetwarnings()
        
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
 
# Create the Set name filter       
class SetFilter(QtWidgets.QWidget):
    def __init__(self, sets):
        super().__init__()
        
        # Create the filter
        self.type = 'id'
        title = QtWidgets.QLabel("Set:", self)
        
        # Create the list widget
        self.list = QtWidgets.QComboBox()
        
        # Add each set and their icon
        for set_name in sets:
            # Get the icon from the URL
            response = requests.get(sets[set_name])
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(response.content)
            icon = QtGui.QIcon(pixmap)
            
            # Add the item to the list with its own icon
            self.list.addItem(icon, set_name)
        
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.list)
        
        
    def get_content(self):
        return self.list.currentText()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    selection = SearchSelection(600, 300)
    selection.resize(selection.width, selection.height)
    selection.show()
    
    sys.exit(app.exec())