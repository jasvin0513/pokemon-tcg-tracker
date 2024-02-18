import sys
from PySide6 import QtCore, QtWidgets, QtGui

# Create the search table
class SearchSelection(QtWidgets.QTableWidget):
    def __init__(self, width, height):
        super().__init__()
        
        # Initialize home page size
        self.width = width
        self.height = height
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    # table = SearchTable()
    # table.resize(1000, 600)
    # table.show()
    
    selection = SearchSelection(1150, 700)
    selection.resize(selection.width, selection.height)
    selection.show()
    
    sys.exit(app.exec())