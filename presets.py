"""Preset text for the Artfat LLM Prompter node.

Two layers:
  * system presets  -> HOW to write (engine / style). Read from models/LLM/prompts/*.txt
  * instruction presets -> WHAT to do (task / output format). Defined below.
Both auto-fill an editable widget on the node (web/llm_prompter.js), so the
chosen text is visible and can be edited live before running.
"""

import os

import folder_paths

# System presets are read from TWO places, in this priority:
#   1. USER_DIR  -> ComfyUI/models/LLM/prompts/   (user's own presets + live overrides)
#   2. BUNDLED_DIR -> this node's own prompts/     (ships with the node via git, always present)
# A .txt in USER_DIR overrides a bundled one of the same name, so users can tweak a preset
# by dropping an edited copy into models/LLM/prompts/ without touching the node files.
_HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLED_DIR = os.path.join(_HERE, "prompts")
USER_DIR = os.path.join(folder_paths.models_dir, "LLM", "prompts")
# Reference presets live in their own subfolder. They describe a PERSON, not a scene, so they
# must never appear in the scene dropdown and no scene preset may appear in theirs — picking the
# wrong one produces an identity block that is silently prepended to every caption in a batch.
# The split costs nothing: the listers below only collect *.txt, so a subdirectory is skipped.
BUNDLED_REF_DIR = os.path.join(BUNDLED_DIR, "reference")
USER_REF_DIR = os.path.join(USER_DIR, "reference")
# Kept for backward compatibility (older code/imports referenced PROMPTS_DIR).
PROMPTS_DIR = USER_DIR

# name -> instruction text ("Custom" leaves the box empty for a free / user preset)
INSTRUCTION_PRESETS = {
    "Custom": "",
    "Describe -> prompt": (
        "Look at the image and write a single detailed text-to-image prompt that "
        "faithfully describes it: subject, setting, composition, lighting and mood. "
        "Output only the prompt as one flowing paragraph, no preamble, no analysis."
    ),
    "Extreme detailed": (
        "Write an extremely detailed text-to-image prompt from the image. Elaborate on "
        "the subject's appearance, clothing textures, specific background elements, the "
        "quality and colour of light, shadows and overall atmosphere. One rich paragraph. "
        "Output only the prompt."
    ),
    "Tags": (
        "Generate a clean list of comma-separated tags for a text-to-image model based only "
        "on the visible content of the image: subject, clothing, environment, colours, lighting, "
        "composition. Max 50 unique tags, no abstract or marketing terms. Output only the tags."
    ),
    "Cinematic": (
        "Act as a master prompt engineer. Write a highly detailed, evocative cinematic prompt for "
        "an image-generation model: subject, pose, environment, lighting, mood and photographic "
        "style. Weave everything into one natural-language paragraph. Output only the prompt."
    ),
    "Refine & expand": (
        "Refine and enhance the following prompt for text-to-image generation. Keep its meaning "
        "and key words, make it more expressive and visually rich. Output only the improved prompt "
        "text itself, with no reasoning, thinking or commentary."
    ),
    "Ref face (Image1) + frame (Image2)": (
        "Take the face and head shape from the FIRST image and everything else from the "
        "SECOND image - body, pose, hair styling, clothing, light, environment, framing. "
        "The woman in the second image is given the first woman's face. Reproduce that face "
        "exactly, never narrowing or beautifying it. Output only the final prompt as one paragraph."
    ),
    "Scene only (face comes from ref_description)": (
        "Describe ONLY what changes from photo to photo: shot size and framing, camera height "
        "and angle, body and build, pose, hair styling, clothing, footwear and jewellery, skin "
        "of the body, light source and direction, environment and props, and the image character "
        "(grain, sharpness, exposure). Do NOT describe the face, head shape or facial features - "
        "the identity is supplied separately and prepended to your text, so describing it again "
        "would contradict it. Start straight at the framing. Output only the description as one "
        "flowing paragraph, no preamble."
    ),
    "Replace subject (Image1 scene + Image2 person)": (
        "Generate a detailed prompt describing the reference Image 1. Replace the person from "
        "Image 1 with the person from Image 2, adapting the pose naturally to the scene. Output "
        "only the final prompt as one paragraph."
    ),
    "Replace + keep outfit from Image1": (
        "Generate a detailed prompt describing the reference Image 1. Replace the person from "
        "Image 1 with the person from Image 2, but she should be dressed exactly the same as in "
        "Image 1. Output only the final prompt as one paragraph."
    ),
    "Appearance only (face + body)": (
        "Describe only the appearance of the person: face first, then body. No clothing, "
        "accessories, environment, pose or action unless explicitly told. If two images are given, "
        "blend the features into one coherent person. Output only the description."
    ),
    "Scene + lighting mix": (
        "Combine the architecture and composition of Image 1 with the time-of-day lighting and "
        "colour mood of Image 2 into a single text-to-image prompt. Output only the prompt."
    ),
    "Pose only": (
        "Describe only the body pose and positioning: limb placement, weight and balance, torso "
        "and head orientation, gaze direction, hand placement, the body's angle to the camera, "
        "the framing and shot size as it relates to the pose, and, if more than one figure is "
        "present, their spatial relation to each other. Do not describe identity, face features, "
        "hair, clothing, colours, environment, lighting or art style/medium. Express the result "
        "in the output format defined by the system prompt. Output only the result."
    ),
    "Style only": (
        "Describe only the visual style: medium and technique, rendering and linework, colour "
        "palette and grading, lighting character, texture and grain, era and aesthetic. Do not "
        "describe who or what is depicted, pose, clothing or setting specifics. The result must "
        "be reusable on any unrelated subject. Express the result in the output format defined "
        "by the system prompt. Output only the result."
    ),
    "Style transfer (Image1 subject + Image2 style)": (
        "Two images are provided: Image 1 is the subject source, Image 2 is the style source. "
        "Take the subject and composition - what is depicted, the pose, the framing and the "
        "layout - from the subject source. Take "
        "only the visual style from the style source: its medium and technique, rendering and "
        "linework, colour palette and grading, lighting character, texture and grain, era and "
        "aesthetic. Nothing depicted in the style source - its people, objects or setting - may "
        "carry over, and none of the original style belonging to the subject source may carry "
        "over. Describe the subject and composition rendered entirely in the borrowed style. "
        "Express the result in the output format defined by the system prompt. Output only the "
        "result."
    ),
    "Full composition": (
        "Describe everything visible: subject(s), pose, clothing, environment, framing, lighting, "
        "colour and style. Express the result in the output format defined by the system prompt. "
        "Output only the result."
    ),
}

