#!/usr/bin/env python3
"""
Enhance encyclopedia pages with detailed content and related terms.
Adds comprehensive information, related terms sections, and connections.
"""

import os
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Enhanced content database with detailed descriptions and related terms
ENHANCED_CONTENT = {
    "anatomical": {
        "fascia": {
            "detailed": """Fascia is a continuous web of connective tissue that surrounds and connects every structure in the body—muscles, bones, organs, nerves, and blood vessels. This three-dimensional matrix provides structural support, facilitates movement, and plays a crucial role in proprioception and force transmission.

In ELDOA practice, fascia is not merely passive wrapping but an active, responsive tissue that can be trained and optimized. The fascial system responds to mechanical loading through a process called mechanotransduction, where physical forces are converted into cellular responses. ELDOA specifically targets fascial chains—interconnected pathways that span multiple body segments—to create systematic decompression and improved tissue quality.

Research has shown that fascia contains numerous mechanoreceptors and free nerve endings, making it a significant contributor to our sense of body position and movement. When fascia becomes restricted or adhered, it can limit mobility, alter movement patterns, and contribute to pain. ELDOA addresses these restrictions through precise, sustained stretching that encourages fascial remodeling and hydration.""",
            "related": ["myofascial-chains", "connective-tissue", "tensegrity", "proprioception", "mechanotransduction"],
            "connections": ["superficial-back-line", "deep-front-line", "spiral-line", "fascial-tension", "tissue-hydration"]
        },
        "cervical-spine": {
            "detailed": """The cervical spine consists of seven vertebrae (C1-C7) that support the head and enable its remarkable range of motion. This region is unique in its anatomy, with C1 (atlas) and C2 (axis) designed specifically for rotation, while C3-C7 provide flexion, extension, and lateral bending capabilities.

Modern lifestyles have created unprecedented challenges for cervical health. The average human head weighs 10-12 pounds in neutral position, but forward head posture—common in our digital age—can increase effective weight to 40-60 pounds, placing enormous stress on cervical structures. ELDOA offers specific positions for each cervical segment to counteract these forces.

ELDOA cervical positions target not only the vertebral joints but also the intricate fascial networks surrounding the neck. These include connections to the shoulder girdle, thoracic inlet, and cranial base. Specific ELDOA exercises like C7-T1 decompression address the critical cervicothoracic junction, often a site of restriction and discomfort.""",
            "related": ["forward-head-posture", "cervicogenic-headache", "neck-pain", "text-neck", "whiplash"],
            "connections": ["c1-atlas", "c2-axis", "c7-t1-junction", "upper-crossed-syndrome", "thoracic-outlet-syndrome"]
        },
        "lumbar-spine": {
            "detailed": """The lumbar spine comprises five large vertebrae (L1-L5) that bear the majority of the body's weight and serve as the foundation for upright posture. This region experiences the highest compressive and shear forces during daily activities, making it particularly vulnerable to injury and degeneration.

Each lumbar segment has specific biomechanical characteristics: L1-L2 transitions from thoracic to lumbar curvature, L3 often serves as a transitional or neutral segment, L4-L5 experiences maximal shear stress, and L5-S1 bears the greatest compressive load while transitioning to the sacrum. ELDOA provides targeted decompression for each of these critical junctions.

The lumbar spine's relationship to the psoas muscle, quadratus lumborum, and multifidus creates complex force patterns that ELDOA specifically addresses. Lower back pain often originates from segmental dysfunction at specific levels rather than generalized "back problems." ELDOA's precision allows practitioners to target the exact segment requiring intervention, whether addressing disc issues, facet joint restrictions, or muscular imbalances.""",
            "related": ["lower-back-pain", "disc-herniation", "sciatica", "spinal-stenosis", "spondylolisthesis"],
            "connections": ["l4-l5-segment", "l5-s1-junction", "lumbosacral-angle", "psoas-muscle", "lumbar-lordosis"]
        }
    },
    "conditions": {
        "achilles-tendinopathy": {
            "detailed": """Achilles tendinopathy is a degenerative condition affecting the Achilles tendon, typically resulting from overuse, poor biomechanics, or inadequate recovery. Unlike acute tendinitis (inflammation), tendinopathy involves structural changes within the tendon tissue, including collagen disorganization and neovascularization.

ELDOA addresses Achilles tendinopathy through a whole-system approach, recognizing that distal symptoms often have proximal causes. The posterior fascial chain—connecting plantar fascia, Achilles tendon, calves, hamstrings, and lumbar spine—functions as an integrated unit. Restrictions or dysfunctions anywhere along this chain can create compensatory stress at the Achilles.

Specific ELDOA protocols for Achilles issues include L5-S1 decompression to address lumbosacral tension patterns, full posterior chain integration exercises, and targeted fascial work for the lower leg. This approach differs from conventional treatment by addressing root causes rather than solely treating local symptoms. The sustained holds in ELDOA positions encourage tendon remodeling and improved tissue quality through controlled mechanical loading.""",
            "related": ["posterior-chain", "plantar-fasciitis", "calf-strain", "overuse-injury", "tendon-healing"],
            "connections": ["l5-s1-decompression", "posterior-fascial-line", "eccentric-loading", "tissue-remodeling"]
        },
        "sciatica": {
            "detailed": """Sciatica refers to pain radiating along the sciatic nerve pathway, typically from the lower back through the buttock and down the leg. True sciatica involves nerve compression or irritation, most commonly from disc herniation, spinal stenosis, or piriformis syndrome.

ELDOA approaches sciatica by creating space at the specific spinal segment where nerve compression occurs. Most commonly, this involves L4-L5 or L5-S1 decompression exercises. Unlike passive treatments, ELDOA's active approach engages the neuromuscular system to create lasting changes in spinal positioning and intervertebral spacing.

The ELDOA protocol for sciatica includes: (1) identifying the specific level of compression through assessment, (2) daily practice of segment-specific ELDOA positions during acute phases, (3) integration of full posterior chain work to address fascial restrictions, and (4) gradual progression to maintenance protocols. Many practitioners report significant symptom reduction within 2-4 weeks of consistent practice, though individual responses vary based on severity and underlying pathology.""",
            "related": ["disc-herniation", "piriformis-syndrome", "spinal-stenosis", "radiculopathy", "nerve-compression"],
            "connections": ["l4-l5-decompression", "l5-s1-decompression", "posterior-chain", "neural-tension"]
        },
        "scoliosis": {
            "detailed": """Scoliosis is a three-dimensional spinal deformity involving lateral curvature (frontal plane), rotation (transverse plane), and altered sagittal curves. While structural scoliosis involves bony changes, functional scoliosis results from muscular imbalances, leg length discrepancies, or habitual postures.

ELDOA offers unique benefits for scoliosis management by addressing each spinal segment individually. Rather than treating the spine as a single unit, ELDOA positions can target specific levels within or adjacent to the curve, promoting better segmental mobility and potentially influencing curve progression. This is particularly valuable for functional curves and in managing symptoms associated with structural curves.

For scoliosis, ELDOA protocols typically include: (1) convex-side stretching to address shortened tissues, (2) segment-specific decompression at apical vertebrae, (3) integration of rotational control exercises, and (4) breathing work to address rib cage asymmetries. While ELDOA cannot "cure" structural scoliosis, it can improve function, reduce discomfort, and potentially slow progression, especially when started early.""",
            "related": ["spinal-curvature", "postural-asymmetry", "rib-cage-deformity", "structural-vs-functional"],
            "connections": ["thoracic-rotation", "cobb-angle", "convex-concave", "apical-vertebra", "compensatory-curves"]
        }
    },
    "concepts": {
        "decoaptation": {
            "detailed": """Decoaptation is the fundamental mechanism of ELDOA—the creation of space between joint surfaces, particularly between vertebral segments. The term comes from French osteopathic tradition and literally means "to separate or disjoin." This is the opposite of coaptation (compression or approximation of joint surfaces).

In ELDOA practice, decoaptation is achieved through precise body positioning combined with active muscular engagement. The practitioner creates longitudinal traction through the spine while maintaining specific rotations, lateral bends, and flexion/extension angles that target individual vertebral joints. This active, self-generated force distinguishes ELDOA from passive traction methods.

The benefits of decoaptation include: (1) increased intervertebral disc height and hydration, (2) reduced pressure on nerve roots, (3) improved facet joint mobility, (4) enhanced circulation to spinal tissues, (5) proprioceptive re-education, and (6) fascial release along spinal segments. Research suggests that even brief periods of decoaptation can produce measurable changes in disc height and spinal mechanics.""",
            "related": ["spinal-decompression", "joint-separation", "traction", "intervertebral-space"],
            "connections": ["active-vs-passive", "fascial-tension", "proprioception", "disc-hydration", "myofascial-stretching"]
        },
        "proprioception": {
            "detailed": """Proprioception is the body's ability to sense its position, movement, and spatial orientation without relying on vision. This "sixth sense" depends on mechanoreceptors in muscles, tendons, ligaments, fascia, and joint capsules that constantly feed information to the nervous system.

ELDOA uniquely enhances proprioception through sustained, precise positioning that requires intense neuromuscular control. Unlike passive stretching, ELDOA demands active awareness of every body segment, creating a powerful feedback loop between sensory input and motor control. This proprioceptive training has applications far beyond spinal health, improving balance, coordination, and movement quality.

The fascial system is particularly rich in proprioceptive receptors—containing more mechanoreceptors than muscles themselves. ELDOA's fascial focus thus becomes a form of sensory re-education, teaching the nervous system to better perceive and control spinal position. For athletes, this translates to improved performance; for older adults, better fall prevention; for everyone, enhanced body awareness and movement efficiency.""",
            "related": ["mechanoreceptors", "body-awareness", "kinesthesia", "balance", "sensory-feedback"],
            "connections": ["fascial-mechanoreceptors", "neuromuscular-control", "motor-learning", "spatial-awareness"]
        },
        "myofascial-chains": {
            "detailed": """Myofascial chains, also called anatomy trains or fascial lines, are continuous sequences of muscles and fascia that work together to transmit force and create movement patterns. These chains span multiple joints and body segments, functioning as integrated units rather than isolated muscles.

Thomas Myers identified major myofascial chains including the Superficial Back Line (plantar fascia to eyebrow line), Deep Front Line (inner arch to jaw), Spiral Line (wrapping the body diagonally), and others. ELDOA recognizes these connections and specifically targets them through full-chain integration exercises. For example, treating a foot problem might require addressing the entire posterior chain up through the lumbar spine.

Understanding myofascial chains revolutionizes how we approach pain and dysfunction. A restriction in one area creates compensatory patterns throughout the chain, often manifesting as symptoms far from the original problem. ELDOA's segmental specificity combined with chain awareness allows practitioners to address both local restrictions and global patterns, creating more comprehensive and lasting results.""",
            "related": ["anatomy-trains", "fascial-lines", "superficial-back-line", "deep-front-line", "spiral-line"],
            "connections": ["posterior-chain", "anterior-chain", "lateral-chain", "force-transmission", "compensatory-patterns"]
        }
    },
    "mechanisms": {
        "neuroplasticity": {
            "detailed": """Neuroplasticity is the nervous system's ability to reorganize itself by forming new neural connections throughout life. This capacity for change allows the brain and spinal cord to adapt to injury, learn new skills, and modify existing movement patterns—making it fundamental to ELDOA's therapeutic effects.

ELDOA induces neuroplastic changes through several mechanisms: (1) novel movement patterns that challenge existing motor programs, (2) proprioceptive feedback that refines body awareness, (3) sustained positions that allow nervous system adaptation, and (4) pain reduction that removes inhibitory signals. The precision required in ELDOA positions creates a rich learning environment for the nervous system.

Research in neuroplasticity shows that focused attention, repetition, and progressive challenge are key factors in creating lasting neural changes. ELDOA incorporates all three: practitioners must concentrate intensely on positioning (attention), practice regularly (repetition), and advance through increasingly complex variations (progressive challenge). This neuroplastic training extends beyond the time spent in ELDOA positions, influencing daily posture and movement patterns.""",
            "related": ["brain-plasticity", "motor-learning", "neural-adaptation", "habit-formation"],
            "connections": ["motor-cortex", "body-schema", "movement-patterns", "pain-neuroscience", "sensorimotor-integration"]
        },
        "mechanotransduction": {
            "detailed": """Mechanotransduction is the process by which cells convert mechanical stimuli into biochemical signals and cellular responses. In the context of ELDOA, this explains how physical forces applied to fascia, bones, and other tissues create changes at the cellular level.

When ELDOA creates tension in fascial tissue, specialized proteins called integrins sense this mechanical force and trigger intracellular signaling cascades. These signals can influence gene expression, protein synthesis, and tissue remodeling. For example, sustained stretching encourages fibroblasts to lay down new collagen in alignment with the direction of tension, improving tissue organization and strength.

This mechanism explains why ELDOA's sustained holds (typically 60 seconds) are more effective than brief stretching. It takes time for mechanotransduction to occur—mechanical forces must be maintained long enough to trigger cellular responses. The precision of ELDOA positioning ensures that these mechanical signals reach the intended tissues, maximizing therapeutic benefit while minimizing stress on surrounding structures.""",
            "related": ["cellular-response", "tissue-remodeling", "collagen-synthesis", "fibroblast-activity"],
            "connections": ["integrins", "extracellular-matrix", "gene-expression", "protein-synthesis", "tissue-adaptation"]
        }
    }
}

