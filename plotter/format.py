from pyqtgraph import mkPen
from PySide2 import QtCore
from PySide2.QtCore import Qt

# Prepare pens for the plot
width = 2
default_pen_signatures = [
    {'color':'#FFFF00', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'o'},
    {'color':'#FF0000', 'width':width, 'style': Qt.SolidLine, 'symbol' : 't'},
    {'color':'#00EAFF', 'width':width, 'style': Qt.SolidLine, 'symbol' : 't1'},
    {'color':'#AA00FF', 'width':width, 'style': Qt.SolidLine, 'symbol' : 's'}, 
    {'color':'#FF7F00', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'p'}, 
    {'color':'#BFFF00', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'h'}, 
    {'color':'#0095FF', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'star'}, 
    {'color':'#FF00AA', 'width':width, 'style': Qt.SolidLine, 'symbol' : '+'}, 
    {'color':'#6AFF00', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'd'},
    {'color':'#0040FF', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'x'},
    {'color':'#EDB9B9', 'width':width, 'style': Qt.SolidLine, 'symbol' : 't2'},
    {'color':'#B9D7ED', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'o'},
    {'color':'#E7E9B9', 'width':width, 'style': Qt.SolidLine, 'symbol' : 't'},
    {'color':'#DCB9ED', 'width':width, 'style': Qt.SolidLine, 'symbol' : 't1'},
    {'color':'#B9EDE0', 'width':width, 'style': Qt.SolidLine, 'symbol' : 's'},
    {'color':'#8F2323', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'p'},
    {'color':'#23628F', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'h'},
    {'color':'#8F6A23', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'star'},
    {'color':'#6B238F', 'width':width, 'style': Qt.SolidLine, 'symbol' : '+'},
    {'color':'#4F8F23', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'd'},
    {'color':'#737373', 'width':width, 'style': Qt.SolidLine, 'symbol' : 'x'},
    {'color':'#CCCCCC', 'width':width, 'style': Qt.SolidLine, 'symbol' : 't2'},
]

brushes = [
    'r', 'b', 'g', 'c', 'm', 'y', 'k', 'w'
]

class PlotLineFormat():

    def __init__(    
    self,
    pen_color,
    pen_width = 1,
    pen_style = Qt.SolidLine,
    symbol = None,
    symbol_pen = None,
    symbol_brush = None):
        
        # Create a pen with the pen inputs
        pen_dict = {'color': pen_color,
                    'width': pen_width,
                    'style': pen_style}
        self.pen = mkPen(pen_dict)

        self.symbol = symbol
        
        if symbol_pen is None:
            self.symbol_pen = self.pen
        else:
            self.symbol_pen = symbol_pen

        if symbol_brush is None:
            self.symbol_brush = 0.3
        else:
            self.symbol_brush = symbol_brush

plf_defaults = []
for sig in default_pen_signatures:
    plf = PlotLineFormat(
            pen_color=sig['color'],
            pen_width=sig['width'],
            pen_style=sig['style'],
            symbol=sig['symbol'])
    plf_defaults.append(plf)


class PlotLineFormatPresets:

    defaults_list = plf_defaults

    # DASH
    RED_1PX_DASH = PlotLineFormat(
        pen_color='r', pen_width=1, pen_style=Qt.DashLine)
    RED_2PX_DASH = PlotLineFormat(
        pen_color='r', pen_width=2, pen_style=Qt.DashLine)
    GREEN_1PX_DASH = PlotLineFormat(
        pen_color='g', pen_width=1, pen_style=Qt.DashLine)
    GREEN_1PX_DASH = PlotLineFormat(
        pen_color='g', pen_width=2, pen_style=Qt.DashLine)
    
    # SOLID
    RED_1PX_SOLID = PlotLineFormat(
        pen_color='r', pen_width=1, pen_style=Qt.SolidLine)
    RED_2PX_SOLID = PlotLineFormat(
        pen_color='r', pen_width=2, pen_style=Qt.SolidLine)
    GREEN_1PX_SOLID = PlotLineFormat(
        pen_color='g', pen_width=1, pen_style=Qt.SolidLine)
    GREEN_1PX_SOLID = PlotLineFormat(
        pen_color='g', pen_width=2, pen_style=Qt.SolidLine)
    YELLOW_1PX_SOLID = PlotLineFormat(
        pen_color='y', pen_width=1, pen_style=Qt.SolidLine)
    YELLOW_2PX_SOLID = PlotLineFormat(
        pen_color='y', pen_width=2, pen_style=Qt.SolidLine)
       
    # DOTTED
    RED_1PX_DOT = PlotLineFormat(
        pen_color='r', pen_width=1, pen_style=Qt.DotLine)
    RED_2PX_DOT = PlotLineFormat(
        pen_color='r', pen_width=2, pen_style=Qt.DotLine)
    GREEN_1PX_DOT = PlotLineFormat(
        pen_color='g', pen_width=1, pen_style=Qt.DotLine)
    GREEN_1PX_DOT = PlotLineFormat(
        pen_color='g', pen_width=2, pen_style=Qt.DotLine)