# Python Standard Library Imports
from time import sleep


# Third Party Imports
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QTableWidgetItem, QSizePolicy
from pyqtgraph import mkPen
import pyqtgraph as pg
import numpy as np

# Local Imports
from ui.ui_styles import Style
from plotter.plotter import *
from psu_tests.tests import (TestItem, TestPlan)


from pyqtgraph import PlotWidget


# Typing Imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import MainWindow, Ui_MainWindow

TEST_LIST_UPDATE_TIMER_MS = 200


class TestResultsPageHandler():
    """Handler for the test results page."""
    
    def __init__(self, parent):
        # Get a link from the parent
        self.parent:MainWindow = parent
        # Let the handler control the ui
        self.ui:Ui_MainWindow = parent.ui

        self.test_plan = parent.test_plan

        self.plot_widget = self.ui.plotwidget_test_results_plots




        # Test List Selection
        self.prev_table_selection_i = -1
        self.prev_cbx_selection_i = -1

        # Bind UI elements to functionss
        self.bind_ui_elements()
        self.bind_ui_change_events()
        self.initialize_ui_states()

        self.setup_test_list_update_timer()
        self.state = True
        self.demote_plotwidget()
        pass

    def start(self):
        """Run when this Stackwidget page is enabled."""
        # Promote
        self.promote_plotwidget()

        # Show the test list in the test list table
        self.update_test_list_details()
        self.test_list_update_timer.start(TEST_LIST_UPDATE_TIMER_MS)

    def stop(self):
        """Run when the stack widget page changes from this one."""
        self.test_list_update_timer.stop()
        QTimer.singleShot(1000,self.demote_plotwidget)  

    def promote_plotwidget(self):
        ui = self.ui
        ui.plotwidget_test_results_plots \
            = PlotWidget(self.ui.page_test_results_plots)
        ui.plotwidget_test_results_plots\
            .setObjectName(u"plotwidget_test_results_plots")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            ui.plotwidget_test_results_plots.sizePolicy()\
                .hasHeightForWidth())
        ui.plotwidget_test_results_plots.setSizePolicy(sizePolicy)
        ui.plotwidget_test_results_plots.setStyleSheet(u"")

        ui.layout_test_results_plot.\
            addWidget(ui.plotwidget_test_results_plots)
        
        self.plot_widget = self.ui.plotwidget_test_results_plots
        self.legend = self.plot_widget.addLegend()
                # Plot objects
        self.lines = []
        self.bars = []
        self.legend = None
        self.with_legend = True
    
    def demote_plotwidget(self):
        self.ui.plotwidget_test_results_plots.setParent(None)
        self.ui.plotwidget_test_results_plots.deleteLater()
        
        self.ui.plotwidget_test_results_plots = None
        
        self.plot_widget = None
    
    def setup_test_list_update_timer(self):
        self.test_list_update_timer = QTimer(self.parent)
        self.test_list_update_timer.timeout.connect(
            self.timer_update_service)

    def bind_ui_elements(self):
        """Bind the ui elements to the methods 
        that will be run for each event"""
        # Bind buttons for showing plot or data
        self.ui.btn_test_results_show_data.clicked.connect(
            self.show_data_btn_clicked)
        self.ui.btn_test_results_show_plots.clicked.connect(
            self.show_plots_btn_clicked)
        self.ui.table_test_results_test_list.itemSelectionChanged.connect(
            self.update_test_data)
        self.ui.table_test_results_test_list.cellClicked.connect(
            lambda r, c: self.update_test_data())
        
    def bind_ui_change_events(self):
        """Bind the ui elements to the methods 
        that will be run for events that change the UI states"""
        # self.ui.cbx_test_results_plots.currentIndexChanged.connect(
        # )
        
    def initialize_ui_states(self):
        # Stretch the rows of the table to equalize the widths
        self.ui.table_test_results_data.horizontalHeader().\
            setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.table_test_results_data.horizontalHeader().\
            setVisible(True)
        
        # self.ui.table_test_results_test_list.horizontalHeader().\
        #     setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.table_test_results_test_list.horizontalHeader().\
            setVisible(True)
        
        self.ui.table_test_results_test_list.setColumnWidth(0, 50)
        
        self.show_plots_btn_clicked()
    
    ###########################################################################
    #                   Widget Visibility Functions                           #
    ###########################################################################
    def show_plots_btn_clicked(self):
        ui = self.ui
        # Set the stacked widget page to the plots page
        ui.stacked_widget_test_results.setCurrentWidget(
            ui.page_test_results_plots)
        # Disable the show plots button and enable the show data button
        ui.btn_test_results_show_data.setEnabled(True)
        ui.btn_test_results_show_plots.setEnabled(False)

    def show_data_btn_clicked(self):
        ui = self.ui
        # Set the stacked widget page to the plots page
        ui.stacked_widget_test_results.setCurrentWidget(
            ui.page_test_results_data_table)
        # Disable the show plots button and enable the show data button
        ui.btn_test_results_show_data.setEnabled(False)
        ui.btn_test_results_show_plots.setEnabled(True)
        self.update_test_data()

    ###########################################################################
    #                   TestPlan Table Related Functions                      #
    ###########################################################################
    def timer_update_service(self):
        """Run in a timer whenever the page is active"""
        self.update_test_list_details()
        self.update_test_data()
        
    def update_test_list_details(self):
        """Takes information from the TestPlan and 
        updates the details of the test list"""

        # Use the test plan
        test_plan:TestPlan = self.test_plan
        test_list_table = self.ui.table_test_results_test_list

        self.available_test_items_indexes = []
        test_list_available_index = 0

        for test_item_index,test_item in enumerate(test_plan.test_items):
            # Process the test item only if already has test data
            if not test_item.with_test_data:
                continue
            
            self.available_test_items_indexes.append(test_item_index)

            # Add a row to the table for the current item
            current_row_count = test_list_table.rowCount()
            if current_row_count <= test_list_available_index:
                test_list_table.setRowCount(test_list_available_index + 1)

            # Get the details text from the test object
            test_object = test_item.test_object
            test_object.update_test_list_text()
            details_text = test_item.test_object.test_list_text

            # Add the details to the table
            test_list_table.setItem(
                test_list_available_index, 0, 
                QtWidgets.QTableWidgetItem(str(test_item_index+1)))
            test_list_table.setItem(
                test_list_available_index, 1, 
                QtWidgets.QTableWidgetItem(details_text))
            
            test_list_available_index += 1
        
        # Make sure the row count is exact so there will be
        # no error for selecting blank rows
        len_table = len(self.available_test_items_indexes)
        if test_list_table.rowCount() != len_table:
            test_list_table.setRowCount(len_table)

        if len_table > 0 and test_list_table.currentRow() == -1:
            test_list_table.selectRow(0)

    def update_test_data(self):
        """Update test data based on selection"""
        # UI short names
        ui = self.ui
        test_list_table = ui.table_test_results_test_list
        cbx_plots = ui.cbx_test_results_plots

        if not self.available_test_items_indexes:
            return

        # TEST LIST TABLE
        # Default to row 0 if nothing valid is selected
        self.testitem_select_index = test_list_table.currentRow()
        if self.testitem_select_index < 0 or self.testitem_select_index >= len(self.available_test_items_indexes):
            self.testitem_select_index = 0
            test_list_table.selectRow(0)

        # Get the test item
        test_items_index = self.available_test_items_indexes[
            self.testitem_select_index]
        test_item:TestItem = self.test_plan.test_items[test_items_index]
        
        # TEST RESULTS TABLE DATA
        if test_item.test_data_table is not None:
            self.update_data_table(test_item.test_data_table)

        # PLOT SELECTION COMBO BOX
        # IF there is a change on the selection, update combo box
        if not (self.testitem_select_index == self.prev_table_selection_i):
            ui.cbx_test_results_plots.clear()

            plot_names = [plt.title for plt in test_item.plottables]
            cbx_plots.addItems(plot_names)

            self.prev_cbx_selection_i = -1

        # Get the combo box selection
        self.cbx_selection_i = ui.cbx_test_results_plots.currentIndex()
        if 0 <= self.cbx_selection_i < len(test_item.plottables):
            selected_plottable = test_item.plottables[self.cbx_selection_i]
            # If there is a change in combo box selection,
            # Update the whole plot
            if not (self.cbx_selection_i == self.prev_cbx_selection_i):    
                self.plot(selected_plottable) 
            # If there is no change in cbx selection, Change only the plot contents
            else:
                self.update_plot(selected_plottable)

        # Set the previous selection index to the current selection
        # so that the processing will no longer happen afterwards
        self.prev_table_selection_i = self.testitem_select_index
        self.prev_cbx_selection_i = self.cbx_selection_i
       
    
    ###########################################################################
    #                   PLOTTING Related Functions                            #
    ###########################################################################
    def plot(self, plottable_object):
        """Plot the given plottable object in the plot widget"""

        po:PlottableObject = plottable_object
        pw:pg.PlotWidget = self.plot_widget
        
        self.clear_plots()

        # Set labels
        pw.setTitle(po.title)
        pw.setLabel('bottom', po.x_label)
        pw.setLabel('left', po.y_label)

        # Set Range
        pw.setXRange(po.x_min, po.x_max)
        pw.setYRange(po.y_min, po.y_max)

        # Plot the series
        match po.type:
            case PlotType.LINE:
                self.plot_lines(po.plot_series_list)
            case PlotType.BAR:
                self.plot_bars(po.plot_series_list)

    def update_plot(self, selected_plottable):
        """Update the plot data without reapplying the plot settings."""
        
        po:PlottableObject = selected_plottable
        po.plot_series_list
        if (po.type == PlotType.LINE):
            # Loop through the plot data and update the values
            for i, ps in enumerate(po.plot_series_list):
                f:PlotLineFormat = ps.format
                try:
                    self.lines[i].setData(ps.x_values, ps.y_values)
                # If there is a new plot series, plot it as new
                except IndexError:
                    self.lines.append(self.plot_widget.plot(
                        ps.x_values, ps.y_values, name=ps.name,
                        pen=f.pen, symbol=f.symbol, symbolPen=f.symbol_pen,
                        symbolBrush=f.symbol_brush))
        elif (po.type == PlotType.BAR):
            for i, ps in enumerate(po.plot_series_list):
                self.bars[i].setData(ps.x_values, ps.y_values)
    
    def plot_lines(self, plot_series_list:list[PlotSeries]):
        """Plot the data contained in the plot_series_list
        in a line plot."""
        
        for i, ps in enumerate(plot_series_list):
            f:PlotLineFormat = ps.format
            self.lines.append(
                self.plot_widget.plot(
                        ps.x_values, ps.y_values, name=ps.name,
                        pen=f.pen, symbol=f.symbol, symbolPen=f.symbol_pen,
                        symbolBrush=f.symbol_brush))

    def plot_bars(self, plot_series_list:list[PlotSeries]):
        """Plot the data contained in the plot_series_list
        in a bar plot."""
        
        for i, ps in enumerate(plot_series_list):
            bg = pg.BarGraphItem(
                x=ps.x_values, height=ps.y_values,
                width=0.3, brush=brushes[i], name=ps.name)

            self.bars.append(bg)
            self.plot_widget.addItem(bg)
        
    def clear_plots(self):

        self.reset_legend()
        # Clear the line plots
        [line.clear() for line in self.lines]
        self.lines.clear()

        # Clear the bar plots
        [self.plot_widget.removeItem(bar) for bar in self.bars]
        self.bars.clear()

    def remove_legend(self):
        """Remove the legend from the scene and 
        set it to none inside the plot object"""
        self.plot_widget.scene().removeItem(self.legend)
        self.plot_widget.plotItem.legend = None
    
    def add_legend(self):
        """Add back the legend to the scene"""
        self.legend = self.plot_widget.addLegend()

    def reset_legend(self):
        """Have you tried turning it off and on again?"""
        self.remove_legend()
        self.add_legend()

    
    ###########################################################################
    #                   Test Data Table Related Functions                     #
    ###########################################################################
    def update_data_table(self, data_table:DataTable):
        """Update the tablewidget with contents from the DataTable object"""
        # UI Shortnames
        ui = self.ui
        test_data_table = ui.table_test_results_data

        if data_table is None or data_table.header is None:
            return

        # HEADER PROCESSING
        header = data_table.header
        len_header = len(header)
        # Set column size to header size
        test_data_table.setColumnCount(len_header)
        # Set the ui header with the contents of data_table header
        test_data_table.setHorizontalHeaderLabels(header)
        
        # Set the number of rows
        data = data_table.data or []
        len_data = len(data)
        test_data_table.setRowCount(len_data)
        # Loop through the object and set the table values
        for ri, row in enumerate(data):
            for ci, val in enumerate(row):
                if val is None:
                    v = ''
                elif isinstance(val, (float, int)):
                    v = f'{val:g}'
                else:
                    v = str(val)
                test_data_table.setItem(ri, ci, QTableWidgetItem(v))