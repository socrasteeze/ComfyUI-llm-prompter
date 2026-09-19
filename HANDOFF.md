# HANDOFF

**Updated:** 2026-09-18 · **Branch:** main · **Base:** cec6951 · **Tree:** clean

## State
Preset pack shipped: 7 format presets in `prompts/`, 4 scope presets in `presets.py`, README updated. Validated on Qwen3.8-27B through the live node. llama-cpp-python is 0.3.48.

## Done this session
- 7 format-only system presets — `prompts/{klein-4b,klein-9b,krea2,illustrious,anima,minimax-ref2va,minimax-fl2va}.txt`
- 4 scope-only instruction presets — `presets.py`
- README section "Scope-only instruction presets" + Unreleased changelog
- llama-cpp-python 0.3.20 → 0.3.48+cu130 via `install.py`; host GPU gate passes; the other five `llama_cpp` nodes import (not exercised)
- A/B on 10 character images × 28 combos: 27B 261/280 format-clean (tags 80/80), 4B 220/280 (tags 41/80)
- Two API-format workflows saved in the ComfyUI user workflows folder: `llm-prompter-presets`, `llm-prompter-presets-two-image`

## Open
1. Optional: 27B prose presets still emit descriptive negations ("with no visible lean") in about 8% of runs; `klein-4b` overruns 120 words in 8 of 40
2. Optional: cut a release (version bump in `pyproject.toml`, move Unreleased to a numbered changelog entry)
3. Optional: delete the 0.3.20 backup folder once the other `llama_cpp` nodes have been used for real
4. Watch: ComfyUI exited silently once right after a `/free` unload of the LLM on 0.3.48. Not reproduced; an earlier `/free` was fine

## Decisions
- Scope presets live in the `presets.py` dict over `.txt` files — the node has no `.txt` loader for instructions; files would land in the system dropdown
- `minimax-fl2va` uses the vendor's 3-section FL2VA format over the six-section one — six sections belong to Ref2VA per MiniMax-H3 `SKILL.md`; the first handoff had them swapped
- FL2VA clip duration comes from `user_preset` text, default `6.00` — the alignment line requires one and the node has no duration input
- Illustrious defaults to space-separated tags over underscores — matches how the family is prompted; user text can override
- Anima always opens with `masterpiece, best quality`; score, year, highres tags only on request — free choice made the 4B inconsistent
- Style-transfer instruction names Image 1 / Image 2 explicitly over neutral wording — the model must know which is which; the two-image warning it trips fires only with `reference_image`, where it is correct
- Format presets bundled in repo `prompts/` over the user models folder — versioned with the fork; a same-named file in the user folder still overrides

## Traps
- Small VLMs copy any content-bearing example tag from a system preset into every output. Tag presets carry none; keep it that way
- Naming `no humans` in a preset makes a 4B append it everywhere
- Standalone `import llama_cpp` fails unless `os.add_dll_directory(<torch>/lib)` runs first
- JoyCaption via the `LLaVA-1.5` handler never stops on its own and ignores `image_2`; cap `max_tokens`
- `control_after_generate = fixed` freezes `final_prompt` and skips the LLM
- The node keeps the LLM resident (about 18 GB for the 27B) until ComfyUI's `/free` is called or a diffusion model evicts it
- On 0.3.48 `llama_supports_gpu_offload()` is False until a model is loaded; backends load lazily. Not a CPU fallback

## Verify
none documented. Manual: load node → pick `system_preset` + `instruction_preset` → `control_after_generate = randomize` → queue → read `final_prompt`
