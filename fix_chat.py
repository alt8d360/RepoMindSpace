import os
import re

html_dir = r"c:\RepoMindSpace\RepoMindSpace\pages"

for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        path = os.path.join(html_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        
        # Backgrounds
        html = html.replace("rgba(30, 27, 46, 0.6)", "var(--glass-bg)")
        html = html.replace("rgba(30, 27, 46, 0.8)", "var(--glass-hover-bg)")
        html = html.replace("rgba(0, 0, 0, 0.2)", "var(--bg-dark)")
        html = html.replace("rgba(0, 0, 0, 0.3)", "var(--bg-card)")
        html = html.replace("rgba(30, 41, 59, 0.6)", "var(--glass-bg)")
        
        # Borders and alphas
        html = html.replace("rgba(255, 255, 255, 0.08)", "var(--alpha-10)")
        html = html.replace("rgba(255, 255, 255, 0.05)", "var(--alpha-5)")
        html = html.replace("rgba(255, 255, 255, 0.1)", "var(--alpha-10)")
        html = html.replace("rgba(255, 255, 255, 0.2)", "var(--alpha-20)")
        html = html.replace("rgba(255, 255, 255, 0.3)", "var(--alpha-30)")
        
        # Texts
        html = re.sub(r"color:\s*white\s*;", "color: var(--text-main);", html)
        html = re.sub(r"color:\s*#e2e8f0\s*;", "color: var(--text-muted);", html)
        html = re.sub(r"color:\s*#cbd5e1\s*;", "color: var(--text-muted);", html)
        
        # Fix primary buttons where text was incorrectly changed to text-main
        html = html.replace("color: var(--text-main);\n  background: linear-gradient", "color: white;\n  background: linear-gradient")
        html = html.replace("color: var(--text-main);\n            border-bottom-right-radius", "color: white;\n            border-bottom-right-radius")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

print("Fixed HTML pages.")
