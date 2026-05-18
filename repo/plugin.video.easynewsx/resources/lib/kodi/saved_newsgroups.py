from time import time


class SavedNewsgroups:
    """Persists saved newsgroup names (browse shortcuts), not search-query history."""

    filename = "saved_newsgroups.json"
    _setting_max = "browse.saved_newsgroups_max"

    def __init__(self, settings, vfs):
        self.settings = settings
        self.vfs = vfs
        self.size = int(self.settings.get(self._setting_max) or "10")
        self.history = self.vfs.get_json_as_obj(self.filename, default={})

    def get(self):
        return {k: self.history[k] for k in list(self.history)[: self.size]}

    def add(self, newsgroup):
        for k, v in list(self.history.items()):
            if isinstance(v, dict) and v.get("newsgroup") == newsgroup:
                return

        self.history[str(int(time()))] = {"newsgroup": newsgroup}
        self.history = self._reduce(self.history)
        self._save()

    def remove(self, newsgroup):
        self.history = {
            k: v
            for k, v in list(self.history.items())
            if not (isinstance(v, dict) and v.get("newsgroup") == newsgroup)
        }
        self._save()

    def clear(self):
        return self.vfs.delete(self.filename)

    def _save(self):
        return self.vfs.save_obj_to_json(self.filename, self.history)

    def _reduce(self, history):
        return {k: history[k] for k in sorted(list(history), reverse=True)[: self.size]}
