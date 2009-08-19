# Copyright (c) 2008 David Aguilar
"""This module provides miscellaneous Qt utility functions.
"""
import os

from PyQt4 import QtCore
from PyQt4 import QtGui

from cola import core
from cola import utils
from cola import resources

LOGGER = None

def log(status, output):
    """Sends messages to the log window.
    """
    if not LOGGER or not output:
        return
    LOGGER.log(status, output)

def input(msg, title=None):
    """Presents the user with an input widget and returns the input."""
    if title is None:
        title = msg
    parent = QtGui.QApplication.instance().activeWindow()
    result = QtGui.QInputDialog.getText(parent, msg, title)
    return (unicode(result[0]), result[1])

def create_listwidget_item(text, filename):
    """Creates a QListWidgetItem with text and the icon at filename."""
    item = QtGui.QListWidgetItem()
    item.setIcon(QtGui.QIcon(filename))
    item.setText(text)
    return item

_icon_cache = {}
def create_treewidget_item(text, filename):
    """Creates a QTreeWidgetItem with text and the icon at filename."""
    global _icon_cache
    if filename not in _icon_cache:
        _icon_cache[filename] = QtGui.QIcon(filename)
    icon = _icon_cache[filename]
    item = QtGui.QTreeWidgetItem()
    item.setIcon(0, icon)
    item.setText(0, text)
    return item

def information(title, message=None):
    """Launches a QMessageBox information with the
    provided title and message."""
    if message is None:
        message = title
    parent = QtGui.QApplication.instance().activeWindow()
    QtGui.QMessageBox.information(parent, title, message)

def get_selected_treeitem(tree_widget):
    """Returns a(id_number, is_selected) for a QTreeWidget."""
    id_number = None
    selected = False
    item = tree_widget.currentItem()
    if item:
        id_number = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        selected = True
    return(id_number, selected)

def get_selected_row(list_widget):
    """Returns a(row_number, is_selected) tuple for a QListWidget."""
    row = list_widget.currentRow()
    item = list_widget.item(row)
    selected = item is not None and item.isSelected()
    return(row, selected)

def get_selection_list(listwidget, items):
    """Returns an array of model items that correspond to
    the selected QListWidget indices."""
    selected = []
    itemcount = listwidget.count()
    widgetitems = [ listwidget.item(idx) for idx in range(itemcount) ]

    for item, widgetitem in zip(items, widgetitems):
        if widgetitem.isSelected():
            selected.append(item)
    return selected

def get_tree_selection(treeitem, items):
    """Returns model items that correspond to selected widget indices"""
    itemcount = treeitem.childCount()
    widgetitems = [ treeitem.child(idx) for idx in range(itemcount) ]
    selected = []
    for item, widgetitem in zip(items[:len(widgetitems)], widgetitems):
        if widgetitem.isSelected():
            selected.append(item)

    return selected

def get_selected_item(list_widget, items):
    """Returns the selected item in a QListWidget."""
    row, selected = get_selected_row(list_widget)
    if selected and row < len(items):
        return items[row]
    else:
        return None

def open_dialog(parent, title, filename=None):
    """Creates an Open File dialog and returns a filename."""
    title_tr = parent.tr(title)
    return unicode(QtGui.QFileDialog
                        .getOpenFileName(parent, title_tr, filename))

def opendir_dialog(parent, title, path):
    """Prompts for a directory path"""

    flags = (QtGui.QFileDialog.ShowDirsOnly |
             QtGui.QFileDialog.DontResolveSymlinks)
    title_tr = parent.tr(title)
    qstr = (QtGui.QFileDialog
                 .getExistingDirectory(parent, title_tr, path, flags))
    return unicode(qstr)


def save_dialog(parent, title, filename=''):
    """Creates a Save File dialog and returns a filename."""
    title_tr = parent.tr(title)
    return unicode(QtGui.QFileDialog
                        .getSaveFileName(parent, title_tr, filename))

def get_icon(basename):
    """Given a basename returns a QIcon from the corresponding cola icon."""
    return QtGui.QIcon(resources.icon(basename))

