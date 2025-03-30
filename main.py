import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QMessageBox, QToolBar, QAction, QFontDialog,
    QColorDialog, QLabel, QWidget, QVBoxLayout,
    QTabWidget, QHBoxLayout, QPushButton, QStyle,
    QStyleFactory
)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QTextCursor # Import QPalette from QtGui
from PyQt5.QtCore import Qt, QTimer, QObject, pyqtSignal


class WordEditor(QMainWindow):
    """
    A basic word processor application built using PyQt5.  Now with tabs!
    """
    def __init__(self):
        super().__init__()

        # Initialize the tab counter
        self.tab_count = 0  # Initialize here, before initUI()

        # Initialize the user interface
        self.initUI()

    def initUI(self):
        """
        Sets up the main window, tab widget, toolbar, and menu.
        """
        # Set window title and icon
        self.setWindowTitle("PyWord2.0")  # Renamed window title
        self.setWindowIcon(QIcon.fromTheme("edit-document", QIcon("edit.png")))

        # Create the central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Create a vertical layout for the central widget
        self.verticalLayout = QVBoxLayout(self.centralWidget)

        # Create the tab widget
        self.tabWidget = QTabWidget(self.centralWidget)
        self.tabWidget.setTabsClosable(True)  # Enable close buttons on tabs
        self.tabWidget.tabCloseRequested.connect(self.closeTab)  # Connect close signal
        self.verticalLayout.addWidget(self.tabWidget)

        # Create the toolbar
        self.toolbar = QToolBar("Main Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # Create actions for the toolbar and menu
        self.createActions()
        # Add actions to the toolbar
        self.addActionsToToolbar()
        # Create the menu bar
        self.createMenu()

        # Set the initial font
        self.default_font = QFont("Arial", 12)

        # Add the first tab
        self.addTab()

        # Set the initial window size
        self.setGeometry(300, 300, 800, 600)

        # Create the status bar
        self.statusBar().showMessage("Ready")

        # Create word count label in the status bar
        self.wordCountLabel = QLabel("Words: 0", self)
        self.statusBar().addPermanentWidget(self.wordCountLabel)  # Add to the right side of status bar

        # Create timer for delayed word count updates
        self.wordCountTimer = QTimer(self)  # Initialize the timer
        self.wordCountTimer.timeout.connect(self.updateWordCount)
        self.wordCountTimer.setSingleShot(True)

        # Apply dark mode settings if enabled
        self.applyDarkModeSettings()

        # Show the main window
        self.show()

    def createActions(self):
        # Support for MacOS will be comming soon (CMD)
        """
        Creates the actions for opening, saving, and exiting files,
        as well as for font and color customization.
        """
        # File menu actions
        self.newAction = QAction(QIcon.fromTheme("document-new", QIcon("new.png")), "New ➕", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new document")
        self.newAction.triggered.connect(self.addTab)

        self.openAction = QAction(QIcon.fromTheme("document-open", QIcon("open.png")), "Open 📂", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Open a file")
        self.openAction.triggered.connect(self.openFile)

        self.saveAction = QAction(QIcon.fromTheme("document-save", QIcon("save.png")), "Save 💾", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.setStatusTip("Save the file")
        self.saveAction.triggered.connect(self.saveFile)

        self.saveAsAction = QAction("Save As... 📝", self)
        self.saveAsAction.setShortcut("Ctrl+Shift+S")
        self.saveAsAction.setStatusTip("Save the file with a new name")
        self.saveAsAction.triggered.connect(self.saveAsFile)

        self.exitAction = QAction(QIcon.fromTheme("application-exit", QIcon("exit.png")), "Exit 🚪", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.setStatusTip("Exit the application")
        self.exitAction.triggered.connect(self.close)

        # Edit menu actions
        self.fontAction = QAction(QIcon.fromTheme("preferences-desktop-font", QIcon("font.png")), "Font ✒️", self)
        self.fontAction.setStatusTip("Change font")
        self.fontAction.triggered.connect(self.setFont)

        self.colorAction = QAction(QIcon.fromTheme("preferences-desktop-color", QIcon("color.png")), "Color 🎨", self)
        self.colorAction.setStatusTip("Change text color")
        self.colorAction.triggered.connect(self.setColor)

        self.aboutAction = QAction("About ℹ️", self)
        self.aboutAction.setStatusTip("Show About Box")
        self.aboutAction.triggered.connect(self.showAbout)

        # View menu actions
        self.darkModeAction = QAction("Dark Mode", self)
        self.darkModeAction.setCheckable(True)
        self.darkModeAction.toggled.connect(self.toggleDarkMode)
        self.darkModeAction.setStatusTip("Toggle dark mode")

    def addActionsToToolbar(self):
        """Adds the defined actions to the toolbar."""
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.fontAction)
        self.toolbar.addAction(self.colorAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addAction(self.darkModeAction)  # Add dark mode action to toolbar

    def createMenu(self):
        """
        Creates the menu bar and adds the file and edit menus.
        """
        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        editMenu = self.menuBar.addMenu("&Edit")
        editMenu.addAction(self.fontAction)
        editMenu.addAction(self.colorAction)

        viewMenu = self.menuBar.addMenu("&View")  # Add a View menu
        viewMenu.addAction(self.darkModeAction)  # Add the Dark Mode action to the View menu

        helpMenu = self.menuBar.addMenu("&Help")
        helpMenu.addAction(self.aboutAction)
        self.statusBar()

    def addTab(self):
        """
        Adds a new tab with a QTextEdit widget.
        """
        self.textEdit = QTextEdit(self.tabWidget)
        self.textEdit.setFont(self.default_font)  # set default font
        tab_name = f"Document {self.tab_count + 1}"
        self.tabWidget.addTab(self.textEdit, tab_name)
        self.tabWidget.setCurrentIndex(self.tab_count)  # Switch to the new tab
        self.tab_count += 1

        # Connect the textChanged signal to the updateWordCount method for the current text edit
        self.textEdit.textChanged.connect(self.updateWordCount)
        self.statusBar().showMessage(f"New tab '{tab_name}' created.", 3000)

    def closeTab(self, index):
        """
        Closes the tab at the given index.
        """
        widget = self.tabWidget.widget(index)
        if widget:
            widget.deleteLater()  # Properly delete the widget
        self.tabWidget.removeTab(index)
        self.tab_count -= 1
        self.statusBar().showMessage(f"Tab closed.", 3000)
        if self.tab_count == 0:
            self.addTab()

    def getCurrentTextEdit(self):
        """
        Returns the QTextEdit widget of the currently selected tab.
        """
        current_index = self.tabWidget.currentIndex()
        if current_index >= 0:
            return self.tabWidget.widget(current_index)
        else:
            return None

    def openFile(self):
        """
        Opens a file and loads its content into the text edit widget of the current tab.
        """
        textEdit = self.getCurrentTextEdit()
        if textEdit is None:
            return

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    text = file.read()
                    textEdit.setText(text)
                    self.statusBar().showMessage(f"Opened file: {file_name}", 3000)
                    self.current_file = file_name # set current file.
                    self.tabWidget.setTabText(self.tabWidget.currentIndex(), file_name.split('/')[-1]) # set tab name
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {e}")
                self.statusBar().showMessage(f"Error opening file: {e}", 3000)

    def saveFile(self):
        """
        Saves the content of the text edit widget to the current file.
        If no file is currently open, it calls saveAsFile().
        """
        textEdit = self.getCurrentTextEdit()
        if textEdit is None:
            return

        if hasattr(self, 'current_file'):
            try:
                with open(self.current_file, 'w') as file:
                    file.write(textEdit.toPlainText())
                self.statusBar().showMessage(f"Saved to {self.current_file}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")
                self.statusBar().showMessage(f"Error saving file: {e}", 3000)
        else:
            self.saveAsFile()

    def saveAsFile(self):
        """
        Saves the content of the text edit widget to a new file.
        """
        textEdit = self.getCurrentTextEdit()
        if textEdit is None:
            return

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(textEdit.toPlainText())
                self.current_file = file_name
                self.statusBar().showMessage(f"Saved as {file_name}", 3000)
                self.tabWidget.setTabText(self.tabWidget.currentIndex(), file_name.split('/')[-1]) # set tab name
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")
                self.statusBar().showMessage(f"Error saving file: {e}", 3000)

    def setFont(self):
        """
        Opens a font dialog and sets the selected font for the text edit widget.
        """
        textEdit = self.getCurrentTextEdit()
        if textEdit is None:
            return

        font, ok = QFontDialog.getFont(self.default_font, self)
        if ok:
            textEdit.setFont(font)
            self.default_font = font

    def setColor(self):
        """
        Opens a color dialog and sets the selected text color for the text edit widget.
        """
        textEdit = self.getCurrentTextEdit()
        if textEdit is None:
            return
        color = QColorDialog.getColor(Qt.black, self)
        if color.isValid():
            textEdit.setTextColor(color)

    def showAbout(self):
        """Displays a simple About dialog box."""
        QMessageBox.about(self, "About PyQt5 Word Editor",
                            "This is a basic word processor application created with PyQt5.")

    def updateWordCount(self):
        """
        Updates the word count in the status bar for the current tab.
        """
        textEdit = self.getCurrentTextEdit()
        if textEdit is None:
            return  # Exit if there's no active text edit

        # Use a timer to delay the actual word count calculation
        # This improves performance, especially with large documents.
        self.wordCountTimer.start(200)

        text = textEdit.toPlainText()
        words = text.split()
        word_count = len(words)
        self.wordCountLabel.setText(f"Words: {word_count}")
        self.statusBar().showMessage(f"Word Count: {word_count}", 3000)

    def applyDarkModeSettings(self):
        """
        Applies dark mode settings to the application.
        """
        if self.darkModeAction.isChecked():
            QApplication.setStyle(QStyleFactory.create("Fusion"))  # Use Fusion style for better dark mode
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(45, 45, 45))
            palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
            palette.setColor(QPalette.Base, QColor(30, 30, 30))
            palette.setColor(QPalette.Text, QColor(220, 220, 220))
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
            palette.setColor(QPalette.Highlight, QColor(100, 100, 150))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
            QApplication.setPalette(palette)



            # Style the tab widget for dark mode
            self.tabWidget.setStyleSheet("""
                QTabWidget::pane {
                    background-color: #2d2d2d;
                    border: none;
                }
                QTabBar::tab {
                    background-color: #333333;
                    color: #dddddd;
                    border: 1px solid #555555;
                    border-bottom: none;
                    padding: 8px 20px;
                    min-width: 80px;
                }
                QTabBar::tab:selected {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QTabBar::tab:hover {
                    background-color: #444444;
                }
                QTabBar::close-button {
                    image: url(close.png); /* Replace with a path to a close icon */
                    subcontrol-position: right;
                    margin-left: 10px;
                    border: none;
                }
                QTabBar::close-button:hover {
                    image: url(close-hover.png);  /* Replace with a path to a close hover icon */
                }
            """)
        else:
            QApplication.setStyle(QStyleFactory.create("windows"))  # Or "Fusion", or whatever the default is
            QApplication.setPalette(QApplication.style().standardPalette())  # Reset to default palette
            self.tabWidget.setStyleSheet("") # reset tab style

    def toggleDarkMode(self, checked):
        """
        Toggles dark mode on or off.
        """
        self.applyDarkModeSettings() # apply settings.

if __name__ == '__main__':
    # Create the application instance
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    # Create and show the main window
    word_editor = WordEditor()
    # Start the event loop
    sys.exit(app.exec_())
