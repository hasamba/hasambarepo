# -*- coding: utf-8 -*-
"""Easynews HTTP/JSON search API."""
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

import xbmc

from resources.lib.easynews import context as ctx

_LOG = "plugin.video.easynewsx"

_RES_TERM_RE = re.compile(r"(?<!\d)(720|1080|2160)(?!\d)")


def easynews_gps_with_resolution_term(query, res=""):
    """Append +720, +1080, or +2160 to gps search terms (EasyNews +term syntax)."""
    res = (res or "").strip().lower()
    if res not in ("720", "1080", "2160"):
        return query or ""
    q = query or ""
    norm = q.replace("+", " ").lower()
    if _RES_TERM_RE.search(norm):
        return q
    if not q.strip():
        return res
    return q + "+" + res


_OPENER_CACHE = {
    "key": None,  # (username, password)
    "opener": None,
    "cookies": None,
}


def _headers_to_dict(msg):
    out = {}
    if msg is None:
        return out
    try:
        for k, v in msg.items():
            out[k] = v
    except Exception:
        pass
    return out


def _hdr(headers, name, default=""):
    if not headers:
        return default
    nl = name.lower()
    for k, v in headers.items():
        if k.lower() == nl:
            return v
    return default


def _safe_body_preview(raw, max_chars=400):
    """UTF-8 safe snippet for logs; newlines collapsed; no huge dumps."""
    if raw is None:
        return "<none>"
    if isinstance(raw, bytes):
        chunk = raw[:1200]
        try:
            s = chunk.decode("utf-8", errors="replace")
        except Exception:
            s = repr(chunk[:120])
    else:
        s = str(raw)[:1200]
    s = s.replace("\r", " ").replace("\n", " ").strip()
    if len(s) > max_chars:
        s = s[: max_chars - 3] + "..."
    return s


def _log_search_diag(context, **parts):
    """One ERROR line per failure (status, headers, body preview). No auth secrets."""
    try:
        bits = ["search {}".format(context)]
        for k in sorted(parts.keys()):
            v = parts[k]
            if v is None or v == "":
                continue
            if isinstance(v, str) and len(v) > 500:
                v = v[:497] + "..."
            bits.append(str(k) + "=" + str(v))
        xbmc.log(_LOG + ": " + " | ".join(bits), xbmc.LOGERROR)
    except Exception as log_err:
        try:
            xbmc.log(
                "{}: search diag logging failed: {}".format(_LOG, log_err),
                xbmc.LOGWARNING,
            )
        except Exception:
            pass


class EasynewsSearchFailed(Exception):
    """Search request failed; ``args[0]`` is a short user-facing reason."""

    @property
    def reason(self):
        return self.args[0] if self.args else ""


def ng_condense(newsgroup):
    return newsgroup.replace("alt.binaries.", "a.b.")


def easynews_thumbnail_url_from_dl_url(dl_url):
    """
    Best-effort Easynews thumbnail URL from a members dl link (same pattern as search results).
    Parses /dl/<id+codec>/... and strips a known file extension to recover id.
    """
    if not dl_url or "members.easynews.com/dl/" not in dl_url:
        return None
    try:
        path = urllib.parse.urlparse(dl_url).path.strip("/")
        parts = path.split("/")
        if len(parts) < 2 or parts[0] != "dl":
            return None
        segment = parts[1]
        exts = (
            ".mkv",
            ".mp4",
            ".avi",
            ".wmv",
            ".divx",
            ".mpg",
            ".mpeg",
            ".mov",
            ".webm",
            ".flv",
            ".001",
            ".zip",
            ".rar",
        )
        id_val = None
        low = segment.lower()
        for ext in exts:
            if low.endswith(ext):
                id_val = segment[: -len(ext)]
                break
        if not id_val or len(id_val) < 3:
            return None
        return (
            "https://th.easynews.com/thumbnails-"
            + id_val[0]
            + id_val[1]
            + id_val[2]
            + "/pr-"
            + id_val
            + ".jpg"
        )
    except (IndexError, TypeError, ValueError):
        return None


