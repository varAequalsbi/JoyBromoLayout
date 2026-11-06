# JoyBromo Layout

Interactive Three.js reconstruction of the existing cafe site, based on the owner’s plan, satellite reference and three photo visits. This is a visual study, not a measured architectural survey.

Published preview: https://joybromo-layout.purplegibbon.chatgpt.site

## Explore

Orbit, zoom and use the named viewpoints to inspect the site. Adjust gate-to-house distance, planted-yard depth, side-path width and alcove depth. Estimates save in the current browser; **Download adjusted model** exports the current geometry as GLB. Photo references are included. The recessed corner is identified as a future photo spot, while the model retains the existing setting.

## Run locally

With Python installed, run from this repository:

```sh
python -m http.server 8766 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8766/. No npm installation or build step is needed.

## Rebuild the model

```sh
python -m pip install -r model/requirements.txt
python model/build_model.py --skip-preview
```

This updates `dist/model.glb`. Omit `--skip-preview` for the optional software-rendered image, which is slower. `model/EVIDENCE.md` records source references, corrections and remaining estimates. Original full-resolution phone batches and local browser profiles are not part of this repository.

## Files and hosting

- `dist/`: complete deployable site, portable GLB and curated reference images.
- `model/`: reproducible geometry and vegetation generators.
- `.openai/hosting.json`: Sites deployment identity and static directory.

The static site can also be served by any host supporting JavaScript modules and binary GLB files. Three.js and its bundled addons retain their MIT license in `dist/vendor/`. Site photos and drawings belong to their respective owners; the satellite screenshot retains its map attribution.
