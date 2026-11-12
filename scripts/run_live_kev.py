from app.kev import fetch_live,enrich
try:
    feed=fetch_live()
    print('KEV entries:',len(feed['vulnerabilities']))
    print('FIN-DB01:',enrich('FIN-DB01',feed))
except Exception as exc:
    print('Live KEV unavailable; use bundled offline fixture:',type(exc).__name__)
