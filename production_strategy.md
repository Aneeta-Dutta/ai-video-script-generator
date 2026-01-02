# Production Strategy: The Assembly Line Protocol

**Objective:** To industrialize the generation of "Cinema-Grade" video assets for the Arindam Roy campaign.
**Inputs:** 8 Video Concepts, Research Report, 6 Reference Guides.
**Outputs:** A single Master Manifest containing Veo 3 Prompts and Bengali Scripts.

---

## 1. The "Assembly Line" Workflow

We will treat every Video Concept as a raw material that must pass through four stations:

### Station 1: The Research Validation (The Reality Check)
*   **The Swarm:**
    1.  **Lead Investigator:** Synthesizes the overall validity.
    2.  **Data Miner:** Checks statistics (e.g., "Is 4% unemployment accurate?").
    3.  **Grassroots Voice:** Checks emotional resonance (e.g., "Do students actually protest like this?").
    4.  **Historian:** Checks context (e.g., "Is the 1970s factory visually correct?").
    5.  **Trend Scout:** Checks virality (e.g., "Is this concept 'shareable' right now?").
    6.  **Narrative Architect:** Checks structural integrity (e.g., "Does this store have a beginning, middle, and end?").
*   **Reference:** [research_team_personas.md](file:///Users/sargupta/Desktop/AI Video/research_team_personas.md)
*   **Task:** Verify the concept against the [Research Report](file:///Users/sargupta/Desktop/AI Video/research_reports/west_bengal_unemployment_deep_dive.md).
*   **Check:** "Is the Coromandel Express physically accurate for migrant travel?" "Is the 'Teacher Protest' visually aligned with the 1000-day dharna?"
*   **Output:** Validated Concept.

### Station 2: The Production Refinery (The Polish)
*   **Agents:** The Production Team.
*   **Reference:** [production_team_personas.md](file:///Users/sargupta/Desktop/AI Video/production_team_personas.md)
*   **Task:** Apply the *Masterclass Reference Guides*.
    *   *DoP:* [cinematography_guide.md](file:///Users/sargupta/Desktop/AI Video/production_references/cinematography_guide.md) (Assign Lens/Angle).
    *   *Designer:* [production_design_guide.md](file:///Users/sargupta/Desktop/AI Video/production_references/production_design_guide.md) (Assign PBR textures).
    *   *Costume:* [costume_guide.md](file:///Users/sargupta/Desktop/AI Video/production_references/costume_guide.md) (Clean Leader doctrine).
    *   *Director:* [director_guide.md](file:///Users/sargupta/Desktop/AI Video/production_references/director_guide.md) (Semiotics).
    *   *Post:* [post_production_guide.md](file:///Users/sargupta/Desktop/AI Video/production_references/post_production_guide.md) (Color Grade).
*   **Output:** Technical Visual Description.

### Station 3: The Dialogue Injection (The Voice)
*   **Agent:** Kobiyal (The Dialogue Writer).
*   **Reference:** [dialogue_guide.md](file:///Users/sargupta/Desktop/AI Video/production_references/dialogue_guide.md)
*   **Task:** Write the specific Bengali slogan or internal monologue.
    *   *Format:* Bengali Script (Transliterated) + English Translation.
    *   *Style:* Slogan (Rhyming) or Whisper (Intimate).
*   **Output:** Cultural Context Layer.

### Station 4: The Executive Loop (The Iterative Quality Gate)
*   **Agent:** The Showrunner.
*   **Reference:** [executive_producer_persona.md](file:///Users/sargupta/Desktop/AI Video/executive_producer_persona.md)
*   **Task:** The "Red Pen" Review. The Showrunner does not just say "No"; they give *Directives*.
*   **The Feedback Loop (The "3-Strike" Protocol):**
    *   **Iteration 1 (Initial Review):** Standard Critique. (e.g., "Too theatrical.")
    *   **Iteration 2 (The Escalation):** If rejected again, feedback must be **Technical & Granular**. (e.g., "Lighting is incorrectly keying Arindam. Use Rembrandt lighting at 3200K. Lower fill by -2 stops.")
    *   **Iteration 3 (The Force Majeure):** If it fails a third time, The Showrunner **Overrules and Approves** the best version to prevent deadlock.
*   **Output:** Only *Greenlit* concepts move.

### Station 5: The Editor's Cut (The Glue)
*   **Agent:** The Editor (Satyajit).
*   **Reference:** [storytelling_guide.md](file:///Users/sargupta/Desktop/AI Video/production_references/storytelling_guide.md)
*   **Task:** Ensure transition logic between scenes.
*   **Check:** "Does Scene A end on a visual that matches Scene B's start?" "Is there an Audio Bridge?"
*   **Output:** The Final Shooting Script.

---

## 2. The Final Output Structure (The Shooting Script)

We generate a **Sequential Shooting Script**. Each row is a scene, but the *columns* define the flow.

### Sequence: [Story Title]
**Story Arc:**
> **Scene N:** [Title]
> *   **Visual Hook (Start):** Matches previous scene's end.
> *   **Veo 3 Prompt:** The technical code block.
> *   **Audio Bridge (J-Cut):** Sound that starts *before* the visual cut.
> *   **Visual Hook (End):** Exploring a shape/motion for the *next* scene.
> *   **Dialogue:** The 8-second monologue.

**1. The Veo 3 Prompt (Code Block):**
> Reference: [veo_prompt_guide.md](file:///Users/sargupta/Desktop/AI Video/veo_prompt_guide.md)
```text
[SUBJECT] :: [ENVIRONMENT] :: [LIGHTING] :: [CAMERA] :: [POST] --style cinematic
```

**2. The 8-Second Monologue (Kobiyal's Canvas):**
> Reference: [dialogue_guide.md](file:///Users/sargupta/Desktop/AI Video/production_references/dialogue_guide.md)
*   **Time:** 8 Seconds.
*   **Dialogue (Bengali):** "[Bengali Text]"
*   **Translation:** "[English Meaning]"

---

## 3. Execution Plan
1.  **Iterate:** I will process concepts 1-8 sequentially through this logic.
2.  **Compile:** Write to `final_generation_manifest.md`.
3.  **Review:** Present to User for final Veo generation.
