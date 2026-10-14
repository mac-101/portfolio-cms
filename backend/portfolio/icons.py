import re

# Check the latest versions on npmjs.com (simple-icons, lucide-static) and update these.
SIMPLE_ICONS_VERSION = "15"
LUCIDE_VERSION = "0"

TECH_ICON_BASE = f"https://cdn.jsdelivr.net/npm/simple-icons@{SIMPLE_ICONS_VERSION}/icons/"
SERVICE_ICON_BASE = f"https://cdn.jsdelivr.net/npm/lucide-static@{LUCIDE_VERSION}/icons/"

TECH_ICONS = [
    ("python", "Python"), ("django", "Django"), ("flask", "Flask"), ("fastapi", "FastAPI"),
    ("javascript", "JavaScript"), ("typescript", "TypeScript"), ("react", "React"),
    ("nextdotjs", "Next.js"), ("vuedotjs", "Vue.js"), ("nodedotjs", "Node.js"),
    ("express", "Express"), ("html5", "HTML"), ("css3", "CSS"), ("tailwindcss", "Tailwind CSS"),
    ("bootstrap", "Bootstrap"), ("postgresql", "PostgreSQL"), ("mysql", "MySQL"),
    ("sqlite", "SQLite"), ("mongodb", "MongoDB"), ("redis", "Redis"), ("supabase", "Supabase"),
    ("firebase", "Firebase"), ("cloudinary", "Cloudinary"), ("git", "Git"), ("github", "GitHub"),
    ("docker", "Docker"), ("figma", "Figma"), ("wordpress", "WordPress"), ("vercel", "Vercel"),
    ("netlify", "Netlify"), ("render", "Render"), ("graphql", "GraphQL"), ("redux", "Redux"),
    ("vite", "Vite"), ("php", "PHP"), ("laravel", "Laravel"),
]

SERVICE_ICONS = [
    ("globe", "Websites"), ("monitor", "Web apps"), ("layout-dashboard", "Dashboards"),
    ("server", "Backend"), ("database", "Database"), ("code", "Development"),
    ("smartphone", "Mobile"), ("palette", "Design"), ("shopping-cart", "E-commerce"),
    ("shield-check", "Security"), ("lock", "Authentication"), ("cloud", "Hosting"),
    ("rocket", "Launch"), ("zap", "Performance"), ("wrench", "Maintenance"),
    ("layers", "Systems"), ("mail", "Email"),
]

TECH_ICON_KEYS = {key for key, _ in TECH_ICONS}

# Names people type that differ from the icon key
TECH_ALIASES = {
    "node.js": "nodedotjs", "node": "nodedotjs", "nodejs": "nodedotjs",
    "next.js": "nextdotjs", "next": "nextdotjs", "vue": "vuedotjs", "vue.js": "vuedotjs",
    "html": "html5", "css": "css3", "tailwind": "tailwindcss",
    "postgres": "postgresql", "drf": "django", "django rest framework": "django",
}


def guess_tech_icon(name):
    """Best-guess icon key for a technology name, or '' if there isn't one."""
    cleaned = name.strip().lower()
    if cleaned in TECH_ALIASES:
        return TECH_ALIASES[cleaned]
    key = re.sub(r"[^a-z0-9]", "", cleaned)
    return key if key in TECH_ICON_KEYS else ""