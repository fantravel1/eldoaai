#!/usr/bin/env python3
"""
Script to fix broken links in newly created encyclopedia pages by
replacing them with links to existing pages.
"""

import re
from pathlib import Path

ENCYCLOPEDIA_DIR = Path("/home/user/eldoaai/encyclopedia")

# Get all existing encyclopedia files
existing_files = {f.stem for f in ENCYCLOPEDIA_DIR.glob('*.html')}

# Map of broken links to replacement links (existing pages)
REPLACEMENTS = {
    # Anatomy replacements
    "atlanto-occipital": "c1-atlas",
    "atlanto-axial": "c2-axis",
    "suboccipital-muscles": "neck-pain",
    "cranial-base": "c1-atlas",
    "skull-base": "c1-atlas",
    "dens": "c2-axis",
    "first-rib": "thoracic-spine",
    "brachial-plexus": "cervical-spine",
    "cervical-rotation": "thoracic-rotation",
    "neck-mobility": "cervical-spine",
    "gluteals": "posterior-chain",
    "hip-flexor": "psoas-muscle",
    "hip-extension": "hip-decoaptation",
    "hip-mechanics": "hip-decoaptation",
    "ankle-function": "plantar-fasciitis",
    "pelvic-mechanics": "sacrum",
    "transition-zone": "c7-t1-junction",
    "annulus-fibrosus": "disc-herniation",
    "nucleus-pulposus": "disc-herniation",
    "calf-muscles": "calf-strain",
    "foot-pain": "plantar-fasciitis",
    "joint-capsule": "facet-joints",
    "gastrocnemius": "calf-strain",
    "soleus": "calf-strain",
    "hamstrings": "hamstring-flexibility",
    "obliques": "core-stability",
    "it-band": "fascial-chains",

    # Tissue/cellular replacements
    "fibroblasts": "connective-tissue",
    "extracellular-matrix": "connective-tissue",
    "tissue-capacity": "tissue-healing",
    "tissue-tension": "fascial-tension",
    "cellular-response": "mechanotransduction",
    "tissue-continuity": "fascial-chains",

    # Function/control replacements
    "postural-control": "posture",
    "motor-unit": "neuromuscular-control",
    "cerebellum": "coordination",
    "central-nervous-system": "neuroplasticity",
    "receptor-types": "fascial-mechanoreceptors",
    "motor-control": "neuromuscular-control",
    "muscle-activation": "neuromuscular-control",
    "muscle-function": "neuromuscular-control",
    "skill-development": "skill-acquisition",

    # Treatment/clinical replacements
    "fascial-restrictions": "myofascial-release",
    "soft-tissue-work": "myofascial-release",
    "pain-relief": "pain-management",
    "self-treatment": "rehabilitation",
    "patient-empowerment": "rehabilitation",
    "treatment-planning": "movement-assessment",
    "central-sensitization": "chronic-pain",
    "threat-perception": "pain-neuroscience",

    # Spinal/mechanical replacements
    "spinal-extension": "spinal-mechanics",
    "spinal-degeneration": "spinal-stenosis",
    "segmental-mobility": "vertebral-segment",
    "lumbosacral-mechanics": "l5-s1-junction",
    "load-distribution": "spinal-mechanics",
    "spinal-instability": "spondylolisthesis",
    "segmental-stability": "core-stability",
    "force-transmission": "tensegrity",

    # Strength/training
    "strength-training": "eccentric-loading",
    "training-load": "progressive-loading",

    # Other
    "back-muscles": "erector-spinae",
    "respiratory-function": "diaphragm",
    "joint-nutrition": "joint-separation",
    "cartilage-health": "facet-joints",
    "training-principles": "practice-principles",
    "feedback-mechanisms": "proprioception",
    "deliberate-practice": "practice-principles",
    "daily-practice": "practice-principles",
    "trunk-stability": "core-stability",
    "latissimus-dorsi": "posterior-chain",
    "gluteus-maximus": "posterior-chain",
    "transversus-abdominis": "core-stability",
    "pain-avoidance": "compensatory-patterns",
    "muscle-imbalance": "compensatory-patterns",
    "self-correction": "body-awareness",
    "behavior-change": "habit-formation",
    "cortical-representation": "motor-cortex",
    "voluntary-movement": "motor-cortex",
    "postural-habits": "posture",
    "disc-health": "disc-hydration",
    "disc-loading": "spinal-mechanics",
    "end-vertebra": "cobb-angle",
    "balanced-treatment": "structural-vs-functional",
    "spinal-base": "sacrum",
    "disc-nutrition": "disc-hydration",
    "osmotic-pressure": "disc-hydration",
    "sensory-integration": "proprioception",
    "spatial-awareness": "kinesthesia",
    "mindfulness": "body-awareness",
    "chest-wall": "thoracic-spine",
    "balance": "coordination",
    "postural-assessment": "movement-assessment",
    "radiographic-assessment": "cobb-angle",
    "manual-therapy": "myofascial-release",
    "tendinopathy": "achilles-tendinopathy",
    "muscle-strain": "calf-strain",
    "repetitive-strain": "overuse-injury",
    "joint-mobility": "joint-separation",
    "postural-awareness": "body-awareness",
    "disc-height": "intervertebral-space",
    "spinal-mobility": "spinal-mechanics",
    "trunk-rotation": "thoracic-rotation",
    "pelvis": "sacrum",
    "referred-pain": "sciatica",
    "plantar-fascia": "plantar-fasciitis",
    "pelvic-tilt": "lumbosacral-angle",
    "postural-balance": "posture",
    "movement-control": "neuromuscular-control",
}

def fix_links_in_file(filepath):
    """Fix broken links in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Find all encyclopedia links
    pattern = r'<a href="/encyclopedia/([^"]+)\.html">([^<]+)</a>'

    def replace_link(match):
        slug = match.group(1)
        title = match.group(2)

        if slug not in existing_files:
            # Try to find a replacement
            if slug in REPLACEMENTS:
                new_slug = REPLACEMENTS[slug]
                if new_slug in existing_files:
                    # Generate proper title from slug
                    new_title = new_slug.replace('-', ' ').title()
                    return f'<a href="/encyclopedia/{new_slug}.html">{new_title}</a>'
            # If no replacement found, keep original (will be a broken link)
            return match.group(0)
        return match.group(0)

    content = re.sub(pattern, replace_link, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    fixed_count = 0
    for filepath in ENCYCLOPEDIA_DIR.glob('*.html'):
        if fix_links_in_file(filepath):
            print(f"Fixed links in: {filepath.name}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} files")


if __name__ == "__main__":
    main()