INSTRUCTION_NAMES = list(INSTRUCTION_PRESETS.keys())


def list_system_presets():
    """Dropdown values: 'Custom' plus every .txt from the bundled prompts/ and
    models/LLM/prompts/ (deduped by filename, user dir wins, case-insensitive sort)."""
    seen = set()
    for d in (BUNDLED_DIR, USER_DIR):
        try:
            if os.path.isdir(d):
                for fn in os.listdir(d):
                    if fn.lower().endswith(".txt"):
                        seen.add(fn)
        except Exception as e:
            print(f"[llm-prompter] Could not list system presets in {d}: {e}")
    return ["Custom"] + sorted(seen, key=str.lower)


def list_ref_presets():
    """Dropdown values for ref_preset: 'Custom' plus every .txt from prompts/reference/ and
    models/LLM/prompts/reference/ (deduped by filename, user dir wins, case-insensitive sort)."""
    seen = set()
    for d in (BUNDLED_REF_DIR, USER_REF_DIR):
        try:
            if os.path.isdir(d):
                for fn in os.listdir(d):
                    if fn.lower().endswith(".txt"):
                        seen.add(fn)
        except Exception as e:
            print(f"[llm-prompter] Could not list reference presets in {d}: {e}")
    return ["Custom"] + sorted(seen, key=str.lower)


def load_ref_preset(name):
    """Text of a reference preset, or None for 'Custom'/missing. User copy wins.

    Falls back to the flat prompts/ dir so a workflow saved before the split — when
    Face_Only_Identity_Im1.txt still lived there — keeps resolving instead of silently
    dropping to the built-in instruction.
    """
    if not name or name in ("Custom", "None"):
        return None
    for d in (USER_REF_DIR, BUNDLED_REF_DIR, USER_DIR, BUNDLED_DIR):
        path = os.path.join(d, name)
        try:
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            print(f"[llm-prompter] Could not read reference preset {path}: {e}")
    return None


def load_system_preset(name):
    """Return the text of a .txt system preset, or None for 'Custom'/missing.
    Checks USER_DIR first (so a user copy overrides the bundled one), then BUNDLED_DIR."""
    if not name or name in ("Custom", "None"):
        return None
    for d in (USER_DIR, BUNDLED_DIR):
        path = os.path.join(d, name)
        try:
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as fh:
                    return fh.read()
        except Exception as e:
            print(f"[llm-prompter] Could not read preset {name} from {d}: {e}")
    return None
