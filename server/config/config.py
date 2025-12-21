import os
from dotenv import load_dotenv

load_dotenv()

YT_KEY = os.getenv("YT_KEY")
YT_BASE_URL = "https://www.googleapis.com/youtube/v3/search"

CONTEXT = {
    "endorse": {
        "philosophy",
        "formal logic",
        "philosophy of mind",
        "epistemology",
        "critical rationalism",
        "computation",
        "turing machine",
        "automata theory",
        "complex systems",
        "reinforcement learning",
        "probabilistic reasoning",
        "anomaly detection",
        "systems design",
        "romanticism (late)",
        "proto-romanticism",
        "anti-enlightenment thought",
        "negative capability",
        "the sublime",
        "visionary mysticism (non-theological)",
        "william blake",
        "sketching as thinking",
        "line over color",
        "gesture drawing",
        "impressionism (structural, not decorative)",
        "unfinished form",
        "drafts and marginalia",
        "western classical music",
        "counterpoint",
        "fugue",
        "late beethoven",
        "bach (structural reading)",
        "tchaikovsky",
        "theme and variation",
        "classic literature",
        "modernist fragmentation",
        "symbolism (austere)",
        "myth as cognitive scaffold",
        "essay as inquiry",
        "aphoristic prose",
        "first principles",
        "model-based thinking",
        "precision over eloquence",
        "minimalism",
    },
    "reject": {
        "tutorial",
        "hand-holding",
        "survey courses",
        "buzzwords",
        "cargo-cult ai",
        "overengineering",
        "romantic nostalgia",
        "aestheticized vagueness",
        "poetic obscurity",
        "motivational fluff",
        "linkedin prose",
    },
}

CONTEXT_ENDORSE_KEY = "endorse"
CONTEXT_REJECT_KEY = "reject"
