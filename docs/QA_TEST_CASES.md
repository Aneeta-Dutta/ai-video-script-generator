# QA Test Cases: Cinematic Production House

## 1. Persona Continuity Test
- **Objective:** Verify that a character (e.g., "Arindam Roy") retains his profile across 5+ scenes.
- **Steps:**
    1. Run `python run_direct_sequential.py "A rainy night in North Kolkata"`.
    2. Open the resulting JSON.
    3. Check `performance_detailing.voice_dna` for Arindam in Scene 1 and Scene 5.
- **Expected Result:** `voice_dna` must be identical. `veo3_stack` should mention physical traits defined in the Creative Brief (e.g., "rumpled khadi kurta").

## 2. Audio Separation Test
- **Objective:** Ensure dialogue and background sounds are not mixed in the same JSON string.
- **Steps:**
    1. Inspect the `spoken_dialogue` block.
    2. Inspect the `background_soundscape` block.
- **Expected Result:** Background ambiance (e.g., "lapping water") must exclusively reside in `background_soundscape`.

## 3. Dynamic Performance Intensity Test
- **Objective:** Verify that [CLIMAX] beats have higher performance intensity than [INTRO] beats.
- **Steps:**
    1. Run a 5-scene beat.
    2. Compare `performance_intensity` for Scene 1 (INTRO) and Scene 4 (CLIMAX).
- **Expected Result:** INTRO should be ~0.4-0.6. CLIMAX should be ~0.9-1.0.

## 4. Bengali Authenticity Test
- **Objective:** Verify that dialogue uses Standard/Kolkata Bengali.
- **Steps:**
    1. Review `text_bengali` from 3 different scenes.
    2. Check for colloquialisms or sophisticated city-based phrasing.
- **Expected Result:** No rural east-Bengal (Bangal) dialects unless explicitly specified for a character.

## 5. Deployment Health Check
- **Objective:** Verify CI/CD pipeline health.
- **Steps:**
    1. Push a minor change to a release branch.
    2. Monitor GitHub Actions.
- **Expected Result:** `test`, `build`, and `deploy-staging` jobs all turn green.
