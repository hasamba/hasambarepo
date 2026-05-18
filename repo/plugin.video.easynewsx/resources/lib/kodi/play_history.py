from time import time


class PlayHistory:
    """Rolling list of recently played Easynews stream URLs with display titles."""

    MAX_ENTRIES = 10
    filename = "play_history.json"

    def __init__(self, vfs):
        self.vfs = vfs
        self.history = self.vfs.get_json_as_obj(self.filename, default={})

    def get(self):
        keys = sorted(list(self.history), reverse=True)[: self.MAX_ENTRIES]
        return {k: self.history[k] for k in keys}

    def add(self, title, video_url, thumb=None, plot=None, runtime=None, newsgroups=None):
        title = (title or "").strip()
        video_url = (video_url or "").strip()
        if not video_url:
            return
        if not title:
            title = video_url.split("/")[-1] or video_url
        if len(title) > 500:
            title = title[:500]
        for k, v in list(self.history.items()):
            if isinstance(v, dict) and v.get("video") == video_url:
                del self.history[k]
                break
        entry = {"title": title, "video": video_url}
        if thumb:
            entry["thumb"] = thumb
        if plot:
            entry["plot"] = plot
        ng = (newsgroups or "").strip()
        if ng:
            entry["newsgroups"] = ng
        if runtime is not None:
            try:
                entry["runtime"] = int(runtime)
            except (TypeError, ValueError):
                pass
        self.history[str(int(time()))] = entry
        self.history = self._reduce(self.history)
        self._save()

    def remove(self, video_url):
        video_url = video_url or ""
        self.history = {
            k: v
            for k, v in list(self.history.items())
            if not (isinstance(v, dict) and v.get("video") == video_url)
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
