from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QInputDialog, QTableWidget, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject, QThread, QThreadPool
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import string
import time
from collections import OrderedDict
from logic.learner import write_json_in_file
import traceback
import threading
import learn as learn_module
import benchmark as bench_module
from learn import main as Learn
from decrypt import main as Decrypt
from encrypt import main as Encrypt
from benchmark import main as Benchmark
import logic.decryptor as decrypt_module
import decrypt as decrypt_main_module



class Window(object):
    def __init__(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(468, 354)
        self.centralWidget = QtWidgets.QWidget(main_window)
        self.centralWidget.setObjectName("centralWidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 451, 291))
        self.tabWidget.setObjectName("tabWidget")

        '''Encrypt Tab'''
        self.Encrypt = QtWidgets.QWidget()
        self.Encrypt.setObjectName("Encrypt")
        self.encrypt_select_substitution = QtWidgets.QPushButton(self.Encrypt)
        self.encrypt_select_substitution.setGeometry(QtCore.QRect(140, 70, 141, 23))
        self.encrypt_select_substitution.setObjectName("encrypt_select_substitution")
        self.encrypt_generate_subst = QtWidgets.QCheckBox(self.Encrypt)
        self.encrypt_generate_subst.setGeometry(QtCore.QRect(140, 150, 191, 17))
        self.encrypt_generate_subst.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.encrypt_generate_subst.setObjectName("encrypt_generate_subst")
        self.encrypt_select_files_button = QtWidgets.QPushButton(self.Encrypt)
        self.encrypt_select_files_button.setGeometry(QtCore.QRect(140, 30, 141, 23))
        self.encrypt_select_files_button.setObjectName("encrypt_select_files_button")
        self.encrypt_button = QtWidgets.QPushButton(self.Encrypt)
        self.encrypt_button.setGeometry(QtCore.QRect(170, 200, 75, 23))
        self.encrypt_button.setObjectName("encrypt_button")
        self.tabWidget.addTab(self.Encrypt, "")

        '''Decrypt Tab'''
        self.Decrypt = QtWidgets.QWidget()
        self.Decrypt.setObjectName("Decrypt")
        self.label_3 = QtWidgets.QLabel(self.Decrypt)
        self.label_3.setGeometry(QtCore.QRect(131, 161, 118, 16))
        self.label_3.setObjectName("label_3")
        self.decrypt_select_encrypt_files_button = QtWidgets.QPushButton(self.Decrypt)
        self.decrypt_select_encrypt_files_button.setGeometry(QtCore.QRect(150, 60, 141, 23))
        self.decrypt_select_encrypt_files_button.setObjectName("decrypt_select_encrypt_files_button")
        self.decrypt_select_stat_button = QtWidgets.QPushButton(self.Decrypt)
        self.decrypt_select_stat_button.setGeometry(QtCore.QRect(180, 20, 75, 23))
        self.decrypt_select_stat_button.setObjectName("decrypt_select_stat_button")
        self.decrypt_button = QtWidgets.QPushButton(self.Decrypt)
        self.decrypt_button.setGeometry(QtCore.QRect(190, 220, 75, 23))
        self.decrypt_button.setObjectName("decrypt_button")
        self.decrypt_variants_amount = QtWidgets.QSpinBox(self.Decrypt)
        self.decrypt_variants_amount.setGeometry(QtCore.QRect(255, 161, 37, 20))
        self.decrypt_variants_amount.setMaximum(20)
        self.decrypt_variants_amount.setProperty("value", 10)
        self.decrypt_variants_amount.setObjectName("decrypt_variants_amount")
        self.decrypt_progress = QtWidgets.QProgressBar(self.Decrypt)
        self.decrypt_progress.setGeometry(100, 187, 250, 20)

        '''Learn Tab'''
        self.learn_popular_words_box_3 = QtWidgets.QSpinBox(self.Decrypt)
        self.learn_popular_words_box_3.setGeometry(QtCore.QRect(229, 111, 55, 20))
        self.learn_popular_words_box_3.setMinimum(10000)
        self.learn_popular_words_box_3.setMaximum(20000)
        self.learn_popular_words_box_3.setSingleStep(10)
        self.learn_popular_words_box_3.setProperty("value", 15000)
        self.learn_popular_words_box_3.setObjectName("learn_popular_words_box_3")
        self.label_11 = QtWidgets.QLabel(self.Decrypt)
        self.label_11.setGeometry(QtCore.QRect(151, 111, 72, 16))
        self.label_11.setObjectName("label_11")
        self.tabWidget.addTab(self.Decrypt, "")
        self.Learn = QtWidgets.QWidget()
        self.Learn.setObjectName("Learn")
        self.learn_select_files_button = QtWidgets.QPushButton(self.Learn)
        self.learn_select_files_button.setGeometry(QtCore.QRect(130, 30, 141, 23))
        self.learn_select_files_button.setObjectName("learn_select_files_button")
        self.label_5 = QtWidgets.QLabel(self.Learn)
        self.label_5.setGeometry(QtCore.QRect(131, 141, 72, 16))
        self.label_5.setObjectName("label_5")
        self.learn_button = QtWidgets.QPushButton(self.Learn)
        self.learn_button.setGeometry(QtCore.QRect(160, 210, 75, 23))
        self.learn_button.setObjectName("learn_button")
        self.learn_update_file_button = QtWidgets.QPushButton(self.Learn)
        self.learn_update_file_button.setGeometry(QtCore.QRect(160, 70, 75, 23))
        self.learn_update_file_button.setObjectName("learn_update_file_button")
        self.learn_popular_words_box = QtWidgets.QSpinBox(self.Learn)
        self.learn_popular_words_box.setGeometry(QtCore.QRect(209, 141, 55, 20))
        self.learn_popular_words_box.setMinimum(10000)
        self.learn_popular_words_box.setMaximum(20000)
        self.learn_popular_words_box.setSingleStep(10)
        self.learn_popular_words_box.setProperty("value", 15000)
        self.learn_popular_words_box.setObjectName("learn_popular_words_box")
        self.learn_progress = QtWidgets.QProgressBar(self.Learn)
        self.learn_progress.setGeometry(90, 105, 250, 20)
        self.tabWidget.addTab(self.Learn, "")

        '''Benchmark Tab'''
        self.Benchmark = QtWidgets.QWidget()
        self.Benchmark.setObjectName("Benchmark")
        self.benchmark_select_stat_button = QtWidgets.QPushButton(self.Benchmark)
        self.benchmark_select_stat_button.setGeometry(QtCore.QRect(300, 10, 101, 23))
        self.benchmark_select_stat_button.setObjectName("benchmark_select_stat_button")
        self.benchmark_select_files_button = QtWidgets.QPushButton(self.Benchmark)
        self.benchmark_select_files_button.setGeometry(QtCore.QRect(290, 40, 141, 31))
        self.benchmark_select_files_button.setObjectName("benchmark_select_files_button")
        self.benchmark_debug = QtWidgets.QCheckBox(self.Benchmark)
        self.benchmark_debug.setGeometry(QtCore.QRect(320, 80, 70, 17))
        self.benchmark_debug.setObjectName("benchmark_debug")
        self.benchmark_iterations = QtWidgets.QSpinBox(self.Benchmark)
        self.benchmark_iterations.setGeometry(QtCore.QRect(370, 120, 61, 20))
        self.benchmark_iterations.setWrapping(False)
        self.benchmark_iterations.setFrame(True)
        self.benchmark_iterations.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.benchmark_iterations.setProperty("showGroupSeparator", False)
        self.benchmark_iterations.setMaximum(1000)
        self.benchmark_iterations.setProperty("value", 50)
        self.benchmark_iterations.setObjectName("benchmark_iterations")
        self.label = QtWidgets.QLabel(self.Benchmark)
        self.label.setGeometry(QtCore.QRect(300, 120, 51, 16))
        self.label.setObjectName("label")
        self.benchmark_button = QtWidgets.QPushButton(self.Benchmark)
        self.benchmark_button.setGeometry(QtCore.QRect(320, 220, 75, 23))
        self.benchmark_button.setObjectName("benchmark_button")
        self.plot_canvas = QtWidgets.QWidget(self.Benchmark)
        self.plot_canvas.setGeometry(QtCore.QRect(10, 10, 271, 251))
        self.plot_canvas.setObjectName("plot_canvas")
        self.benchmark_progress = QtWidgets.QProgressBar(self.Benchmark)
        self.benchmark_progress.setGeometry(290, 190, 170, 20)
        self.benchmark_popular_words_box = QtWidgets.QSpinBox(self.Benchmark)
        self.benchmark_popular_words_box.setGeometry(QtCore.QRect(370, 160, 61, 22))
        self.benchmark_popular_words_box.setMinimum(10000)
        self.benchmark_popular_words_box.setMaximum(20000)
        self.benchmark_popular_words_box.setSingleStep(10)
        self.benchmark_popular_words_box.setProperty("value", 15000)
        self.benchmark_popular_words_box.setObjectName("benchmark_popular_words_box")
        self.label_6 = QtWidgets.QLabel(self.Benchmark)
        self.label_6.setGeometry(QtCore.QRect(290, 160, 81, 21))
        self.label_6.setObjectName("label_6")
        self.tabWidget.addTab(self.Benchmark, "")
        main_window.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(main_window)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 468, 21))
        self.menuBar.setObjectName("menuBar")
        main_window.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(main_window)
        self.mainToolBar.setObjectName("mainToolBar")
        main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(main_window)
        self.statusBar.setObjectName("statusBar")
        main_window.setStatusBar(self.statusBar)
        self.plot = None
        self.files = None
        self.file = None
        self.update_file = None
        self.stat = None
        self.subst = None
        self.layout = QtWidgets.QVBoxLayout(self.plot_canvas)
        self.retranslate_gui(main_window)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_gui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowIcon(QIcon('icon.png'))
        main_window.setWindowTitle(_translate("main_window", "Ciphers"))
        self.encrypt_select_substitution.setText(_translate("main_window", "Set Substitution"))
        self.encrypt_generate_subst.setText(_translate("main_window", "Generate Substitution File"))
        self.encrypt_select_files_button.setText(_translate("main_window", "Select File for Encrypt"))
        self.encrypt_button.setText(_translate("main_window", "Encrypt"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Encrypt), _translate("main_window", "Encrypt"))

        '''ENCRYPT BUTTONS'''
        self.encrypt_select_files_button.clicked.connect(self.open_single_file)
        self.encrypt_select_substitution.clicked.connect(self.substitution_dialog)
        self.encrypt_button.clicked.connect(self.encrypt_loader)

        self.label_3.setText(_translate("main_window", "Max amount of variants:"))
        self.decrypt_select_encrypt_files_button.setText(_translate("main_window", "Select Encrypted File"))
        self.decrypt_select_stat_button.setText(_translate("main_window", "Select Stat"))
        self.decrypt_button.setText(_translate("main_window", "Decrypt"))
        self.label_11.setText(_translate("main_window", "Popular words:"))

        '''DECRYPT BUTTONS'''
        self.decrypt_select_encrypt_files_button.clicked.connect(self.open_single_file)
        self.decrypt_select_stat_button.clicked.connect(self.open_stat)
        self.decrypt_button.clicked.connect(self.decrypt_loader)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Decrypt), _translate("main_window", "Decrypt"))
        self.learn_select_files_button.setText(_translate("main_window", "Select Files For Learning"))
        self.label_5.setText(_translate("main_window", "Popular words:"))
        self.learn_button.setText(_translate("main_window", "Learn"))
        self.learn_update_file_button.setText(_translate("main_window", "Update File"))
        self.label_5.setText(_translate("main_window", "Popular words:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Learn), _translate("main_window", "Learn"))
        self.benchmark_select_stat_button.setText(_translate("main_window", "Select Stat"))

        '''LEARN BUTTONS'''
        self.learn_select_files_button.clicked.connect(self.open_multiple_files)
        self.learn_update_file_button.clicked.connect(self.open_learn_update)
        self.learn_button.clicked.connect(self.learn_loader)

        self.benchmark_select_stat_button.setText(_translate("main_window", "Select Statistics"))
        self.benchmark_select_files_button.setText(_translate("main_window", "Select File for Encrypt"))
        self.benchmark_debug.setText(_translate("main_window", "Debug"))
        self.benchmark_iterations.setSpecialValueText(_translate("main_window", "Iterations"))
        self.label.setText(_translate("main_window", "Iterations:"))
        self.benchmark_button.setText(_translate("main_window", "Run"))
        self.label_6.setText(_translate("main_window", "Popular words:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Benchmark), _translate("main_window", "Benchmark"))

        '''BENCHMARK BUTTONS'''
        self.benchmark_select_files_button.clicked.connect(self.open_single_file)
        self.benchmark_select_stat_button.clicked.connect(self.open_stat)
        self.benchmark_button.clicked.connect(self.benchmark_loader)

        self.threadpool = QThreadPool()
        self.plot = QtWidgets.QWidget()
        self.layout.addWidget(self.plot)


    def open_stat(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(main_window, "Select file with Statistics", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if filename:
            self.stat = filename

    def open_multiple_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(main_window, "Select files...", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            self.files = files

    def open_single_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(main_window, "Select file...", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if filename:
            self.file = filename

    def open_learn_update(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(main_window, "Select file...", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if filename:
            self.update_file = filename

    def substitution_dialog(self):
        text, ok = QInputDialog.getText(main_window, 'Substitution',
                                        'Enter your substitution:', text='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower())
        if ok:
            subst = OrderedDict(zip(string.ascii_lowercase, list(str(text))))
            write_json_in_file('subst.txt', subst, 'utf-8')
            self.subst = 'subst.txt'

    def variant_picker_dialog(self):
        items = ("0","1","2")
        item, ok = QInputDialog.getItem(main_window, 'Pick The Best Variant',
                                        'Select:', items, 0, False)
        if ok and item:
            print('Ok')

    """FUNCTIONS FOR BUTTONS"""

    def decrypt_loader(self):
        worker = Decryptor(stat=self.stat, file=self.file, top=self.learn_popular_words_box_3.value(),
                           variants=self.decrypt_variants_amount.value())
        worker.signals.finished.connect(self.variant_picker_dialog)
        self.threadpool.start(worker)


    def plot_generator(self, coords):
        x, y = coords
        self.layout.removeWidget(self.plot)
        self.plot = Plot(self.plot_canvas, x_coord=x, y_coord=y, width=5, height=4, dpi=100)
        self.layout.addWidget(self.plot)

    def benchmark_loader(self):
        worker = Benchmarker(self.stat, self.file, self.benchmark_iterations.value(),
                              self.benchmark_popular_words_box.value(), self.benchmark_debug.isChecked())
        worker.signals.result.connect(self.plot_generator)
        self.threadpool.start(worker)

    def learn_progress_bar(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            self.learn_progress.setValue(learn_module.workdone*100)
            time.sleep(1)
        print('Thread Completed')

    def learn_loader(self):
        t = threading.Thread(target=self.learn_progress_bar)
        t.start()
        learner = Learner(self.files, self.update_file, self.learn_popular_words_box.value())
        if learner.signals.finished is True:
            t.do_run = False
            t.join()
        self.threadpool.start(learner)
        self.file = None

    def encrypt_loader(self):
        Encrypt(self.file, substitution=self.subst, save=self.encrypt_generate_subst.isChecked(), output='crypto.txt')

class ThreadSignals(QObject):
    finished = pyqtSignal(bool)
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Decryptor(QRunnable):
    def __init__(self, stat, file, top, variants):
        super(Decryptor, self).__init__()
        self.file = file
        self.stat = stat
        self.top = top
        self.variants = variants
        self.signals = ThreadSignals()

    @pyqtSlot()
    def run(self):
        try:
            Decrypt(self.stat, self.file, self.top, self.variants)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(None)
        finally:
            self.signals.finished.emit()


class Learner(QRunnable):
    def __init__(self, files, file, top):
        super(Learner, self).__init__()
        self.files = files
        self.file = file
        self.top = top
        self.signals = ThreadSignals()

    @pyqtSlot()
    def run(self):
        try:
            Learn(files=self.files, update_file=self.file, top=self.top)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(None)
        finally:
            self.signals.finished.emit(True)


class Benchmarker(QRunnable):
    def __init__(self, stat, file, iterations, top, debug):
        super(Benchmarker, self).__init__()
        self.stat = stat
        self.file = file
        self.iterations = iterations
        self.top = top
        self.debug = debug
        self.signals = ThreadSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = Benchmark(self.stat, self.file, self.iterations, self.top, self.debug)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()

class Plot(FigureCanvas):
    def __init__(self, parent=None, x_coord=None, y_coord=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.plot(x_coord, y_coord, color='black')
        self.axes.set(xlabel="Text's length", ylabel="Success rate, %", title="Benchmark")
        self.axes.grid(True)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self, x_coord, y_coord):
        self.axes.plot(x_coord, y_coord)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    gui = Window(main_window)
    main_window.show()
    sys.exit(app.exec_())
