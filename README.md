# JSON Checker site

Static site for the Chrome extension: home, post-install welcome, help, and
privacy. Plain HTML and CSS — no build step. Copy the folder to any static host
(GitHub Pages works as-is).

```
index.html              Home — product pitch + Install
welcome/index.html      Post-install: pin (1–2), then open (3)
welcome/next/index.html Redirect to ../#open  (old link)
help/index.html         How to open, check, and fix
privacy/index.html      Privacy policy for the Web Store listing
assets/welcome.css
assets/img/             Screenshots as WebP, 1x and 2x, light and dark
tools/prepare_screens.py
```

Paths between the files are relative, so the site opens from disk for a preview
and keeps working under any prefix on a server (including
`https://USER.github.io/REPO/`).

| URL | Page |
| --- | --- |
| `/` | Home |
| `/welcome/` | Welcome (open after install) |
| `/help/` | Help / support URL |
| `/privacy/` | Privacy policy URL |

## Install button

Every page links Install to:

```
https://chromewebstore.google.com/detail/json-checker/kpglnjajdcmgpbokcnkffecbnemopnkm
```

## Light and dark

The theme follows `prefers-color-scheme`. Page colours come from custom
properties in one media query, and each screenshot exists twice: `<picture>`
picks the matching file. There is no theme toggle and no JavaScript.

## Rebuilding the screenshots

Source captures live in the project root as `7.png` … `10.png`: the extensions
menu (`7` dark, `9` light) and the pinned icon (`8` dark, `10` light). All four
are full Chrome windows, 3420 × 2146, taken with an English interface and the
same window geometry, which is what keeps the markers aligned across themes.

```bash
python3 welcome-site/tools/prepare_screens.py   # needs Pillow
```

The script paints out the macOS window buttons, the new tab page shortcut
tiles, the "Add extensions" promo card and the Gmail/Images row, crops the
empty bottom of the page and writes 1000 px and 2000 px WebP. The row next to
the extensions popup is rebuilt by copying a clean row from below rather than
filled flat, so the popup's drop shadow survives.

If the captures are ever retaken, the marker coordinates in `welcome/index.html`
have to follow. They live in inline `<svg>` overlays whose `viewBox` is the
cropped image, `0 0 3420 1700`, so every circle and arrow is written in original
screenshot pixels — no percentages to recompute.

## Opening welcome on install

Once the site is live, add this to `json-checker/src/background/index.ts`:

```ts
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    void chrome.tabs.create({ url: 'https://YOUR-DOMAIN/welcome/' })
  }
})
```

For a GitHub Pages project site the URL is
`https://USER.github.io/REPO/welcome/` (keep the trailing slash).

Use `/help/` as the Web Store support URL and `/privacy/` as the privacy policy
URL.
