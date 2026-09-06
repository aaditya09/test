import urllib.request
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

GITHUB_USER = "aaditya09"


def fetch_repos():
    url = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100&sort=updated"
    req = urllib.request.Request(url, headers={"User-Agent": "webapp"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


@app.get("/", response_class=HTMLResponse)
def index():
    try:
        repos = fetch_repos()
    except Exception as e:
        return f"<h1>Error fetching repos</h1><p>{e}</p>"

    rows = "".join(
        f"<tr><td><a href='{r['html_url']}' target='_blank'>{r['name']}</a></td>"
        f"<td>{r.get('description') or ''}</td>"
        f"<td>{'private' if r['private'] else 'public'}</td>"
        f"<td>&#9733; {r['stargazers_count']}</td></tr>"
        for r in repos
    )

    return f"""
    <html>
    <head>
        <title>{GITHUB_USER}'s Repos</title>
        <style>
            body {{ font-family: sans-serif; margin: 2rem; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
            th {{ background: #f4f4f4; }}
        </style>
    </head>
    <body>
        <h1>{GITHUB_USER}'s GitHub Repositories</h1>
        <table>
            <tr><th>Name</th><th>Description</th><th>Visibility</th><th>Stars</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """
