# Esatinproje

> Engineering README reviewed from the repository state on 2026-09-05. Observed facts are separated from items that still need manual verification.

**Repository:** [parzidev/esatinproje](https://github.com/parzidev/esatinproje)  
**Visibility:** public  
**Default branch:** `main`  
**Latest GitHub push observed:** `2026-08-29T09:12:06Z`  
**Scanned HEAD:** `7a3ed964c63022a6a7d67f580780f28d59bae2c7`  
**Repository description:** kart oyunu

## Purpose and scope

A browser-based collectible card/game experiment with a large locally stored card and artwork catalogue.

The repository currently contains **318** source-tree files, including **17** code-like files. This README describes the repository as it exists in the scanned snapshot; it is not a claim that every historical or runtime path is still active.

## Capability inventory

### README evidence

The source README exposes these sections: `Esat Card Project`, `What this project includes`, `Technology`, `Repository structure`, `Getting started`, `Configuration and data`, `Development and validation`, `Security and responsible use`, `Project status`, `License`.

### Detected technology profile

| `Python` | 13 code-like files |
| `JavaScript` | 2 code-like files |
| `CSS` | 1 code-like files |
| `HTML` | 1 code-like files |

### Project structure

Top-level paths observed:

- `README.md`
- `app.js`
- `cards`
- `index.html`
- `kartlar_tam.json`
- `rare`
- `scraper xd`
- `script.js`
- `style.css`
- `type`

Key entrypoint candidates:

- `app.js`
- `index.html`
- `scraper xd/main.py`

## Architecture and runtime shape

| Area | Observed evidence |
| --- | --- |
| Entrypoint candidates | `app.js`, `index.html`, `scraper xd/main.py` |

Interpretation boundary: filenames and manifests show where a component may start, but they do not prove deployment topology, request flow, persistence semantics, or production readiness. Those items should be confirmed against the implementation before making operational claims about the project.

## Code-level signals

The following patterns were extracted from readable code files. They are navigation aids for the next human review, not a substitute for reading the implementation:

**Integration/framework keywords:** `Discord`, `Riot`

**Named functions/classes/types observed:** `loadData`, `getDailyTarget`, `isSameDay`, `restoreState`, `saveState`, `showMessage`, `updateUI`, `gameWon`, `renderGuesses`, `renderFeedbackRow`, `getMatchClass`, `handleGuess`, `revealTarget`, `shareResults`, `html_ile_kart_bilgilerini_al`, `kart_bilgilerini_al_worker`, `tum_kartlari_tara`, `json_olustur`, `kart_bilgilerini_cek`, `kart_detaylarini_al`, `klasor_kart_eslestir`, `main`, `kart_tipine_gore_deger_ata`, `dosya_adina_gore_deger_ata`, `kartlari_isle`, `klasor_adina_gore_tip_ata`, `isime_gore_deger_ata`, `kart_detaylarini_cek`, `selenium_ile_kart_bilgilerini_al`, `offline_kart_bilgilerini_al`, `kart_bilgilerini_al`, `nadirligi_ekle`, `offline_kart_bilgilerini_topla`, `ornek_html_parse`, `mevcut_klasorler_ile_eslestir`, `initLanguage`, `applyTranslations`, `getImagePath`, `initGame`, `updateBlur`, `closeAllLists`, `submitGuess`, `renderGuess`, `createAttributeBox`, `createNumericAttributeBox`, `endGame`, `showWinModal`

**Top-level import/module signals:** `os`, `json`, `requests`, `time`, `bs4`, `tqdm`, `concurrent.futures`, `re`, `selenium`, `selenium.webdriver.common.by`, `selenium.webdriver.chrome.options`, `selenium.webdriver.support.ui`, `selenium.webdriver.support`, `selenium.common.exceptions`, `argparse`, `kart_degerlerini_ekle_v2`, `nadirligi_ekle`, `PIL`, `io`, `random`

## Setup and operation

The most relevant source README material is reproduced below:

## Getting started

For browser-based content, serve the relevant directory over HTTP:
```bash
python3 -m http.server 8000
```
Open `http://localhost:8000/` or the selected subdirectory.

## Configuration and data

- Keep relative paths intact when deploying the locally stored data and assets.
- Scraping utilities are separate from normal browser use and may have their own dependencies or source-site constraints.

Static setup/deployment evidence:

- Docker files: none detected
- Build/config manifests: none detected
- Configuration-like paths: none detected

### Command evidence

```bash
python3 -m http.server 8000
```

## API, integrations, and data flow

No API/integration section was detected in the source README. External boundaries require code-level review before publication.

Before publishing a public README, confirm the following from code and deployment configuration:

- inbound routes, ports, webhooks, and authentication middleware;
- outbound providers, rate limits, retries, and failure behavior;
- persistence files/databases and backup/restore expectations;
- whether any endpoint can mutate external state.

## Configuration and secrets

Detected names (names only; values were intentionally excluded):

No conventional environment-variable names were detected in the sampled manifests/entrypoints.

Configuration paths observed:

- None detected in the static scan.

Do not paste real tokens, passwords, private keys, cookies, or production URLs into this README or a public README. Replace them with placeholders and document where the operator should provision them.

## Security and privacy

## Security and responsible use

- Only run scraping utilities against sources you are authorized to access and respect site terms and rate limits.
- Review third-party artwork and data licensing before redistributing a hosted copy.

Minimum publication checklist:

- document trust boundaries and the intended network exposure;
- explain authentication and authorization separately;
- state whether logs, uploads, identifiers, or third-party data are retained;
- include a responsible-use note where the project interacts with Steam, Kick, Riot, Spotify, Cloudflare, or other external platforms;
- keep example configuration values synthetic.

## Validation and maintenance

## Development and validation

- Keep changes focused on the relevant module or subproject and verify the user-facing path manually before publishing.
- Do not commit generated build output, local environments, caches, logs, or credentials unless an artifact is intentionally retained as source material.

Test-like paths were detected, but no tests were executed during this documentation-only scan.

Test-like paths observed:

- `cards/Units/Spectral Matron.webp`
- `scraper xd/test.py`

CI/workflow and maintenance evidence should be verified before adding badges or claiming release guarantees.

## Known gaps and verification notes

- Repository snapshot was available for static inspection.
- This was a static documentation scan; no repository code, containers, network services, or test suites were executed.
- “Detected” means a filename, README section, manifest, or sampled entrypoint matched the scanner; it is not a security audit.
- README sections may describe an older state than the current code. Compare the published README with the latest default-branch files before committing it upstream.

## Reference README material (sanitized)

The relevant source README is retained below as reference material, with credential-shaped values removed.

# Esat Card Project

A browser-based collectible card/game experiment with a large locally stored card and artwork catalogue.

The repository combines a static web interface, game data, themed card sets, and utility scripts used to gather or prepare assets. It can be explored as a frontend prototype without a compilation step.

## What this project includes

- Interactive card-oriented browser UI
- Multiple card types and rarity groups
- Locally bundled artwork and structured data
- Utility scripts for collecting or transforming content
- Static hosting compatibility

## Technology

- HTML
- CSS
- JavaScript
- JSON data
- Python utility scripts

## Repository structure

- `index.html` — Main browser entry point.
- `app.js` — Client-side behavior.
- `cards/` — Card definitions or assets.
- `rare/` — Rarity content.
- `type/` — Type content.

## Getting started

For browser-based content, serve the relevant directory over HTTP:
```bash
python3 -m http.server 8000
```
Open `http://localhost:8000/` or the selected subdirectory.

## Configuration and data

- Keep relative paths intact when deploying the locally stored data and assets.
- Scraping utilities are separate from normal browser use and may have their own dependencies or source-site constraints.

## Development and validation

- Keep changes focused on the relevant module or subproject and verify the user-facing path manually before publishing.
- Do not commit generated build output, local environments, caches, logs, or credentials unless an artifact is intentionally retained as source material.

## Security and responsible use

- Only run scraping utilities against sources you are authorized to access and respect site terms and rate limits.
- Review third-party artwork and data licensing before redistributing a hosted copy.

## Project status

An experimental game and asset archive. Browser features and utility scripts may be at different levels of completeness.

## License

No repository-wide license file is currently provided. Unless the owner grants permission, all rights are reserved.
