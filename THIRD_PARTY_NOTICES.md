# Third-party components and visual references

This is rainbow鱼's personal portfolio and GitHub profile. Project artwork belongs to the respective projects; repository imagery is credited in `assets/catalog/manifest.json`. No reference site's portrait, project photography, or personal claims are reused.

## React Bits Aurora

The website's Aurora background adapts the simplex-noise shader from David Haz's React Bits Aurora component for this site's native WebGL renderer. The source is integrated into `script.js`, rather than distributed as a standalone component package.

- Source: https://github.com/DavidHDev/react-bits/blob/e12c22192ac7b4b452c5e2feb9b586d74765d696/src/content/Backgrounds/Aurora/Aurora.jsx
- Copyright (c) 2026 David Haz
- License: MIT + Commons Clause License Condition v1.0. The complete notice is preserved in `assets/licenses/react-bits-LICENSE.txt`.

## Design research

The following were reviewed for composition, interaction or profile structure. Their site/template code is not copied unless separately identified above.

- Dennis Snellenberg: https://dennissnellenberg.com/ and https://dennissnellenberg.com/work — typography, project hierarchy, spatial rhythm and restrained motion.
- React Bits portfolio: https://rbp-portfolio.vercel.app/ and https://github.com/DavidHDev/rbp-portfolio — pill navigation, shader-backed hero, readable project imagery and accessibility-aware motion.
- DenverCoder1: https://github.com/DenverCoder1/DenverCoder1 — GitHub-native widgets and distinct profile sections.
- abhisheknaiidu: https://github.com/abhisheknaiidu/abhisheknaiidu — compact introduction and expressive technology icons.

README widget sources and local copies are recorded separately in their asset manifests and notices. Dynamic statistics describe public GitHub activity or optional measured WakaTime aggregates, not proficiency, employment, or research validation.

## Restored icon widgets

- qkrdmstlr3/techstack-generator: six locally mirrored animated technology icons, under MIT. Full notice: `assets/catalog/techstack-generator-LICENSE.txt`. The GitHub icon includes a local light backplate for contrast; its original vector paths and animation are retained.
- LelouchFR/skill-icons: locally mirrored skill-icon strip, under MIT. Full notice: `assets/catalog/skill-icons-LICENSE.txt`.
- Exact source URLs, local modifications and integrity hashes: `assets/catalog/widgets.json`.
- Original profile artwork, buttons and the independent local text animation: `assets/readme/ATTRIBUTION.md`.

## Taste Skill design guidance

The 2026-10-27 paired-theme restyle applies colour-role, contrast and visual-review guidance from Leonxlnx/taste-skill, reviewed at commit `12af471f627f866411b4bd785b19646d3672784c`:

- https://github.com/Leonxlnx/taste-skill/blob/12af471f627f866411b4bd785b19646d3672784c/skills/taste-skill/SKILL.md
- https://github.com/Leonxlnx/taste-skill/blob/12af471f627f866411b4bd785b19646d3672784c/skills/taste-skill/references/colour.md

This is design guidance, not a copied component or template. No Taste Skill runtime code is shipped. The theme-aware artwork and generators are original adaptations for this profile; original project logos, supplied project compositions and credited widgets retain their respective provenance.

## Rainbow Fieldnotes components — 2026-10-28

The active website and bilingual GitHub profile now share an original hand-painted component system. Eight new conceptual illustrations were made with Qwen Image 3.0 Pro through official DashScope, using only the approved public hero illustration as a style reference. They depict the user's research and creative themes, not measurements or project outcomes. Sanitized task IDs, prompts and file hashes are recorded in assets/components/provenance.json.

Project cards preserve original project logos and distinct brand colours. Desktop and mobile layouts, tool shelves, disclosure controls and link buttons are generated locally by scripts/profile_components.py and scripts/generate_readme.py. See COMPONENTS.md for the component contract. Existing statistics, timestamps, daily workflows, project source covers and original icon files remain available. Redundant typing/separator decorations and duplicate navigation are no longer part of the active layout.

The previous React Bits Aurora shader is no longer executed by the current site. Its existing license and historical attribution remain in the repository. GitHub's native details and picture elements provide folding and theme-responsive artwork; no third-party JavaScript widget is added by this component update.
