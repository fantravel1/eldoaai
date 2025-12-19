#!/usr/bin/env python3
"""
Script to create missing encyclopedia pages.
"""

import os
from pathlib import Path

ENCYCLOPEDIA_DIR = Path("/home/user/eldoaai/encyclopedia")

# Define content for each missing page
MISSING_PAGES = {
    "tissue-healing": {
        "title": "Tissue Healing",
        "simple_desc": "How your body repairs itself after injury, like when a cut slowly closes up and gets better.",
        "detailed_desc": """<p>Tissue healing is the complex biological process by which the body repairs damaged structures, including muscles, tendons, ligaments, and fascia. This process occurs in overlapping phases: inflammation, proliferation, and remodeling, each with specific cellular and molecular events.</p>
<p>ELDOA supports tissue healing by creating optimal mechanical conditions for repair. The controlled loading and decompression techniques stimulate mechanotransduction—the process by which cells convert mechanical signals into biological responses. This promotes collagen synthesis, tissue remodeling, and improved alignment of healing fibers.</p>
<p>Understanding tissue healing timelines is essential for appropriate ELDOA prescription. Early-stage healing requires gentler approaches, while later stages benefit from progressive loading to optimize tissue strength and function. The fascial system plays a crucial role in healing, as it provides the structural framework within which repair occurs.</p>""",
        "benefits": ["Optimizes healing environment", "Promotes proper tissue alignment", "Reduces scar tissue formation", "Improves blood flow to injured areas", "Supports collagen synthesis", "Enhances functional recovery"],
        "applications": ["Post-injury rehabilitation", "Surgical recovery", "Chronic condition management", "Tissue remodeling", "Pain reduction during healing", "Return to activity planning"],
        "related_terms": [("injury-prevention", "Injury Prevention"), ("rehabilitation", "Rehabilitation"), ("connective-tissue", "Connective Tissue"), ("chronic-pain", "Chronic Pain")],
        "connections": [("fascial-system", "Fascial System"), ("inflammation", "Inflammation"), ("collagen", "Collagen"), ("recovery", "Recovery")]
    },
    "functional-anatomy": {
        "title": "Functional Anatomy",
        "simple_desc": "Understanding how all your body parts work together when you move, not just what they look like.",
        "detailed_desc": """<p>Functional anatomy examines the body's structures in terms of their movement capabilities and interdependencies rather than as isolated components. This approach recognizes that muscles, fascia, joints, and neural systems work as integrated units to produce coordinated movement.</p>
<p>In ELDOA practice, functional anatomy provides the foundation for understanding why specific positions create targeted effects. Each ELDOA position is designed based on functional anatomical principles—considering fascial connections, joint mechanics, and neural pathways to achieve precise decompression and tissue optimization.</p>
<p>Dr. Guy Voyer's approach emphasizes the importance of understanding functional chains—how movement at one segment affects the entire kinetic system. This knowledge allows practitioners to address root causes rather than just symptoms, creating lasting improvements in movement quality and pain reduction.</p>""",
        "benefits": ["Deeper understanding of movement", "Better exercise prescription", "Improved treatment targeting", "Recognition of compensation patterns", "Enhanced postural assessment", "Holistic body understanding"],
        "applications": ["Movement assessment", "Exercise design", "Postural correction", "Injury analysis", "Performance optimization", "Rehabilitation planning"],
        "related_terms": [("biomechanics", "Biomechanics"), ("kinetic-chain", "Kinetic Chain"), ("posture", "Posture"), ("alignment", "Alignment")],
        "connections": [("fascial-system", "Fascial System"), ("spinal-mechanics", "Spinal Mechanics"), ("joint-mobility", "Joint Mobility"), ("movement-assessment", "Movement Assessment")]
    },
    "facet-joints": {
        "title": "Facet Joints",
        "simple_desc": "Small joints on the back of your spine that help your back bend and twist safely.",
        "detailed_desc": """<p>Facet joints, also known as zygapophyseal joints, are paired synovial joints located at the posterior aspect of the spine. These joints guide and limit spinal motion while bearing a portion of axial load, particularly during extension and rotation movements.</p>
<p>ELDOA specifically addresses facet joint health through precise positioning that creates space within and around these structures. When facet joints become compressed or irritated—common in conditions like facet syndrome or spinal degeneration—they can cause localized pain and referred symptoms.</p>
<p>The orientation of facet joints varies by spinal region: cervical facets allow more rotation, thoracic facets permit rotation with limited flexion/extension, and lumbar facets primarily allow flexion/extension. Understanding these regional differences is essential for appropriate ELDOA selection and positioning.</p>""",
        "benefits": ["Reduces facet joint compression", "Improves joint nutrition", "Decreases local inflammation", "Enhances spinal mobility", "Relieves referred pain", "Supports joint health"],
        "applications": ["Facet syndrome treatment", "Spinal degeneration management", "Back pain relief", "Movement restoration", "Preventive care", "Post-surgical rehabilitation"],
        "related_terms": [("zygapophyseal-joints", "Zygapophyseal Joints"), ("spinal-segments", "Spinal Segments"), ("thoracic-spine", "Thoracic Spine"), ("lumbar-spine", "Lumbar Spine")],
        "connections": [("spinal-decompression", "Spinal Decompression"), ("joint-capsule", "Joint Capsule"), ("spinal-extension", "Spinal Extension"), ("nerve-root", "Nerve Root")]
    },
    "vertebral-segment": {
        "title": "Vertebral Segment",
        "simple_desc": "One building block of your spine, including the bone and the soft cushion between it and the next bone.",
        "detailed_desc": """<p>A vertebral segment, or motion segment, consists of two adjacent vertebrae, the intervertebral disc between them, the facet joints, ligaments, and associated neural structures. This functional unit is the basis for understanding spinal mechanics and the target of ELDOA interventions.</p>
<p>Each vertebral segment has specific characteristics based on its location in the spine. Cervical segments are designed for mobility, thoracic segments for stability and rib articulation, and lumbar segments for load-bearing. ELDOA positions are precisely designed to target individual segments, creating space and improving function at specific levels.</p>
<p>Segmental dysfunction—when a motion segment doesn't move or function properly—can result from injury, degeneration, or chronic postural stress. ELDOA addresses these dysfunctions by creating targeted decompression, improving disc hydration, and normalizing segmental mechanics.</p>""",
        "benefits": ["Targeted spinal treatment", "Improved segmental mobility", "Enhanced disc health", "Better load distribution", "Reduced nerve compression", "Optimized spinal function"],
        "applications": ["Specific level treatment", "Disc pathology management", "Segmental mobility restoration", "Spinal health maintenance", "Degeneration management", "Performance optimization"],
        "related_terms": [("intervertebral-disc", "Intervertebral Disc"), ("spinal-segments", "Spinal Segments"), ("l4-l5-segment", "L4 L5 Segment"), ("l5-s1-junction", "L5 S1 Junction")],
        "connections": [("facet-joints", "Facet Joints"), ("disc-hydration", "Disc Hydration"), ("spinal-decompression", "Spinal Decompression"), ("neural-foramen", "Neural Foramen")]
    },
    "tensegrity": {
        "title": "Tensegrity",
        "simple_desc": "How your body stays balanced using a mix of stiff parts (bones) and stretchy parts (muscles and fascia) working together.",
        "detailed_desc": """<p>Tensegrity (tensional integrity) is a structural principle where isolated compression elements (bones) are held in place by a continuous network of tension elements (fascia, muscles, ligaments). This concept revolutionizes our understanding of how the body maintains structural integrity and distributes forces.</p>
<p>In ELDOA practice, tensegrity explains why local treatments often fail—the body functions as an integrated tensional network, not a stack of independent parts. When we create tension in one area through ELDOA positioning, that force is transmitted throughout the entire fascial network, creating global effects from targeted interventions.</p>
<p>Understanding tensegrity helps explain why spinal decompression achieved through ELDOA can affect distant body regions. The fascial continuity that characterizes tensegrity means that creating space at one vertebral level can improve tissue quality and function throughout connected fascial chains.</p>""",
        "benefits": ["Holistic body understanding", "Explains force distribution", "Guides treatment approach", "Supports fascial training", "Improves structural balance", "Enhances body awareness"],
        "applications": ["Fascial system training", "Postural optimization", "Movement efficiency", "Injury prevention", "Structural assessment", "Treatment planning"],
        "related_terms": [("fascial-system", "Fascial System"), ("biomechanics", "Biomechanics"), ("structural-integration", "Structural Integration"), ("connective-tissue", "Connective Tissue")],
        "connections": [("myofascial-chains", "Myofascial Chains"), ("global-fascial-integration", "Global Fascial Integration"), ("force-transmission", "Force Transmission"), ("postural-balance", "Postural Balance")]
    },
    "mechanotransduction": {
        "title": "Mechanotransduction",
        "simple_desc": "How your cells sense when you stretch or press on them and respond by getting stronger or healing.",
        "detailed_desc": """<p>Mechanotransduction is the process by which cells convert mechanical stimuli into biochemical signals, triggering cellular responses such as protein synthesis, gene expression, and tissue remodeling. This fundamental biological process explains how physical interventions like ELDOA create lasting tissue changes.</p>
<p>In fascia and connective tissue, mechanotransduction occurs through specialized cells called fibroblasts. When these cells experience appropriate mechanical loading—as created during ELDOA holds—they respond by producing collagen, ground substance, and other extracellular matrix components that improve tissue quality.</p>
<p>The sustained holds characteristic of ELDOA (typically 60 seconds) are specifically designed to optimize mechanotransduction. This duration allows sufficient time for cellular signaling cascades to activate, promoting tissue remodeling, improved hydration, and enhanced structural properties.</p>""",
        "benefits": ["Promotes tissue remodeling", "Stimulates cellular repair", "Improves tissue quality", "Enhances adaptation", "Supports healing processes", "Optimizes tissue response"],
        "applications": ["Tissue rehabilitation", "Fascial training", "Injury recovery", "Chronic condition management", "Performance enhancement", "Anti-aging protocols"],
        "related_terms": [("fascial-system", "Fascial System"), ("connective-tissue", "Connective Tissue"), ("tissue-healing", "Tissue Healing"), ("collagen", "Collagen")],
        "connections": [("fibroblasts", "Fibroblasts"), ("sustained-holds", "Sustained Holds"), ("tissue-remodeling", "Tissue Remodeling"), ("cellular-response", "Cellular Response")]
    },
    "superficial-back-line": {
        "title": "Superficial Back Line",
        "simple_desc": "A chain of connected tissues running from your toes, up the back of your legs and spine, to the top of your head.",
        "detailed_desc": """<p>The Superficial Back Line (SBL) is one of the primary myofascial meridians described by Thomas Myers in Anatomy Trains. It runs from the plantar fascia of the feet, up through the gastrocnemius, hamstrings, sacrotuberous ligament, erector spinae, and galea aponeurotica to the brow ridge.</p>
<p>In ELDOA practice, the SBL is frequently addressed because of its role in postural control and its common involvement in back pain conditions. Restrictions anywhere along this line can create compensatory patterns and symptoms at distant locations—explaining why foot problems can contribute to headaches and vice versa.</p>
<p>ELDOA positions that address the posterior spine simultaneously affect the entire Superficial Back Line due to fascial continuity. This understanding allows practitioners to create comprehensive treatment strategies that address the full chain rather than isolated segments.</p>""",
        "benefits": ["Improves posterior chain mobility", "Reduces back tension", "Enhances postural control", "Addresses chain restrictions", "Improves forward bending", "Supports spinal health"],
        "applications": ["Back pain treatment", "Hamstring flexibility", "Postural correction", "Athletic performance", "Headache management", "Whole-body integration"],
        "related_terms": [("myofascial-chains", "Myofascial Chains"), ("fascial-system", "Fascial System"), ("deep-front-line", "Deep Front Line"), ("spiral-line", "Spiral Line")],
        "connections": [("erector-spinae", "Erector Spinae"), ("hamstrings", "Hamstrings"), ("plantar-fascia", "Plantar Fascia"), ("thoracolumbar-fascia", "Thoracolumbar Fascia")]
    },
    "deep-front-line": {
        "title": "Deep Front Line",
        "simple_desc": "The deepest chain of tissues in your body that supports your core and connects your breathing to your movement.",
        "detailed_desc": """<p>The Deep Front Line (DFL) is the body's core myofascial meridian, running from the deep foot structures through the inner leg, pelvic floor, psoas, diaphragm, and deep cervical structures to the base of the skull. It provides the body's central axis of support and stability.</p>
<p>In ELDOA methodology, the DFL is particularly important because it directly relates to spinal health and core stability. The psoas muscle, a key component of the DFL, has direct attachments to the lumbar vertebrae and is frequently implicated in lower back conditions.</p>
<p>ELDOA positions that target the lumbar spine inherently affect the Deep Front Line, particularly through their influence on the psoas and diaphragm. Understanding this connection helps explain why ELDOA practice often improves breathing patterns alongside spinal mobility.</p>""",
        "benefits": ["Enhances core stability", "Improves breathing function", "Supports spinal alignment", "Addresses deep restrictions", "Improves pelvic function", "Balances posture"],
        "applications": ["Core training", "Breathing optimization", "Pelvic floor therapy", "Postural rehabilitation", "Lower back treatment", "Movement integration"],
        "related_terms": [("myofascial-chains", "Myofascial Chains"), ("superficial-back-line", "Superficial Back Line"), ("spiral-line", "Spiral Line"), ("fascial-system", "Fascial System")],
        "connections": [("psoas-muscle", "Psoas Muscle"), ("diaphragm", "Diaphragm"), ("pelvic-floor", "Pelvic Floor"), ("core-stability", "Core Stability")]
    },
    "spiral-line": {
        "title": "Spiral Line",
        "simple_desc": "A twisted chain of tissues that wraps around your body and helps you rotate and turn.",
        "detailed_desc": """<p>The Spiral Line is a myofascial meridian that wraps around the body in a double helix pattern, connecting the skull to the feet through rotational pathways. It includes structures like the splenius capitis, rhomboids, serratus anterior, external obliques, IT band, and tibialis anterior.</p>
<p>This line is essential for rotational movements and plays a key role in gait mechanics. In ELDOA practice, addressing the Spiral Line helps resolve rotational imbalances and asymmetries that often contribute to spinal dysfunction and pain patterns.</p>
<p>The Spiral Line's influence on trunk rotation makes it particularly relevant for thoracic spine ELDOA positions. Restrictions in this line can limit thoracic mobility, affecting breathing, upper extremity function, and overall movement quality.</p>""",
        "benefits": ["Improves rotational mobility", "Addresses asymmetries", "Enhances gait mechanics", "Supports trunk rotation", "Balances left-right differences", "Improves coordination"],
        "applications": ["Rotational sports training", "Gait optimization", "Scoliosis management", "Asymmetry correction", "Trunk mobility", "Movement coordination"],
        "related_terms": [("myofascial-chains", "Myofascial Chains"), ("superficial-back-line", "Superficial Back Line"), ("deep-front-line", "Deep Front Line"), ("fascial-system", "Fascial System")],
        "connections": [("thoracic-rotation", "Thoracic Rotation"), ("obliques", "Obliques"), ("it-band", "IT Band"), ("gait-mechanics", "Gait Mechanics")]
    },
    "fascial-chains": {
        "title": "Fascial Chains",
        "simple_desc": "Connected lines of tissue that run through your whole body, linking distant parts together.",
        "detailed_desc": """<p>Fascial chains, also called myofascial meridians, are continuous lines of connective tissue that traverse the body, connecting muscles, bones, and organs into functional units. These chains explain how force and tension are transmitted throughout the body and why symptoms often appear distant from their source.</p>
<p>ELDOA methodology incorporates fascial chain concepts to create comprehensive treatment approaches. Rather than treating isolated structures, ELDOA positions are designed to affect entire chains, creating more lasting and global improvements.</p>
<p>Major fascial chains include the Superficial Back Line, Deep Front Line, Spiral Line, Lateral Line, and Arm Lines. Understanding these pathways allows practitioners to trace dysfunction patterns and design interventions that address root causes rather than just symptoms.</p>""",
        "benefits": ["Explains distant symptoms", "Guides comprehensive treatment", "Improves force transmission", "Enhances movement efficiency", "Supports whole-body health", "Addresses root causes"],
        "applications": ["Pain pattern analysis", "Treatment planning", "Movement optimization", "Injury prevention", "Performance enhancement", "Postural assessment"],
        "related_terms": [("myofascial-chains", "Myofascial Chains"), ("superficial-back-line", "Superficial Back Line"), ("deep-front-line", "Deep Front Line"), ("spiral-line", "Spiral Line")],
        "connections": [("fascial-system", "Fascial System"), ("tensegrity", "Tensegrity"), ("connective-tissue", "Connective Tissue"), ("force-transmission", "Force Transmission")]
    },
    "myofascial-release": {
        "title": "Myofascial Release",
        "simple_desc": "A gentle hands-on technique that helps loosen tight fascia and reduce pain in your muscles.",
        "detailed_desc": """<p>Myofascial release (MFR) is a manual therapy technique that applies sustained pressure to fascial restrictions to reduce pain and restore motion. Unlike ELDOA, which uses active positioning and self-treatment, traditional MFR is typically performed by a therapist.</p>
<p>In the broader context of ELDOA practice, myofascial release techniques can complement the active work of ELDOA positions. While ELDOA creates space through precise positioning and sustained holds, MFR can address specific adhesions and restrictions that limit the effectiveness of active approaches.</p>
<p>The philosophy underlying both approaches is similar—recognition that fascia plays a crucial role in pain and dysfunction, and that appropriate mechanical input can stimulate tissue change. ELDOA offers the advantage of self-treatment capability, while MFR provides therapist-guided precision for specific restrictions.</p>""",
        "benefits": ["Reduces fascial restrictions", "Relieves muscle tension", "Improves tissue mobility", "Decreases pain", "Enhances circulation", "Supports healing"],
        "applications": ["Pain management", "Movement restoration", "Injury recovery", "Chronic tension relief", "Complementary treatment", "Tissue optimization"],
        "related_terms": [("fascial-system", "Fascial System"), ("connective-tissue", "Connective Tissue"), ("manual-therapy", "Manual Therapy"), ("soft-tissue-work", "Soft Tissue Work")],
        "connections": [("fascial-restrictions", "Fascial Restrictions"), ("tissue-hydration", "Tissue Hydration"), ("mechanotransduction", "Mechanotransduction"), ("pain-relief", "Pain Relief")]
    },
    "motor-learning": {
        "title": "Motor Learning",
        "simple_desc": "How your brain learns new movements and makes them automatic through practice.",
        "detailed_desc": """<p>Motor learning is the neurological process by which the brain acquires, refines, and retains movement skills. This involves changes in neural pathways, improved coordination, and the eventual automation of movement patterns through practice and repetition.</p>
<p>ELDOA practice involves significant motor learning components. The precise positioning required for effective ELDOA demands body awareness, coordination, and the ability to maintain specific alignments. With practice, these positions become more accessible and effective as neural pathways strengthen.</p>
<p>Understanding motor learning principles helps optimize ELDOA practice. Consistent practice, appropriate feedback, and progressive challenge all enhance the learning process. Over time, the postural awareness developed through ELDOA transfers to daily activities, improving movement quality throughout life.</p>""",
        "benefits": ["Improves movement skill", "Enhances body awareness", "Develops coordination", "Automates good patterns", "Supports practice efficiency", "Transfers to daily life"],
        "applications": ["ELDOA skill development", "Movement re-education", "Athletic training", "Rehabilitation", "Postural correction", "Coordination improvement"],
        "related_terms": [("neuroplasticity", "Neuroplasticity"), ("proprioception", "Proprioception"), ("kinesthetic-awareness", "Kinesthetic Awareness"), ("movement-patterns", "Movement Patterns")],
        "connections": [("neural-adaptation", "Neural Adaptation"), ("practice-principles", "Practice Principles"), ("skill-acquisition", "Skill Acquisition"), ("body-awareness", "Body Awareness")]
    },
    "posterior-chain": {
        "title": "Posterior Chain",
        "simple_desc": "All the muscles on the back of your body that help you stand up straight, run, and jump.",
        "detailed_desc": """<p>The posterior chain refers to the interconnected muscles along the back of the body, including the erector spinae, gluteals, hamstrings, and calves. These muscles work together to extend the hip and spine, providing power for activities like running, jumping, and lifting.</p>
<p>In ELDOA practice, the posterior chain is frequently addressed because of its role in spinal support and its common involvement in pain conditions. Restrictions or weakness in the posterior chain can lead to compensatory patterns, altered spinal mechanics, and chronic pain.</p>
<p>ELDOA positions that target the lumbar and thoracic spine inherently engage and stretch the posterior chain. This integrated approach addresses both spinal decompression and posterior chain flexibility, creating comprehensive improvements in function and pain reduction.</p>""",
        "benefits": ["Improves posterior flexibility", "Enhances power production", "Supports spinal health", "Reduces back strain", "Improves athletic performance", "Balances anterior muscles"],
        "applications": ["Athletic training", "Back pain management", "Postural improvement", "Power development", "Injury prevention", "Movement optimization"],
        "related_terms": [("superficial-back-line", "Superficial Back Line"), ("hamstring-flexibility", "Hamstring Flexibility"), ("gluteals", "Gluteals"), ("erector-spinae", "Erector Spinae")],
        "connections": [("lumbar-spine", "Lumbar Spine"), ("hip-extension", "Hip Extension"), ("fascial-system", "Fascial System"), ("force-transmission", "Force Transmission")]
    },
    "plantar-fasciitis": {
        "title": "Plantar Fasciitis",
        "simple_desc": "Pain in the bottom of your foot, especially near your heel, from the tissue there getting irritated.",
        "detailed_desc": """<p>Plantar fasciitis is a common condition characterized by pain at the plantar fascia attachment to the calcaneus (heel bone). It typically presents as heel pain that is worst with the first steps in the morning and after periods of rest.</p>
<p>From an ELDOA perspective, plantar fasciitis is rarely a purely local problem. The plantar fascia is continuous with the Superficial Back Line, connecting to the calf muscles, hamstrings, and spinal structures. Restrictions or dysfunctions anywhere along this chain can contribute to plantar fascial stress.</p>
<p>ELDOA treatment for plantar fasciitis addresses the entire posterior chain rather than just the foot. By improving mobility and tissue quality throughout the Superficial Back Line, stress on the plantar fascia is reduced, promoting healing and preventing recurrence.</p>""",
        "benefits": ["Addresses root causes", "Reduces heel pain", "Improves whole-chain mobility", "Prevents recurrence", "Supports tissue healing", "Enhances foot function"],
        "applications": ["Heel pain treatment", "Running injury management", "Standing tolerance improvement", "Morning pain reduction", "Chronic foot pain", "Athletic recovery"],
        "related_terms": [("superficial-back-line", "Superficial Back Line"), ("posterior-chain", "Posterior Chain"), ("foot-pain", "Foot Pain"), ("achilles-tendinopathy", "Achilles Tendinopathy")],
        "connections": [("fascial-chains", "Fascial Chains"), ("calf-muscles", "Calf Muscles"), ("tissue-healing", "Tissue Healing"), ("gait-mechanics", "Gait Mechanics")]
    },
    "calf-strain": {
        "title": "Calf Strain",
        "simple_desc": "When you hurt the muscles in the back of your lower leg, often from running or jumping.",
        "detailed_desc": """<p>Calf strain refers to injury to the gastrocnemius or soleus muscles of the posterior lower leg. These injuries range from mild fiber disruption to complete tears and commonly occur during explosive movements like sprinting or jumping.</p>
<p>In the ELDOA framework, calf strains are understood within the context of the posterior fascial chain. The calf muscles are continuous with the Achilles tendon below and the hamstrings above, meaning that restrictions or weaknesses elsewhere in the chain can predispose to calf injury.</p>
<p>ELDOA approaches calf strain recovery by addressing the entire posterior chain while allowing appropriate healing time for the local injury. This comprehensive approach reduces the likelihood of re-injury by addressing contributing factors rather than just the symptomatic area.</p>""",
        "benefits": ["Addresses contributing factors", "Supports healing", "Prevents re-injury", "Improves chain mobility", "Restores function", "Enhances recovery"],
        "applications": ["Calf injury recovery", "Running rehabilitation", "Athletic return-to-play", "Prevention programs", "Posterior chain balance", "Movement restoration"],
        "related_terms": [("posterior-chain", "Posterior Chain"), ("achilles-tendinopathy", "Achilles Tendinopathy"), ("hamstring-flexibility", "Hamstring Flexibility"), ("muscle-strain", "Muscle Strain")],
        "connections": [("superficial-back-line", "Superficial Back Line"), ("tissue-healing", "Tissue Healing"), ("gastrocnemius", "Gastrocnemius"), ("soleus", "Soleus")]
    },
    "overuse-injury": {
        "title": "Overuse Injury",
        "simple_desc": "When a body part gets hurt from doing the same movement too many times without enough rest.",
        "detailed_desc": """<p>Overuse injuries result from repetitive stress that exceeds tissue capacity for adaptation and repair. Common examples include tendinopathies, stress fractures, and chronic muscle strains. These conditions develop gradually rather than from a single traumatic event.</p>
<p>ELDOA addresses overuse injuries by improving tissue quality and addressing biomechanical factors that contribute to excessive stress. By optimizing fascial health and spinal mechanics, ELDOA can reduce the abnormal loading patterns that lead to overuse conditions.</p>
<p>Prevention of overuse injuries is a key benefit of regular ELDOA practice. The improved tissue quality, better load distribution, and enhanced body awareness developed through ELDOA help maintain tissue health even with high training volumes.</p>""",
        "benefits": ["Addresses contributing factors", "Improves tissue quality", "Optimizes biomechanics", "Supports prevention", "Enhances recovery", "Reduces recurrence"],
        "applications": ["Injury prevention", "Training optimization", "Chronic condition management", "Athletic performance", "Work-related injury", "Repetitive strain treatment"],
        "related_terms": [("injury-prevention", "Injury Prevention"), ("tissue-healing", "Tissue Healing"), ("tendinopathy", "Tendinopathy"), ("repetitive-strain", "Repetitive Strain")],
        "connections": [("biomechanics", "Biomechanics"), ("tissue-capacity", "Tissue Capacity"), ("training-load", "Training Load"), ("recovery", "Recovery")]
    },
    "tendon-healing": {
        "title": "Tendon Healing",
        "simple_desc": "How your tendons repair themselves after injury, which takes longer than muscle healing.",
        "detailed_desc": """<p>Tendon healing is a complex process that typically proceeds more slowly than muscle healing due to tendons' relatively limited blood supply. The healing process involves inflammation, proliferation, and remodeling phases, with full recovery often taking months to years.</p>
<p>ELDOA supports tendon healing through mechanotransduction—the process by which mechanical loading stimulates cellular repair and tissue remodeling. The sustained holds in ELDOA positions provide appropriate mechanical input that promotes tendon adaptation without overwhelming healing tissues.</p>
<p>Understanding tendon healing timelines is essential for appropriate ELDOA prescription. Early-stage healing requires reduced loading, while later stages benefit from progressive mechanical challenge to optimize tissue strength and collagen alignment.</p>""",
        "benefits": ["Supports healing process", "Optimizes collagen alignment", "Promotes tissue quality", "Provides appropriate loading", "Enhances remodeling", "Improves outcomes"],
        "applications": ["Tendinopathy treatment", "Post-injury recovery", "Chronic tendon issues", "Athletic rehabilitation", "Surgical recovery", "Prevention programs"],
        "related_terms": [("tissue-healing", "Tissue Healing"), ("achilles-tendinopathy", "Achilles Tendinopathy"), ("collagen", "Collagen"), ("mechanotransduction", "Mechanotransduction")],
        "connections": [("eccentric-loading", "Eccentric Loading"), ("progressive-loading", "Progressive Loading"), ("rehabilitation", "Rehabilitation"), ("fascial-system", "Fascial System")]
    },
    "l5-s1-decompression": {
        "title": "L5 S1 Decompression",
        "simple_desc": "A specific ELDOA exercise that creates space at the lowest part of your spine where it meets your pelvis.",
        "detailed_desc": """<p>L5-S1 decompression is one of the most commonly prescribed ELDOA positions, targeting the lumbosacral junction—the transition between the lumbar spine and sacrum. This segment bears significant load and is a frequent site of disc pathology and pain.</p>
<p>The L5-S1 ELDOA position uses precise body positioning to create axial tension that separates the L5 and S1 vertebrae. This decompression improves disc hydration, reduces pressure on neural structures, and creates space within the facet joints.</p>
<p>This position is particularly valuable for conditions like L5-S1 disc herniation, sciatica with L5 or S1 nerve root involvement, and lumbosacral facet syndrome. Regular practice helps maintain space at this crucial junction and prevents progression of degenerative changes.</p>""",
        "benefits": ["Creates lumbosacral space", "Reduces disc pressure", "Improves disc hydration", "Relieves nerve compression", "Supports facet health", "Addresses L5-S1 pathology"],
        "applications": ["L5-S1 disc herniation", "Sciatica treatment", "Lower back pain", "Degenerative changes", "Post-surgical care", "Prevention maintenance"],
        "related_terms": [("l5-s1-junction", "L5 S1 Junction"), ("spinal-decompression", "Spinal Decompression"), ("lumbar-spine", "Lumbar Spine"), ("sacrum", "Sacrum")],
        "connections": [("disc-hydration", "Disc Hydration"), ("nerve-root", "Nerve Root"), ("facet-joints", "Facet Joints"), ("lumbosacral-mechanics", "Lumbosacral Mechanics")]
    },
    "posterior-fascial-line": {
        "title": "Posterior Fascial Line",
        "simple_desc": "The connected sheet of tissue running down the entire back of your body from head to heels.",
        "detailed_desc": """<p>The posterior fascial line, closely related to the Superficial Back Line, describes the continuous fascial sheet running along the posterior aspect of the body. This includes the plantar fascia, Achilles tendon, gastrocnemius fascia, hamstring fascia, sacrotuberous ligament, thoracolumbar fascia, and cranial fascia.</p>
<p>In ELDOA practice, understanding the posterior fascial line explains why spinal positions affect the entire back body. When we create tension and space in the lumbar spine, that effect transmits through the fascial continuity to influence tissues from the feet to the head.</p>
<p>Restrictions in the posterior fascial line commonly manifest as limited forward bending, hamstring tightness, lower back pain, and tension headaches. ELDOA addresses these issues by improving tissue quality throughout the entire line rather than treating isolated segments.</p>""",
        "benefits": ["Improves whole-body flexibility", "Reduces posterior tension", "Addresses chain restrictions", "Enhances forward bending", "Relieves headaches", "Supports spinal health"],
        "applications": ["Back pain treatment", "Flexibility improvement", "Headache management", "Postural correction", "Athletic performance", "Movement optimization"],
        "related_terms": [("superficial-back-line", "Superficial Back Line"), ("fascial-chains", "Fascial Chains"), ("posterior-chain", "Posterior Chain"), ("thoracolumbar-fascia", "Thoracolumbar Fascia")],
        "connections": [("fascial-system", "Fascial System"), ("tensegrity", "Tensegrity"), ("myofascial-chains", "Myofascial Chains"), ("tissue-continuity", "Tissue Continuity")]
    },
    "eccentric-loading": {
        "title": "Eccentric Loading",
        "simple_desc": "Strengthening your muscles while they lengthen, like lowering yourself slowly from a pull-up.",
        "detailed_desc": """<p>Eccentric loading refers to muscle contraction during lengthening, as opposed to concentric contraction during shortening. Research has demonstrated that eccentric exercise is particularly effective for tendon rehabilitation and tissue remodeling.</p>
<p>While ELDOA is not primarily an eccentric loading technique, understanding this principle helps explain tissue adaptation. The sustained holds in ELDOA positions create isometric loading that shares some benefits with eccentric work, particularly in promoting mechanotransduction and tissue remodeling.</p>
<p>For conditions like Achilles tendinopathy or patellar tendinopathy, eccentric loading protocols may complement ELDOA practice. The combination of ELDOA for spinal and fascial optimization with targeted eccentric work for specific tendons can provide comprehensive treatment.</p>""",
        "benefits": ["Promotes tendon health", "Enhances tissue remodeling", "Improves strength in lengthened positions", "Supports injury recovery", "Builds resilient tissue", "Complements ELDOA"],
        "applications": ["Tendinopathy treatment", "Athletic training", "Injury prevention", "Rehabilitation programs", "Strength development", "Tissue optimization"],
        "related_terms": [("tendon-healing", "Tendon Healing"), ("mechanotransduction", "Mechanotransduction"), ("tissue-remodeling", "Tissue Remodeling"), ("strength-training", "Strength Training")],
        "connections": [("achilles-tendinopathy", "Achilles Tendinopathy"), ("progressive-loading", "Progressive Loading"), ("muscle-function", "Muscle Function"), ("rehabilitation", "Rehabilitation")]
    },
    "joint-separation": {
        "title": "Joint Separation",
        "simple_desc": "Creating space between the bones in a joint to help it move better and feel less painful.",
        "detailed_desc": """<p>Joint separation, or articular decoaptation, is a core principle of ELDOA methodology. It involves creating space within a joint through precise positioning and sustained tension, allowing for improved joint nutrition, reduced compression, and enhanced mobility.</p>
<p>ELDOA achieves joint separation through myofascial tension rather than external traction. By precisely positioning the body and creating tension through the fascial system, space is created within targeted joints—particularly the intervertebral joints of the spine.</p>
<p>The benefits of joint separation include improved synovial fluid circulation, reduced pressure on articular cartilage, decreased nerve compression, and enhanced joint proprioception. This principle applies to both spinal and peripheral joints, though ELDOA primarily focuses on the spine.</p>""",
        "benefits": ["Creates joint space", "Improves nutrition", "Reduces compression", "Enhances mobility", "Decreases pain", "Supports joint health"],
        "applications": ["Spinal decompression", "Joint pain treatment", "Degenerative conditions", "Movement restoration", "Preventive care", "Performance optimization"],
        "related_terms": [("hip-decoaptation", "Hip Decoaptation"), ("spinal-decompression", "Spinal Decompression"), ("traction", "Traction"), ("intervertebral-space", "Intervertebral Space")],
        "connections": [("disc-hydration", "Disc Hydration"), ("joint-nutrition", "Joint Nutrition"), ("facet-joints", "Facet Joints"), ("cartilage-health", "Cartilage Health")]
    },
    "traction": {
        "title": "Traction",
        "simple_desc": "Gently pulling on a body part to stretch it and create space, often used for the spine.",
        "detailed_desc": """<p>Traction is the application of pulling force to create separation within a joint or along a tissue. In spinal therapy, traction has been used for centuries to create intervertebral space and relieve nerve compression.</p>
<p>ELDOA differs from traditional traction by using active, internal tension rather than external pulling forces. While mechanical traction relies on external devices, ELDOA creates decompression through precise positioning and sustained muscular effort, making it more sustainable and accessible.</p>
<p>The active nature of ELDOA provides advantages over passive traction, including improved motor learning, better tissue quality through mechanotransduction, and the development of postural awareness that maintains benefits beyond the practice session.</p>""",
        "benefits": ["Creates joint space", "Relieves compression", "Improves disc health", "Reduces nerve pressure", "Enhances mobility", "Supports healing"],
        "applications": ["Spinal conditions", "Disc pathology", "Nerve compression", "Joint stiffness", "Pain management", "Decompression therapy"],
        "related_terms": [("joint-separation", "Joint Separation"), ("spinal-decompression", "Spinal Decompression"), ("inversion-therapy", "Inversion Therapy"), ("intervertebral-space", "Intervertebral Space")],
        "connections": [("disc-hydration", "Disc Hydration"), ("nerve-root", "Nerve Root"), ("vertebral-segment", "Vertebral Segment"), ("active-vs-passive", "Active Vs Passive")]
    },
    "intervertebral-space": {
        "title": "Intervertebral Space",
        "simple_desc": "The gap between the bones in your spine where the cushioning disc sits.",
        "detailed_desc": """<p>The intervertebral space is the region between adjacent vertebrae, occupied by the intervertebral disc, neural structures, and surrounding soft tissues. The height and health of this space are critical for spinal function and nerve integrity.</p>
<p>ELDOA's primary goal is to increase and maintain intervertebral space through active decompression. By creating axial tension through precise positioning, ELDOA positions increase the distance between vertebrae, reducing disc pressure and creating room for neural structures.</p>
<p>Loss of intervertebral space—from disc degeneration, poor posture, or aging—can lead to nerve compression, facet joint overload, and pain. Regular ELDOA practice helps maintain disc height and intervertebral space, potentially slowing degenerative processes.</p>""",
        "benefits": ["Increases disc space", "Reduces nerve compression", "Improves disc health", "Decreases facet loading", "Supports spinal height", "Maintains function"],
        "applications": ["Disc degeneration", "Nerve compression", "Height maintenance", "Spinal health", "Pain prevention", "Degenerative changes"],
        "related_terms": [("spinal-decompression", "Spinal Decompression"), ("intervertebral-disc", "Intervertebral Disc"), ("vertebral-segment", "Vertebral Segment"), ("disc-height", "Disc Height")],
        "connections": [("disc-hydration", "Disc Hydration"), ("neural-foramen", "Neural Foramen"), ("facet-joints", "Facet Joints"), ("spinal-mechanics", "Spinal Mechanics")]
    },
    "active-vs-passive": {
        "title": "Active Vs Passive",
        "simple_desc": "The difference between moving yourself versus having someone else move you during exercise or treatment.",
        "detailed_desc": """<p>The distinction between active and passive approaches is fundamental in rehabilitation and movement practice. Active approaches involve the patient's own muscular effort, while passive approaches involve external forces applied by a therapist or device.</p>
<p>ELDOA is fundamentally an active approach—the patient creates and maintains the decompression through their own effort. This active component provides multiple advantages: improved motor learning, enhanced proprioception, better mechanotransduction, and the development of sustainable self-care capabilities.</p>
<p>While passive techniques have their place in treatment, active approaches like ELDOA generally produce more lasting changes because they involve neurological learning and adaptation. The patient develops body awareness and control that transfers to daily activities.</p>""",
        "benefits": ["Promotes motor learning", "Develops body awareness", "Creates lasting change", "Enables self-treatment", "Improves proprioception", "Enhances independence"],
        "applications": ["Treatment planning", "Rehabilitation design", "Self-care development", "Patient education", "Long-term management", "Skill acquisition"],
        "related_terms": [("motor-learning", "Motor Learning"), ("proprioception", "Proprioception"), ("self-treatment", "Self Treatment"), ("rehabilitation", "Rehabilitation")],
        "connections": [("mechanotransduction", "Mechanotransduction"), ("neuroplasticity", "Neuroplasticity"), ("body-awareness", "Body Awareness"), ("patient-empowerment", "Patient Empowerment")]
    },
    "disc-hydration": {
        "title": "Disc Hydration",
        "simple_desc": "Keeping the cushions between your spine bones full of water so they stay plump and work well.",
        "detailed_desc": """<p>Disc hydration refers to the water content within intervertebral discs, which is essential for their shock-absorbing function and overall health. The nucleus pulposus, the gel-like center of the disc, is approximately 80% water in healthy young adults.</p>
<p>ELDOA promotes disc hydration through the decompression mechanism. When pressure on a disc is reduced, osmotic forces draw water into the nucleus pulposus, improving disc height and resilience. This is similar to how a sponge absorbs water when pressure is released.</p>
<p>Daily activities, particularly prolonged sitting and axial loading, gradually compress discs and reduce their water content. Regular ELDOA practice counteracts this by creating periods of decompression that allow discs to rehydrate, maintaining their height and function.</p>""",
        "benefits": ["Improves disc health", "Maintains disc height", "Enhances shock absorption", "Supports disc nutrition", "Prevents degeneration", "Restores function"],
        "applications": ["Disc degeneration", "Height loss prevention", "Spinal health maintenance", "Post-activity recovery", "Morning stiffness", "Long-term disc care"],
        "related_terms": [("intervertebral-disc", "Intervertebral Disc"), ("intervertebral-space", "Intervertebral Space"), ("spinal-decompression", "Spinal Decompression"), ("nucleus-pulposus", "Nucleus Pulposus")],
        "connections": [("l5-s1-decompression", "L5 S1 Decompression"), ("osmotic-pressure", "Osmotic Pressure"), ("disc-nutrition", "Disc Nutrition"), ("vertebral-segment", "Vertebral Segment")]
    },
    "spinal-curvature": {
        "title": "Spinal Curvature",
        "simple_desc": "The natural curves in your spine that help you balance, absorb shock, and move well.",
        "detailed_desc": """<p>Spinal curvature refers to the natural curves of the spine: cervical lordosis, thoracic kyphosis, and lumbar lordosis. These curves are essential for shock absorption, balance, and efficient load distribution.</p>
<p>Abnormal spinal curvatures, such as excessive kyphosis, hyperlordosis, or scoliosis, can lead to pain, dysfunction, and accelerated degeneration. ELDOA addresses curvature issues by creating space within segments and improving the postural awareness needed to maintain healthy alignment.</p>
<p>Understanding normal curvature is essential for appropriate ELDOA prescription. Each position is designed with respect to natural curves, and modifications may be needed for individuals with significant curvature abnormalities.</p>""",
        "benefits": ["Addresses curvature issues", "Improves spinal alignment", "Reduces pain from malalignment", "Supports balanced posture", "Enhances load distribution", "Prevents progression"],
        "applications": ["Scoliosis management", "Kyphosis treatment", "Lordosis correction", "Postural rehabilitation", "Spinal health", "Degenerative changes"],
        "related_terms": [("scoliosis", "Scoliosis"), ("kyphosis", "Kyphosis"), ("lordosis", "Lordosis"), ("postural-assessment", "Postural Assessment")],
        "connections": [("thoracic-spine", "Thoracic Spine"), ("lumbar-spine", "Lumbar Spine"), ("cervical-spine", "Cervical Spine"), ("posture", "Posture")]
    },
    "postural-asymmetry": {
        "title": "Postural Asymmetry",
        "simple_desc": "When one side of your body is different from the other in how you stand or move.",
        "detailed_desc": """<p>Postural asymmetry refers to differences in alignment, muscle tension, or movement patterns between the left and right sides of the body. Some asymmetry is normal, but significant differences can lead to compensatory patterns, uneven loading, and pain.</p>
<p>ELDOA addresses asymmetry through bilateral positions that create balanced tension and promote symmetrical alignment. Additionally, awareness developed through ELDOA practice helps individuals recognize and correct asymmetrical patterns in daily life.</p>
<p>Common causes of postural asymmetry include scoliosis, leg length differences, habitual postures, handedness, and occupational demands. ELDOA provides a systematic approach to improving symmetry while respecting anatomical individuality.</p>""",
        "benefits": ["Improves symmetry", "Reduces compensatory patterns", "Balances muscle tension", "Addresses uneven loading", "Enhances body awareness", "Supports alignment"],
        "applications": ["Postural correction", "Scoliosis management", "Athletic performance", "Pain treatment", "Movement optimization", "Body awareness"],
        "related_terms": [("scoliosis", "Scoliosis"), ("posture", "Posture"), ("alignment", "Alignment"), ("compensatory-patterns", "Compensatory Patterns")],
        "connections": [("spiral-line", "Spiral Line"), ("postural-assessment", "Postural Assessment"), ("movement-patterns", "Movement Patterns"), ("body-awareness", "Body Awareness")]
    },
    "rib-cage-deformity": {
        "title": "Rib Cage Deformity",
        "simple_desc": "When the shape of your rib cage is different from normal, which can affect breathing and posture.",
        "detailed_desc": """<p>Rib cage deformity refers to structural abnormalities in the thoracic cage, including conditions like pectus excavatum (sunken chest), pectus carinatum (pigeon chest), and rib asymmetry associated with scoliosis.</p>
<p>In scoliosis, rib cage deformity is common due to vertebral rotation, creating rib prominence on one side and flattening on the other. ELDOA addresses this through thoracic decompression positions that create space and promote more symmetrical rib cage mechanics.</p>
<p>Beyond structural concerns, rib cage deformity can affect breathing mechanics and overall thoracic mobility. ELDOA practice improves rib cage movement and respiratory function, even when structural abnormality cannot be fully corrected.</p>""",
        "benefits": ["Improves rib mobility", "Enhances breathing", "Addresses asymmetry", "Supports thoracic function", "Reduces restrictions", "Promotes better mechanics"],
        "applications": ["Scoliosis treatment", "Breathing improvement", "Thoracic mobility", "Postural correction", "Chest wall conditions", "Movement optimization"],
        "related_terms": [("scoliosis", "Scoliosis"), ("thoracic-spine", "Thoracic Spine"), ("breathing", "Breathing"), ("thoracic-rotation", "Thoracic Rotation")],
        "connections": [("vertebral-rotation", "Vertebral Rotation"), ("respiratory-function", "Respiratory Function"), ("chest-wall", "Chest Wall"), ("postural-assessment", "Postural Assessment")]
    },
    "structural-vs-functional": {
        "title": "Structural Vs Functional",
        "simple_desc": "The difference between problems caused by how your body is built versus how it moves or works.",
        "detailed_desc": """<p>The structural versus functional distinction differentiates between fixed anatomical abnormalities (structural) and adaptable movement or postural dysfunctions (functional). This distinction is crucial for treatment planning and outcome expectations.</p>
<p>Structural issues, such as congenital vertebral anomalies or true leg length discrepancies, cannot be changed through exercise. Functional issues, such as muscle imbalances or habitual postural patterns, can be significantly improved through interventions like ELDOA.</p>
<p>Many conditions have both structural and functional components. For example, scoliosis may have structural curvature that cannot be eliminated, but functional improvements in mobility, pain, and posture are often achievable through ELDOA practice.</p>""",
        "benefits": ["Clarifies treatment approach", "Sets appropriate expectations", "Guides intervention selection", "Identifies modifiable factors", "Supports realistic goals", "Improves outcomes"],
        "applications": ["Assessment and diagnosis", "Treatment planning", "Patient education", "Goal setting", "Outcome prediction", "Condition management"],
        "related_terms": [("scoliosis", "Scoliosis"), ("postural-assessment", "Postural Assessment"), ("functional-anatomy", "Functional Anatomy"), ("movement-assessment", "Movement Assessment")],
        "connections": [("biomechanics", "Biomechanics"), ("rehabilitation", "Rehabilitation"), ("compensatory-patterns", "Compensatory Patterns"), ("treatment-planning", "Treatment Planning")]
    },
    "thoracic-rotation": {
        "title": "Thoracic Rotation",
        "simple_desc": "Your upper back's ability to twist, which is important for reaching, throwing, and many daily activities.",
        "detailed_desc": """<p>Thoracic rotation is the rotational movement capacity of the thoracic spine. The thoracic region is designed to allow more rotation than the lumbar spine, making it essential for activities requiring trunk twisting.</p>
<p>Limited thoracic rotation forces compensatory movement at other segments, particularly the lumbar spine and cervical spine, which can lead to pain and dysfunction. ELDOA addresses thoracic rotation through specific positions that create space and mobility in the thoracic vertebrae.</p>
<p>The Spiral Line, a myofascial chain involved in rotation, heavily involves the thoracic region. ELDOA practice that addresses the thoracic spine often improves rotational capacity throughout the entire trunk and even into the limbs.</p>""",
        "benefits": ["Improves rotational mobility", "Reduces lumbar stress", "Enhances upper body function", "Supports athletic performance", "Decreases neck strain", "Improves movement quality"],
        "applications": ["Rotational sports", "Upper back stiffness", "Scoliosis management", "Golf and tennis performance", "Swimming efficiency", "Daily function"],
        "related_terms": [("thoracic-spine", "Thoracic Spine"), ("spiral-line", "Spiral Line"), ("spinal-mobility", "Spinal Mobility"), ("trunk-rotation", "Trunk Rotation")],
        "connections": [("scoliosis", "Scoliosis"), ("rib-cage-deformity", "Rib Cage Deformity"), ("vertebral-segment", "Vertebral Segment"), ("movement-patterns", "Movement Patterns")]
    },
    "cobb-angle": {
        "title": "Cobb Angle",
        "simple_desc": "A measurement doctors use on X-rays to see how curved your spine is if you have scoliosis.",
        "detailed_desc": """<p>The Cobb angle is the standard radiographic measurement for quantifying spinal curvature in scoliosis. It measures the angle between the most tilted vertebrae at the top and bottom of a curve, providing an objective assessment of curve magnitude.</p>
<p>While ELDOA cannot directly change structural Cobb angles, it can significantly improve functional capacity, pain, and mobility in individuals with scoliosis regardless of curve magnitude. Understanding Cobb angles helps practitioners tailor ELDOA protocols appropriately.</p>
<p>Curves under 10 degrees are generally not classified as scoliosis. Moderate curves (25-40 degrees) may benefit significantly from conservative approaches including ELDOA, while severe curves (over 45-50 degrees) may require surgical consideration alongside conservative management.</p>""",
        "benefits": ["Provides objective measurement", "Guides treatment planning", "Tracks progression", "Supports decision making", "Enables communication", "Sets realistic expectations"],
        "applications": ["Scoliosis assessment", "Treatment planning", "Progress monitoring", "Surgical decisions", "Patient education", "Outcome tracking"],
        "related_terms": [("scoliosis", "Scoliosis"), ("spinal-curvature", "Spinal Curvature"), ("postural-assessment", "Postural Assessment"), ("radiographic-assessment", "Radiographic Assessment")],
        "connections": [("apical-vertebra", "Apical Vertebra"), ("end-vertebra", "End Vertebra"), ("thoracic-spine", "Thoracic Spine"), ("lumbar-spine", "Lumbar Spine")]
    },
    "convex-concave": {
        "title": "Convex Concave",
        "simple_desc": "The two sides of a spinal curve - the outward bulging side and the inward curving side.",
        "detailed_desc": """<p>In scoliosis terminology, convex and concave describe the two sides of a spinal curve. The convex side is the outward bulging aspect of the curve, while the concave side is the inward aspect. This distinction is important for understanding tissue states and treatment approaches.</p>
<p>Tissues on the convex side of a scoliotic curve are typically stretched and elongated, while concave-side tissues are shortened and compressed. ELDOA addresses both sides through balanced positioning that creates space throughout the curve.</p>
<p>Understanding convex-concave dynamics helps practitioners modify ELDOA positions appropriately for individuals with scoliosis, ensuring that interventions create beneficial effects rather than exacerbating existing imbalances.</p>""",
        "benefits": ["Guides treatment approach", "Explains tissue states", "Informs positioning", "Supports balanced treatment", "Improves outcomes", "Enhances understanding"],
        "applications": ["Scoliosis treatment", "Position modification", "Tissue assessment", "Treatment planning", "Patient education", "Rehabilitation design"],
        "related_terms": [("scoliosis", "Scoliosis"), ("spinal-curvature", "Spinal Curvature"), ("postural-asymmetry", "Postural Asymmetry"), ("cobb-angle", "Cobb Angle")],
        "connections": [("apical-vertebra", "Apical Vertebra"), ("vertebral-rotation", "Vertebral Rotation"), ("tissue-tension", "Tissue Tension"), ("balanced-treatment", "Balanced Treatment")]
    },
    "apical-vertebra": {
        "title": "Apical Vertebra",
        "simple_desc": "The most tilted bone in a curved spine, sitting at the peak of the curve.",
        "detailed_desc": """<p>The apical vertebra is the most laterally deviated and rotated vertebra at the apex of a scoliotic curve. It represents the point of maximum displacement from the midline and is a key reference point in scoliosis assessment and treatment.</p>
<p>In ELDOA for scoliosis, understanding the location of the apical vertebra helps target interventions appropriately. Positions can be selected or modified to create space and improve mechanics at the level of greatest deformity.</p>
<p>The apical vertebra typically shows the greatest rotation in addition to lateral deviation. This rotation contributes to rib cage asymmetry in thoracic curves and affects the overall three-dimensional nature of scoliotic deformity.</p>""",
        "benefits": ["Targets treatment accurately", "Identifies key dysfunction level", "Guides position selection", "Improves treatment precision", "Supports assessment", "Enhances outcomes"],
        "applications": ["Scoliosis assessment", "Treatment targeting", "Position selection", "Progress monitoring", "Patient education", "Surgical planning"],
        "related_terms": [("scoliosis", "Scoliosis"), ("cobb-angle", "Cobb Angle"), ("vertebral-rotation", "Vertebral Rotation"), ("spinal-curvature", "Spinal Curvature")],
        "connections": [("convex-concave", "Convex Concave"), ("rib-cage-deformity", "Rib Cage Deformity"), ("thoracic-spine", "Thoracic Spine"), ("lumbar-spine", "Lumbar Spine")]
    },
    "kinesthesia": {
        "title": "Kinesthesia",
        "simple_desc": "Your ability to sense where your body is and how it's moving without looking.",
        "detailed_desc": """<p>Kinesthesia is the sense of body position and movement, mediated by receptors in muscles, tendons, and joints. It is a component of proprioception and is essential for coordinated movement and postural control.</p>
<p>ELDOA practice significantly develops kinesthesia through the precise positioning and sustained awareness required. The subtle adjustments needed to maintain ELDOA positions enhance the body's ability to sense and control position.</p>
<p>Improved kinesthesia developed through ELDOA transfers to daily activities, enhancing movement quality, reducing injury risk, and supporting better posture throughout the day. This neurological benefit complements the structural effects of decompression.</p>""",
        "benefits": ["Improves body awareness", "Enhances movement control", "Develops coordination", "Supports postural control", "Reduces injury risk", "Improves performance"],
        "applications": ["Movement training", "Rehabilitation", "Athletic performance", "Fall prevention", "Postural correction", "Skill development"],
        "related_terms": [("proprioception", "Proprioception"), ("body-awareness", "Body Awareness"), ("motor-learning", "Motor Learning"), ("coordination", "Coordination")],
        "connections": [("fascial-mechanoreceptors", "Fascial Mechanoreceptors"), ("neuromuscular-control", "Neuromuscular Control"), ("movement-patterns", "Movement Patterns"), ("postural-control", "Postural Control")]
    },
    "fascial-mechanoreceptors": {
        "title": "Fascial Mechanoreceptors",
        "simple_desc": "Tiny sensors in your fascia that tell your brain about pressure, stretch, and movement.",
        "detailed_desc": """<p>Fascial mechanoreceptors are sensory nerve endings within fascia that detect mechanical stimuli such as pressure, stretch, and vibration. Research has revealed that fascia is richly innervated, making it a significant sensory organ.</p>
<p>In ELDOA practice, stimulation of fascial mechanoreceptors contributes to the neurological benefits observed. The sustained tension created in ELDOA positions provides prolonged stimulation that enhances proprioceptive input and body awareness.</p>
<p>Different types of mechanoreceptors respond to different stimuli: Ruffini endings detect sustained pressure and stretch, Pacinian corpuscles respond to rapid changes and vibration, and free nerve endings contribute to pain and temperature sensation. ELDOA's sustained holds particularly activate Ruffini endings.</p>""",
        "benefits": ["Enhances proprioception", "Improves body awareness", "Supports movement control", "Provides sensory feedback", "Develops neural pathways", "Improves coordination"],
        "applications": ["Proprioceptive training", "Balance improvement", "Movement re-education", "Pain management", "Rehabilitation", "Performance enhancement"],
        "related_terms": [("proprioception", "Proprioception"), ("fascial-system", "Fascial System"), ("kinesthesia", "Kinesthesia"), ("sensory-input", "Sensory Input")],
        "connections": [("neuromuscular-control", "Neuromuscular Control"), ("body-awareness", "Body Awareness"), ("mechanotransduction", "Mechanotransduction"), ("neural-adaptation", "Neural Adaptation")]
    },
    "neuromuscular-control": {
        "title": "Neuromuscular Control",
        "simple_desc": "How your brain and muscles work together to make smooth, coordinated movements.",
        "detailed_desc": """<p>Neuromuscular control refers to the integration of sensory information and motor output that produces coordinated movement. It involves the central nervous system processing proprioceptive input and generating appropriate muscle activation patterns.</p>
<p>ELDOA develops neuromuscular control through the precise positioning and sustained holds required. The practice demands continuous adjustment and awareness, training the nervous system to better coordinate muscle activity for postural control.</p>
<p>Poor neuromuscular control is associated with injury risk, movement inefficiency, and chronic pain. The neuromuscular training inherent in ELDOA practice helps address these issues by improving the quality of movement coordination.</p>""",
        "benefits": ["Improves coordination", "Enhances movement quality", "Reduces injury risk", "Supports postural control", "Develops motor skills", "Optimizes muscle activation"],
        "applications": ["Athletic training", "Rehabilitation", "Injury prevention", "Movement optimization", "Postural correction", "Skill development"],
        "related_terms": [("motor-learning", "Motor Learning"), ("proprioception", "Proprioception"), ("coordination", "Coordination"), ("muscle-activation", "Muscle Activation")],
        "connections": [("fascial-mechanoreceptors", "Fascial Mechanoreceptors"), ("kinesthesia", "Kinesthesia"), ("movement-patterns", "Movement Patterns"), ("motor-control", "Motor Control")]
    },
    "brain-plasticity": {
        "title": "Brain Plasticity",
        "simple_desc": "Your brain's amazing ability to change and adapt by forming new connections throughout your life.",
        "detailed_desc": """<p>Brain plasticity, or neuroplasticity, is the brain's ability to reorganize itself by forming new neural connections throughout life. This capacity allows learning, adaptation to new situations, and recovery from injury.</p>
<p>ELDOA practice leverages brain plasticity to create lasting changes in movement patterns and body awareness. The repeated precise positioning and sustained attention required for ELDOA drive neural adaptations that persist beyond the practice session.</p>
<p>Understanding brain plasticity explains why consistent practice is essential for ELDOA benefits. Neural changes require repetition and time to consolidate, meaning that regular practice over weeks and months produces increasingly significant and lasting improvements.</p>""",
        "benefits": ["Enables lasting change", "Supports learning", "Allows adaptation", "Improves function", "Promotes recovery", "Enhances development"],
        "applications": ["Movement re-education", "Rehabilitation", "Skill acquisition", "Pain management", "Postural change", "Performance improvement"],
        "related_terms": [("neuroplasticity", "Neuroplasticity"), ("motor-learning", "Motor Learning"), ("neural-adaptation", "Neural Adaptation"), ("habit-formation", "Habit Formation")],
        "connections": [("motor-cortex", "Motor Cortex"), ("body-schema", "Body Schema"), ("practice-principles", "Practice Principles"), ("skill-development", "Skill Development")]
    },
    "neural-adaptation": {
        "title": "Neural Adaptation",
        "simple_desc": "How your nervous system changes and gets better at controlling movement with practice.",
        "detailed_desc": """<p>Neural adaptation refers to changes in nervous system function that occur in response to training or experience. These adaptations include improved motor unit recruitment, enhanced coordination, and more efficient movement patterns.</p>
<p>In ELDOA practice, neural adaptation accounts for much of the early improvement observed. Before significant structural changes occur in tissues, the nervous system adapts to better control the precise positions and tensions required.</p>
<p>Neural adaptations from ELDOA include improved postural awareness, better coordination of stabilizing muscles, and more efficient movement patterns. These changes contribute to both the immediate and long-term benefits of practice.</p>""",
        "benefits": ["Improves movement efficiency", "Enhances coordination", "Develops new skills", "Supports early gains", "Enables lasting change", "Optimizes control"],
        "applications": ["Skill development", "Rehabilitation", "Performance enhancement", "Postural training", "Movement optimization", "Learning efficiency"],
        "related_terms": [("neuroplasticity", "Neuroplasticity"), ("motor-learning", "Motor Learning"), ("brain-plasticity", "Brain Plasticity"), ("skill-acquisition", "Skill Acquisition")],
        "connections": [("neuromuscular-control", "Neuromuscular Control"), ("practice-principles", "Practice Principles"), ("motor-unit", "Motor Unit"), ("coordination", "Coordination")]
    },
    "habit-formation": {
        "title": "Habit Formation",
        "simple_desc": "How repeated actions become automatic behaviors that you do without thinking.",
        "detailed_desc": """<p>Habit formation is the neurological process by which behaviors become automatic through repetition. Once a habit is established, it requires less conscious effort and becomes a default pattern.</p>
<p>ELDOA practice aims to create positive postural and movement habits. Through consistent practice, the awareness and positioning developed during ELDOA sessions gradually become automatic aspects of daily posture and movement.</p>
<p>Understanding habit formation helps optimize ELDOA practice. Regular practice at consistent times, in consistent environments, helps establish the neural pathways that support lasting behavioral change and improved movement habits.</p>""",
        "benefits": ["Creates lasting change", "Reduces conscious effort", "Supports daily posture", "Improves consistency", "Builds positive patterns", "Enhances sustainability"],
        "applications": ["Postural improvement", "Movement re-education", "Self-care establishment", "Practice consistency", "Behavioral change", "Long-term health"],
        "related_terms": [("neuroplasticity", "Neuroplasticity"), ("motor-learning", "Motor Learning"), ("neural-adaptation", "Neural Adaptation"), ("practice-principles", "Practice Principles")],
        "connections": [("brain-plasticity", "Brain Plasticity"), ("postural-awareness", "Postural Awareness"), ("daily-practice", "Daily Practice"), ("behavior-change", "Behavior Change")]
    },
    "motor-cortex": {
        "title": "Motor Cortex",
        "simple_desc": "The part of your brain that plans and controls all your voluntary movements.",
        "detailed_desc": """<p>The motor cortex is the region of the cerebral cortex responsible for planning, controlling, and executing voluntary movements. It includes the primary motor cortex, premotor cortex, and supplementary motor area, each with specific roles in movement control.</p>
<p>ELDOA practice engages the motor cortex extensively through the precise voluntary positioning required. The sustained holds and subtle adjustments demand continuous motor cortex activity, driving neural plasticity in movement control regions.</p>
<p>Regular ELDOA practice is thought to expand motor cortex representation for postural control muscles, improving the brain's capacity to precisely control spinal positioning. This neural change contributes to lasting improvements in posture and movement.</p>""",
        "benefits": ["Improves movement control", "Enhances precision", "Supports skill development", "Develops coordination", "Enables complex movement", "Drives plasticity"],
        "applications": ["Movement training", "Rehabilitation", "Skill acquisition", "Coordination development", "Performance enhancement", "Neural rehabilitation"],
        "related_terms": [("brain-plasticity", "Brain Plasticity"), ("motor-learning", "Motor Learning"), ("neural-adaptation", "Neural Adaptation"), ("movement-control", "Movement Control")],
        "connections": [("neuromuscular-control", "Neuromuscular Control"), ("voluntary-movement", "Voluntary Movement"), ("body-schema", "Body Schema"), ("cortical-representation", "Cortical Representation")]
    },
    "body-schema": {
        "title": "Body Schema",
        "simple_desc": "Your brain's internal map of your body that helps you know where all your parts are.",
        "detailed_desc": """<p>Body schema is the brain's internal representation of the body's position, configuration, and capabilities. This neural map is constantly updated based on sensory input and is essential for coordinated movement and spatial awareness.</p>
<p>ELDOA practice refines and enhances the body schema through heightened proprioceptive input during precise positioning. The detailed awareness required for ELDOA positions provides rich sensory information that improves the accuracy of the body's neural representation.</p>
<p>An enhanced body schema from ELDOA practice transfers to daily activities, improving posture, movement efficiency, and body awareness throughout the day. This represents one of the key neurological benefits of consistent practice.</p>""",
        "benefits": ["Improves body awareness", "Enhances spatial sense", "Supports coordination", "Refines movement control", "Develops proprioception", "Enables precise movement"],
        "applications": ["Movement training", "Rehabilitation", "Body awareness development", "Postural improvement", "Performance enhancement", "Skill acquisition"],
        "related_terms": [("proprioception", "Proprioception"), ("kinesthesia", "Kinesthesia"), ("body-awareness", "Body Awareness"), ("spatial-awareness", "Spatial Awareness")],
        "connections": [("motor-cortex", "Motor Cortex"), ("brain-plasticity", "Brain Plasticity"), ("sensory-integration", "Sensory Integration"), ("movement-patterns", "Movement Patterns")]
    },
    "movement-patterns": {
        "title": "Movement Patterns",
        "simple_desc": "The typical ways your body moves to do different activities, which can be good or compensatory.",
        "detailed_desc": """<p>Movement patterns are the habitual ways the body organizes movement to accomplish tasks. These patterns can be efficient and health-promoting or dysfunctional and contributing to pain and injury.</p>
<p>ELDOA addresses movement patterns by improving the underlying tissue quality and neural control that influence how we move. As spinal mobility improves and body awareness develops, movement patterns naturally become more efficient and balanced.</p>
<p>Dysfunctional movement patterns often develop as compensations for pain, stiffness, or weakness. ELDOA addresses these root causes, allowing the body to adopt more optimal patterns once restrictions are resolved.</p>""",
        "benefits": ["Improves movement quality", "Reduces compensation", "Enhances efficiency", "Prevents injury", "Supports performance", "Addresses root causes"],
        "applications": ["Movement assessment", "Rehabilitation", "Performance optimization", "Injury prevention", "Postural correction", "Pain management"],
        "related_terms": [("motor-learning", "Motor Learning"), ("functional-anatomy", "Functional Anatomy"), ("compensatory-patterns", "Compensatory Patterns"), ("movement-assessment", "Movement Assessment")],
        "connections": [("neuromuscular-control", "Neuromuscular Control"), ("body-schema", "Body Schema"), ("biomechanics", "Biomechanics"), ("postural-habits", "Postural Habits")]
    },
    "pain-neuroscience": {
        "title": "Pain Neuroscience",
        "simple_desc": "Understanding how your brain creates and processes pain, not just where it hurts.",
        "detailed_desc": """<p>Pain neuroscience is the study of how the nervous system generates and modulates pain experiences. Modern pain science recognizes that pain is a brain-generated protective response, not simply a direct readout of tissue damage.</p>
<p>ELDOA interacts with pain neuroscience through multiple mechanisms: reducing tissue stress through decompression, providing positive sensory input that can modulate pain processing, and improving body awareness that changes the relationship with painful areas.</p>
<p>Understanding pain neuroscience helps explain why ELDOA can reduce pain even when structural changes are not immediately apparent. The neurological effects of practice—improved proprioception, reduced threat perception, enhanced body control—all contribute to pain modulation.</p>""",
        "benefits": ["Explains pain mechanisms", "Guides treatment approach", "Reduces fear-avoidance", "Supports pain education", "Improves outcomes", "Enhances understanding"],
        "applications": ["Chronic pain management", "Patient education", "Treatment planning", "Fear reduction", "Rehabilitation design", "Self-management"],
        "related_terms": [("chronic-pain", "Chronic Pain"), ("neuroplasticity", "Neuroplasticity"), ("central-sensitization", "Central Sensitization"), ("pain-management", "Pain Management")],
        "connections": [("brain-plasticity", "Brain Plasticity"), ("body-awareness", "Body Awareness"), ("threat-perception", "Threat Perception"), ("sensory-input", "Sensory Input")]
    },
    "lower-back-pain": {
        "title": "Lower Back Pain",
        "simple_desc": "Pain in the bottom part of your spine, one of the most common reasons people see a doctor.",
        "detailed_desc": """<p>Lower back pain (LBP) is pain occurring in the lumbar region of the spine, affecting up to 80% of adults at some point. It is one of the leading causes of disability worldwide and a primary reason for seeking ELDOA treatment.</p>
<p>ELDOA addresses lower back pain through targeted decompression of lumbar segments, typically L4-L5 and L5-S1. By creating space within these segments, ELDOA reduces disc pressure, improves facet joint mechanics, and decreases neural compression.</p>
<p>The effectiveness of ELDOA for lower back pain extends beyond local effects. By addressing the fascial system and improving postural awareness, ELDOA treats contributing factors that perpetuate pain, leading to more sustainable improvement than symptomatic treatments alone.</p>""",
        "benefits": ["Reduces lumbar compression", "Improves disc health", "Decreases nerve irritation", "Addresses root causes", "Supports long-term relief", "Enhances function"],
        "applications": ["Acute back pain", "Chronic back pain", "Disc conditions", "Facet syndrome", "Prevention", "Post-surgical care"],
        "related_terms": [("lumbar-spine", "Lumbar Spine"), ("back-pain", "Back Pain"), ("disc-herniation", "Disc Herniation"), ("sciatica", "Sciatica")],
        "connections": [("l5-s1-decompression", "L5 S1 Decompression"), ("l4-l5-segment", "L4 L5 Segment"), ("tissue-healing", "Tissue Healing"), ("posture", "Posture")]
    },
    "disc-herniation": {
        "title": "Disc Herniation",
        "simple_desc": "When the soft center of a spinal disc pushes through its outer layer, sometimes pressing on nerves.",
        "detailed_desc": """<p>Disc herniation occurs when the nucleus pulposus (inner disc material) protrudes through tears in the annulus fibrosus (outer disc layer). This can cause local pain and, if neural structures are compressed, radiating symptoms like sciatica.</p>
<p>ELDOA addresses disc herniation through decompression that reduces intradiscal pressure, potentially reducing herniation pressure on neural structures. The positioning also promotes disc hydration and may support the natural resorption process that often occurs with herniations.</p>
<p>While not all herniations respond to conservative care, many can be successfully managed with ELDOA and related approaches. The key is addressing contributing factors—poor posture, muscle imbalances, and repetitive loading patterns—while optimizing the environment for healing.</p>""",
        "benefits": ["Reduces disc pressure", "Decreases nerve compression", "Supports healing", "Improves hydration", "Addresses contributing factors", "Prevents recurrence"],
        "applications": ["Herniation management", "Sciatica treatment", "Non-surgical care", "Prevention", "Post-surgical rehabilitation", "Long-term maintenance"],
        "related_terms": [("intervertebral-disc", "Intervertebral Disc"), ("sciatica", "Sciatica"), ("lumbar-spine", "Lumbar Spine"), ("nerve-root", "Nerve Root")],
        "connections": [("spinal-decompression", "Spinal Decompression"), ("disc-hydration", "Disc Hydration"), ("l5-s1-decompression", "L5 S1 Decompression"), ("annulus-fibrosus", "Annulus Fibrosus")]
    },
    "sciatica": {
        "title": "Sciatica",
        "simple_desc": "Pain that travels down your leg from your lower back, following the path of the sciatic nerve.",
        "detailed_desc": """<p>Sciatica refers to pain radiating along the sciatic nerve pathway, typically from the lower back through the buttock and down the posterior thigh. It results from compression or irritation of the lumbar nerve roots that form the sciatic nerve, commonly L4, L5, or S1.</p>
<p>ELDOA addresses sciatica by creating space at the lumbar segments where nerve root compression typically occurs. L5-S1 and L4-L5 ELDOA positions are particularly valuable for reducing pressure on the neural structures involved in sciatica.</p>
<p>Beyond local decompression, ELDOA addresses sciatica by improving posterior chain mobility. Tension in the piriformis, hamstrings, and other posterior structures can contribute to sciatic symptoms, and ELDOA's whole-system approach addresses these factors.</p>""",
        "benefits": ["Reduces nerve compression", "Decreases radiating pain", "Improves lumbar space", "Addresses contributing factors", "Supports nerve healing", "Enhances function"],
        "applications": ["Sciatic pain relief", "Disc-related sciatica", "Piriformis syndrome", "Lumbar radiculopathy", "Non-surgical management", "Prevention"],
        "related_terms": [("lumbar-spine", "Lumbar Spine"), ("disc-herniation", "Disc Herniation"), ("nerve-root", "Nerve Root"), ("piriformis-syndrome", "Piriformis Syndrome")],
        "connections": [("l5-s1-decompression", "L5 S1 Decompression"), ("posterior-chain", "Posterior Chain"), ("neural-tension", "Neural Tension"), ("lower-back-pain", "Lower Back Pain")]
    },
    "spinal-stenosis": {
        "title": "Spinal Stenosis",
        "simple_desc": "Narrowing of the spaces in your spine that can put pressure on nerves, often causing leg pain with walking.",
        "detailed_desc": """<p>Spinal stenosis is narrowing of the spinal canal or neural foramina, resulting in compression of neural structures. It commonly develops with age due to disc degeneration, facet hypertrophy, and ligament thickening.</p>
<p>ELDOA can benefit spinal stenosis by creating temporary space within affected segments and improving overall spinal mechanics. While structural narrowing cannot be reversed, optimizing the remaining space and reducing dynamic compression can significantly improve symptoms.</p>
<p>Lumbar stenosis typically causes neurogenic claudication—leg symptoms that worsen with walking and improve with sitting or forward bending. ELDOA positions that promote lumbar flexion may provide particular benefit by opening the neural foramina.</p>""",
        "benefits": ["Creates temporary space", "Reduces nerve compression", "Improves function", "Addresses contributing factors", "Enhances mobility", "Supports quality of life"],
        "applications": ["Stenosis management", "Walking tolerance", "Symptom relief", "Functional improvement", "Conservative care", "Post-surgical maintenance"],
        "related_terms": [("lumbar-spine", "Lumbar Spine"), ("neural-foramen", "Neural Foramen"), ("spinal-degeneration", "Spinal Degeneration"), ("sciatica", "Sciatica")],
        "connections": [("spinal-decompression", "Spinal Decompression"), ("facet-joints", "Facet Joints"), ("intervertebral-space", "Intervertebral Space"), ("nerve-root", "Nerve Root")]
    },
    "spondylolisthesis": {
        "title": "Spondylolisthesis",
        "simple_desc": "When one vertebra slips forward over the one below it, which can cause back pain and stiffness.",
        "detailed_desc": """<p>Spondylolisthesis is anterior displacement of one vertebra relative to the one below. It can result from developmental defects (isthmic), degeneration (degenerative), or other causes. The L5-S1 and L4-L5 levels are most commonly affected.</p>
<p>ELDOA requires careful consideration in spondylolisthesis cases. While decompression can benefit the condition by reducing segmental compression, positioning must avoid promoting further slippage. Modified approaches and professional guidance are recommended.</p>
<p>Stable, mild spondylolisthesis often responds well to conservative care including ELDOA. The focus is on improving core stability, reducing segmental stress, and optimizing mechanics while respecting the underlying instability.</p>""",
        "benefits": ["Reduces segmental compression", "Improves stability", "Addresses contributing factors", "Supports function", "Manages symptoms", "Prevents progression"],
        "applications": ["Spondylolisthesis management", "Stability training", "Pain reduction", "Functional improvement", "Conservative care", "Preventive maintenance"],
        "related_terms": [("lumbar-spine", "Lumbar Spine"), ("l5-s1-junction", "L5 S1 Junction"), ("spinal-instability", "Spinal Instability"), ("core-stability", "Core Stability")],
        "connections": [("vertebral-segment", "Vertebral Segment"), ("facet-joints", "Facet Joints"), ("segmental-stability", "Segmental Stability"), ("lower-back-pain", "Lower Back Pain")]
    },
    "lumbosacral-angle": {
        "title": "Lumbosacral Angle",
        "simple_desc": "The angle where your lower spine meets your pelvis, which affects how your back curves.",
        "detailed_desc": """<p>The lumbosacral angle is the angle between the top surface of the sacrum and the horizontal plane, typically measuring 30-40 degrees. This angle significantly influences lumbar lordosis and load distribution through the lower spine.</p>
<p>An increased lumbosacral angle creates greater shear stress at L5-S1, potentially contributing to disc and facet pathology. ELDOA addresses this by creating space at the lumbosacral junction and improving the muscular control that influences pelvic positioning.</p>
<p>Understanding lumbosacral angle helps explain individual variations in response to ELDOA and guides appropriate position selection. Those with increased angles may particularly benefit from L5-S1 decompression approaches.</p>""",
        "benefits": ["Addresses L5-S1 stress", "Improves load distribution", "Guides treatment selection", "Supports pelvic alignment", "Reduces shear forces", "Optimizes mechanics"],
        "applications": ["Lumbar assessment", "Treatment planning", "L5-S1 conditions", "Postural analysis", "Individual prescription", "Mechanical optimization"],
        "related_terms": [("l5-s1-junction", "L5 S1 Junction"), ("lumbar-lordosis", "Lumbar Lordosis"), ("pelvic-tilt", "Pelvic Tilt"), ("sacrum", "Sacrum")],
        "connections": [("biomechanics", "Biomechanics"), ("spinal-mechanics", "Spinal Mechanics"), ("disc-loading", "Disc Loading"), ("postural-assessment", "Postural Assessment")]
    },
    "psoas-muscle": {
        "title": "Psoas Muscle",
        "simple_desc": "A deep hip flexor muscle that connects your spine to your leg and affects your posture and movement.",
        "detailed_desc": """<p>The psoas major is a deep muscle originating from the lumbar vertebrae (T12-L5) and inserting on the lesser trochanter of the femur. It is the only muscle directly connecting the spine to the lower extremity and plays crucial roles in hip flexion, spinal stability, and posture.</p>
<p>In ELDOA methodology, the psoas is recognized as a key structure affecting lumbar spine health. Psoas dysfunction—whether tightness, weakness, or poor coordination—can significantly impact lumbar mechanics and contribute to lower back pain.</p>
<p>ELDOA positions that address the lumbar spine inherently affect the psoas through its vertebral attachments. Additionally, the Deep Front Line, a fascial chain including the psoas, is engaged through lumbar ELDOA positions, creating comprehensive effects on this important muscle.</p>""",
        "benefits": ["Addresses hip-spine connection", "Improves hip flexion", "Supports lumbar stability", "Reduces back pain", "Enhances posture", "Optimizes movement"],
        "applications": ["Lower back pain", "Hip mobility", "Postural correction", "Athletic performance", "Sitting-related issues", "Core integration"],
        "related_terms": [("deep-front-line", "Deep Front Line"), ("lumbar-spine", "Lumbar Spine"), ("hip-flexor", "Hip Flexor"), ("core-stability", "Core Stability")],
        "connections": [("l5-s1-junction", "L5 S1 Junction"), ("pelvic-mechanics", "Pelvic Mechanics"), ("diaphragm", "Diaphragm"), ("fascial-chains", "Fascial Chains")]
    },
    "cervicogenic-headache": {
        "title": "Cervicogenic Headache",
        "simple_desc": "A headache that starts from problems in your neck, often felt on one side of your head.",
        "detailed_desc": """<p>Cervicogenic headache is head pain originating from structures in the cervical spine, particularly the upper cervical segments (C1-C3). It typically presents as unilateral headache that may be triggered by neck movement or sustained postures.</p>
<p>ELDOA addresses cervicogenic headache through cervical spine decompression, particularly targeting the upper cervical segments. By creating space and improving mobility at C1-C2 and C2-C3, ELDOA can reduce the cervical dysfunction driving headache symptoms.</p>
<p>The relationship between neck mechanics and headache makes comprehensive cervical ELDOA practice valuable. Addressing the entire cervical chain, not just symptomatic levels, helps resolve contributing factors and prevent recurrence.</p>""",
        "benefits": ["Addresses neck-headache connection", "Reduces cervical dysfunction", "Improves cervical mobility", "Decreases headache frequency", "Treats root cause", "Supports long-term relief"],
        "applications": ["Headache treatment", "Neck pain relief", "Upper cervical dysfunction", "Tension headache", "Post-whiplash care", "Prevention"],
        "related_terms": [("cervical-spine", "Cervical Spine"), ("neck-pain", "Neck Pain"), ("c1-atlas", "C1 Atlas"), ("c2-axis", "C2 Axis")],
        "connections": [("upper-cervical", "Upper Cervical"), ("forward-head-posture", "Forward Head Posture"), ("suboccipital-muscles", "Suboccipital Muscles"), ("referred-pain", "Referred Pain")]
    },
    "c1-atlas": {
        "title": "C1 Atlas",
        "simple_desc": "The topmost bone in your spine that your skull sits on, named after the Greek Titan who held up the world.",
        "detailed_desc": """<p>The atlas (C1) is the first cervical vertebra, uniquely adapted to support the skull and allow nodding movements. Unlike other vertebrae, it lacks a vertebral body and spinous process, consisting primarily of two lateral masses connected by anterior and posterior arches.</p>
<p>The atlanto-occipital joint (skull-C1) primarily allows flexion and extension, contributing significantly to the ability to look up and down. In ELDOA methodology, this junction requires specific attention due to its unique mechanics and importance for overall cervical function.</p>
<p>Dysfunction at C1 can contribute to headaches, upper cervical pain, and balance issues due to the density of proprioceptors in this region. ELDOA approaches the upper cervical region with particular care, using positions that create space without excessive force.</p>""",
        "benefits": ["Addresses upper cervical function", "Improves head mobility", "Reduces cervical pain", "Supports balance", "Treats headaches", "Optimizes cervical mechanics"],
        "applications": ["Upper cervical dysfunction", "Headache treatment", "Neck pain relief", "Balance issues", "Post-whiplash care", "Cervical optimization"],
        "related_terms": [("cervical-spine", "Cervical Spine"), ("c2-axis", "C2 Axis"), ("atlanto-occipital", "Atlanto Occipital"), ("upper-cervical", "Upper Cervical")],
        "connections": [("cervicogenic-headache", "Cervicogenic Headache"), ("skull-base", "Skull Base"), ("vertebral-segment", "Vertebral Segment"), ("neck-mobility", "Neck Mobility")]
    },
    "c2-axis": {
        "title": "C2 Axis",
        "simple_desc": "The second bone in your neck with a special peg that lets you turn your head side to side.",
        "detailed_desc": """<p>The axis (C2) is the second cervical vertebra, distinguished by the dens (odontoid process), a bony projection that extends upward into the atlas. This structure creates a pivot point allowing approximately 50% of cervical rotation to occur at the atlanto-axial joint.</p>
<p>The C1-C2 relationship is critical for head rotation and upper cervical stability. ELDOA recognizes the importance of this junction and includes specific approaches for creating space and optimizing mechanics at this level.</p>
<p>Dysfunction at C2, whether from injury, degeneration, or postural stress, can significantly impact cervical rotation, contribute to headaches, and affect overall neck function. ELDOA provides a non-invasive approach to improving C2 mechanics.</p>""",
        "benefits": ["Improves cervical rotation", "Addresses C1-C2 function", "Reduces upper cervical pain", "Supports head turning", "Treats headaches", "Optimizes neck mechanics"],
        "applications": ["Rotation restriction", "Upper cervical pain", "Headache treatment", "Neck stiffness", "Post-injury care", "Cervical optimization"],
        "related_terms": [("cervical-spine", "Cervical Spine"), ("c1-atlas", "C1 Atlas"), ("atlanto-axial", "Atlanto Axial"), ("dens", "Dens")],
        "connections": [("cervical-rotation", "Cervical Rotation"), ("cervicogenic-headache", "Cervicogenic Headache"), ("vertebral-segment", "Vertebral Segment"), ("upper-cervical", "Upper Cervical")]
    },
    "c7-t1-junction": {
        "title": "C7 T1 Junction",
        "simple_desc": "Where your neck meets your upper back, a transition point that often gets stiff from computer work.",
        "detailed_desc": """<p>The cervicothoracic junction (C7-T1) is the transition between the mobile cervical spine and the more stable thoracic spine. This region commonly develops dysfunction due to its transitional nature and the postural stresses of modern life.</p>
<p>ELDOA addresses the C7-T1 junction through positions that create space at this transitional level. The prominence of C7 (vertebra prominens) and the first rib attachments at T1 create unique mechanical considerations that ELDOA positioning accounts for.</p>
<p>Dysfunction at C7-T1 can contribute to neck pain, shoulder issues, and upper extremity symptoms due to the brachial plexus proximity. ELDOA provides targeted decompression that can address these interconnected problems.</p>""",
        "benefits": ["Addresses transition zone", "Improves cervicothoracic mobility", "Reduces neck-shoulder pain", "Optimizes junction mechanics", "Supports upper extremity", "Treats postural dysfunction"],
        "applications": ["Cervicothoracic pain", "Neck stiffness", "Shoulder issues", "Computer-related problems", "Postural correction", "Upper body optimization"],
        "related_terms": [("cervical-spine", "Cervical Spine"), ("thoracic-spine", "Thoracic Spine"), ("transition-zone", "Transition Zone"), ("upper-back-pain", "Upper Back Pain")],
        "connections": [("first-rib", "First Rib"), ("brachial-plexus", "Brachial Plexus"), ("forward-head-posture", "Forward Head Posture"), ("vertebral-segment", "Vertebral Segment")]
    },
    "tissue-remodeling": {
        "title": "Tissue Remodeling",
        "simple_desc": "How your body rebuilds and reorganizes tissues to become stronger and better organized.",
        "detailed_desc": """<p>Tissue remodeling is the biological process by which tissues adapt their structure and composition in response to mechanical demands. This process involves the breakdown of existing tissue components and synthesis of new ones, optimizing tissue architecture for function.</p>
<p>ELDOA promotes positive tissue remodeling through mechanotransduction—the sustained loading during ELDOA positions signals fibroblasts and other cells to produce and organize collagen and extracellular matrix components.</p>
<p>The 60-second holds characteristic of ELDOA are specifically designed to optimize the remodeling stimulus. This duration allows sufficient time for cellular signaling cascades to activate, promoting lasting tissue adaptations rather than temporary changes.</p>""",
        "benefits": ["Improves tissue quality", "Optimizes tissue structure", "Promotes adaptation", "Enhances function", "Supports healing", "Creates lasting change"],
        "applications": ["Tissue optimization", "Injury recovery", "Chronic conditions", "Performance enhancement", "Anti-aging", "Fascial training"],
        "related_terms": [("mechanotransduction", "Mechanotransduction"), ("tissue-healing", "Tissue Healing"), ("collagen", "Collagen"), ("fascial-system", "Fascial System")],
        "connections": [("eccentric-loading", "Eccentric Loading"), ("sustained-holds", "Sustained Holds"), ("fibroblasts", "Fibroblasts"), ("cellular-response", "Cellular Response")]
    }
}


