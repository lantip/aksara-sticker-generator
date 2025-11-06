# Aksara Nusantara Sticker Generator

A powerful Python utility built with **Pillow (PIL)**, **svgwrite**, and **fontTools** for generating high-quality text stickers in Indonesian traditional scripts (Aksara Nusantara). It can automatically transcribe Latin text into regional scripts and render them as bordered, shadowed, and scalable stickers — optionally combined with images.

---

## ✨ Features

* **Automatic Transcription:** Converts Latin text (e.g., `kebo nyusu gudèl`) into various Aksara scripts like *Kawi*, *Javanese*, or *Balinese* using the `ScriptConverter` module.
* **Accurate Vector Rendering:** Leverages `uharfbuzz` and `fontTools` for precise SVG generation with complex glyphs, falling back to PIL rendering when needed.
* **Custom Sticker Effects:** Apply customizable borders, shadows, and paddings for polished results.
* **Flexible Combination Modes:** Combine text with images in overlay or stacked layouts.
* **Multi-Format Output:** Generate both PNG (`png_small`, `png_high`) and SVG outputs with consistent visual quality.

---

## ⚙️ Installation

### Prerequisites

* **Python 3.8+**
* The following libraries:

  * `Pillow`
  * `svgwrite`
  * `fontTools`
  * `uharfbuzz`
  * `cairosvg`

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/lantip/aksara-sticker-generator
   cd aksara-sticker-generator
   ```

2. **Install dependencies:**

   ```bash
   pip install Pillow svgwrite fontTools uharfbuzz cairosvg
   ```

   > ⚠️ *Note:* `cairosvg` may require system libraries like `cairo`. Refer to its documentation if installation issues occur.

3. **Add Font Files:**
   Place your `.ttf` or `.otf` font files (for the desired Aksara script) in a known path and reference it in `StickerMaker(font_path=...)`.

---

## 🚀 Quick Start

### Example: Generate a High-Resolution Text Sticker

```python
from sticker_generator import StickerMaker
from pathlib import Path

maker = StickerMaker(
    font_path="./fonts/AksaraFont.ttf",
    font_size=150,
    border_size=12,
    shadow_blur_strength=5,
    text_color=(255, 0, 0, 255)  # Red
)

output_data, content_type = maker.process_request(
    input_text="aksara jawa",
    scheme_name="kawi",
    output_type="png_high"
)

if output_data:
    with open("aksara_jawa_sticker.png", "wb") as f:
        f.write(output_data)
    print("Sticker saved successfully!")
```

### Example: Combine Image and Text (Overlay)

```python
output_file = maker.process_combined_sticker(
    image_path=Path("./kebo.png"),
    input_text="kebo nyusu gudèl",
    scheme_name="kawi",
    mode="over",        # Overlay text on image
    scale=1.0,
    output_path=Path("kebo_overlay_sticker.png")
)
print(f"Combined sticker saved to: {output_file}")
```

---

## ⚙️ Configuration Parameters

| Parameter              | Default                | Description                                           |
| ---------------------- | ---------------------- | ----------------------------------------------------- |
| `font_path`            | `None`                 | Path to TTF/OTF font for Aksara rendering (required). |
| `font_size`            | `100`                  | Base font size in pixels.                             |
| `text_color`           | `(0, 0, 0, 255)`       | RGBA fill color for text.                             |
| `border_size`          | `10`                   | Thickness of the border around content.               |
| `border_color`         | `(255, 255, 255, 255)` | RGBA color for the border.                            |
| `shadow_blur_strength` | `6`                    | Gaussian blur strength for shadows.                   |
| `padding`              | `20`                   | Extra transparent padding space.                      |
| `bg_transparent`       | `True`                 | If `False`, uses solid background color.              |

### Combination Modes

| Mode           | Description                                     |
| -------------- | ----------------------------------------------- |
| `over`         | Text centered and overlaid on top of the image. |
| `v_image_text` | Image on top, text stacked below.               |
| `v_text_image` | Text on top, image stacked below.               |

---

## 🧠 Internals

### `ScriptConverter`

Handles Latin-to-Aksara transcription based on specific schemes (`kawi`, `javanese_standard`, etc.). 

### Scaling & Resolution

* **`png_small`** → scale = 1.0 → Suitable for quick previews and chat stickers.
* **`png_high`** → scale = 4.0 → Ideal for print or HD usage.

---

## 📜 License & Ethics

This project is released under the **ABRMS License**, meaning:

* You can freely use, modify, distribute, and even sell derivative works.
* **No warranty** is provided.
* However, we encourage every user who gains financially from this project to **donate a portion of their revenue to the poor or to educational causes.**

> “Ilmu yang bermanfaat adalah ilmu yang dibagikan.”
> — Semangat Gotong Royong Nusantara 🇮🇩

---

## 🌐 Acknowledgements

* [Tabler.io](https://tabler.io) for the beautiful UI components
* [Fastapi](https://fastapi.tiangolo.com/) for simplicity and flexibility
* Educators and cultural activists who preserve Aksara Nusantara
* [Firdavs Shodiev](https://github.com/Firdavs-coder) — for the insight.
* Open-source community contributors everywhere 🌏 — your shared knowledge makes this project possible.

---

### 🧑‍🛏️ Contact

For suggestions or collaboration, please visit:
👉 [GitHub Repository](https://github.com/lantip/aksara-sticker-generator)

---

### ❤️ Support the Mission

If this project helps your teaching, community, or organization —
please share it, contribute back, or help those in need.
That’s how we keep the spirit of **Nusantara** alive.
