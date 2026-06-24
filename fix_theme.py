import os

# Fix style.css
css_path = r"c:\RepoMindSpace\RepoMindSpace\css\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Fix glass-panel
css = css.replace("background: rgba(30, 41, 59, 0.6);", "background: var(--glass-bg);")
css = css.replace("border: 1px solid rgba(255, 255, 255, 0.05);", "border: 1px solid var(--glass-border);")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

# Fix create-workspace.html
html_path = r"c:\RepoMindSpace\RepoMindSpace\pages\create-workspace.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix .form-input-saas
html = html.replace("background: rgba(0, 0, 0, 0.2);", "background: var(--bg-dark);")
html = html.replace("border: 1px solid rgba(255, 255, 255, 0.1);", "border: 1px solid var(--border-color);")
html = html.replace("color: white;\n            transition: border-color", "color: var(--text-main);\n            transition: border-color")
html = html.replace("background: rgba(255, 255, 255, 0.03);", "background: var(--bg-card);")
html = html.replace("background: rgba(255, 255, 255, 0.1);", "background: var(--glass-border);")
html = html.replace("color: white;", "color: var(--text-main);")
html = html.replace("color: white", "color: var(--text-main)")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
