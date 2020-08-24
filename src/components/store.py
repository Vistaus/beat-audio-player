from gettext import gettext as _
from gi.repository import Gtk

from beat.widgets.cell_renderers import CellRendererActiveTrack

__all__ = ["PlayListStore", "PLAYLIST_COLS"]


PLAYLIST_COLS = [
    {"key": "src",      "label": "",           "type": str,  "cell_type": None},
    {"key": "_state",   "label": "",           "type": str,  "cell_type": CellRendererActiveTrack},
    {"key": "artist",   "label": _("Artist"),  "type": str,  "cell_type": Gtk.CellRendererText},
    {"key": "album",    "label": _("Album"),   "type": str,  "cell_type": Gtk.CellRendererText},
    {"key": "title",    "label": _("Title"),   "type": str,  "cell_type": Gtk.CellRendererText},
    {"key": "length",   "label": _("Length"),  "type": str,  "cell_type": Gtk.CellRendererText},
    {"key": "_queue",   "label": "",           "type": str,  "cell_type": Gtk.CellRendererText},
]


def __get_col_id(key):
    for i, v in enumerate(PLAYLIST_COLS):
        if key == v.get("key"):
            return i


SRC_ID = __get_col_id("src")
STATE_ID = __get_col_id("_state")
QUEUE_ID = __get_col_id("_queue")
ARTIST_ID = __get_col_id("artist")
ALBUM_ID = __get_col_id("album")
TITLE_ID = __get_col_id("title")


class PlayListStore(Gtk.ListStore):
    __gtype_name__ = "PlayListStore"

    def __init__(self, uuid):
        super().__init__(*[col["type"] for col in PLAYLIST_COLS])
        self.__active_ref = None
        self.__uuid = uuid

    def __get_iter_for_ref(self, ref):
        if not ref:
            return None

        if ref.valid():
            return self.get_iter(ref.get_path())

    @property
    def active_ref(self):
        return self.__active_ref

    def set_active_ref(self, ref):
        self.set_state_for_active_ref(None)
        self.__active_ref = ref

    def remove_refs(self, refs):
        for ref in refs:
            tree_iter = self.__get_iter_for_ref(ref)
            if tree_iter:
                self.remove(tree_iter)

    def get_next_ref(self, ref):
        tree_iter = self.__get_iter_for_ref(ref)
        if not tree_iter:
            return None

        next_iter = self.iter_next(tree_iter)
        if not next_iter:
            return None

        return Gtk.TreeRowReference.new(self, self.get_path(next_iter))

    def get_prev_ref(self, ref):
        tree_iter = self.__get_iter_for_ref(ref)
        if not tree_iter:
            return None

        prev_iter = self.iter_previous(tree_iter)
        if not prev_iter:
            return None

        return Gtk.TreeRowReference.new(self, self.get_path(prev_iter))

    def get_position_for_ref(self, ref):
        tree_iter = self.get_iter(ref.get_path())
        return self.get_value(tree_iter, QUEUE_ID)

    def update_position_for_ref(self, ref, position):
        tree_iter = self.get_iter(ref.get_path())
        if position is not None:
            self.set_value(tree_iter, QUEUE_ID, position)
        else:
            self.set_value(tree_iter, QUEUE_ID, None)

    def get_track_path_for_ref(self, ref):
        tree_iter = self.__get_iter_for_ref(ref)
        if tree_iter:
            return self.get_value(tree_iter, SRC_ID)

    def get_artist_for_ref(self, ref):
        tree_iter = self.__get_iter_for_ref(ref)
        if tree_iter:
            return self.get_value(tree_iter, ARTIST_ID)

    def get_album_for_ref(self, ref):
        tree_iter = self.__get_iter_for_ref(ref)
        if tree_iter:
            return self.get_value(tree_iter, ALBUM_ID)

    def get_title_for_ref(self, ref):
        tree_iter = self.__get_iter_for_ref(ref)
        if tree_iter:
            return self.get_value(tree_iter, TITLE_ID)

    def add_row(self, row: dict, position_iter=None, insert_after=True):
        row = [row.get(c.get("key")) for c in PLAYLIST_COLS]
        if position_iter:
            if insert_after:
                tree_iter = self.insert_after(position_iter, row)
            else:
                tree_iter = self.insert_before(position_iter, row)
        else:
            tree_iter = self.append(row)

        return Gtk.TreeRowReference.new(self, self.get_path(tree_iter))

    def set_state_for_active_ref(self, value):
        tree_iter = self.__get_iter_for_ref(self.__active_ref)
        if tree_iter:
            self.set_value(tree_iter, STATE_ID, value)

    def get_state_for_iter(self, tree_iter):
        return self.get_value(tree_iter, STATE_ID)

    def get_first_and_select(self) -> str:
        tree_iter = self.get_iter_first()
        if not tree_iter:
            return None
        else:
            ref = Gtk.TreeRowReference.new(self, self.get_path(tree_iter))
            if ref:
                self.set_active_ref(ref)
                return ref

    def get_next_and_select(self):
        if self.__active_ref:
            next_ref = self.get_next_ref(self.__active_ref)
            if next_ref:
                self.set_active_ref(next_ref)
                return next_ref

    def get_prev_and_select(self):
        if self.__active_ref:
            prev_ref = self.get_prev_ref(self.__active_ref)
            if prev_ref:
                self.set_active_ref(prev_ref)
                return prev_ref

    @property
    def uuid(self):
        return uuid
