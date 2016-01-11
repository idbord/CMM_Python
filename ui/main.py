# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from test.lexerTest import lexer
from test.parserTest import parser
from test.generatorTest import generator
from test.interpreterTest import interpreter


class Ui_main(object):
    path = None

    def setupUi(self, main):
        main.setObjectName("main")
        main.resize(701, 520)
        self.centralwidget = QtWidgets.QWidget(main)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(3, 2, 641, 360))
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.setObjectName("textEdit")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(3, 370, 641, 115))
        self.textBrowser.setAutoFillBackground(True)
        self.textBrowser.setObjectName("textBrowser")
        main.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 701, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuWork = QtWidgets.QMenu(self.menubar)
        self.menuWork.setObjectName("menuWork")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        main.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main)
        self.statusbar.setObjectName("statusbar")
        main.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(main)
        self.toolBar.setObjectName("toolBar")
        main.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionNew = QtWidgets.QAction(main)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(main)
        self.actionOpen.setObjectName("actionOpen")
        self.actionStore = QtWidgets.QAction(main)
        self.actionStore.setObjectName("actionStore")
        self.actionExit = QtWidgets.QAction(main)
        self.actionExit.setObjectName("actionExit")
        self.actionLexer = QtWidgets.QAction(main)
        self.actionLexer.setObjectName("actionLexer")
        self.actionParser = QtWidgets.QAction(main)
        self.actionParser.setObjectName("actionParser")
        self.actionGenerator = QtWidgets.QAction(main)
        self.actionGenerator.setObjectName("actionGenerator")
        self.actionInterpreter = QtWidgets.QAction(main)
        self.actionInterpreter.setObjectName("actionInterpreter")
        self.actionRun = QtWidgets.QAction(main)
        self.actionRun.setObjectName("actionRun")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionStore)
        self.menuFile.addAction(self.actionExit)
        self.menuWork.addAction(self.actionLexer)
        self.menuWork.addAction(self.actionParser)
        self.menuWork.addAction(self.actionGenerator)
        self.menuWork.addAction(self.actionInterpreter)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuWork.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionStore)
        self.toolBar.addAction(self.actionRun)

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "CMM解释器——Python版"))
        self.menuFile.setTitle(_translate("main", "文件"))
        self.menuWork.setTitle(_translate("main", "操作"))
        self.menuAbout.setTitle(_translate("main", "关于"))
        self.toolBar.setWindowTitle(_translate("main", "toolBar"))
        self.actionNew.setText(_translate("main", "新建"))
        self.actionNew.setShortcut(_translate("main", "Ctrl+N"))
        self.actionOpen.setText(_translate("main", "打开"))
        self.actionStore.setText(_translate("main", "保存"))
        self.actionStore.setShortcut(_translate("main", "Ctrl+S"))
        self.actionExit.setText(_translate("main", "退出"))
        self.actionExit.setShortcut(_translate("main", "Esc"))
        self.actionLexer.setText(_translate("main", "Lexer"))
        self.actionLexer.setShortcut(_translate("main", "Ctrl+L"))
        self.actionParser.setText(_translate("main", "Parser"))
        self.actionParser.setShortcut(_translate("main", "Ctrl+P"))
        self.actionGenerator.setText(_translate("main", "Generator"))
        self.actionGenerator.setShortcut(_translate("main", "Ctrl+G"))
        self.actionInterpreter.setText(_translate("main", "Interpreter"))
        self.actionInterpreter.setShortcut(_translate("main", "Ctrl+I"))
        self.actionRun.setText(_translate("main", "Run"))
        self.actionRun.setShortcut(_translate("main", "Ctrl+R"))

    # 绑定事件
    def bind_event(self):
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionStore.triggered.connect(self.store_file)
        self.actionExit.triggered.connect(self.exit)

        self.actionLexer.triggered.connect(self.lexer)
        self.actionParser.triggered.connect(self.parser)
        self.actionGenerator.triggered.connect(self.generator)
        self.actionInterpreter.triggered.connect(self.interpreter)

    # 新建文件
    def new_file(self):
        pass

    # 打开文件
    def open_file(self):
        file_path, selected_filter = QtWidgets.QFileDialog().getOpenFileName()
        Ui_main.path = file_path
        stream = open(file_path, 'r')
        content = stream.read()
        stream.close()
        self.textEdit.setText(content)

    # 存储文件
    def store_file(self):
        content = self.textEdit.toPlainText()
        if Ui_main.path is None:
            file_path, selected_filter = QtWidgets.QFileDialog().getSaveFileName()
            QtWidgets.QFileDialog().Options(QtWidgets.QFileDialog().DontConfirmOverwrite)
            f = open(file_path, 'w')
            f.write(content.encode('utf-8'))
            f.close()
            Ui_main.path = file_path
        else:
            f = open(Ui_main.path, 'w')
            f.write(content.encode('utf-8'))
            f.close()

    def exit(self):
        self.store_file()
        QtWidgets.qApp.quit()

    # 词法分析
    def lexer(self):
        self.store_file()
        self.textBrowser.clear()
        result = lexer(Ui_main.path)
        for i in result:
            self.textBrowser.append(i)

    # 语法分析
    def parser(self):
        self.store_file()
        self.textBrowser.clear()
        result = parser(Ui_main.path)
        for i in result:
            self.textBrowser.append(i)

    # 生成中间代码
    def generator(self):
        self.store_file()
        self.textBrowser.clear()
        result = generator(Ui_main.path)
        for i in result:
            self.textBrowser.append(i)

    # 解释执行
    def interpreter(self):
        self.store_file()
        self.textBrowser.clear()
        result = interpreter(Ui_main.path)
        for i in result:
            self.textBrowser.append(str(i))