def generate_html_page(slug, data):
    """Generate HTML page content for an encyclopedia entry."""
    title = data["title"]
    simple_desc = data["simple_desc"]
    detailed_desc = data["detailed_desc"]

    # Generate related terms HTML
    related_html = ""
    for rel_slug, rel_title in data.get("related_terms", []):
        related_html += f'<li><a href="/encyclopedia/{rel_slug}.html">{rel_title}</a></li>'

    # Generate connections HTML
    connections_html = ""
    for conn_slug, conn_title in data.get("connections", []):
        connections_html += f'<li><a href="/encyclopedia/{conn_slug}.html">{conn_title}</a></li>'

    # Generate benefits list
    benefits_html = ""
    for benefit in data.get("benefits", []):
        benefits_html += f"<li>{benefit}</li>"

    # Generate applications list
    applications_html = ""
    for app in data.get("applications", []):
        applications_html += f"<li>{app}</li>"

    html = f'''<!DOCTYPE html>

<html lang="en">
<head> <meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<!-- Primary Meta Tags -->
<title>{title} – ELDOA Encyclopedia</title>
<meta content="{title} – ELDOA Encyclopedia" name="title"/>
<meta content="{simple_desc}" name="description"/>
<meta content="ELDOA, {title}, Guy Voyer, fascia, spinal decompression" name="keywords"/>
<meta content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" name="robots"/>
<!-- Canonical URL -->
<link href="https://eldoa.ai/encyclopedia/{slug}" rel="canonical"/>
<!-- Open Graph / Facebook -->
<meta content="article" property="og:type"/>
<meta content="https://eldoa.ai/encyclopedia/{slug}" property="og:url"/>
<meta content="{title} – ELDOA Encyclopedia" property="og:title"/>
<meta content="{simple_desc}" property="og:description"/>
<meta content="https://eldoa.ai/images/og-encyclopedia.jpg" property="og:image"/>
<meta content="ELDOA AI" property="og:site_name"/>
<!-- Twitter -->
<meta content="summary_large_image" name="twitter:card"/>
<meta content="https://eldoa.ai/encyclopedia/{slug}" name="twitter:url"/>
<meta content="{title} – ELDOA Encyclopedia" name="twitter:title"/>
<meta content="{simple_desc}" name="twitter:description"/>
<meta content="https://eldoa.ai/images/og-encyclopedia.jpg" name="twitter:image"/>
<!-- Favicon -->
<link href="/favicon.png" rel="icon" type="image/png"/>
<link href="/apple-touch-icon.png" rel="apple-touch-icon"/>
<!-- Theme Color -->
<meta content="#1a1a1a" name="theme-color"/>
<meta content="#ffffff" media="(prefers-color-scheme: light)" name="theme-color"/>
<meta content="#1a1a1a" media="(prefers-color-scheme: dark)" name="theme-color"/>
<!-- Schema.org Structured Data -->
<script type="application/ld+json">
{{
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": "{title}",
        "description": "{simple_desc}",
        "inDefinedTermSet": {{
                "@type": "DefinedTermSet",
                "name": "ELDOA AI Encyclopedia",
                "url": "https://eldoa.ai/encyclopedia/"
        }},
        "url": "https://eldoa.ai/encyclopedia/{slug}"
}}
    </script>
<!-- Breadcrumb Schema -->
<script type="application/ld+json">
{{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
                {{
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://eldoa.ai/"
                }},
                {{
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Encyclopedia",
                        "item": "https://eldoa.ai/encyclopedia/"
                }},
                {{
                        "@type": "ListItem",
                        "position": 3,
                        "name": "{title}",
                        "item": "https://eldoa.ai/encyclopedia/{slug}"
                }}
        ]
}}
    </script>
<style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #0d0f13;
            background-color: #f5f5f5;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background-color: white;
            min-height: 100vh;
        }}

        .header {{
            margin-bottom: 2rem;
        }}

        .eldoa-logo {{
            font-size: 2.5rem;
            font-weight: 900;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .eldoa-logo .eldoa {{
            color: #0d0f13;
        }}

        .eldoa-logo .ai {{
            background: linear-gradient(90deg, #2f2fe6, #0891b2);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}

        .eldoa-underline {{
            width: 150px;
            height: 4px;
            background: linear-gradient(90deg, #2f2fe6, #0891b2);
            margin-bottom: 2rem;
        }}

        .entry-title {{
            font-size: 2rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 1.5rem;
        }}

        .entry-content {{
            font-size: 1.125rem;
            line-height: 1.8;
            color: #333;
        }}

        .entry-content p {{
            margin-bottom: 1rem;
        }}

        mark {{
            background-color: #fef08a;
            padding: 0.125rem 0.25rem;
        }}

        .back-link {{
            display: inline-block;
            margin-top: 2rem;
            color: #2f2fe6;
            text-decoration: none;
            font-weight: 600;
        }}

        .back-link:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            .eldoa-logo {{
                font-size: 2rem;
            }}

            .entry-title {{
                font-size: 1.5rem;
            }}

            .entry-content {{
                font-size: 1rem;
            }}
        }}


        .content-section {{
            margin-bottom: 2.5rem;
        }}

        .content-section h2 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #2f2fe6;
        }}

        .related-terms, .connections {{
            background-color: #f9fafb;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 2rem;
        }}

        .related-list, .connections-list {{
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 0.75rem;
            margin-top: 1rem;
        }}

        .related-list li, .connections-list li {{
            margin: 0;
        }}

        .related-list a, .connections-list a {{
            color: #2f2fe6;
            text-decoration: none;
            font-weight: 500;
            display: block;
            padding: 0.5rem;
            background-color: white;
            border-radius: 4px;
            transition: all 0.2s;
        }}

        .related-list a:hover, .connections-list a:hover {{
            background-color: #2f2fe6;
            color: white;
            transform: translateX(4px);
        }}

        @media (max-width: 768px) {{
            .related-list, .connections-list {{
                grid-template-columns: 1fr;
            }}
        }}


        .content-section h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #2f2fe6;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }}

        .content-section ul,
        .content-section ol {{
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }}

        .content-section li {{
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }}

        .content-section ul li {{
            list-style-type: disc;
        }}

        .content-section ol li {{
            list-style-type: decimal;
        }}
</style></head>
<body>
<div class="container">
<div class="header">
<div class="eldoa-logo">
<span class="eldoa">ELDOA</span> <span class="ai">AI</span>
</div>
<div class="eldoa-underline"></div>
</div>
<h1 class="entry-title">{title}</h1>
<div class="entry-content"><div class="content-section"><h2>Overview</h2><p><mark>{simple_desc}</mark></p></div><div class="content-section"><h2>Detailed Description</h2>{detailed_desc}</div><div class="content-section"><h3>Key Benefits</h3><ul>{benefits_html}</ul><h3>Practical Applications</h3><ul>{applications_html}</ul></div><div class="content-section related-terms"><h2>Related Terms</h2><ul class="related-list">{related_html}</ul></div><div class="content-section connections"><h2>Key Connections</h2><ul class="connections-list">{connections_html}</ul></div></div>
<a class="back-link" href="/encyclopedia.html">← Back to Encyclopedia</a>
</div>
</body>
</html>'''

    return html


def create_all_missing_pages():
    """Create all missing encyclopedia pages."""
    created = []
    for slug, data in MISSING_PAGES.items():
        filepath = ENCYCLOPEDIA_DIR / f"{slug}.html"
        if not filepath.exists():
            html = generate_html_page(slug, data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            created.append(slug)
            print(f"Created: {slug}.html")
        else:
            print(f"Already exists: {slug}.html")
    return created


if __name__ == "__main__":
    print("Creating missing encyclopedia pages...")
    created = create_all_missing_pages()
    print(f"\nCreated {len(created)} new pages")
