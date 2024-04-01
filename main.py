import sys, sqlite3
from PySide6 import QtWidgets
from Home.home import HomePage
from Sidebar.sidebar import SideBar
from Search.search_page import SearchPage

def create_db():
    # Connect to database
    conn = sqlite3.connect('Database/card_collection.db')
    cursor = conn.cursor()
    
    # Create a new card collection if one doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS card_collection (
                        "ID" INTEGER PRIMARY KEY,
                        "Supertype" CHAR,
                        "Name" CHAR,
                        "National #" INT,
                        "Set" CHAR,
                        "Set #" INT,
                        "Type" CHAR,
                        "Subtype" CHAR,
                        "Rarity" CHAR,
                        "Worth" DECIMAL
                    );''')
    
    # Create a new card collection if one doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS card_counts (
                        "ID" INTEGER PRIMARY KEY,
                        "Set" CHAR,
                        "Set #" INT
                    );''')
    
    conn.commit()
    conn.close()

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize the collection database if it doesn't already exist
        create_db()
        
        # Create instances of each page
        self.page_width = 1150
        self.page_height = 700
        
        # Home Page
        self.home = HomePage(self.page_width, self.page_height)
        
        # Search Page
        self.search = SearchPage(self.page_width, self.page_height)
        
        # Create stacked widget to switch between pages
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.stackedWidget.addWidget(self.home)
        self.stackedWidget.addWidget(self.search)
        
        # Create an instance of the sidebar
        self.sidebar_width = 100
        self.sidebar = SideBar(self.sidebar_width, self.page_height, self.stackedWidget)
        
        
        # Arrange the sidebar and stacked widget horizontally
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.stackedWidget)
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    main = MainWindow()
    main.resize(main.page_width + main.sidebar_width, main.page_height)
    main.show()
    
    sys.exit(app.exec())