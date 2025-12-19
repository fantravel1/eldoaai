#!/usr/bin/env python3
"""
Script to create missing encyclopedia pages - Batch 2.
"""

import os
from pathlib import Path

ENCYCLOPEDIA_DIR = Path("/home/user/eldoaai/encyclopedia")

# Define content for each missing page
MISSING_PAGES = {
    "nerve-root": {
        "title": "Nerve Root",
        "simple_desc": "The beginning part of a nerve where it branches off from the spinal cord.",
        "detailed_desc": """<p>Nerve roots are the initial segments of spinal nerves as they exit the spinal cord through the neural foramina. Each nerve root carries motor, sensory, and autonomic fibers that will eventually innervate specific body regions in characteristic patterns called dermatomes and myotomes.</p>
<p>ELDOA directly benefits nerve roots by creating space within the neural foramina—the bony channels through which nerve roots pass. When these spaces narrow due to disc degeneration, facet hypertrophy, or other conditions, nerve roots can become compressed, causing pain, weakness, and sensory changes.</p>
<p>Understanding nerve root anatomy helps explain the radiating symptoms common in spinal conditions. L5 nerve root compression, for example, typically causes pain and weakness along the outer leg and top of the foot, while S1 compression affects the back of the leg and sole of the foot.</p>""",
        "benefits": ["Reduces nerve compression", "Increases neural space", "Relieves radiating pain", "Improves nerve function", "Addresses radiculopathy", "Supports nerve healing"],
        "applications": ["Sciatica treatment", "Radiculopathy management", "Disc herniation care", "Stenosis treatment", "Pain relief", "Functional restoration"],
        "related_terms": [("sciatica", "Sciatica"), ("disc-herniation", "Disc Herniation"), ("spinal-stenosis", "Spinal Stenosis"), ("neural-tension", "Neural Tension")],
        "connections": [("intervertebral-space", "Intervertebral Space"), ("facet-joints", "Facet Joints"), ("spinal-decompression", "Spinal Decompression"), ("vertebral-segment", "Vertebral Segment")]
    },
    "collagen": {
        "title": "Collagen",
        "simple_desc": "The main protein that gives strength and structure to your skin, bones, tendons, and fascia.",
        "detailed_desc": """<p>Collagen is the most abundant protein in the human body, providing structural support to connective tissues including skin, tendons, ligaments, fascia, and bone. Different collagen types have specific properties suited to their tissue locations.</p>
<p>ELDOA promotes collagen synthesis and organization through mechanotransduction. The sustained loading during ELDOA positions signals fibroblasts to produce new collagen and organize existing fibers along lines of force, improving tissue strength and resilience.</p>
<p>Collagen quality and organization significantly impact tissue function. Well-organized collagen provides strength and flexibility, while disorganized collagen (as seen in scar tissue) may limit function. ELDOA's mechanical input helps optimize collagen architecture.</p>""",
        "benefits": ["Stimulates collagen synthesis", "Improves tissue strength", "Enhances tissue quality", "Supports healing", "Optimizes fiber alignment", "Promotes tissue health"],
        "applications": ["Tissue rehabilitation", "Injury recovery", "Anti-aging protocols", "Tendon health", "Fascial optimization", "Connective tissue care"],
        "related_terms": [("connective-tissue", "Connective Tissue"), ("tissue-healing", "Tissue Healing"), ("fascial-system", "Fascial System"), ("mechanotransduction", "Mechanotransduction")],
        "connections": [("tissue-remodeling", "Tissue Remodeling"), ("tendon-healing", "Tendon Healing"), ("fibroblasts", "Fibroblasts"), ("extracellular-matrix", "Extracellular Matrix")]
    },
    "neural-foramen": {
        "title": "Neural Foramen",
        "simple_desc": "The opening in your spine where nerves exit to go to different parts of your body.",
        "detailed_desc": """<p>The neural foramen (intervertebral foramen) is the bony opening between adjacent vertebrae through which spinal nerve roots exit the spinal canal. The size of this foramen is influenced by disc height, facet joint position, and ligament thickness.</p>
<p>ELDOA targets neural foraminal space by creating intervertebral decompression. When disc height is increased and facet joints are separated through ELDOA positioning, the neural foramen opens, reducing pressure on the exiting nerve roots.</p>
<p>Foraminal stenosis—narrowing of the neural foramen—is a common cause of radicular symptoms. ELDOA provides a non-invasive approach to temporarily increasing foraminal space and improving neural function.</p>""",
        "benefits": ["Increases foraminal space", "Reduces nerve compression", "Relieves radicular symptoms", "Improves nerve function", "Addresses stenosis", "Supports neural health"],
        "applications": ["Foraminal stenosis", "Radiculopathy treatment", "Nerve pain relief", "Spinal degeneration", "Conservative management", "Prevention"],
        "related_terms": [("nerve-root", "Nerve Root"), ("spinal-stenosis", "Spinal Stenosis"), ("intervertebral-space", "Intervertebral Space"), ("vertebral-segment", "Vertebral Segment")],
        "connections": [("spinal-decompression", "Spinal Decompression"), ("disc-hydration", "Disc Hydration"), ("facet-joints", "Facet Joints"), ("sciatica", "Sciatica")]
    },
    "upper-cervical": {
        "title": "Upper Cervical",
        "simple_desc": "The top part of your neck including the first two vertebrae that support your head.",
        "detailed_desc": """<p>The upper cervical region consists of the atlas (C1), axis (C2), and their joints with the occiput and C3. This region has unique anatomy and mechanics, providing the majority of cervical rotation and significant flexion/extension.</p>
<p>ELDOA approaches the upper cervical region with particular care due to its unique mechanics and vital structure proximity. Specific upper cervical ELDOA positions create space and improve mobility while respecting the region's sensitivity.</p>
<p>Upper cervical dysfunction can contribute to headaches, dizziness, neck pain, and referred symptoms. The high density of mechanoreceptors in this region also makes it important for proprioception and balance.</p>""",
        "benefits": ["Improves upper cervical mobility", "Reduces headaches", "Enhances balance", "Addresses neck pain", "Optimizes head position", "Supports proprioception"],
        "applications": ["Headache treatment", "Neck pain relief", "Dizziness management", "Post-whiplash care", "Cervical optimization", "Balance improvement"],
        "related_terms": [("c1-atlas", "C1 Atlas"), ("c2-axis", "C2 Axis"), ("cervical-spine", "Cervical Spine"), ("cervicogenic-headache", "Cervicogenic Headache")],
        "connections": [("atlanto-occipital", "Atlanto Occipital"), ("atlanto-axial", "Atlanto Axial"), ("suboccipital-muscles", "Suboccipital Muscles"), ("cranial-base", "Cranial Base")]
    },
    "coordination": {
        "title": "Coordination",
        "simple_desc": "Your ability to make smooth, accurate movements by having different body parts work together.",
        "detailed_desc": """<p>Coordination is the ability to execute smooth, accurate, and efficient movement through the integration of sensory input, motor planning, and muscle activation. It involves the cerebellum, motor cortex, and proprioceptive systems working together.</p>
<p>ELDOA develops coordination through the precise positioning and sustained control required. The practice demands continuous adjustment and balance, training the nervous system to better coordinate multiple muscle groups for postural control.</p>
<p>Improved coordination from ELDOA practice transfers to daily activities and athletic performance. The body awareness developed during practice enhances the quality of all movement, reducing injury risk and improving efficiency.</p>""",
        "benefits": ["Improves movement quality", "Enhances motor control", "Develops precision", "Supports athletic performance", "Reduces injury risk", "Optimizes efficiency"],
        "applications": ["Movement training", "Athletic development", "Rehabilitation", "Fall prevention", "Skill acquisition", "Daily function"],
        "related_terms": [("motor-learning", "Motor Learning"), ("neuromuscular-control", "Neuromuscular Control"), ("proprioception", "Proprioception"), ("balance", "Balance")],
        "connections": [("cerebellum", "Cerebellum"), ("motor-cortex", "Motor Cortex"), ("body-awareness", "Body Awareness"), ("movement-patterns", "Movement Patterns")]
    },
    "compensatory-patterns": {
        "title": "Compensatory Patterns",
        "simple_desc": "Ways your body moves differently to avoid pain or work around a weak or stiff area.",
        "detailed_desc": """<p>Compensatory patterns are altered movement strategies the body adopts to accomplish tasks when normal movement is limited by pain, weakness, stiffness, or structural issues. While initially protective, these patterns can create secondary problems.</p>
<p>ELDOA addresses compensatory patterns by improving the underlying restrictions that necessitate compensation. As mobility and tissue quality improve through ELDOA practice, the body can return to more efficient, balanced movement patterns.</p>
<p>Recognizing compensatory patterns is important for comprehensive treatment. ELDOA practitioners learn to identify these patterns and address their root causes rather than just treating secondary symptoms.</p>""",
        "benefits": ["Addresses root dysfunction", "Restores normal patterns", "Reduces secondary strain", "Improves movement quality", "Prevents new problems", "Enhances efficiency"],
        "applications": ["Movement assessment", "Pain treatment", "Rehabilitation", "Performance optimization", "Injury prevention", "Postural correction"],
        "related_terms": [("movement-patterns", "Movement Patterns"), ("postural-asymmetry", "Postural Asymmetry"), ("functional-anatomy", "Functional Anatomy"), ("biomechanics", "Biomechanics")],
        "connections": [("pain-avoidance", "Pain Avoidance"), ("muscle-imbalance", "Muscle Imbalance"), ("fascial-restrictions", "Fascial Restrictions"), ("movement-assessment", "Movement Assessment")]
    },
    "movement-assessment": {
        "title": "Movement Assessment",
        "simple_desc": "Looking at how someone moves to find problems that might be causing pain or poor performance.",
        "detailed_desc": """<p>Movement assessment is the systematic evaluation of how a person moves to identify dysfunction, asymmetry, compensation patterns, and movement quality issues. It forms the foundation for targeted intervention design.</p>
<p>In ELDOA methodology, movement assessment helps determine which positions will be most beneficial for an individual. By understanding where restrictions and dysfunctions exist, practitioners can prescribe ELDOA sequences that address specific needs.</p>
<p>Effective movement assessment considers the whole kinetic chain, not just symptomatic areas. This comprehensive approach ensures that root causes are identified and addressed, leading to more lasting improvements.</p>""",
        "benefits": ["Identifies dysfunction", "Guides treatment selection", "Reveals compensation", "Targets intervention", "Tracks progress", "Individualizes care"],
        "applications": ["Treatment planning", "Progress monitoring", "Root cause identification", "Performance analysis", "Injury prevention", "Rehabilitation design"],
        "related_terms": [("functional-anatomy", "Functional Anatomy"), ("biomechanics", "Biomechanics"), ("compensatory-patterns", "Compensatory Patterns"), ("postural-assessment", "Postural Assessment")],
        "connections": [("kinetic-chain", "Kinetic Chain"), ("movement-patterns", "Movement Patterns"), ("fascial-system", "Fascial System"), ("treatment-planning", "Treatment Planning")]
    },
    "spinal-mechanics": {
        "title": "Spinal Mechanics",
        "simple_desc": "How your spine moves, bends, and carries loads through its joints and discs.",
        "detailed_desc": """<p>Spinal mechanics refers to the biomechanical behavior of the spine, including how vertebrae move relative to each other, how loads are transmitted through discs and facets, and how the spine responds to different postures and activities.</p>
<p>ELDOA is designed based on detailed understanding of spinal mechanics. Each position precisely manipulates spinal mechanics to create targeted decompression, using body position, muscle tension, and breath to achieve specific effects at individual segments.</p>
<p>Understanding spinal mechanics helps explain why certain positions and postures cause problems and how ELDOA counteracts these issues. It also guides appropriate exercise selection based on individual mechanical needs.</p>""",
        "benefits": ["Optimizes spinal function", "Improves load distribution", "Enhances mobility", "Reduces mechanical stress", "Guides treatment", "Prevents problems"],
        "applications": ["Treatment design", "Exercise prescription", "Ergonomic guidance", "Athletic training", "Rehabilitation", "Prevention"],
        "related_terms": [("biomechanics", "Biomechanics"), ("vertebral-segment", "Vertebral Segment"), ("intervertebral-disc", "Intervertebral Disc"), ("facet-joints", "Facet Joints")],
        "connections": [("spinal-decompression", "Spinal Decompression"), ("disc-hydration", "Disc Hydration"), ("load-distribution", "Load Distribution"), ("posture", "Posture")]
    },
    "practice-principles": {
        "title": "Practice Principles",
        "simple_desc": "The guidelines that make your ELDOA practice more effective and help you improve faster.",
        "detailed_desc": """<p>Practice principles are the guidelines that optimize learning and adaptation in ELDOA training. These include consistency, appropriate duration, proper progression, and mindful attention during practice.</p>
<p>Key principles for effective ELDOA practice include: holding positions for 60 seconds to optimize mechanotransduction, practicing regularly (ideally daily), maintaining precise alignment throughout holds, and progressing gradually as competence develops.</p>
<p>Understanding practice principles helps maximize the benefits of ELDOA. Rather than simply going through the motions, adherence to these principles ensures that practice creates lasting neurological and structural adaptations.</p>""",
        "benefits": ["Optimizes learning", "Maximizes adaptation", "Ensures consistency", "Guides progression", "Improves outcomes", "Develops mastery"],
        "applications": ["Self-practice optimization", "Teaching methodology", "Program design", "Progress tracking", "Skill development", "Long-term maintenance"],
        "related_terms": [("motor-learning", "Motor Learning"), ("neural-adaptation", "Neural Adaptation"), ("habit-formation", "Habit Formation"), ("sustained-holds", "Sustained Holds")],
        "connections": [("mechanotransduction", "Mechanotransduction"), ("neuroplasticity", "Neuroplasticity"), ("skill-acquisition", "Skill Acquisition"), ("daily-practice", "Daily Practice")]
    },
    "diaphragm": {
        "title": "Diaphragm",
        "simple_desc": "Your main breathing muscle that sits like a dome between your chest and belly.",
        "detailed_desc": """<p>The diaphragm is the primary muscle of respiration, a dome-shaped structure separating the thoracic and abdominal cavities. It attaches to the lumbar vertebrae, lower ribs, and sternum, intimately connecting breathing with spinal mechanics.</p>
<p>In ELDOA practice, the diaphragm plays multiple roles. It is part of the Deep Front Line fascial chain, influences lumbar spine mechanics through its vertebral attachments, and proper diaphragmatic breathing enhances the effectiveness of ELDOA positions.</p>
<p>Diaphragm dysfunction can contribute to lower back pain, poor posture, and reduced core stability. ELDOA practice improves diaphragmatic function through its effects on the Deep Front Line and through the breathing awareness developed during practice.</p>""",
        "benefits": ["Improves breathing", "Supports core stability", "Enhances spinal mechanics", "Addresses DFL restrictions", "Optimizes posture", "Reduces back pain"],
        "applications": ["Breathing optimization", "Core training", "Back pain treatment", "Postural correction", "Athletic performance", "Stress management"],
        "related_terms": [("deep-front-line", "Deep Front Line"), ("core-stability", "Core Stability"), ("breathing", "Breathing"), ("psoas-muscle", "Psoas Muscle")],
        "connections": [("lumbar-spine", "Lumbar Spine"), ("fascial-chains", "Fascial Chains"), ("respiratory-function", "Respiratory Function"), ("trunk-stability", "Trunk Stability")]
    },
    "erector-spinae": {
        "title": "Erector Spinae",
        "simple_desc": "The group of muscles running up your back that help you stand straight and bend backwards.",
        "detailed_desc": """<p>The erector spinae is a group of muscles running along the length of the spine, including the iliocostalis, longissimus, and spinalis. These muscles extend the spine, control spinal flexion eccentrically, and provide postural support.</p>
<p>In ELDOA practice, the erector spinae are engaged to create the axial tension necessary for spinal decompression. Precise activation of these muscles, combined with proper positioning, generates the forces that separate vertebrae and create space.</p>
<p>The erector spinae are part of the Superficial Back Line, connecting them functionally to structures from the feet to the head. ELDOA's effect on these muscles influences the entire posterior chain.</p>""",
        "benefits": ["Improves spinal extension", "Supports posture", "Provides stability", "Enables decompression", "Enhances back strength", "Optimizes function"],
        "applications": ["Back strengthening", "Postural support", "ELDOA positioning", "Athletic performance", "Rehabilitation", "Pain management"],
        "related_terms": [("superficial-back-line", "Superficial Back Line"), ("posterior-chain", "Posterior Chain"), ("spinal-extension", "Spinal Extension"), ("back-muscles", "Back Muscles")],
        "connections": [("thoracolumbar-fascia", "Thoracolumbar Fascia"), ("lumbar-spine", "Lumbar Spine"), ("core-stability", "Core Stability"), ("posture", "Posture")]
    },
    "sacrum": {
        "title": "Sacrum",
        "simple_desc": "The triangular bone at the base of your spine that connects to your pelvis.",
        "detailed_desc": """<p>The sacrum is a triangular bone formed by five fused vertebrae (S1-S5), located at the base of the spine between the lumbar spine and coccyx. It articulates with the pelvis at the sacroiliac joints and with L5 at the lumbosacral junction.</p>
<p>In ELDOA methodology, the sacrum is crucial as the base of the spine. The L5-S1 ELDOA position specifically targets the lumbosacral junction, and sacral position influences the effectiveness of all lumbar ELDOA positions.</p>
<p>Sacral mechanics affect the entire spine through the kinetic chain. Sacral position influences lumbar lordosis, and restrictions at the sacroiliac joints can create compensation patterns throughout the spine.</p>""",
        "benefits": ["Supports spinal base", "Influences posture", "Affects lumbar mechanics", "Provides pelvic stability", "Transmits forces", "Anchors spine"],
        "applications": ["Lumbar treatment", "Pelvic mechanics", "Postural assessment", "SI joint function", "Lower back pain", "Foundation work"],
        "related_terms": [("l5-s1-junction", "L5 S1 Junction"), ("lumbosacral-angle", "Lumbosacral Angle"), ("sacroiliac-joint", "Sacroiliac Joint"), ("pelvis", "Pelvis")],
        "connections": [("lumbar-spine", "Lumbar Spine"), ("pelvic-mechanics", "Pelvic Mechanics"), ("deep-front-line", "Deep Front Line"), ("spinal-base", "Spinal Base")]
    },
    "thoracolumbar-fascia": {
        "title": "Thoracolumbar Fascia",
        "simple_desc": "A large sheet of connective tissue on your back that helps transfer force and stabilize your spine.",
        "detailed_desc": """<p>The thoracolumbar fascia (TLF) is a large aponeurotic structure covering the back of the trunk. It has multiple layers and provides attachment for numerous muscles including the latissimus dorsi, gluteus maximus, and transversus abdominis.</p>
<p>In ELDOA, the thoracolumbar fascia is recognized as a key structure for force transmission and spinal support. The fascial tension created during ELDOA positions is transmitted through the TLF, contributing to spinal decompression effects.</p>
<p>The TLF connects the upper and lower body, making it central to the fascial continuity that ELDOA addresses. Restrictions in the TLF can affect spinal mechanics, hip mobility, and shoulder function.</p>""",
        "benefits": ["Transmits force efficiently", "Stabilizes spine", "Connects body regions", "Supports core function", "Enables decompression", "Integrates movement"],
        "applications": ["Back pain treatment", "Core stability", "Movement integration", "Athletic performance", "Fascial work", "Postural support"],
        "related_terms": [("fascial-system", "Fascial System"), ("posterior-chain", "Posterior Chain"), ("core-stability", "Core Stability"), ("back-muscles", "Back Muscles")],
        "connections": [("erector-spinae", "Erector Spinae"), ("latissimus-dorsi", "Latissimus Dorsi"), ("gluteus-maximus", "Gluteus Maximus"), ("transversus-abdominis", "Transversus Abdominis")]
    },
    "gait-mechanics": {
        "title": "Gait Mechanics",
        "simple_desc": "How your body moves when you walk or run, including how all parts work together.",
        "detailed_desc": """<p>Gait mechanics refers to the biomechanical processes involved in walking and running, including stance and swing phases, force generation and absorption, and the coordination of multiple body segments.</p>
<p>ELDOA influences gait mechanics through its effects on spinal mobility, fascial tension, and proprioception. Improved spinal function and tissue quality contribute to more efficient and comfortable gait patterns.</p>
<p>Understanding gait mechanics helps explain how spinal and fascial dysfunction can contribute to lower extremity problems and vice versa. The Superficial Back Line and Spiral Line are particularly involved in gait, making their optimization through ELDOA relevant for walking and running function.</p>""",
        "benefits": ["Improves walking efficiency", "Enhances running mechanics", "Reduces compensations", "Optimizes force use", "Decreases injury risk", "Supports performance"],
        "applications": ["Walking rehabilitation", "Running optimization", "Injury prevention", "Athletic performance", "Pain management", "Functional improvement"],
        "related_terms": [("biomechanics", "Biomechanics"), ("functional-anatomy", "Functional Anatomy"), ("spiral-line", "Spiral Line"), ("superficial-back-line", "Superficial Back Line")],
        "connections": [("plantar-fasciitis", "Plantar Fasciitis"), ("hip-mechanics", "Hip Mechanics"), ("ankle-function", "Ankle Function"), ("core-stability", "Core Stability")]
    },
    "spinal-segments": {
        "title": "Spinal Segments",
        "simple_desc": "The individual sections of your spine, each with its own disc and joints.",
        "detailed_desc": """<p>Spinal segments refer to the functional units of the spine, each consisting of two adjacent vertebrae, the intervertebral disc between them, facet joints, and associated ligaments and neural structures. The spine contains 24 mobile segments.</p>
<p>ELDOA is designed to target specific spinal segments with precision. Each ELDOA position creates decompression at a particular level, allowing practitioners to address individual segment dysfunction rather than treating the spine as a uniform structure.</p>
<p>Segmental specificity is a hallmark of ELDOA methodology. Understanding the characteristics of different spinal segments—cervical, thoracic, and lumbar—allows for appropriate position selection and modification.</p>""",
        "benefits": ["Enables targeted treatment", "Addresses specific dysfunction", "Allows precision care", "Respects regional differences", "Guides ELDOA selection", "Improves outcomes"],
        "applications": ["Specific level treatment", "ELDOA prescription", "Assessment guidance", "Treatment planning", "Progress tracking", "Regional focus"],
        "related_terms": [("vertebral-segment", "Vertebral Segment"), ("l4-l5-segment", "L4 L5 Segment"), ("l5-s1-junction", "L5 S1 Junction"), ("intervertebral-disc", "Intervertebral Disc")],
        "connections": [("facet-joints", "Facet Joints"), ("spinal-mechanics", "Spinal Mechanics"), ("segmental-mobility", "Segmental Mobility"), ("disc-health", "Disc Health")]
    },
    "progressive-loading": {
        "title": "Progressive Loading",
        "simple_desc": "Gradually increasing the challenge of exercises as your body gets stronger and adapts.",
        "detailed_desc": """<p>Progressive loading is the principle of gradually increasing mechanical demands on tissues to stimulate adaptation. This approach allows tissues to strengthen and remodel in response to appropriate challenge without overwhelming healing capacity.</p>
<p>In ELDOA practice, progressive loading applies to the development of more challenging positions and longer hold times as competence develops. Beginners start with modified positions and shorter holds, progressing as tissue quality and body awareness improve.</p>
<p>Progressive loading is particularly important for tendon rehabilitation and tissue remodeling. The gradual increase in mechanical demand stimulates adaptation while respecting tissue healing timelines.</p>""",
        "benefits": ["Stimulates adaptation", "Builds tissue strength", "Prevents overload", "Optimizes progression", "Supports healing", "Enables advancement"],
        "applications": ["Rehabilitation programs", "Athletic training", "ELDOA progression", "Tendon healing", "Tissue strengthening", "Skill development"],
        "related_terms": [("mechanotransduction", "Mechanotransduction"), ("tissue-remodeling", "Tissue Remodeling"), ("eccentric-loading", "Eccentric Loading"), ("tendon-healing", "Tendon Healing")],
        "connections": [("practice-principles", "Practice Principles"), ("tissue-capacity", "Tissue Capacity"), ("rehabilitation", "Rehabilitation"), ("training-principles", "Training Principles")]
    },
    "skill-acquisition": {
        "title": "Skill Acquisition",
        "simple_desc": "The process of learning new movements and getting better at them through practice.",
        "detailed_desc": """<p>Skill acquisition is the process by which new motor skills are learned and refined through practice. It involves stages from initial cognitive learning through associative refinement to automatic performance.</p>
<p>ELDOA practice involves significant skill acquisition as practitioners learn precise positioning and develop the body awareness needed for effective holds. This learning process follows predictable stages, with positions becoming easier and more effective over time.</p>
<p>Understanding skill acquisition principles helps optimize ELDOA practice. Appropriate feedback, consistent practice, and progressive challenge all support the learning process that underlies ELDOA competence.</p>""",
        "benefits": ["Develops new abilities", "Improves with practice", "Enables mastery", "Supports automaticity", "Enhances performance", "Builds competence"],
        "applications": ["ELDOA learning", "Movement training", "Athletic development", "Rehabilitation", "Teaching methodology", "Practice design"],
        "related_terms": [("motor-learning", "Motor Learning"), ("neural-adaptation", "Neural Adaptation"), ("practice-principles", "Practice Principles"), ("neuroplasticity", "Neuroplasticity")],
        "connections": [("brain-plasticity", "Brain Plasticity"), ("motor-cortex", "Motor Cortex"), ("feedback-mechanisms", "Feedback Mechanisms"), ("deliberate-practice", "Deliberate Practice")]
    },
    "vertebral-rotation": {
        "title": "Vertebral Rotation",
        "simple_desc": "When the bones in your spine twist or turn along their axis, often seen in scoliosis.",
        "detailed_desc": """<p>Vertebral rotation refers to the twisting of vertebrae along the longitudinal axis of the spine. It is a normal component of spinal movement but becomes pathological when excessive or fixed, as seen in scoliosis.</p>
<p>In scoliosis, vertebral rotation is coupled with lateral curvature, creating the three-dimensional deformity characteristic of the condition. The apical vertebra typically shows the greatest rotation.</p>
<p>ELDOA addresses vertebral rotation by creating space that allows for improved vertebral positioning. While structural rotation cannot be eliminated, ELDOA can improve segmental mechanics and reduce the functional consequences of rotation.</p>""",
        "benefits": ["Addresses rotational component", "Improves spinal mechanics", "Reduces asymmetry effects", "Creates segmental space", "Optimizes function", "Supports derotation"],
        "applications": ["Scoliosis management", "Spinal asymmetry", "Rib cage effects", "Thoracic treatment", "Movement improvement", "Postural correction"],
        "related_terms": [("scoliosis", "Scoliosis"), ("apical-vertebra", "Apical Vertebra"), ("thoracic-rotation", "Thoracic Rotation"), ("spiral-line", "Spiral Line")],
        "connections": [("rib-cage-deformity", "Rib Cage Deformity"), ("convex-concave", "Convex Concave"), ("spinal-curvature", "Spinal Curvature"), ("vertebral-segment", "Vertebral Segment")]
    },
    "sensory-input": {
        "title": "Sensory Input",
        "simple_desc": "Information your body sends to your brain about touch, position, temperature, and pain.",
        "detailed_desc": """<p>Sensory input refers to the information transmitted from peripheral receptors to the central nervous system about the body's state and environment. This includes proprioceptive, tactile, thermal, and nociceptive (pain) information.</p>
<p>ELDOA provides rich sensory input through the precise positioning and sustained tension involved. This input stimulates mechanoreceptors throughout the fascial system, enhancing proprioception and body awareness.</p>
<p>Quality sensory input is essential for movement control and can modulate pain perception. The sensory experience during ELDOA practice contributes to both its neurological benefits and its effects on pain.</p>""",
        "benefits": ["Enhances proprioception", "Improves body awareness", "Supports motor control", "Modulates pain", "Develops neural pathways", "Optimizes function"],
        "applications": ["Proprioceptive training", "Pain management", "Movement re-education", "Rehabilitation", "Body awareness development", "Neural optimization"],
        "related_terms": [("proprioception", "Proprioception"), ("fascial-mechanoreceptors", "Fascial Mechanoreceptors"), ("kinesthesia", "Kinesthesia"), ("pain-neuroscience", "Pain Neuroscience")],
        "connections": [("body-schema", "Body Schema"), ("neuromuscular-control", "Neuromuscular Control"), ("central-nervous-system", "Central Nervous System"), ("receptor-types", "Receptor Types")]
    },
    "body-awareness": {
        "title": "Body Awareness",
        "simple_desc": "Your conscious sense of how your body feels, where it is, and how it's moving.",
        "detailed_desc": """<p>Body awareness is the conscious perception of one's body, including its position, movement, tension, and sensations. It encompasses proprioception, interoception, and the cognitive understanding of one's physical state.</p>
<p>ELDOA significantly develops body awareness through its demands for precise positioning and sustained attention. The practice requires continuous monitoring of body position and tension, training the ability to perceive subtle physical states.</p>
<p>Enhanced body awareness is one of the lasting benefits of ELDOA practice. This awareness helps individuals maintain better posture throughout the day, recognize early signs of tension or dysfunction, and move more efficiently.</p>""",
        "benefits": ["Improves posture awareness", "Enhances movement quality", "Supports self-correction", "Enables early detection", "Develops mindfulness", "Optimizes daily function"],
        "applications": ["Postural improvement", "Movement training", "Pain awareness", "Self-care development", "Athletic performance", "Daily life"],
        "related_terms": [("proprioception", "Proprioception"), ("kinesthesia", "Kinesthesia"), ("body-schema", "Body Schema"), ("mindfulness", "Mindfulness")],
        "connections": [("sensory-input", "Sensory Input"), ("movement-patterns", "Movement Patterns"), ("postural-control", "Postural Control"), ("self-correction", "Self Correction")]
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
    print("Creating missing encyclopedia pages (Batch 2)...")
    created = create_all_missing_pages()
    print(f"\nCreated {len(created)} new pages")
