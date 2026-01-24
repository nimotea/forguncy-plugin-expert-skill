from pathlib import Path
from typing import Optional

# Base directory for the skill
# Assuming the skill directory is sibling to this mcp directory
BASE_DIR = Path(__file__).parent.parent / "forguncy-plugin-master-skill"

# Subdirectories according to current project structure
DOCS_DIR = BASE_DIR / "references"
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
ICONS_DIR = BASE_DIR / "assets" / "icons"
SKILL_FILE = BASE_DIR / "SKILL.md"
SCRIPTS_DIR = BASE_DIR / "scripts"

def ensure_base_dir():
    if not BASE_DIR.exists():
        raise FileNotFoundError(f"Base directory not found at {BASE_DIR}")
    if not DOCS_DIR.exists():
        raise FileNotFoundError(f"Docs directory not found at {DOCS_DIR}")
    if not TEMPLATES_DIR.exists():
        raise FileNotFoundError(f"Templates directory not found at {TEMPLATES_DIR}")

def find_plugin_project(cwd: Path) -> Optional[Path]:
    """Finds the nearest Forguncy plugin project directory (containing .csproj)."""
    curr = cwd
    while curr != curr.parent:
        csprojs = list(curr.glob("*.csproj"))
        if csprojs:
            return curr
        curr = curr.parent
    return None