# Category-based related terms that apply broadly
CATEGORY_CONNECTIONS = {
    "spine": ["vertebrae", "spinal-column", "intervertebral-disc", "spinal-cord", "facet-joints"],
    "fascia": ["connective-tissue", "myofascial", "fascial-chains", "tensegrity", "extracellular-matrix"],
    "pain": ["chronic-pain", "acute-pain", "pain-science", "pain-management", "nociception"],
    "posture": ["alignment", "postural-patterns", "forward-head", "rounded-shoulders", "anterior-pelvic-tilt"],
    "movement": ["biomechanics", "kinesiology", "motor-control", "movement-patterns", "functional-movement"]
}

def generate_related_terms(title, category=None):
    """Generate contextually appropriate related terms based on title and category."""
    title_lower = title.lower()
    related = []

    # Spinal segments get related segments
    if any(seg in title_lower for seg in ['cervical', 'thoracic', 'lumbar', 'sacral', 'c1', 'c2', 'l1', 'l5', 't1']):
        related.extend(['spinal-decompression', 'vertebral-segment', 'intervertebral-disc', 'facet-joints'])

    # Conditions get related conditions and treatments
    if any(word in title_lower for word in ['pain', 'syndrome', 'injury', 'dysfunction', 'disorder', 'pathology']):
        related.extend(['eldoa-protocol', 'rehabilitation', 'pain-management', 'tissue-healing'])

    # Fascial terms get fascial connections
    if any(word in title_lower for word in ['fascia', 'myofascial', 'connective']):
        related.extend(['fascial-chains', 'tissue-hydration', 'myofascial-release', 'structural-integration'])

    # Biomechanical terms
    if any(word in title_lower for word in ['alignment', 'posture', 'biomech', 'kinetic']):
        related.extend(['postural-assessment', 'movement-analysis', 'functional-anatomy'])

    # Remove duplicates and return
    return list(set(related))[:6]

