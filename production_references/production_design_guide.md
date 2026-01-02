# The Production Design Bible: World Building & Texture Maps (Masterclass Edition)

## 1. Architectural Vernacular & Atmospheric Theory
**Core Aesthetic:** **"Wabi-Sabi" Realism**. Finding beauty in the imperfection and impermanence of the environment.
*   **The Palette:** Earth tones (Burnt Sienna, Umber), Monsoon greys, and Industrial cyans.
*   **Texture Mapping:** High-frequency detail (Displacement Maps) on all surfaces. Nothing is smooth.

## 2. Location Analysis & Set Dressing

### A. The War Room (Brutalist Modernism)
*   **Architectural Style:** Neo-Modern / Brutalist. Exposed concrete meeting sleek glass.
*   **Lighting Practical:** 6500K LED strips embedded in coves (cool, clinical).
*   **Materiality:**
    *   *Walls:* Sound-dampened acoustic panels (fabric texture) vs. Glass.
    *   *Surfaces:* Anti-fingerprint matte black laminates.
*   **Prop Logic:** "Controlled Cutter." Stacks of dossiers are aligned perfectly. Digital displays show *Vector Data* (GIS maps), not generic "hacker screens."
*   **Atmospherics:** Sterile air, slight "bloom" on the screens (Pro-Mist filter effect).

### B. The Rally Stage (Vernacular Construction)
*   **Architectural Style:** Indigenous Temporary Structure (Bamboo Scaffolding).
*   **Materiality:**
    *   *Structural:* Rough-hewn bamboo tied with jute ropes.
    *   *Textile:* Coarse cotton banners (hand-painted typography, paint bleeding slightly).
*   **Lighting Practical:** Sodium Vapor Halogens (warm orange glow, slight flicker) mixed with harsh HMI spotlights.
*   **Atmospherics:** Volumetric Fog (Dust/Smoke coefficient 0.7). Tyndall rays visible from spotlights.

### C. Ground Zero / Flood Zone (Entropy & Decay)
*   **Architectural Style:** Ruined Vernacular.
*   **Materiality:**
    *   *Water:* High turbidity (muddy brown/green). Specular highlights should be dull, not crystalline.
    *   *Vegetation:* Hydrophobic leaves (Banana/Colocasia) with water beading (Surface Tension).
*   **Erosion Logic:** Mudlines on walls indicating water levels. Salt efflorescence on brickwork.
*   **Atmospherics:** 99% Humidity. Lens condensation (subtle). Overcast sky (Softbox lighting).

## 3. Texture Protocols (PBR Workflow)
For all generated environments, imply these Physically Based Rendering (PBR) properties:
*   **Roughness Map:** High on walls/ground (matte, dusty), Low on sweat/water (glossy).
*   **Normal Map:** Deep distinct grooves in wood and fabric.
*   **Albedo:** Desaturated and stained. No pure RGB primary colors except the **Saffron Scarf**.

## 4. How to Use This Guide in Prompting
**Core Syntax:**
> "Set the scene in [Location Name] using [Architectural Style]. Ensure textures show [Materiality details]."

**Examples:**
*   "Set the scene in **The War Room**. Use **Brutalist Modernism** with **exposed concrete**. Ensure screens show **Vector Data**."
*   "Set the scene in **Ground Zero**. Use **ruined vernacular** architectural style. Show **mudlines** on the walls."
