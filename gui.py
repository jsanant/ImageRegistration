import sys
import subprocess
from PyQt4 import QtGui
from PyQt4 import QtCore


class Window(QtGui.QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.initUI()

    def initUI(self):

        self.browse1 = QtGui.QPushButton('Browse')
        self.browse2 = QtGui.QPushButton('Browse')
        self.align = QtGui.QPushButton('Align Images')


        self.edit1 = QtGui.QLineEdit()
        self.edit2 = QtGui.QLineEdit()

        grid = QtGui.QGridLayout()
        grid.setSpacing(1)

        grid.addWidget(self.edit1, 1,0)
        grid.addWidget(self.browse1, 1, 1)

        grid.addWidget(self.edit2, 2, 0)
        grid.addWidget(self.browse2, 2, 1)

        grid.addWidget(self.align, 3,0)

        self.setLayout(grid)

        self.browse1.connect(self.browse1,QtCore.SIGNAL("clicked()"),self.on_click1)
        self.browse2.connect(self.browse2,QtCore.SIGNAL("clicked()"),self.on_click2)
        self.align.connect(self.align,QtCore.SIGNAL("clicked()"),self.align_image)

        self.setGeometry(200, 200,550, 400)
        self.setWindowTitle('Image Registration')
        self.setWindowIcon(QtGui.QIcon('python-logo.png'))
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_click1(self):
        global fileName1
        filePath1 = QtGui.QFileDialog.getOpenFileName(self, "Open File",QtCore.QDir.currentPath())

        print filePath1

        fileInfo=QtCore.QFileInfo(filePath1)
        fileName1=fileInfo.fileName()

        print fileName1

        if fileName1:
            image = QtGui.QImage(fileName1)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Registration","Please load an image file.")
                return

        self.edit1.setText(filePath1)

    def on_click2(self):
        global fileName2
        filePath2 = QtGui.QFileDialog.getOpenFileName(self, "Open File",QtCore.QDir.currentPath())

        print filePath2

        fileInfo=QtCore.QFileInfo(filePath2)
        fileName2=fileInfo.fileName()
        print fileName2

        if fileName2:
            image = QtGui.QImage(fileName2)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Registration","Please load an image file.")
                return

        self.edit2.setText(filePath2)

    def align_image(self):

        try:
            subprocess.call([sys.executable, 'align.py', fileName1,fileName2])
        except NameError as e:
            QtGui.QMessageBox.information(self, "Image Registration","Please select a file first.")
        else:
            return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window= Window()
    window.show()
    app.exec_()
