# coding: utf-8
import serial
import sys, time

 # �ʼ������� �ҷ��;��� QT ���̺귯��
from PyQt4 import QtGui, QtCore
from ui import Ui_Dialog # UI �� �ִ� ����

# RX Thread

class serialHandler():
    def __init__(self, ui):
        self.serialComport = 0
        self.serialBaudrate = [0, 0]
        self.serialDataBit = 0
        self.serialStopBit = 0
        self.Buf = []
        self.ui = ui
        global Buf 

    def connectSerial(self):          # �����͸� ��û�ϴ� �Լ�
        try:                          # ���� �õ�
            self.ser = serial.Serial(self.serialComport, self.serialBaudrate[0], timeout=0.5)
        except serial.SerialException:
            return -1
        else:
            if self.ser.isOpen():
                return 0

    def getData(self, ch):
        self.ser.write(ch)

    def readData(self):
        self.Buf = self.ser.readline(255)
        if len(self.Buf) == 0:  # ���� �����Ͱ� ���ٸ� ȭ�鿡 ������� �ʰ� ���� 
            return
        else:
            print self.Buf[:16]
            # self.ui.tableWidget.setItem(0, 0, QtGui.QTableWidgetItem("Hi"))
            self.ui.textEdit.append(self.Buf[:16])
            
        
        
class rxThread(QtCore.QThread):
    def __init__(self, ser, ui, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.ser = ser
        self.ui = ui
        global Buf

    def run(self):
        while True:
            # QtCore.QThread.msleep(100)
            self.ser.readData()

# MyForm Ŭ���� ����
class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.handler = serialHandler(self.ui)
        self.rxThread_inst = rxThread(self.handler, self.ui)
        # self.dataProc = 

    # GUI���� �̺�Ʈ�� ���� �ñ׳��� ���� ���� �Լ�
    # �ش� �̺�Ʈ�� ���� �Լ� ȣ��

    def connectSerial(self):          # �����͸� ��û�ϴ� �Լ�
        if 0 == self.handler.connectSerial():
            self.ui.textEdit.setText("CONNECT SUCCEED!")
            self.rxThread_inst.start()
            # self.dip_inst.start()
        else:
            self.ui.textEdit.setText("CONNECT FAILED!")

    def changedSerialConfig(self):
        self.handler.serialComport = self.ui.comboBox_ComPort.currentIndex()
        self.handler.serialBaudrate = self.ui.comboBox_Baudrate.currentText().toInt()

    def getData(self):          # �����͸� ��û�ϴ� �Լ�
        self.handler.getData('p')

    def saveData(self):
        self.fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '.csv')
        self.fname = open(self.fileName, 'w')
        self.fname.write(self.ui.textEdit.toPlainText())
        self.fname.close()














        
# python sample_main.py �� ���� �������� ��� '��'�� �Ǿ� �Ʒ��� ����
if __name__ == "__main__":
    threads = []
    Buf = []
    
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