def format_video_duration(seconds):
    """Human-readable duration for info text, e.g. 2h32m43s, 32m43s, 43s."""
    try:
        sec = int(seconds)
    except (TypeError, ValueError):
        return ""
    if sec <= 0:
        return ""
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return "{}h{}m{}s".format(h, m, s)
    if m > 0:
        return "{}m{}s".format(m, s)
    return "{}s".format(s)


def video_list_item_plot(video):
    """Sidebar / info panel plot: newsgroups, post subject, resolution+fps one line, duration (search + play history)."""
    ng_raw = (video.get("newsgroups") or "").strip()
    if ng_raw:
        ng_parts = [p for p in ng_raw.split() if p]
        ng_head = ng_parts[:3]
        ng_line = " ".join(ng_head)
        if len(ng_parts) > 3:
            ng_line += " ..."
        plot = ng_line + "\n\n"
    else:
        plot = "\n\n"
    plot += (video.get("post_subject") or "") + "\n"
    res = (video.get("resolution") or "").strip()
    if res:
        res = re.sub(r"(\d+)\s*[xX]\s*(\d+)", r"\1 x \2", res, count=1)
    try:
        fps = int(video.get("fps") or 0)
    except (TypeError, ValueError):
        fps = 0
    if res and fps > 0:
        plot += "{}, {}fps\n".format(res, fps)
    elif res:
        plot += res + "\n"
    elif fps > 0:
        plot += "{}fps\n".format(fps)
    try:
        runtime_sec = int(video.get("runtime") or 0)
    except (TypeError, ValueError):
        runtime_sec = 0
    if runtime_sec > 0:
        dur = format_video_duration(runtime_sec)
        if dur:
            plot += "Duration: {}".format(dur)
    return plot


def append_duration_to_plot(plot, runtime_seconds):
    """If plot text has no Duration line yet, append one (for older play-history JSON)."""
    if not runtime_seconds:
        return plot or ""
    try:
        sec = int(runtime_seconds)
    except (TypeError, ValueError):
        return plot or ""
    if sec <= 0:
        return plot or ""
    text = plot or ""
    if "Duration:" in text:
        return text
    dur = format_video_duration(sec)
    if not dur:
        return text
    return text.rstrip() + "\nDuration: {}".format(dur)


def easynews_search_strip(query):
    query = query.lower()
    strip_chars = list(":()\"!&+-,.")
    query = query.replace("’", "")
    query = query.replace("'", "")
    query = query.replace("the ", "")
    for c in strip_chars:
        query = query.replace(c, " ")
    return query


def parse_easynews_data(data, dl_farm=None, dl_port=None, down_url=None):
    video_data = []
    for field in data:
        id = field['0']
        size = field['4']
        date_posted = field["5"].split(" ")[0]
        date_posted = date_posted.split("-")
        date_posted = "{}-{}-{}".format(date_posted[2], date_posted[0], date_posted[1])
        codec = field['11']
        name = field['10']
        post_name = name.replace(".", " ")
        downloadname = str(name).replace('+', ' ') + codec
        lang = field['alangs']
        lang = '[COLOR yellow]%s[/COLOR]' % (lang)
        url = 'https://members.easynews.com/dl/' + id + codec + '/' + name + codec
        try:
            sig = field.get("sig") if isinstance(field, dict) else None
        except Exception:
            sig = None
        if dl_farm and dl_port and down_url and sig:
            try:
                base = (down_url or "").rstrip("/")
                qs = urllib.parse.urlencode({"sig": sig})
                url = "{}/{}/{}/{}{}{}?{}".format(
                    base, dl_farm, dl_port, id, codec, "/" + name + codec, qs
                )
            except Exception:
                pass
        codec_disp = codec.replace('.', '').upper()
        name = "{} [B][{} {}] {}[/B] {}".format(date_posted, size, codec_disp, lang, name)
        name = name.replace('None', '').replace("u'", '').replace("'", '')
        iconimage = 'https://th.easynews.com/thumbnails-' + id[0] + id[1] + id[2] + '/pr-' + id + '.jpg'
        vd = {
            "name": name,
            "thumb": iconimage,
            "video": url,
            "runtime": field["runtime"],
            "downloadname": downloadname,
            "newsgroups": field["9"],
            "postname": post_name,
            "fps": field["17"],
            "resolution": field["fullres"],
            "rawsize": field["rawSize"],
            "post_subject": field["6"],
            "file_ext": codec.replace('.', '').upper(),
        }
        video_data.append(vd)
    return video_data


