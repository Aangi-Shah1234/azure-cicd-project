from flask import Flask, jsonify, render_template_string
from datetime import datetime
import platform, sys

app = Flask(__name__)
START_TIME = datetime.utcnow()

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Azure CI/CD — Live</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Syne:wght@400;700;800&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg:      red;
    --surface: #0d1117;
    --border:  #1e2a3a;
    --accent:  #00d4ff;
    --accent2: #7c3aed;
    --green:   #22c55e;
    --amber:   #f59e0b;
    --text:    #e2e8f0;
    --muted:   #4a5568;
    --glow:    rgba(0,212,255,0.15);
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'JetBrains Mono',monospace;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
  body::before{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(0,212,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,0.03) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;z-index:0}
  body::after{content:'';position:fixed;top:-200px;left:-200px;width:600px;height:600px;background:radial-gradient(circle,rgba(124,58,237,0.12) 0%,transparent 70%);pointer-events:none;z-index:0}
  .orb2{position:fixed;bottom:-150px;right:-100px;width:500px;height:500px;background:radial-gradient(circle,rgba(0,212,255,0.08) 0%,transparent 70%);pointer-events:none;z-index:0}
  main{position:relative;z-index:1;max-width:900px;margin:0 auto;padding:60px 24px 80px}

  .header{display:flex;align-items:center;gap:16px;margin-bottom:56px;animation:fadeDown 0.6s ease both}
  .logo{width:48px;height:48px;background:linear-gradient(135deg,var(--accent2),var(--accent));border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 0 24px rgba(0,212,255,0.3);flex-shrink:0}
  .header-text h1{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;letter-spacing:-0.02em;color:#fff}
  .header-text p{font-size:12px;color:var(--muted);margin-top:2px}
  .live-badge{margin-left:auto;display:flex;align-items:center;gap:6px;background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.3);border-radius:20px;padding:6px 14px;font-size:12px;color:var(--green);font-weight:600}
  .pulse{width:7px;height:7px;background:var(--green);border-radius:50%;animation:pulse 1.8s infinite}

  .status-banner{background:linear-gradient(135deg,rgba(0,212,255,0.06),rgba(124,58,237,0.06));border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:12px;padding:20px 24px;margin-bottom:32px;display:flex;align-items:center;gap:16px;animation:fadeUp 0.6s 0.1s ease both}
  .status-icon{font-size:28px}
  .status-text h2{font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:#fff}
  .status-text p{font-size:12px;color:var(--muted);margin-top:3px}

  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:32px}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:20px;transition:border-color 0.2s,box-shadow 0.2s;animation:fadeUp 0.6s ease both}
  .card:hover{border-color:var(--accent);box-shadow:0 0 20px var(--glow)}
  .card:nth-child(1){animation-delay:0.15s}.card:nth-child(2){animation-delay:0.22s}.card:nth-child(3){animation-delay:0.29s}.card:nth-child(4){animation-delay:0.36s}
  .card-label{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.12em;color:var(--muted);margin-bottom:8px}
  .card-value{font-size:20px;font-weight:700;color:var(--accent)}
  .card-sub{font-size:11px;color:var(--muted);margin-top:4px}

  .section-title{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.12em;color:var(--muted);margin-bottom:12px;animation:fadeUp 0.6s 0.4s ease both}
  .endpoints{background:var(--surface);border:1px solid var(--border);border-radius:12px;overflow:hidden;margin-bottom:32px;animation:fadeUp 0.6s 0.45s ease both}
  .endpoint-row{display:flex;align-items:center;gap:16px;padding:14px 20px;border-bottom:1px solid var(--border);transition:background 0.15s}
  .endpoint-row:last-child{border-bottom:none}
  .endpoint-row:hover{background:rgba(255,255,255,0.02)}
  .method{font-size:11px;font-weight:700;padding:3px 8px;border-radius:5px;min-width:46px;text-align:center}
  .get{background:rgba(0,212,255,0.1);color:var(--accent);border:1px solid rgba(0,212,255,0.2)}
  .path{font-size:14px;color:#fff;flex:1}
  .ep-desc{font-size:12px;color:var(--muted)}
  .ep-status{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 6px var(--green);flex-shrink:0}

  .terminal{background:#020408;border:1px solid var(--border);border-radius:12px;overflow:hidden;animation:fadeUp 0.6s 0.5s ease both;margin-bottom:48px}
  .terminal-header{background:#0d1117;padding:10px 16px;display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--border)}
  .dot{width:10px;height:10px;border-radius:50%}
  .dot-r{background:#ef4444}.dot-y{background:#f59e0b}.dot-g{background:#22c55e}
  .terminal-title{font-size:11px;color:var(--muted);margin-left:8px}
  .terminal-body{padding:20px 24px;font-size:13px;line-height:2.1}
  .t-muted{color:var(--muted)}.t-accent{color:var(--accent)}.t-green{color:var(--green)}.t-amber{color:var(--amber)}.t-purple{color:#a78bfa}.t-white{color:#fff}

  footer{text-align:center;font-size:11px;color:var(--muted);animation:fadeUp 0.6s 0.6s ease both}
  footer span{color:var(--accent)}

  .cursor{display:inline-block;width:8px;height:14px;background:var(--accent);vertical-align:middle;margin-left:2px;animation:blink 1s infinite}

  @keyframes fadeDown{from{opacity:0;transform:translateY(-16px)}to{opacity:1;transform:translateY(0)}}
  @keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
  @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.4;transform:scale(0.85)}}
  @keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
</style>
</head>
<body>
<div class="orb2"></div>
<main>

  <div class="header">
    <div class="logo">☁️</div>
    <div class="header-text">
      <h1>Azure CI/CD Pipeline</h1>
      <p>Deployment Monitor &nbsp;·&nbsp; Production Environment</p>
    </div>
    <div class="live-badge"><div class="pulse"></div>LIVE</div>
  </div>

  <div class="status-banner">
    <div class="status-icon">✅</div>
    <div class="status-text">
      <h2>Azure CI/CD App Running Successfully</h2>
      <p>All systems operational &nbsp;·&nbsp; Last checked just now</p>
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="card-label">Status</div>
      <div class="card-value" style="color:var(--green)">● Healthy</div>
      <div class="card-sub">All endpoints responding</div>
    </div>
    <div class="card">
      <div class="card-label">Environment</div>
      <div class="card-value">Production</div>
      <div class="card-sub">Azure App Service</div>
    </div>
    <div class="card">
      <div class="card-label">Runtime</div>
      <div class="card-value">Python {{ py }}</div>
      <div class="card-sub">Flask &nbsp;·&nbsp; {{ os }}</div>
    </div>
    <div class="card">
      <div class="card-label">Started (UTC)</div>
      <div class="card-value" style="font-size:13px">{{ started }}</div>
      <div class="card-sub">Uptime tracking active</div>
    </div>
  </div>

  <div class="section-title">API Endpoints</div>
  <div class="endpoints">
    <div class="endpoint-row">
      <span class="method get">GET</span>
      <span class="path">/</span>
      <span class="ep-desc">Home — deployment status page</span>
      <div class="ep-status"></div>
    </div>
    <div class="endpoint-row">
      <span class="method get">GET</span>
      <span class="path">/health</span>
      <span class="ep-desc">Health check — returns "healthy"</span>
      <div class="ep-status"></div>
    </div>
    <div class="endpoint-row">
      <span class="method get">GET</span>
      <span class="path">/api/status</span>
      <span class="ep-desc">JSON system status &amp; metadata</span>
      <div class="ep-status"></div>
    </div>
  </div>

  <div class="section-title">Deployment Log</div>
  <div class="terminal">
    <div class="terminal-header">
      <div class="dot dot-r"></div>
      <div class="dot dot-y"></div>
      <div class="dot dot-g"></div>
      <span class="terminal-title">bash — azure-pipeline · ci-cd-deploy</span>
    </div>
    <div class="terminal-body">
      <div><span class="t-muted">$</span> <span class="t-accent">az pipeline run</span> <span class="t-muted">--name</span> <span class="t-white">ci-cd-deploy</span></div>
      <div><span class="t-muted">›</span> <span class="t-green">✔</span> <span class="t-white">Source code pulled from GitHub</span></div>
      <div><span class="t-muted">›</span> <span class="t-green">✔</span> <span class="t-white">Dependencies installed</span> <span class="t-muted">(requirements.txt)</span></div>
      <div><span class="t-muted">›</span> <span class="t-green">✔</span> <span class="t-white">Unit tests passed</span> <span class="t-muted">— 0 failures</span></div>
      <div><span class="t-muted">›</span> <span class="t-green">✔</span> <span class="t-white">Docker image built and pushed to ACR</span></div>
      <div><span class="t-muted">›</span> <span class="t-green">✔</span> <span class="t-white">Deployed to Azure App Service</span></div>
      <div><span class="t-muted">›</span> <span class="t-purple">ℹ</span> <span class="t-white">Listening on</span> <span class="t-accent">0.0.0.0:5000</span></div>
      <div><span class="t-muted">$</span> <span class="t-amber">_</span><span class="cursor"></span></div>
    </div>
  </div>

  <footer>Built with <span>Flask</span> &nbsp;·&nbsp; Deployed via <span>Azure DevOps</span> &nbsp;·&nbsp; Python {{ py }}</footer>

</main>
</body>
</html>"""


@app.route("/")
def home():
    return render_template_string(
        HTML,
        py=sys.version.split()[0],
        os=platform.system(),
        started=START_TIME.strftime("%Y-%m-%d  %H:%M:%S")
    )


@app.route("/health")
def health():
    return "healthy"


@app.route("/api/status")
def status():
    return jsonify({
        "status":      "healthy",
        "message":     "Azure CI/CD App Running Successfully",
        "python":      sys.version.split()[0],
        "platform":    platform.system(),
        "started_utc": START_TIME.isoformat()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
