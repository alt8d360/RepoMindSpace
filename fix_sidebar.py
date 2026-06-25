import os
import re

PAGES_DIR = r"c:\RepoMindSpace\RepoMindSpace\pages"

def fix_pages():
    for filename in os.listdir(PAGES_DIR):
        if not filename.endswith(".html"):
            continue
            
        filepath = os.path.join(PAGES_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Add theme.js if missing
        if "theme.js" not in content and "login.html" not in filename and "register.html" not in filename:
            content = content.replace("</head>", "    <script src=\"../js/theme.js\"></script>\n</head>")

        # 2. Replace User Profile Area
        # Find everything from <!-- User Profile Area (Unified) --> up to the next </aside>
        pattern = r"<!-- User Profile Area \(Unified\) -->.*?</div>\s*</aside>"
        
        replacement = """<!-- User Profile Area (Unified) -->
            <div style="margin-top: auto; padding-top: 1.5rem; border-top: 1px solid var(--glass-border); display: flex; flex-direction: column; gap: 1rem;">
                <a href="profile.html" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none; color: var(--text-main);">
                    <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #a855f7); display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 0.9rem;">JD</div>
                    <div style="font-size: 0.95rem; font-weight: 500;">User Profile</div>
                </a>
                
                <!-- Theme Switcher Pop-out -->
                <div class="theme-switcher-container" style="background: var(--bg-dark); border: 1px solid var(--glass-border); border-radius: 8px; padding: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.8rem; color: var(--text-muted); padding-left: 0.25rem;">Theme</span>
                    <div style="display: flex; gap: 0.25rem;">
                        <button onclick="setThemeMode('system')" title="System Theme" class="theme-btn" data-theme-btn="system" style="background: transparent; border: none; color: var(--text-muted); cursor: pointer; padding: 6px; border-radius: 6px;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg></button>
                        <button onclick="setThemeMode('light')" title="Light Theme" class="theme-btn" data-theme-btn="light" style="background: transparent; border: none; color: var(--text-muted); cursor: pointer; padding: 6px; border-radius: 6px;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg></button>
                        <button onclick="setThemeMode('dark')" title="Dark Theme" class="theme-btn" data-theme-btn="dark" style="background: transparent; border: none; color: var(--text-muted); cursor: pointer; padding: 6px; border-radius: 6px;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg></button>
                    </div>
                </div>

                <a href="#" class="sidebar-link" id="logoutBtn" style="color: #ef4444; margin-top: 0.5rem; padding: 0.5rem 0.75rem;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 1rem; height: 1rem; margin-right: 0.5rem;"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
                    Logout
                </a>
            </div>
        </aside>"""
        
        # Some files might not have </aside> in the same match block if formatted differently, so use a safer replacement
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

fix_pages()