def get_easynews_results(query, newsgroup, page, filetype, override_results_per_page):
    url = "https://members.easynews.com/2.0/search/solr-search/advanced?"
    url += "gps=" + query
    url += "&sbj="
    url += "&ns=" + newsgroup
    url += "&pno=" + str(page)
    if override_results_per_page == 0:
        url += "&pby=" + str(ctx.results_per_page)
    else:
        url += "&pby=" + str(override_results_per_page)
    url += "&u=1"
    url += "&fty[]=" + str(filetype)
    url += "&s1=dtime&s1d="
    if ctx.date_sort_order == 0:
        url += "-"
    else:
        url += "+"
    url += "&s2=nrfile&s2d=-"
    url += "&st=adv&safeO"
    xbmc.log("{}: search URL: {}".format(_LOG, url), xbmc.LOGDEBUG)
    meta = {}
    t0 = time.time()
    try:
        raw, _cookies, meta = get_https_with_auth(url)
    except urllib.error.HTTPError as e:
        err_body = b""
        try:
            err_body = e.read(8000)
        except Exception:
            pass
        hdrs = _headers_to_dict(e.headers)
        final = ""
        try:
            final = e.geturl() or ""
        except Exception:
            pass
        _log_search_diag(
            "HTTPError",
            http_code=e.code,
            request_url=url,
            final_url=final,
            content_type=_hdr(hdrs, "Content-Type"),
            content_length=_hdr(hdrs, "Content-Length"),
            transfer_encoding=_hdr(hdrs, "Transfer-Encoding"),
            server=_hdr(hdrs, "Server"),
            www_authenticate=_hdr(hdrs, "WWW-Authenticate"),
            body_len=len(err_body),
            body_preview=_safe_body_preview(err_body),
        )
        if e.code == 401:
            raise EasynewsSearchFailed(
                "EasyNews authentication failed (HTTP 401). Check your username and password in settings."
            )
        if e.code == 403:
            raise EasynewsSearchFailed(
                "EasyNews access failed (HTTP 403). Check your EasyNews account status and try again."
            )
        raise EasynewsSearchFailed(
            "EasyNews search failed (HTTP {}). Try again later.".format(e.code)
        )
    except urllib.error.URLError as e:
        _log_search_diag(
            "URLError",
            request_url=url,
            reason=repr(e.reason),
        )
        raise EasynewsSearchFailed(
            "Could not reach EasyNews. Check your connection and try again."
        )

    hdrs = meta.get("headers") or {}
    if raw is None or not (raw.strip() if isinstance(raw, (bytes, bytearray)) else str(raw).strip()):
        _log_search_diag(
            "empty_body",
            http_code=meta.get("status"),
            request_url=url,
            final_url=meta.get("final_url") or "",
            content_type=_hdr(hdrs, "Content-Type"),
            content_length=_hdr(hdrs, "Content-Length"),
            transfer_encoding=_hdr(hdrs, "Transfer-Encoding"),
            server=_hdr(hdrs, "Server"),
            body_len=len(raw or b""),
        )
        raise EasynewsSearchFailed("EasyNews returned an empty response. Try again.")

    try:
        response = json.loads(raw)
    except json.JSONDecodeError as e:
        _log_search_diag(
            "JSONDecodeError",
            http_code=meta.get("status"),
            request_url=url,
            final_url=meta.get("final_url") or "",
            content_type=_hdr(hdrs, "Content-Type"),
            content_length=_hdr(hdrs, "Content-Length"),
            body_len=len(raw),
            body_preview=_safe_body_preview(raw),
            json_msg=str(e),
        )
        raise EasynewsSearchFailed(
            "EasyNews did not return valid search data. Try again."
        )

    try:
        results = response["results"]
        page = response["page"]
        data = response["data"]
    except (KeyError, TypeError) as e:
        keys = ""
        if isinstance(response, dict):
            keys = ",".join(sorted(str(k) for k in list(response.keys())[:25]))
        _log_search_diag(
            "response_shape_error",
            http_code=meta.get("status"),
            content_type=_hdr(hdrs, "Content-Type"),
            body_len=len(raw),
            top_keys=keys or type(response).__name__,
            err=repr(e),
        )
        raise EasynewsSearchFailed(
            "EasyNews response was incomplete. Try again or check for add-on updates."
        )

    dl_farm = response.get("dlFarm") if isinstance(response, dict) else None
    dl_port = response.get("dlPort") if isinstance(response, dict) else None
    down_url = response.get("downURL") if isinstance(response, dict) else None

    try:
        video_data = parse_easynews_data(
            data,
            dl_farm=dl_farm,
            dl_port=str(dl_port or ""),
            down_url=down_url,
        )
    except (KeyError, TypeError) as e:
        _log_search_diag(
            "parse_rows_error",
            http_code=meta.get("status"),
            data_type=type(data).__name__,
            err=repr(e),
        )
        raise EasynewsSearchFailed(
            "Could not read search results. The service format may have changed."
        )

    try:
        ms = int((time.time() - t0) * 1000)
        xbmc.log(
            "{}: search total {}ms results={} page={}".format(_LOG, ms, results, page),
            xbmc.LOGDEBUG,
        )
    except Exception:
        pass

    return video_data, results, page


