# -*- coding: utf-8 -*-
"""Addon-wide constants (URLs, filenames).

Release version: bump ``addon.xml`` (``version="x.y.z"``) for GitHub/Kodi builds.
``context.addon_version`` is read from Kodi after install; keep ``ADDON_VERSION``
below in sync as a fallback / quick reference.
"""

# Bump with addon.xml for each release.
ADDON_VERSION = "6.5.1"

# TMDB API v3 key (EasyNewsKodi developer registration; read-only metadata).
# Paste the key from https://www.themoviedb.org/settings/api — required for new installs
# after the settings field was removed. Orphaned ``general.tmdb_api_key`` in userdata
# is still read as a fallback until this is set.
TMDB_V3_API_KEY = "02d95f3b35aace6d1814e6b8ce28a106"

APPLOG_BASE_URL = "https://applog.clientsite.co.uk/easynewskodi/"
INSTALL_ID_FILENAME = "install_id.json"

# Last account banner from /3.0/ scrape (see members_home.run_account_refresh_action).
ACCOUNT_MENU_LABEL_CACHE = "account_menu_label.json"

# Last addon.xml <news> digest shown in the what's-new popup (see addon_news.py).
ADDON_NEWS_SEEN_CACHE = "addon_news_seen.json"
