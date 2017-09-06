import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from axopy import util
from axopy.messaging import transmitter

# This mapping from key names in the Qt namespace to axopy key names just
# allows users to write code without any Qt stuff in it
key_map = {
    QtCore.Qt.Key_A: util.key_a,
    QtCore.Qt.Key_B: util.key_b,
    QtCore.Qt.Key_C: util.key_c,
    QtCore.Qt.Key_D: util.key_d,
    QtCore.Qt.Key_E: util.key_e,
    QtCore.Qt.Key_F: util.key_f,
    QtCore.Qt.Key_G: util.key_g,
    QtCore.Qt.Key_H: util.key_h,
    QtCore.Qt.Key_I: util.key_i,
    QtCore.Qt.Key_J: util.key_j,
    QtCore.Qt.Key_K: util.key_k,
    QtCore.Qt.Key_L: util.key_l,
    QtCore.Qt.Key_M: util.key_m,
    QtCore.Qt.Key_N: util.key_n,
    QtCore.Qt.Key_O: util.key_o,
    QtCore.Qt.Key_P: util.key_p,
    QtCore.Qt.Key_Q: util.key_q,
    QtCore.Qt.Key_R: util.key_r,
    QtCore.Qt.Key_S: util.key_s,
    QtCore.Qt.Key_T: util.key_t,
    QtCore.Qt.Key_U: util.key_u,
    QtCore.Qt.Key_V: util.key_v,
    QtCore.Qt.Key_W: util.key_w,
    QtCore.Qt.Key_X: util.key_x,
    QtCore.Qt.Key_Y: util.key_y,
    QtCore.Qt.Key_Z: util.key_z,
    QtCore.Qt.Key_1: util.key_1,
    QtCore.Qt.Key_2: util.key_2,
    QtCore.Qt.Key_3: util.key_3,
    QtCore.Qt.Key_4: util.key_4,
    QtCore.Qt.Key_5: util.key_5,
    QtCore.Qt.Key_6: util.key_6,
    QtCore.Qt.Key_7: util.key_7,
    QtCore.Qt.Key_8: util.key_8,
    QtCore.Qt.Key_9: util.key_9,
    QtCore.Qt.Key_0: util.key_0,
    QtCore.Qt.Key_Space: util.key_space,
    QtCore.Qt.Key_Return: util.key_return,
    QtCore.Qt.Key_Escape: util.key_escape,
}

qtapp = None


def get_qtapp():
    """Get a `QApplication` instance running.

    Returns the current `QApplication` instance if it exists and creates it
    otherwise.
    """
    global qtapp
    inst = QtWidgets.QApplication.instance()
    if inst is None:
        qtapp = QtWidgets.QApplication(sys.argv)
    else:
        qtapp = inst
    return qtapp


class MainWindow(QtWidgets.QMainWindow):
    """The window containing all graphical content of the application.

    It is a very simple GUI implemented as a `QMainWindow` with a
    `QStackedLayout` holding a list of :class:`Container` objects. The
    containers, which in turn house all of the interesting graphical content.
    """

    def __init__(self):
        app = get_qtapp()
        super(MainWindow, self).__init__()

        app.installEventFilter(self)

        self._central_widget = QtWidgets.QWidget(self)
        self._layout = QtWidgets.QStackedLayout(self._central_widget)
        self.setCentralWidget(self._central_widget)

        status_bar = QtWidgets.QStatusBar(self)
        self.setStatusBar(status_bar)
        self._statusbar_label = QtWidgets.QLabel("status")
        status_bar.addPermanentWidget(self._statusbar_label)

        self.show()

    def run(self):
        """Start the application."""
        get_qtapp().exec_()

    def new_container(self):
        """Add a new container to the stack and give it back.

        Returns
        -------
        container : Container
            The newly added container.
        """
        c = Container()
        self._layout.addWidget(c)
        self._layout.setCurrentWidget(c)
        return c

    def set_container(self, container):
        """Make the given container visible.

        If the container is already somewhere in the stack, it is just made
        visible, otherwise it is added to the stack.
        """
        # FIXME find out if there's a variable in Qt to use instead of -1 here
        if self._layout.indexOf(container) == -1:
            self._layout.addWidget(container)
        self._layout.setCurrentWidget(container)

    def set_status(self, message):
        """Set the status bar message.

        Parameters
        ----------
        message : str
            Message to display in the status bar.
        """
        self._statusbar_label.setText(message)

    def quit(self):
        """Quit the application."""
        get_qtapp().quit()

    #def eventFilter(self, obj, event):
    #    if event.type() == QtCore.QEvent.KeyPress:
    #        try:
    #            key = key_map[event.key()]
    #        except KeyError:
    #            return False

    #        self.key_pressed(key)
    #        return True
    #    else:
    #        return False

    def keyPressEvent(self, event):
        """Qt callback for key presses.

        This overrides the `QMainWindow` method. It does not need to be called
        directly and it doesn't need to be overriden. Connect to the
        :meth:`key_pressed` transmitter to handle key press events.
        """
        try:
            key = key_map[event.key()]
        except KeyError:
            return super().keyPressEvent(event)

        self.key_pressed(key)

    @transmitter(('key', str))
    def key_pressed(self, key):
        """Signal that a key has been pressed.

        Key names are found in :mod:`axopy.util`.

        Returns
        -------
        key : str
            The key name.
        """
        return key


class Container(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Container, self).__init__(parent=parent)

    def set_view(self, view):
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(view, 0, 0)