def get_https_with_auth(url, timeout=60):
    """
    Authenticated HTTPS GET with best-effort connection reuse.

    Historically this function rebuilt a new opener/cookiejar per request, which can be
    noticeably slower for some users (extra DNS+TLS handshakes). We keep a cached opener
    keyed by current credentials to allow keep-alive reuse.
    """
    import gzip
    import http.cookiejar as cookielib

    t0 = time.time()
    try:
        creds_key = (getattr(ctx, "username", None) or "", getattr(ctx, "password", None) or "")

        opener = _OPENER_CACHE.get("opener")
        cookies = _OPENER_CACHE.get("cookies")
        if _OPENER_CACHE.get("key") != creds_key or opener is None or cookies is None:
            cookies = cookielib.LWPCookieJar()
            passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, url, creds_key[0], creds_key[1])
            handlers = [
                urllib.request.HTTPHandler(),
                urllib.request.HTTPSHandler(),
                urllib.request.HTTPCookieProcessor(cookies),
                urllib.request.HTTPBasicAuthHandler(passman),
            ]
            opener = urllib.request.build_opener(*handlers)
            _OPENER_CACHE["key"] = creds_key
            _OPENER_CACHE["opener"] = opener
            _OPENER_CACHE["cookies"] = cookies

        req = urllib.request.Request(url)
        req.add_header("Cookie", ctx.easynews_chickenlicker_cookie_header())
        req.add_header("User-Agent", "{} {}".format(_LOG, getattr(ctx, "addon_version", "")))
        req.add_header("Accept-Encoding", "gzip")
        req.add_header("Connection", "keep-alive")

        response = opener.open(req, timeout=timeout)
        status = response.getcode()
        final_url = response.geturl()
        headers = _headers_to_dict(response.headers)
        raw = response.read()

        enc = _hdr(headers, "Content-Encoding", "").lower()
        if "gzip" in enc and isinstance(raw, (bytes, bytearray)):
            try:
                raw = gzip.decompress(raw)
            except Exception:
                pass

        meta = {
            "status": status,
            "final_url": final_url,
            "headers": headers,
        }

        try:
            ms = int((time.time() - t0) * 1000)
            xbmc.log(
                "{}: search http ok in {}ms status={} len={}".format(_LOG, ms, status, len(raw or b"")),
                xbmc.LOGDEBUG,
            )
        except Exception:
            pass

        return raw, cookies, meta
    except Exception:
        raise