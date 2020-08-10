from gi.repository import Gtk, Gdk, GObject
from gettext import gettext as _

class Tab(Gtk.Box):
    __gtype_name__ = 'Tab'


    __gsignals__ = {
        "deleted": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "renamed": (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }


    def __init__(self, label, tab_content, **kwargs):
        super().__init__(Gtk.Orientation.HORIZONTAL, spacing=10)
        self.__tab_content = tab_content
        self.__label = Gtk.Label(label)
        self.__event_box = Gtk.EventBox()
        self.__menu = Gtk.Menu()
        self.__menu_rename_item = Gtk.MenuItem(_("Rename"))
        self.__menu_delete_item = Gtk.MenuItem(_("Delete"))
        self.__menu.add(self.__menu_rename_item)
        self.__menu.add(self.__menu_delete_item)
        self.__menu.show_all()
        self.__event_box.add(self.__label)

        self.__edit_popower = Gtk.Popover()

        self.__entry = Gtk.Entry()
        self.__entry.set_max_length(50)
        self.__edit_popower.add(self.__entry)

        self.pack_start(self.__event_box, True, True, 0)

        self.__event_box.connect("button-press-event", self.__on_button_press)
        self.__menu_rename_item.connect("activate", self.__on_rename)
        self.__menu_delete_item.connect("activate", self.__on_delete)
        self.__entry.connect("activate", self.__on_entry_changed)

        self.show_all()

    def __on_button_press(self, _widget, event):
        if event.type != Gdk.EventType.BUTTON_PRESS:
            return
        if event.get_button().button != 3:
            return
        self.__menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())

    def __on_delete(self, _widget):
        self.emit("deleted")

    def __on_rename(self, _widget):
        self.__entry.set_text(self.__label.get_text())
        self.__edit_popower.set_relative_to(self)
        self.__edit_popower.show_all()

    def __on_entry_changed(self, *args):
        self.__label.set_text(self.__entry.get_text())
        self.__edit_popower.hide()
        self.emit("renamed", self.__label.get_text())

    @property
    def tab_content(self):
        return self.__tab_content
