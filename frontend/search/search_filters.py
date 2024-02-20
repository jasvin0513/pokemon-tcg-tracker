"""
This script creates all the filter classes for the search module
"""

import sys, warnings, requests
from PySide6 import QtCore, QtWidgets, QtGui
import search_api

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
        self.type = 'set.id'
        title = QtWidgets.QLabel("Set:", self)
        
        # Create the list widget
        self.list = QtWidgets.QComboBox()
        self.list.addItem('All')
        
        # Add each set and their icon
        self.set_data = []  # Create a list to store set data
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
            return self.set_data[selected_index]['id']
        else:
            return ''
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    selection = SetFilter(search_api.get_sets())
    print(selection.get_content())
    selection.show()
    
    sys.exit(app.exec())