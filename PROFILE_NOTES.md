# Profile maintenance

Updated: 2026-10-27. The profile repository stays directly in its existing root.

- README.md and README.en.md are synchronized Chinese and English GitHub profiles. index.html, styles.css and script.js are the static portfolio.
- assets/profile/ contains original SVG artwork and a copy of the owner's existing brand logo. Project covers in assets/showcase/ follow the owner-supplied OmniForge composition: identity and introduction on the left, a conceptual workspace on the right, with project-specific accent colors. The artwork is illustrative, not experiment output.
- The portfolio needs no build step or external JavaScript. Preview: python -m http.server 8768 --bind 127.0.0.1.
- GitHub Pages publishes main at https://rainbowyuyu.github.io/rainbowyuyu/. Existing assets remain in place.
- PhysCast and OmniForge are described with the owner's permission; their source repositories stay private. Do not insert private memory, conversation exports, credentials or infrastructure details here.
- The public identity is rainbow鱼, with the user-confirmed affiliation 浙江大学博士 / PhD researcher at Zhejiang University. Real names must not appear in public copy, metadata or generated cards. Department, graduation status, awards and publication claims are not inferred.

## Reference sites and source repositories reviewed

- https://github.com/antfu — clear personal identity and compact navigation.
- https://github.com/DenverCoder1 — project-first organization and distinct content sections.
- https://brittanychiang.com/ — restrained dark palette, typography, project hierarchy and readable spacing.
- https://github.com/brunosimon/folio-2025 — the public repository metadata and README describe a coordinated physics/input/render loop and model compression. This informed interaction and performance priorities; it is a source review, not a claim of in-depth testing of the live portfolio.
- https://dennissnellenberg.com/ — project imagery, typographic hierarchy and restrained interaction.
- https://rbp-portfolio.vercel.app/ — pill navigation, layered project presentation and shader-backed motion; component attribution is in THIRD_PARTY_NOTICES.md.

The profile restores its original small animated technology icons and mascots. The website uses an attributed React Bits Aurora shader adaptation and the README uses locally cached open-source icon widgets; see THIRD_PARTY_NOTICES.md and assets/readme/ATTRIBUTION.md for sources and licenses. Original repository covers remain available as supporting artwork.

## Verification

Verify desktop/mobile layout, each single-column project's expand/collapse control, project-specific logo and color, command-palette search and keyboard navigation, language switching, pause control, reduced-motion handling, image loading and all local links before publishing. English entry links use ?lang=en; project fragments must match the IDs shared by both language views. Keep README.md and README.en.md project order, links and factual qualifications synchronized.

Keep scientific claims tied to repository evidence. Contribution animations and daily activity cards remain in a dedicated observatory section; their scheduled workflows are maintained separately. Snake generation updates only its designated assets and cannot replace the website branch contents. Check the latest source timestamp before describing a card as current; keep unavailable-source states honest.

### 2026-10-27 previous cover-layout acceptance

Ego Lite validation covered the desktop layout, 390px and 320px mobile layouts, both languages, light/dark themes, seven project covers and detail controls, command search/Enter/Escape, motion pause and the operating-system reduced-motion preference. All 36 website images loaded. Both 320px language views have equal client and scroll widths; header controls are 44px square. The GitHub-rendered local README preview also fit 390px with no broken images. These are browser checks, not a claim of cross-device exhaustive testing.

## Paired light and dark presentation

The 2026-10-27 theme update passed local Ego Lite acceptance at 1440, 768, 390 and 320 CSS pixels in both themes, including Chinese and English views. All 36 site images loaded without horizontal overflow; seven paired covers and full-art links followed the manual theme even with the opposite OS preference. System-default selection, persistence, expansion, command search/Enter/Escape, bilingual controls, pause and reduced-motion alternatives passed. The GitHub-rendered README preview passed 1440/390px checks in both themes. These are bounded browser checks, not exhaustive cross-device testing; deployment status is available in GitHub Actions.

