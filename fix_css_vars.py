import re

css_path = r"c:\RepoMindSpace\RepoMindSpace\css\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Make sure we have the variables defined in :root
root_vars = """
  --alpha-5: rgba(255, 255, 255, 0.05);
  --alpha-10: rgba(255, 255, 255, 0.1);
  --alpha-20: rgba(255, 255, 255, 0.2);
  --alpha-30: rgba(255, 255, 255, 0.3);
"""

light_vars = """
  --alpha-5: rgba(0, 0, 0, 0.05);
  --alpha-10: rgba(0, 0, 0, 0.1);
  --alpha-20: rgba(0, 0, 0, 0.2);
  --alpha-30: rgba(0, 0, 0, 0.3);
"""

if "--alpha-5:" not in css:
    css = css.replace("--glass-hover-bg: rgba(30, 27, 46, 0.8);", "--glass-hover-bg: rgba(30, 27, 46, 0.8);" + root_vars)
    css = css.replace("--glass-hover-bg: rgba(255, 255, 255, 0.9);", "--glass-hover-bg: rgba(255, 255, 255, 0.9);" + light_vars)

# Replace all occurrences
css = css.replace("rgba(255, 255, 255, 0.02)", "var(--alpha-5)")
css = css.replace("rgba(255, 255, 255, 0.03)", "var(--alpha-5)")
css = css.replace("rgba(255, 255, 255, 0.05)", "var(--alpha-5)")
css = css.replace("rgba(255, 255, 255, 0.08)", "var(--alpha-10)")
css = css.replace("rgba(255, 255, 255, 0.1)", "var(--alpha-10)")
css = css.replace("rgba(255, 255, 255, 0.2)", "var(--alpha-20)")
css = css.replace("rgba(255, 255, 255, 0.3)", "var(--alpha-30)")

# Fix all color: white; outside of primary buttons
# Instead of replacing all color: white, let's target specific known ones that should be text-main
css = re.sub(r"color:\s*white\s*;", "color: var(--text-main);", css)
css = re.sub(r"color:\s*#fff\s*;", "color: var(--text-main);", css)

# Make sure primary buttons text stays white
css = css.replace("color: var(--text-main);\n  background: linear-gradient", "color: white;\n  background: linear-gradient")
css = css.replace("color: var(--text-main);\n  background-color: var(--primary-color)", "color: white;\n  background-color: var(--primary-color)")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

# Also fix HTML inline styles
html_dir = r"c:\RepoMindSpace\RepoMindSpace\pages"
import os
for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        path = os.path.join(html_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        
        html = html.replace("rgba(255, 255, 255, 0.05)", "var(--alpha-5)")
        html = html.replace("rgba(255, 255, 255, 0.1)", "var(--alpha-10)")
        html = html.replace("rgba(255, 255, 255, 0.2)", "var(--alpha-20)")
        html = html.replace("rgba(255, 255, 255, 0.3)", "var(--alpha-30)")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
