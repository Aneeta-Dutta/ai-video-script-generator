# The Post-Production Bible: Direct Image & Color Science (Masterclass Edition)

## 1. Color Science & Look Up Tables (LUTs)
**Target Color Space:** Rec.709 (Broadcast) simulated from Arri LogC3.
**The "Rally" LUT (Code: TEAL_ORANGE_GRIT):**
*   **Split Toning:**
    *   *Highlights:* Shift towards Warmer Gold/Orange (Skin tones, Sun, Dust).
    *   *Shadows:* Shift towards Cool Teal/Cyan (Sky, concrete, shadows).
*   **Contrast Curve:** "S-Curve" with lifted blacks (Matte finish) and rolled-off highlights (Soft clipping).
*   **Saturation:** Vibrance +20, Saturation -10 (Selective Saturation: Boost Oranges, Desaturate Blues).

## 2. Emulation Specifications

### A. Film Stock: Kodak Vision3 500T (5219)
*   **Grain Structure:** Super 35mm grain plate overlay.
    *   *Size:* Medium-Fine.
    *   *Intensity:* 15% Overlay.
*   **Halation:** Red/Orange glow around high-contrast edges (e.g., sun behind head, stadium lights).
*   **Gate Weave:** Static (obviously), but imply motion blur in background elements.

### B. Optical Characteristics
*   **Bloom:** Pro-Mist 1/8 lens filter effect. Softens the "digital sharpness" of the skin.
*   **Vignette:** -1.5 EV soft fall-off at corners to center the eye.
*   **Chromatic Aberration:** Minimal, only at extreme edges of the frame (lens imperfection).

## 3. Exposure Logic (False Color)
*   **Skin Tones (Arindam):** 55-65 IRE (Well exposed, separated from background).
*   **Background:** 30-40 IRE (Darker, pushing him forward).
*   **Highlights (Sun/Lights):** 90-95 IRE (Near white, but retraining detail).
*   **Blacks:** 2-5 IRE (Deep, but detailed. Not crushed to 0).

## 4. Grading by Scenario

### "The Bleach Bypass" (War Room)
*   **Process:** Skip the bleaching stage of development. silver retention.
*   **Result:** High Contrast, Low Saturation.
*   **Tone:** "Metallic," cold, cerebral.

### "The Sodium Vapor" (Night Rally)
*   **Process:** Narrow band filtering.
*   **Spectrum:** Dominant 589nm (Orange-Yellow).
*   **Skin:** Corrected to neutral warm amidst the yellow wash.

## 5. How to Use This Guide in Prompting
**Core Syntax:**
> "Apply [Color Palette] grading style. Emulate [Film Stock] with [Grain Level] grain. Ensure [Exposure Logic] for the subject."

**Examples:**
*   "Apply **Bleach Bypass** grading style. Emulate **Kodak Vision3 500T** with **medium grain**. Ensure Arindam’s skin is **60 IRE** against a dark background."
*   "Create a **Teal & Orange** look. Add **red halation** to the streetlights."
