"""
This script creates all the filter classes for the search module
"""

import sys, requests
from PySide6 import QtCore, QtWidgets, QtGui
from . import search_api

# Create a loading screen while the filters load
class LoadingScreen(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading filters...")
        self.setFixedSize(300, 1)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

# Caches the filters to reduce API calls
class FilterCache():
    def __init__(self):
        self.SupertypeFilter = SupertypeFilter()
        self.NameFilter = NameFilter()
        self.NationalNoFilter = NationalNoFilter()
        self.SetFilter = SetFilter()

# Create the Supertype filter
class SupertypeFilter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Create the filter
        self.type = 'supertype'
        title = QtWidgets.QLabel("Supertype:", self)
        
        # Create the dropdown menu
        self.filter = QtWidgets.QComboBox()
        self.filter.addItem("All")
        self.filter.addItem("Energy")
        self.filter.addItem("Pokémon")
        self.filter.addItem("Trainer")
        
        # Align elements horizontally
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.filter)
        
    
    def get_content(self):
        selected_index = self.filter.currentIndex()
        if selected_index > 0:
            return self.filter.currentText()
        else:
            return ''

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
    def __init__(self):
        super().__init__()
        
        # Get all sets from the API
        sets = search_api.get_sets()
        
        # Create the filter
        self.type = 'set.id'
        title = QtWidgets.QLabel("Set:", self)
        
        # Create the list widget
        self.list = QtWidgets.QComboBox()
        self.list.addItem('All')
        
        # Add each set and their icon
        self.set_data = []  # Create a list to store set data
        self.set_data.append({'set_name': 'All', 'id': ''})
        for set_name, id, icon_url in sets:
            # Get the icon from the URL
            response = requests.get(icon_url)
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(response.content)
            icon = QtGui.QIcon(pixmap)
            
            # Add the item to the list with its own icon
            self.list.addItem(icon, set_name)
            
            # Store set data in the list
            self.set_data.append({'set_name': set_name, 'id': id, 'icon_url': icon_url})
        
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.list)
        
        
    def get_content(self):
        selected_index = self.list.currentIndex()
        if selected_index > 0:
            print(f"Searching {self.set_data[selected_index]['id']}")
            return self.set_data[selected_index]['id']
        else:
            return ''
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    selection = SetFilter(search_api.get_sets())
    print(selection.get_content())
    selection.show()
    
    sys.exit(app.exec())