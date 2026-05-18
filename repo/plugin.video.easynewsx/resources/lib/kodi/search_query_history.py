from time import time


class SearchQueryHistory:
    """Rolling list of recent global Easynews search strings (not newsgroup shortcuts)."""

    MAX_ENTRIES = 10
    filename = "search_query_history.json"

    def __init__(self, vfs):
        self.vfs = vfs
        self.history = self.vfs.get_json_as_obj(self.filename, default={})

    def get(self):
        keys = sorted(list(self.history), reverse=True)[: self.MAX_ENTRIES]
        return {k: self.history[k] for k in keys}

    def add(self, query):
        q = (query or "").strip()
        if not q:
            return
        for k, v in list(self.history.items()):
            if isinstance(v, dict) and v.get("query") == q:
                del self.history[k]
                break
        self.history[str(int(time()))] = {"query": q}
        self.history = self._reduce(self.history)
        self._save()

    def remove(self, query):
        self.history = {
            k: v
            for k, v in list(self.history.items())
            if not (isinstance(v, dict) and v.get("query") == query)
        }
        self._save()

    def clear(self):
        r = self.vfs.delete(self.filename)
        self.history = {}
        return r

    def _save(self):
        return self.vfs.save_obj_to_json(self.filename, self.history)

    def _reduce(self, history):
        keys = sorted(list(history), reverse=True)[: self.MAX_ENTRIES]
        return {k: history[k] for k in keys}
