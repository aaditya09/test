import urllib.request
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

GITHUB_USER = "aaditya09"

LANG_COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#2b7489",
    "Go": "#00ADD8", "Java": "#b07219", "HTML": "#e34c26", "CSS": "#563d7c",
    "Shell": "#89e051", "Dockerfile": "#384d54", "Kotlin": "#A97BFF",
}


def fetch_repos():
    url = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100&sort=updated"
    req = urllib.request.Request(url, headers={"User-Agent": "webapp"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def repo_card(r):
    lang = r.get("language") or "Other"
    color = LANG_COLORS.get(lang, "#8b949e")
    desc = r.get("description") or "No description provided."
    updated = (r.get("updated_at") or "")[:10]
    return f"""
    <a class="card" href="{r['html_url']}" target="_blank">
        <div class="card-top">
            <span class="repo-name">{r['name']}</span>
            <span class="badge {'private' if r['private'] else 'public'}">{'Private' if r['private'] else 'Public'}</span>
        </div>
        <p class="desc">{desc}</p>
        <div class="card-bottom">
            <span class="lang"><i style="background:{color}"></i>{lang}</span>
            <span class="stat">&#9733; {r['stargazers_count']}</span>
            <span class="stat">&#9671; {r['forks_count']}</span>
            <span class="updated">Updated {updated}</span>
        </div>
    </a>
    """


@app.get("/", response_class=HTMLResponse)
def index():
    try:
        repos = fetch_repos()
    except Exception as e:
        return f"<h1 style='font-family:sans-serif;color:#e74c3c'>Error fetching repos: {e}</h1>"

    cards = "".join(repo_card(r) for r in repos)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{GITHUB_USER}'s Repositories</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg: #0d1117;
                --bg-alt: #161b22;
                --border: #30363d;
                --text: #e6edf3;
                --muted: #8b949e;
                --accent1: #7c3aed;
                --accent2: #06b6d4;
            }}
            * {{ box-sizing: border-box; }}
            body {{
                margin: 0;
                font-family: 'Inter', sans-serif;
                background:
                    radial-gradient(circle at 15% 0%, rgba(124,58,237,0.25), transparent 40%),
                    radial-gradient(circle at 85% 20%, rgba(6,182,212,0.20), transparent 40%),
                    var(--bg);
                color: var(--text);
                min-height: 100vh;
            }}
            header {{
                padding: 3rem 2rem 2rem;
                text-align: center;
            }}
            header h1 {{
                margin: 0;
                font-size: 2.4rem;
                font-weight: 800;
                background: linear-gradient(90deg, var(--accent1), var(--accent2));
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
            }}
            header p {{
                margin: 0.5rem 0 0;
                color: var(--muted);
                font-size: 1rem;
            }}
            .stats-bar {{
                display: flex;
                justify-content: center;
                gap: 2.5rem;
                margin: 1.5rem 0 0;
                flex-wrap: wrap;
            }}
            .stats-bar div {{
                text-align: center;
            }}
            .stats-bar .num {{
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text);
            }}
            .stats-bar .label {{
                font-size: 0.8rem;
                color: var(--muted);
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            .grid {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 1rem 2rem 4rem;
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 1.25rem;
            }}
            .card {{
                background: var(--bg-alt);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 1.25rem;
                text-decoration: none;
                color: var(--text);
                display: flex;
                flex-direction: column;
                gap: 0.6rem;
                transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
            }}
            .card:hover {{
                transform: translateY(-4px);
                border-color: var(--accent2);
                box-shadow: 0 12px 24px rgba(0,0,0,0.35);
            }}
            .card-top {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 0.5rem;
            }}
            .repo-name {{
                font-weight: 700;
                font-size: 1.05rem;
                color: var(--accent2);
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }}
            .badge {{
                font-size: 0.7rem;
                font-weight: 600;
                padding: 0.15rem 0.55rem;
                border-radius: 999px;
                white-space: nowrap;
            }}
            .badge.public {{ background: rgba(6,182,212,0.15); color: var(--accent2); }}
            .badge.private {{ background: rgba(124,58,237,0.2); color: #c4b5fd; }}
            .desc {{
                margin: 0;
                color: var(--muted);
                font-size: 0.88rem;
                line-height: 1.4;
                flex-grow: 1;
                overflow: hidden;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
            }}
            .card-bottom {{
                display: flex;
                align-items: center;
                gap: 0.9rem;
                flex-wrap: wrap;
                font-size: 0.78rem;
                color: var(--muted);
                border-top: 1px solid var(--border);
                padding-top: 0.6rem;
            }}
            .lang {{
                display: flex;
                align-items: center;
                gap: 0.35rem;
            }}
            .lang i {{
                width: 9px;
                height: 9px;
                border-radius: 50%;
                display: inline-block;
            }}
            .updated {{
                margin-left: auto;
            }}
            footer {{
                text-align: center;
                color: var(--muted);
                font-size: 0.8rem;
                padding-bottom: 2rem;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>{GITHUB_USER}'s Repositories</h1>
            <p>A live snapshot pulled straight from GitHub</p>
            <div class="stats-bar">
                <div><div class="num">{len(repos)}</div><div class="label">Repos</div></div>
                <div><div class="num">{sum(r['stargazers_count'] for r in repos)}</div><div class="label">Stars</div></div>
                <div><div class="num">{sum(r['forks_count'] for r in repos)}</div><div class="label">Forks</div></div>
            </div>
        </header>
        <div class="grid">
            {cards}
        </div>
        <footer>Built with FastAPI &middot; data via GitHub public API</footer>
    </body>
    </html>
    """
