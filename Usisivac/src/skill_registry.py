import os
import yaml
import re

class SkillRegistry:
    """Discovers and parses metadata for available agent skills."""
    
    def __init__(self, skills_path: str = "memory/skills"):
        self.skills_path = skills_path
        self.skills = {}

    def refresh(self):
        """Scans the skills directory for SKILL.md files and standalone .md skills."""
        if not os.path.exists(self.skills_path):
            return {}

        self.skills = {}
        # 1. Look for SKILL.md in subdirectories
        for root, dirs, files in os.walk(self.skills_path):
            if "SKILL.md" in files:
                skill_path = os.path.join(root, "SKILL.md")
                metadata = self._parse_skill(skill_path)
                if metadata:
                    name = metadata.get('name', os.path.basename(root))
                    self.skills[name] = metadata
        
        # 2. Look for standalone .md files in the skills directory
        for f in os.listdir(self.skills_path):
            if f.endswith(".md") and f != "SKILL.md":
                skill_path = os.path.join(self.skills_path, f)
                if os.path.isfile(skill_path):
                    metadata = self._parse_skill(skill_path)
                    if metadata:
                        name = metadata.get('name', f.replace(".md", ""))
                        self.skills[name] = metadata
        return self.skills

    def _parse_skill(self, file_path: str):
        """Extracts YAML frontmatter from a markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Match YAML frontmatter between --- and ---
            match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if match:
                data = yaml.safe_load(match.group(1))
                data['abs_path'] = os.path.abspath(file_path)
                data['dir_path'] = os.path.dirname(os.path.abspath(file_path))
                return data
        except Exception as e:
            print(f"⚠️ Error parsing skill {file_path}: {e}")
        return None

    def get_skill_menu(self):
        """Returns a concise description of all skills for LLM context."""
        menu = []
        for name, meta in self.skills.items():
            desc = meta.get('description', 'No description available.')
            menu.append(f"- **{name}**: {desc}")
        return "\n".join(menu)

if __name__ == "__main__":
    # Test execution
    registry = SkillRegistry()
    skills = registry.refresh()
    print(f"✅ Found {len(skills)} skills.")
    print(registry.get_skill_menu())
