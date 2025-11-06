from fastapi import FastAPI, Request, Form, Response, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from helper.engine import StickerMaker
from pathlib import Path
import io
import os
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent

FONT_MAP = {
    "bali": BASE_DIR / "static/font/bali__vimala.ttf",
    "batak": BASE_DIR / "static/font/batak__Batak-Unicode-Regular Final.otf",
    "jawa": BASE_DIR / "static/font/jawa__nyk Ngayogyan New Italic.ttf",
    "kawi": BASE_DIR / "static/font/kawi__Kawi Roman.ttf",
    "pegon": BASE_DIR / "static/font/pegon__JAWI-Readex Pro-biasa.ttf",
    "rejang": BASE_DIR / "static/font/rejang__NotoRejang.ttf",
    "sunda": BASE_DIR / "static/font/sunda__AwiGombong.ttf",
}

SCHEMES = sorted(FONT_MAP.keys())

TEMP_UPLOAD_DIR = BASE_DIR / "temp_uploads"
TEMP_UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Aksara Nusantara Sticker Generator")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "schemes": SCHEMES,
        "default_text": "Coba tulis aksara Jawa",
        "default_scheme": "jawa"
    })


@app.post("/generate_sticker")
async def generate_sticker(
    text_input: str = Form(..., alias="text_input"),
    scheme_name: str = Form(..., alias="scheme_name"),
    font_size: int = Form(150, alias="font_size"),
    text_color: str = Form("#000000", alias="text_color"),
    border_size: int = Form(12, alias="border_size"),
    shadow_blur: int = Form(10, alias="shadow_blur"),
    output_type: str = Form("png_small", alias="output_type"),
    image_file: UploadFile = File(None, alias="image_file"),
    scale_factor: float = Form(1.0, alias="scale_factor"),
    combine_mode: str = Form("text_only", alias="combine_mode")
):
    if scheme_name not in FONT_MAP:
        raise HTTPException(status_code=400, detail=f"Unsupported script scheme: {scheme_name}")
    
    font_path = FONT_MAP[scheme_name]
    if not font_path.exists():
        raise HTTPException(status_code=500, detail=f"Font file not found: {font_path}")

    try:
        r = int(text_color[1:3], 16)
        g = int(text_color[3:5], 16)
        b = int(text_color[5:7], 16)
        text_color_rgba = (r, g, b, 255)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid text color format.")

    sticker_maker = StickerMaker(
        font_path=str(font_path),
        font_size=font_size,
        text_color=text_color_rgba,
        border_size=border_size,
        border_color=(255, 255, 255, 255), 
        shadow_blur_strength=shadow_blur,
        padding=40,
        bg_transparent=True,
        crop=True,
    )
    
    file_content = None
    content_type = None
    
    try:
        if combine_mode == 'text_only' or not image_file or image_file.filename == '':
            file_content, content_type = sticker_maker.process_request(
                input_text=text_input,
                scheme_name=scheme_name,
                output_type=output_type
            )
            
        else:
            temp_image_path = TEMP_UPLOAD_DIR / f"upload_{os.getpid()}.png"
            try:
                with open(temp_image_path, "wb") as f:
                    f.write(await image_file.read())
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Could not save uploaded image: {e}")

            output_buffer = io.BytesIO()
            sticker_maker.process_combined_sticker(
                image_path=temp_image_path,
                input_text=text_input,
                scheme_name=scheme_name,
                mode=combine_mode,
                scale=scale_factor,
                output_path=output_buffer
            )
            output_buffer.seek(0)
            file_content = output_buffer.read()
            content_type = 'image/png'
            os.remove(temp_image_path)
            
        
        if file_content is None:
             raise HTTPException(status_code=500, detail="File content generation failed.")

        output_buffer = io.BytesIO(file_content)
        print(f"[SERVER END] Sticker generation complete. Type: {content_type}")
        
    except Exception as e:
        print(f"Error during sticker generation: {e}")
        if 'temp_image_path' in locals() and temp_image_path.exists():
             os.remove(temp_image_path)
        raise HTTPException(status_code=500, detail=f"Sticker generation failed: {e}")

    return StreamingResponse(output_buffer, media_type=content_type)