def generate_detailed_content(title, current_content):
    """Generate detailed content for encyclopedia entries."""
    title_lower = title.lower()

    # Check if we have pre-written content
    for category_dict in ENHANCED_CONTENT.values():
        for slug, data in category_dict.items():
            if slug in title_lower or title_lower.replace(' ', '-') == slug:
                return data.get('detailed', ''), data.get('related', []), data.get('connections', [])

    # Generate contextual content based on title
    detailed_content = generate_contextual_content(title, current_content)
    related = generate_related_terms(title)
    connections = generate_related_terms(title)

    return detailed_content, related, connections

def generate_contextual_content(title, current_content):
    """Generate contextual detailed content when no pre-written content exists."""
    title_lower = title.lower()

    # Spinal segment content
    if any(seg in title_lower for seg in ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7']):
        return f"""The {title} is a critical segment of the cervical spine, playing a vital role in head movement, stability, and neurological function. ELDOA provides specific positions targeting this segment to create decompression, improve mobility, and enhance proprioceptive awareness.

Cervical segments are particularly vulnerable to modern postural stresses, including prolonged sitting, computer work, and smartphone use. The {title} can develop restrictions that affect not only local function but also create compensatory patterns throughout the entire spine.

ELDOA exercises for {title} involve precise positioning that creates longitudinal traction while maintaining specific rotational and lateral components. Regular practice can help address common cervical issues including neck pain, headaches, limited range of motion, and nerve-related symptoms."""

    elif any(seg in title_lower for seg in ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12']):
        return f"""The {title} is part of the thoracic spine, which provides structural stability while allowing for rotation and respiratory function. ELDOA targets this segment to improve rib cage mechanics, enhance breathing capacity, and address mid-back restrictions.

Thoracic segments often develop stiffness due to prolonged sitting, poor posture, and reduced rotational movement in daily life. The {title} plays a specific role in the overall thoracic curve and its relationship to adjacent structures including ribs, shoulder girdle, and spinal cord.

ELDOA practice for {title} integrates breathing with precise positioning, creating decompression while optimizing rib mechanics. This can benefit conditions ranging from mid-back pain to respiratory limitations, and plays a crucial role in overall spinal health."""

    elif any(seg in title_lower for seg in ['l1', 'l2', 'l3', 'l4', 'l5']):
        return f"""The {title} is a key segment of the lumbar spine, bearing significant weight-bearing loads and playing a crucial role in trunk stability and movement. ELDOA provides targeted decompression for this segment, addressing the unique biomechanical demands placed on the lower back.

Lumbar segments experience high compressive and shear forces during daily activities. The {title} has specific biomechanical characteristics that make it particularly susceptible to certain types of dysfunction. Common issues include disc degeneration, facet joint restrictions, and muscular imbalances.

ELDOA positions for {title} create space at the intervertebral joint while engaging the deep stabilizing muscles. This active approach promotes disc health, reduces nerve compression, and enhances segmental proprioception. Regular practice can address lower back pain, improve flexibility, and prevent degenerative changes."""

    # Fascial/anatomical terms
    elif 'fascia' in title_lower or 'myofascial' in title_lower:
        return f"""{title} refers to an important aspect of the fascial system, the continuous web of connective tissue that surrounds and connects all structures in the body. Understanding {title.lower()} is essential for appreciating how ELDOA creates systemic changes through targeted interventions.

The fascial system functions as an integrated network, transmitting forces and coordinating movement across multiple body segments. {title} represents a specific component or concept within this larger system, with particular relevance to ELDOA practice and myofascial health.

ELDOA addresses {title.lower()} through sustained, precise positioning that creates controlled tension in fascial tissues. This mechanical loading stimulates cellular responses including tissue remodeling, improved hydration, and enhanced proprioception. The result is improved tissue quality and function."""

    # Pain/condition terms
    elif any(word in title_lower for word in ['pain', 'syndrome', 'pathology', 'disorder', 'dysfunction']):
        return f"""{title} is a condition that can significantly impact quality of life and functional capacity. ELDOA offers a unique approach to addressing {title.lower()} through targeted spinal decompression and fascial work that addresses root causes rather than merely treating symptoms.

The ELDOA perspective on {title.lower()} recognizes that local symptoms often have distant causes. Restrictions or dysfunctions elsewhere in the body can create compensatory patterns that manifest as {title.lower()}. A comprehensive approach examines the entire kinetic chain and fascial system.

Treatment protocols for {title.lower()} typically include specific ELDOA positions targeting the relevant spinal segments, integration of related myofascial chains, and progressive loading to encourage tissue adaptation. Many practitioners report significant improvements with consistent practice, though individual responses vary based on underlying pathology and contributing factors."""

    # Movement/exercise terms
    elif any(word in title_lower for word in ['exercise', 'movement', 'position', 'technique']):
        return f"""{title} represents an important component of ELDOA practice or related movement systems. Understanding {title.lower()} helps practitioners develop more effective exercise protocols and achieve better therapeutic outcomes.

The principles underlying {title.lower()} align with ELDOA's emphasis on precision, active engagement, and neuromuscular control. Whether used as part of ELDOA protocols or integrated from complementary approaches, {title.lower()} contributes to improved movement quality and functional capacity.

Practitioners should approach {title.lower()} with attention to detail, proper progression, and individual adaptation. Like all ELDOA-related work, the quality of execution matters more than quantity, and consistent practice produces better results than sporadic intensive efforts."""

    # Default conceptual content
    else:
        return f"""{title} is an important concept within the ELDOA system and broader understanding of human movement, posture, and therapeutic exercise. This term relates to fundamental principles that guide effective practice and optimal outcomes.

Understanding {title.lower()} provides practitioners with deeper insight into how ELDOA creates change at multiple levels—from cellular tissue responses to whole-body movement patterns. This knowledge informs both practice and teaching, enabling more sophisticated application of ELDOA principles.

The relationship between {title.lower()} and ELDOA practice demonstrates the method's integration of multiple scientific disciplines including anatomy, biomechanics, neuroscience, and physiology. This interdisciplinary foundation gives ELDOA its unique effectiveness and broad applicability across different populations and conditions."""

def enhance_html_content(html_path):
    """Enhance a single HTML file with detailed content and related terms."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Get the title
        title_elem = soup.find('h1', class_='entry-title')
        if not title_elem:
            print(f"Warning: No title found in {html_path}")
            return False

        title = title_elem.get_text()

        # Get current content
        content_div = soup.find('div', class_='entry-content')
        if not content_div:
            print(f"Warning: No content div found in {html_path}")
            return False

        current_paragraphs = content_div.find_all('p')
        current_text = ' '.join([p.get_text() for p in current_paragraphs])

        # Generate enhanced content
        detailed_content, related_terms, connections = generate_detailed_content(title, current_text)

        # Clear existing content
        content_div.clear()

        # Add overview section (keep original simple description)
        overview = soup.new_tag('div', **{'class': 'content-section'})
        overview_h2 = soup.new_tag('h2')
        overview_h2.string = 'Overview'
        overview.append(overview_h2)

        for paragraph in current_paragraphs:
            overview.append(paragraph)

        content_div.append(overview)

        # Add detailed description section
        if detailed_content:
            detailed_section = soup.new_tag('div', **{'class': 'content-section'})
            detailed_h2 = soup.new_tag('h2')
            detailed_h2.string = 'Detailed Description'
            detailed_section.append(detailed_h2)

            # Split into paragraphs
            paragraphs = detailed_content.strip().split('\n\n')
            for para_text in paragraphs:
                if para_text.strip():
                    para = soup.new_tag('p')
                    para.string = para_text.strip()
                    detailed_section.append(para)

            content_div.append(detailed_section)

        # Add related terms section
        if related_terms:
            related_section = soup.new_tag('div', **{'class': 'content-section related-terms'})
            related_h2 = soup.new_tag('h2')
            related_h2.string = 'Related Terms'
            related_section.append(related_h2)

            related_ul = soup.new_tag('ul', **{'class': 'related-list'})
            for term in related_terms[:8]:  # Limit to 8 terms
                li = soup.new_tag('li')
                a = soup.new_tag('a', href=f'/encyclopedia/{term}.html')
                # Convert slug to title
                term_title = term.replace('-', ' ').title()
                a.string = term_title
                li.append(a)
                related_ul.append(li)

            related_section.append(related_ul)
            content_div.append(related_section)

        # Add connections section
        if connections:
            connections_section = soup.new_tag('div', **{'class': 'content-section connections'})
            connections_h2 = soup.new_tag('h2')
            connections_h2.string = 'Key Connections'
            connections_section.append(connections_h2)

            connections_ul = soup.new_tag('ul', **{'class': 'connections-list'})
            for conn in connections[:6]:  # Limit to 6 connections
                li = soup.new_tag('li')
                a = soup.new_tag('a', href=f'/encyclopedia/{conn}.html')
                # Convert slug to title
                conn_title = conn.replace('-', ' ').title()
                a.string = conn_title
                li.append(a)
                connections_ul.append(li)

            connections_section.append(connections_ul)
            content_div.append(connections_section)

        # Add enhanced CSS for new sections
        style_tag = soup.find('style')
        if style_tag:
            additional_css = """

        .content-section {
            margin-bottom: 2.5rem;
        }

        .content-section h2 {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #2f2fe6;
        }

        .related-terms, .connections {
            background-color: #f9fafb;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 2rem;
        }

        .related-list, .connections-list {
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 0.75rem;
            margin-top: 1rem;
        }

        .related-list li, .connections-list li {
            margin: 0;
        }

        .related-list a, .connections-list a {
            color: #2f2fe6;
            text-decoration: none;
            font-weight: 500;
            display: block;
            padding: 0.5rem;
            background-color: white;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .related-list a:hover, .connections-list a:hover {
            background-color: #2f2fe6;
            color: white;
            transform: translateX(4px);
        }

        @media (max-width: 768px) {
            .related-list, .connections-list {
                grid-template-columns: 1fr;
            }
        }
"""
            style_tag.string += additional_css

        # Write enhanced content back to file
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        return True

    except Exception as e:
        print(f"Error enhancing {html_path}: {e}")
        return False

def main():
    """Main function to enhance all encyclopedia pages."""
    encyclopedia_dir = Path('/home/user/eldoaai/public/encyclopedia')

    if not encyclopedia_dir.exists():
        print(f"Error: Encyclopedia directory not found at {encyclopedia_dir}")
        return

    # Get all HTML files
    html_files = sorted(encyclopedia_dir.glob('*.html'))

    print(f"Found {len(html_files)} encyclopedia pages to enhance")
    print("Starting enhancement process...\n")

    success_count = 0
    error_count = 0

    for i, html_file in enumerate(html_files, 1):
        if html_file.name == 'index.html':
            continue

        print(f"[{i}/{len(html_files)}] Enhancing {html_file.name}...")

        if enhance_html_content(html_file):
            success_count += 1
        else:
            error_count += 1

        # Progress update every 50 files
        if i % 50 == 0:
            print(f"\nProgress: {i}/{len(html_files)} files processed")
            print(f"Success: {success_count}, Errors: {error_count}\n")

    print(f"\n{'='*60}")
    print(f"Enhancement complete!")
    print(f"Total files processed: {len(html_files)}")
    print(f"Successfully enhanced: {success_count}")
    print(f"Errors: {error_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