- The website uses a graphite ground (`#151b20`) and a cool paper-white ground (`#f6f8fa`), with coordinated text, controls, surfaces and image sources. Project colours remain distinct. This is explicit paired artwork, not an inversion filter.
- The website defaults to `prefers-color-scheme` and exposes explicit System / Light / Dark choices. Only a valid `rainbow-theme-v2` choice is used; legacy `rainbow-theme` values remain untouched and no longer override the default. The head script and runtime resolve the same preference before painting. System changes remain live in System mode, and a manual choice persists across visits. Hero covers, full project covers, enlarged-artwork links, metrics and contribution alternatives follow the resolved theme. The menu supports keyboard navigation, Escape, outside-click dismissal and both languages.
- GitHub README documents use supported `<picture>` sources for dark and light colour schemes, with light artwork as the fallback. GitHub controls its own page background; source selection supplies matching banner, buttons, text animation, seven project covers and metric cards. Both languages are generated from one source.
- All seven approved 1600×800 dark covers retain their original paths and composition. Each has a `-light.webp` counterpart and editable `-cover-light.svg` source. `assets/catalog/manifest.json` records theme paths, sizes, accents and integrity hashes. Pale original logos keep their appearance on compact slate mounting tiles where needed.
- The 41 README artwork pairs (82 SVGs) are regenerated by `python scripts/generate_readme.py`, together with README.md and README.en.md. Seven footer destinations have paired icon buttons in both languages. The original technology icons, mascots, contribution animations and existing project source artwork remain available.
- The 17 saved metric SVGs have separate `-light.svg` and `-dark.svg` display variants. `python scripts/generate_activity_themes.py` regenerates them without API calls, data changes or freshness changes. It preserves source text and timestamps, including archived cards. Never label an archive as newly refreshed because its colours changed.
- The existing daily metrics workflow calls `scripts/update_activity.py --kind metrics`, which now regenerates both metric themes. `scripts/commit_activity.py` includes only the owned source cards, paired metric variants and status file in its normal non-force push. Snake and 3D schedules also retain theme-appropriate static alternatives for paused or reduced-motion presentation. Daily schedules and their freshness policy remain unchanged.

To rebuild the seven light project covers, run `python scripts/generate_cover_themes.py` with Python 3.10+, Node.js and `sharp` available. An installation outside Node's module lookup can be supplied through `--sharp-module <module-directory>`. The script resolves the repository from its own location, preserves approved dark images and original logo markup, and updates the manifest after rendering. Do not put workstation paths in the repository.

Taste Skill provided art-direction guidance for this restyle: neutral surfaces, stronger text contrast, consistent geometry and purposeful colour. Reviewed source: `Leonxlnx/taste-skill`, commit `12af471f627f866411b4bd785b19646d3672784c`, `skills/taste-skill/SKILL.md` and its colour reference. The selected direction was `contact-sheet`, seed `1811425364`; the user's existing single-column project layout, brand colours, approved cover composition and retained animations take priority over generic defaults. No Taste Skill frontend component, runtime or webpage template is bundled into the site.

## Compact projects and readable activity cards

The GitHub profile initially shows PhysCast, OmniForge and Wiscomper. Four additional projects retain their descriptions and covers inside a closed native details element in both languages. The separate website keeps all seven project rows. The independent historical-card disclosure remains closed by default.

The seven active cards use `scripts/activity_card_renderer.py`, with clearer numerical hierarchy, paired graphite/paper surfaces and visible data qualifications. Four compact cards display at 420 CSS pixels on wide README layouts and become a single column on phones. Their 480-by-372 canvas includes 12 transparent pixels at the bottom for space between stacked cards. The contribution streak is a separate 720-pixel card with the original mascots above it. Existing snake and 3D contribution artwork remains intact.

Each active SVG stores only its public aggregate snapshot in `metadata#activity-snapshot`. The daily updater writes this schema and the shared renderer produces both themes. Repainting saved data does not call APIs or change the source timestamp. This redesign preserves the saved 2026-10-27 11:41:07 UTC snapshot, including recorded WakaTime 0.0 hours. The previous activity SVG stored only normalized curve coordinates; migration preserves that curve without inventing exact event counts. Archive cards retain their original semantics and dates.

Local acceptance covered real Ego Lite interaction with System/Light/Dark, persistence, system changes, keyboard dismissal and menu bounds at 320/390/768/1440 pixels. GitHub Markdown API output and browser interaction verified 3 visible projects, 7 after expansion and 3 after collapse in both languages. Desktop/mobile previews verified paired card themes, all seven footer buttons and intact assets. Automated checks cover the theme state machine, snapshot equality, deterministic regeneration, daily success/failure paths, large-number spacing, XML safety, local links and public-identity privacy. GitHub Actions records deployment status; local acceptance alone does not imply publication.
