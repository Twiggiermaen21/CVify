import urllib.request
import json
import re

req = urllib.request.Request('http://127.0.0.1:8000/api/cv')
res = urllib.request.urlopen(req).read()
resp = json.loads(res.decode('utf-8'))
cv_data = resp["cv"]

for template_name in ["rose", "sidebar"]:
    payload = dict(cv_data)
    payload["_template"] = template_name
    preview_req = urllib.request.Request(
        'http://127.0.0.1:8000/api/preview-html',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    html = urllib.request.urlopen(preview_req).read().decode('utf-8')
    print(f"\n==================== Template: {template_name} ====================")
    # Search for all elements inside sidebar
    sidebar_match = re.search(r'(?:sidebar|cv-sidebar-col|rs-sidebar)[^>]*>(.*?)</td>', html, re.DOTALL | re.IGNORECASE)
    if sidebar_match:
        sidebar_content = sidebar_match.group(1)
        headers = re.findall(r'<div class="[^"]*title[^"]*">([^<]+)</div>|<div class="[^"]*heading[^"]*">([^<]+)</div>', sidebar_content, re.IGNORECASE)
        print("Sidebar headers found:")
        for h in headers:
            print("  *", [x for x in h if x])
    else:
        print("Sidebar not matched with regex, printing slice:")
        print(html[html.find('<body'):html.find('<body')+1000])
