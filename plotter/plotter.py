from plotter.format import *



class PlotType:
    LINE = 0
    BAR = 1

class PlotSeries():
    """Plot data for a single series"""

    def __init__(self, name:str, x_values:list, y_values:list, format:PlotLineFormat):
        self.name = name
        self.x_values = x_values
        self.y_values = y_values
        self.format = format

class PlottableObject():
    """Contains all the details needed to plot data
    
    Structure:
        name = 'Efficiency vs Load'

        series_list:list[PlotSeries]

        x_label = 'Load Current (A)'
        y_label = 'Efficiency (%)'

        x_range:tuple = (0, 5)
        y_range:tuple = (50, 100)

        plot_type


    """
    def __init__(
            self, 
            title:str,
            type:PlotType,
            plot_series_list:list[PlotSeries]=[],
            x_range:tuple[int, int]=(0,0),
            y_range:tuple[int, int]=(0,0),
            x_label:str='',
            y_label:str=''):
        
        self.title = title
        self.type = type
        self.plot_series_list = plot_series_list
        self.x_range = x_range
        self.y_range = y_range

        self.x_label = x_label
        self.y_label = y_label
        
        self.x_min = self.x_range[0]
        self.x_max = self.x_range[1]

        self.y_min = self.y_range[0]
        self.y_max = self.y_range[1]

        self.pen_index = 0

    def append_plot_data(self, plot_index, x, y):
        """Add a point to the plot data"""
        self.plot_series_list[plot_index].x_values.append(x)
        self.plot_series_list[plot_index].y_values.append(y)

    def add_plot_series(
            self, 
            name:str,
            x_values:list = list(),
            y_values:list = list(),
            format:PlotLineFormat = None):
        """Add a plot series to the plottable object
        """


        # If format is not specified, get from the defaults
        if format is None:
            plot_format = PlotLineFormatPresets.defaults_list[self.pen_index]
            self.pen_index += 1
        else:
            plot_format = format

        self.plot_series_list.append(
            PlotSeries(name, x_values, y_values, format=plot_format))

class DataTable:
    def __init__(self, header:list, data:list = None):
        self.header = header
        self.data = data if data is not None else []

    def add_data_row(self, data_row):
        self.data.append(data_row)

    def add_blank_row(self):
        """Add a blank data row"""
        # Get the number of elements for the row
        row_len = len(self.header) if self.header else (len(self.data[0]) if len(self.data) > 0 else 0)
        # Append a list containing blanks with same length
        self.data.append([''] * row_len)