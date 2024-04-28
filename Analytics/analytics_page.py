"""
This is file displays various visualizations card for the card collection
"""
import sys, sqlite3, functools
from PySide6 import QtCore, QtWidgets, QtSql
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.ticker as ticker
from matplotlib.figure import Figure

# Rarity Count visual
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, title=""):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        
        # Set the title
        self.axes.set_title(title)


# Create the collection page
class AnalyticsPage(QtWidgets.QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        
        # Connect to the database
        self.conn = self.connect_database()
        
        # Create a layout for the widget
        layout = QtWidgets.QGridLayout(self)
        
        # Add text labels
        # List the total number of cards in the collection
        card_count = f"Card Count: {self.total_cards()}"
        card_count_label = QtWidgets.QLabel(card_count)
        # List total collection value
        total_worth = f"Total Worth: {self.total_value()}"
        total_worth_label = QtWidgets.QLabel(total_worth)
        # List most valuable card
        most_valuable_card = self.most_valuable_card()
        most_valuable_card_text = f"Most Valuable Card: {most_valuable_card[8]} {most_valuable_card[2]} from {most_valuable_card[4]}"
        most_valuable_card_label = QtWidgets.QLabel(str(most_valuable_card_text))
        
        # Add labels to layout
        layout.addWidget(card_count_label, 0, 0)
        layout.addWidget(total_worth_label, 1, 0)
        layout.addWidget(most_valuable_card_label, 2, 0)
        
        # Create a matplotlib figure and add a subplot for card rarity
        rarity_count = self.rarity_count()
        if rarity_count:
            rarities, counts = zip(*rarity_count)
            rarity_count_visual = MplCanvas(self, width=12, height=4, dpi=100, title="Card Count by Rarity")
            rarity_count_visual.axes.bar(rarities, counts)
            
            # Set the y-axis tick formatter to display integers
            rarity_count_visual.axes.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
            # Add the canvas to the layout, specifying its position and size
            layout.addWidget(rarity_count_visual, 3, 0, 1, 1)  # Parameters: widget, row, column, rowspan, colspan
            
        # Create a matplotlib figure and add a subplot for card rarity frequencies
        rarity_freq= self.rarity_freq()
        if rarity_freq:
            rarities, counts = zip(*rarity_freq)
            rarity_freq_visual = MplCanvas(self, width=12, height=4, dpi=100, title="Frequency of Cards by Rarity")
            rarity_freq_visual.axes.bar(rarities, counts)
            
            # Set the y-axis tick formatter to display integers
            rarity_freq_visual.axes.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
            # Add the canvas to the layout, specifying its position and size
            layout.addWidget(rarity_freq_visual, 4, 0, 1, 1)  # Parameters: widget, row, column, rowspan, colspan
        
        # Add some spacing to fill the rest of the layout
        layout.setColumnStretch(1, 1)
        layout.setRowStretch(1, 1)
        
    # Accesses the database
    def connect_database(self):
        try:
            conn = sqlite3.connect("Database/card_collection.db")
            print("Database connected successfully")
            return conn
        except sqlite3.Error as e:
            print("Could not open the database:", e)
            return None
    
    # Gets the total number of cards in the card collection
    def total_cards(self):
        if not self.conn:
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT COUNT(ID) AS TOTAL_COUNT
                                FROM card_collection""")
            return cursor.fetchall()[0][0]
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return None
    
    # Gets the total value of the card collection
    def total_value(self):
        if not self.conn:
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT SUM(WORTH) AS TOTAL_WORTH
                                FROM card_collection""")
            result = cursor.fetchall()
            
            if result:
                total_worth = round(result[0][0], 2)
                return total_worth
            else:
                return 0
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return None
        
    # Gets the most valuable card from the card collection
    def most_valuable_card(self):
        if not self.conn:
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT *
                                FROM card_collection
                                WHERE WORTH = (SELECT MAX(WORTH) FROM card_collection)""")
            return cursor.fetchall()[0]
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return None
    
    # Returns the count of each card rarity in the database
    def rarity_count(self):
        if not self.conn:
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT Rarity, COUNT(Rarity) AS "Rarity Count"
                              FROM card_collection
                              GROUP BY Rarity""")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return None
    
    # Returns the count of each card rarity in the database
    def rarity_freq(self):
        if not self.conn:
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT 
                                Rarity, 
                                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM card_collection), 2) AS "Rarity Percentage"
                                FROM 
                                card_collection
                                GROUP BY 
                                Rarity;""")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return None
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    analytics = AnalyticsPage(1150, 700)
    analytics.resize(analytics.width, analytics.height)
    analytics.show()
    
    sys.exit(app.exec())