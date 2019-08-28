import sys
import os
import multiprocessing # Stops multiple app opens
from PyQt5 import QtCore, QtGui, QtWidgets, uic
#import numpy.random.common # Needed for fbs build
#import numpy.random.bounded_integers # Needed for fbs build
#import numpy.random.entropy # Needed for fbs build
import scanpy as sc
import matplotlib
matplotlib.use('Qt5Agg')
from fbs_runtime.application_context.PyQt5 import ApplicationContext, \
    cached_property
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QToolTip, QMessageBox, QListWidget, QListView, QLabel, QFileDialog, QWidget, QLineEdit, QAction, QAbstractItemView)

def resource_path(relative_path): # Get the UI Full Path *ONLY REQUIRED FOR FBS BUILD*
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

qtCreatorFile = resource_path("mainwindow.ui") # UI file from QT Designer here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) #loads UI class

class AppContext(ApplicationContext):  #FOR FBS PACKAGING
    def run(self):
        self.main_window.show()
        return self.app.exec_()

    @cached_property
    def main_window(self):
        return MyWindow()


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow): # Initialize and connect all element signals and slots
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Scalpl-Vis")
        self.plot_selection_violin.clicked.connect(self.gene_violin_Plot)
        self.browse_h5ad.clicked.connect(self.browse_file)
        self.plot_selection_umap.clicked.connect(self.gene_UMAP_Plot)
        self.plot_basic_umap.clicked.connect(self.umap_plotter)
        self.plot_selection_tsne.clicked.connect(self.gene_tsne_Plot)
        self.plot_basic_tsne.clicked.connect(self.tsne_plotter)
        self.plot_selection_violin.clicked.connect(self.gene_violin_Plot)
        self.gene_search.textChanged.connect(self.searchItem) #Dynamic Search
        self.gene_search.setPlaceholderText('Search...')

    def browse_file(self):
        checked = False
        global fileLoc
        fileLoc, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)")
        if fileLoc:
            fileName = os.path.basename(os.path.normpath(fileLoc)) #isolates individual file name rather than taking entire paths
            fileNameM = os.path.splitext(fileName)[0]
            #fileQuoted = "'{}'" .format(fileLoc)
            QMessageBox.about(self, "Success!", fileName + " Selected!")
            self.file_selected.setText(fileName)
            try:
                adata = sc.read_h5ad(fileLoc, backed=None, chunk_size=7000)
                gnames = (adata.var_names) # Gene Expressions from data file
                gene_counts = str(len(adata.var_names))
                cell_counts = str(len(adata.obs_names))
                self.gene_count.setText(gene_counts)
                self.cell_count.setText(cell_counts)
                self.model = QtGui.QStandardItemModel() # Initiates a model for the list for each item
                self.gene_list.setModel(self.model) # Sets QListView to MVC
                self.gene_list.setEditTriggers(QAbstractItemView.NoEditTriggers) #Disables editable List
                for i in gnames: # Iterates thourgh each gene epression and adds it to list model
                    item = QtGui.QStandardItem(i)
                    self.model.appendRow(item)
                    item.setCheckable(True)
            except OSError:
                QMessageBox.about(self, "Error", "Incorrect file type. Please select a h5ad file!")

    def searchItem(self):
        try:
            filter_text = self.gene_search.text()
            for row in range(self.model.rowCount()):
                if filter_text in self.model.item(row).text(): # Hide ones not in search, and show ones in search
                    self.gene_list.setRowHidden(row, False)
                else:
                    self.gene_list.setRowHidden(row, True)
        except AttributeError: # Model not created if no file imported
            QMessageBox.about(self, "Error", "Search Error, No file imported or incorrect file type.")

    def gene_UMAP_Plot(self,index): #plots on double clicking a specific gene expression (ONLY UMAP FOR NOW)
        try:
            self.choices = [self.model.item(i).text() for i in
                            range(self.model.rowCount())
                            if self.model.item(i).checkState()
                            == QtCore.Qt.Checked] # Iterates through and checks what items are checked in the QList
        except AttributeError:
            QMessageBox.about(self, "Error", "Please select a h5ad file and gene(s) to plot")
        except OSError:
            QMessageBox.about(self, "Error", "Please select a h5ad file and gene(s) to plot")
        if ((len(self.choices)) > 10):
            QMessageBox.about(self, "Error", 'Application only supports up to 10 Genes for now.  Please choose fewer genes to plot.')
        else:
            print('Plotting...')
            print(self.choices)
            datafile = sc.read_h5ad(fileLoc, backed=None, chunk_size=7000)
            resGene =  ((datafile.obs_keys())[-1])
            try:
                self.choices.insert(0, resGene)
                sc.pl.umap(datafile, color= self.choices, s=50, color_map = "nipy_spectral_r")
            except IndexError: # If res is not an index key in the file, backup to other key
                self.choices.insert(0, 'n_genes') # Insert base UMAP into model
                sc.pl.umap(datafile, color= self.choices, s=50, color_map = "nipy_spectral_r")
        #UNCHECKS EVERYTHING AFTER EACH PLOT
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Unchecked)

    def gene_tsne_Plot(self):
            try:
                self.choices = [self.model.item(i).text() for i in
                                range(self.model.rowCount())
                                if self.model.item(i).checkState()
                                == QtCore.Qt.Checked] # Iterates through and checks what items are checked in the QList
            except AttributeError:
                QMessageBox.about(self, "Error", "Please select a h5ad file and gene(s) to plot")
            except OSError:
                QMessageBox.about(self, "Error", "Please select a h5ad file and gene(s) to plot")
            if ((len(self.choices)) > 10):
                QMessageBox.about(self, "Error", 'Application only supports up to 10 Genes for now.  Please choose fewer genes to plot.')
            else:
                print('Plotting...')
                print(self.choices)
                datafile = sc.read_h5ad(fileLoc, backed=None, chunk_size=7000)
                resGene =  ((datafile.obs_keys())[-1]) # Gene Expression Resolution Key as it varies **! MUST BE LAST KEY IN INDEX !**
                try:
                    self.choices.insert(0, resGene)
                    sc.pl.tsne(datafile, color= self.choices, s=50, color_map = "nipy_spectral_r")
                except IndexError: # If res is not an index key in the file, backup to other key 'colour'
                    self.choices.insert(0, 'n_genes') # Insert base TSNE into model
                    sc.pl.tsne(datafile, color= self.choices, s=50, color_map = "nipy_spectral_r" )
            for i in range(self.model.rowCount()):
                item = self.model.item(i)
                item.setCheckState(QtCore.Qt.Unchecked)

    def gene_violin_Plot(self):
        try: # Iterates through and checks what items are checked in the QList
            self.choices = [self.model.item(i).text() for i in
                            range(self.model.rowCount())
                            if self.model.item(i).checkState()
                            == QtCore.Qt.Checked]
        except AttributeError:
            QMessageBox.about(self, "Error", "Please select a h5ad file and gene(s) to plot")
        except OSError:
            QMessageBox.about(self, "Error", "Please select a h5ad file and gene(s) to plot")
        print('Plotting...')
        print(self.choices)
        try:
            datafile = sc.read_h5ad(fileLoc, backed=None, chunk_size=7000)
            sc.pl.violin(datafile, self.choices)
        except ValueError:
            QMessageBox.about(self, "Error", 'Please select gene(s) to plot!')
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Unchecked)

    def umap_plotter(self):
        try:
            global fileLoc
            umap_h5ad = sc.read_h5ad(fileLoc, backed=None, chunk_size=6000) # Testing for individual h5ad file
            resGene =  ((umap_h5ad.obs_keys())[-1])
            print(resGene)
            try:
                sc.pl.umap(umap_h5ad, color=[resGene,'class'], s=50, color_map = "nipy_spectral_r")
            except IndexError:
                sc.pl.umap(umap_h5ad, color=['n_genes'], s=50)
        except NameError:
             QMessageBox.about(self, "Error", "No File is selected. Please Browse for an h5ad file")
        except OSError:
            QMessageBox.about(self, "Error", "Incorrect file type. Please Browse for an h5ad file")

    def tsne_plotter(self):
        try:
            global fileLoc
            tsne_h5ad = sc.read_h5ad(fileLoc, backed=None, chunk_size=6000) # Testing for individual h5ad file
            resGene =  ((tsne_h5ad.obs_keys())[-1])
            try:
                sc.pl.tsne(tsne_h5ad, color=[resGene,'class'], s=50, color_map = "nipy_spectral_r")
            except IndexError:
                sc.pl.tsne(tsne_h5ad, color=['n_genes'], s=50)
        except NameError:
             QMessageBox.about(self, "Error", "No File is selected. Please Browse for an h5ad file")
        except OSError:
            QMessageBox.about(self, "Error", "Incorrect file type. Please Browse for an h5ad file")


if __name__ == '__main__':
    appctxt = AppContext()
    multiprocessing.freeze_support()
    exit_code = appctxt.run()
    sys.exit(exit_code)