def question(parent, title, message, default=True):
    """Launches a QMessageBox question with the provided title and message.
    Passing "default=False" will make "No" the default choice."""
    yes = QtGui.QMessageBox.Yes
    no = QtGui.QMessageBox.No
    buttons = yes | no
    if default:
        default = yes
    else:
        default = no
    result = QtGui.QMessageBox.question(parent, title, message,
                                        buttons, default)
    return result == QtGui.QMessageBox.Yes

def set_clipboard(text):
    """Sets the copy/paste buffer to text."""
    if not text:
        return
    clipboard = QtGui.QApplication.instance().clipboard()
    clipboard.setText(text, QtGui.QClipboard.Clipboard)
    clipboard.setText(text, QtGui.QClipboard.Selection)

def set_selected_item(widget, idx):
    """Sets a the currently selected item to the item at index idx."""
    if type(widget) is QtGui.QTreeWidget:
        item = widget.topLevelItem(idx)
        if item:
            widget.setItemSelected(item, True)
            widget.setCurrentItem(item)

def add_items(widget, items):
    """Adds items to a widget."""
    for item in items:
        widget.addItem(item)

def set_items(widget, items):
    """Clear the existing widget contents and set the new items."""
    widget.clear()
    add_items(widget, items)

def tr(txt):
    """Translate a string into a local language."""
    return unicode(QtGui.QApplication.instance().translate('', txt))

def get_icon_file(filename, staged=False, untracked=False):
    """Returns a file path representing a corresponding file path."""
    if staged:
        if os.path.exists(core.encode(filename)):
            icon_file = resources.icon('staged.png')
        else:
            icon_file = resources.icon('removed.png')
    elif untracked:
        icon_file = resources.icon('untracked.png')
    else:
        icon_file = utils.get_file_icon(filename)
    return icon_file

def get_icon_for_file(filename, staged=False, untracked=False):
    """Returns a QIcon for a particular file path."""
    icon_file = get_icon_file(filename, staged=staged, untracked=untracked)
    return get_icon(icon_file)

def create_listitem(filename, staged=False, untracked=False):
    """Given a filename, return a QListWidgetItem suitable
    for adding to a QListWidget.  "staged" and "untracked"
    controls whether to use the appropriate icons."""
    icon_file = get_icon_file(filename, staged, untracked)
    return create_listwidget_item(filename, icon_file)

def create_treeitem(filename, staged=False, untracked=False, check=True):
    """Given a filename, return a QListWidgetItem suitable
    for adding to a QListWidget.  "staged" and "untracked"
    controls whether to use the appropriate icons."""
    if check:
        icon_file = get_icon_file(filename, staged=staged, untracked=untracked)
    else:
        icon_file = resources.icon('staged.png')
    return create_treewidget_item(filename, icon_file)


def update_file_icons(widget, items, staged=True,
            untracked=False, offset=0):
    """Populate a QListWidget with custom icon items."""
    for idx, model_item in enumerate(items):
        item = widget.item(idx+offset)
        if item:
            item.setIcon(get_icon_for_file(model_item, staged, untracked))

def update_listwidget(widget, items, staged=True,
            untracked=False, append=False):
    """Populate a QListWidget with custom icon items."""
    if not append:
        widget.clear()
    add_items(widget, [ create_listitem(i, staged, untracked) for i in items ])

def set_listwidget_strings(widget, items):
    """Sets a list widget to the strings passed in items."""
    widget.clear()
    add_items(widget, [ QtGui.QListWidgetItem(i) for i in items ])

_icon_cache = {}
def cached_icon(key):
    """Maintain a cache of standard icons and return cache entries."""
    if key not in _icon_cache:
        style = QtGui.QApplication.instance().style()
        _icon_cache[key] = style.standardIcon(key)
    return _icon_cache[key]

def dir_icon():
    """Return a standard icon for a directory."""
    return cached_icon(QtGui.QStyle.SP_DirIcon)

def file_icon():
    """Return a standard icon for a file."""
    return cached_icon(QtGui.QStyle.SP_FileIcon)
