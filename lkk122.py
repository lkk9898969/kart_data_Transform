from PyQt6 import QtCore, QtGui, QtWidgets
from base64 import b64decode
from icon import img
from UI import Ui_Kart_Data_Transfer,Ui_Kart_Data_Transfer_Add
import Additional_class

class Mainwindow_Controller(QtWidgets.QWidget,Ui_Kart_Data_Transfer):
    def __init__(self) -> None:
        super().__init__(flags=QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setupUi(self)
        pm = QtGui.QPixmap()
        pm.loadFromData(b64decode(img))
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(pm)
        self.setWindowIcon(self.icon)
        self.setdata()
        self.setController()

    def setdata(self):
        self.file=Additional_class.formula_file_processer("Data.data")
        self.file.read()
        self.Data_select.addItems([i.dataname for i in self.file.data.values()])
        self.Data=self.file.data[self.Data_select.currentText()]
        self.Param_in_xml.setValidator(QtGui.QDoubleValidator(parent=self))
        self.Param_in_game.setValidator(QtGui.QDoubleValidator(parent=self))
        self.selectdata_changed()

    def setController(self):
        self.Data_select.currentTextChanged.connect(self.selectdata_changed)
        self.Param_in_xml.textEdited.connect(self.ParaminXml_changed)
        self.Param_in_game.textEdited.connect(self.ParaminGame_changed)
        self.Add_formula.clicked.connect(self.ShowAddDataWindow)

    def selectdata_changed(self):
        self.Data=self.file.data[self.Data_select.currentText()]
        self.Param_in_game.setText('0')
        self.Param_in_xml.setText('0')
        self.Formula.setText("y = "+self.Data.formula.OutputInfixformula())
        self.Default_param.setText("Default : "+ str(self.Data['default']))
        self.Param_in_xml.setEnabled(self.Data.useable)
        self.Param_in_game.setEnabled(self.Data.useable)

    def ParaminXml_changed(self):
        text=self.Param_in_xml.text()
        try:
            evaluate=self.Data.formula.evaluate(float(text))
        except ValueError:
            evaluate=self.Data.formula.evaluate(0)
        self.Param_in_game.setText(Additional_class.float_to_str(evaluate))
    
    def ParaminGame_changed(self):
        text=self.Param_in_game.text()
        try:
            evaluate=self.Data.formula.verylimit_formulainvert_evaluate(float(text))
        except ValueError:
            evaluate=self.Data.formula.verylimit_formulainvert_evaluate(0)
        self.Param_in_xml.setText(Additional_class.float_to_str(evaluate))
    
    def ShowAddDataWindow(self):
        self.AddDataUI=AddDataWindow_Controller(None,QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint,self.icon)
        self.AddDataUI.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.AddDataUI.senddatasingnal.connect(self.AddData)
        self.AddDataUI.sendchecksingnal.connect(self.checkDataname)
        self.AddDataUI.show()
    
    def checkDataname(self,arg:str):
        try:
            self.file.checkDataname(arg)
            self.AddDataUI.receivesingnal.emit(False)
        except KeyError:
            self.AddDataUI.receivesingnal.emit(True)

    def AddData(self,arg:Additional_class.formula_data):
        self.file.newData(arg.dataname,arg.formula,arg.default,arg.useable)
        self.Data_select.currentTextChanged.disconnect()
        self.Data_select.clear()
        self.Data_select.addItems([i.dataname for i in self.file.data.values()])
        self.Data_select.currentTextChanged.connect(self.selectdata_changed)
        self.file.file_write()


class AddDataWindow_Controller(QtWidgets.QWidget,Ui_Kart_Data_Transfer_Add):
    senddatasingnal=QtCore.pyqtSignal(Additional_class.formula_data)
    sendchecksingnal=QtCore.pyqtSignal(str)
    receivesingnal=QtCore.pyqtSignal(bool)
    def __init__(self, parent: QtWidgets.QWidget | None = ..., flags: QtCore.Qt.WindowType = ...,icon:QtGui.QIcon =...) -> None:
        super().__init__(parent, flags)
        self.setupUi(self)
        self.setWindowIcon(icon)
        self.Data=Additional_class.formula_data("",[0,0,0,0])
        self.setControl()
        

    def setControl(self):
        self.receivesingnal.connect(self.signalreceived)
        self.Param_in_xml_input1.setText('0')
        self.Param_in_xml_input2.setText('0')
        self.Param_in_game_input1.setText('0')
        self.Param_in_game_input2.setText('0')
        self.Param_in_xml_input1.setValidator(QtGui.QDoubleValidator(parent=self))
        self.Param_in_xml_input1.textEdited.connect(self.paramchanged)
        self.Param_in_xml_input2.setValidator(QtGui.QDoubleValidator(parent=self))
        self.Param_in_xml_input2.textEdited.connect(self.paramchanged)
        self.Param_in_game_input1.setValidator(QtGui.QDoubleValidator(parent=self))
        self.Param_in_game_input1.textEdited.connect(self.paramchanged)
        self.Param_in_game_input2.setValidator(QtGui.QDoubleValidator(parent=self))
        self.Param_in_game_input2.textEdited.connect(self.paramchanged)
        re=QtCore.QRegularExpression("[a-z|A-Z]+")
        self.Name_input.setValidator(QtGui.QRegularExpressionValidator(re,self))
        self.Name_input.textEdited.connect(self.datanamechanged)
        self.Param_default_input.setValidator(QtGui.QDoubleValidator(parent=self))
        self.Param_default_input.textEdited.connect(self.defaultchanged)
        self.Formula.setText("y = "+self.Data.formula.OutputInfixformula())
        self.Save_formula.setEnabled(False)
        self.Save_formula.clicked.connect(self.save)
        
    def paramchanged(self):
        data=[self.Param_in_xml_input1.text(),self.Param_in_xml_input2.text(),
              self.Param_in_game_input1.text(),self.Param_in_game_input2.text()]
        for i,j in enumerate(data):
            try:
                data[i]=float(j)
            except ValueError:
                data[i]=0

        self.Data.CreateFormula(data)
        self.Formula.setText("y = "+self.Data.formula.OutputInfixformula())
    
    def datanamechanged(self):
        text=self.Name_input.text()
        self.sendchecksingnal.emit(text)
        if text=='':
            self.Save_formula.setEnabled(False)
    
    def defaultchanged(self):
        default=self.Param_default_input.text()
        if default=='':
            default= None
        self.Data.default=default
    
    def save(self):
        self.senddatasingnal.emit(self.Data)
        self.close()

    def signalreceived(self,arg:bool):
        if arg:
            self.Data_name_check.setText("該數據名稱已存在!")
            self.Save_formula.setEnabled(False)
            return
        self.Data_name_check.setText(None)
        self.Save_formula.setEnabled(True)
        self.Data.dataname=self.Name_input.text()


if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Mainwindow_Controller()
    window.show()
    sys.exit(app.exec())