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
