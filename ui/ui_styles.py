################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
## This project can be used freely for all uses, as long as they maintain the
## respective credits only in the Python scripts, any information in the visual
## interface (GUI) can be modified without any implication.
##
## There are limitations on Qt licenses if you want to use your products
## commercially, I recommend reading them on the official website:
## https://doc.qt.io/qtforpython/licenses.html
##
################################################################################

class Style():

    style_bt_standard = (
    """
    QPushButton {
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 28px solid rgb(27, 29, 35);
        background-color: rgb(27, 29, 35);
        text-align: left;
        padding-left: 45px;
    }
    QPushButton[Active=true] {
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 28px solid rgb(27, 29, 35);
        border-right: 5px solid rgb(44, 49, 60);
        background-color: rgb(27, 29, 35);
        text-align: left;
        padding-left: 45px;
    }
    QPushButton:hover {
        background-color: rgb(33, 37, 43);
        border-left: 28px solid rgb(33, 37, 43);
    }
    QPushButton:pressed {
        background-color: rgb(85, 170, 255);
        border-left: 28px solid rgb(85, 170, 255);
    }
    """
    )

    style_button_base = (
    """
    QPushButton {
        border: 2px solid rgb(52, 59, 72);
        border-radius: 5px;
        background-color: rgb(52, 59, 72);
        }
        
        QPushButton:hover {
            background-color: rgb(57, 65, 80);
            border: 2px solid rgb(61, 70, 86);
        }
        
        QPushButton:pressed {
            background-color: rgb(35, 40, 49);
            border: 2px solid rgb(43, 50, 61);
        }
        
        QPushButton:disabled {
            background-color: rgb(25, 30, 39);
            border: 2px solid rgb(33, 40, 51);
            color: rgb(71, 71, 71);
        }
    """
    )

    style_button_red = (
    """
    QPushButton {
        border: 2px solid rgb(52, 59, 72);
        border-radius: 5px;
        background-color: red;
    }
    
    QPushButton:hover {
        background-color: red;
        border: 2px solid rgb(61, 70, 86);
    }
    
    QPushButton:pressed {
        background-color: red;
        border: 2px solid rgb(43, 50, 61);
    }
    
    QPushButton:disabled {
        background-color: red;
        border: 2px solid rgb(33, 40, 51);
        color: rgb(71, 71, 71);
    }
    """
    )

    style_button_green = (
    """
    QPushButton {
        border: 2px solid rgb(52, 59, 72);
        border-radius: 5px;
        background-color: green;
    }
    
    QPushButton:hover {
        background-color: green;
        border: 2px solid rgb(61, 70, 86);
    }
    
    QPushButton:pressed {
        background-color: green;
        border: 2px solid rgb(43, 50, 61);
    }
    
    QPushButton:disabled {
        background-color: green;
        border: 2px solid rgb(33, 40, 51);
        color: rgb(71, 71, 71);
    }
    """
    )

    red_frame = (
        """
        QFrame{
            border:2px solid red;	
            border-radius: 3px;
            background-color: rgb(29,34, 44);
        }
        """
    )

    green_frame = (
        """
        QFrame{
            border:2px solid green;	
            border-radius: 3px;
            background-color: rgb(29,34, 44);
        }
        """
    )
    
    normal_frame = (
        """
        QFrame{
            border:2px solid black;	
            border-radius: 3px;
            background-color: rgb(29,34, 44);
        }
        """
    )

from PySide2.QtWidgets import QSizePolicy
from PySide2.QtWidgets import QWidget

sp_retain = QSizePolicy()
sp_retain.setRetainSizeWhenHidden(True)


sp_horizontal_min_expanding = QSizePolicy()
sp_horizontal_min_expanding.setHorizontalPolicy(QSizePolicy.MinimumExpanding)


def add_setretainsize_policy(widget:QWidget):
    temp_policy:QSizePolicy = widget.sizePolicy()
    temp_policy.setRetainSizeWhenHidden(True)
    widget.setSizePolicy(temp_policy)

from PySide2.QtCore import QTimer
def flash_btn_stylesheet( widget, temp_stylesheet):
    """Temporarily use a stlesheet then return to the original after 1s"""
    widget.setStyleSheet(temp_stylesheet)
    def set_base_style():
            widget.setStyleSheet(Style.style_button_base)
    QTimer.singleShot(1000, set_base_style)