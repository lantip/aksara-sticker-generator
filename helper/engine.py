from typing import Dict, List, Tuple
from PIL import Image, ImageFilter, ImageChops, ImageDraw, ImageFont
import svgwrite
import os
import io
from fontTools.ttLib import TTFont 
from fontTools.pens.svgPathPen import SVGPathPen as SVGPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
import xml.etree.ElementTree as ET
from pathlib import Path
import uharfbuzz as hb
from .utils import ScriptConverter

class StickerMaker:
    def __init__(
        self,
        alpha_threshold=10,
        border_size=10,
        border_color=(255, 255, 255, 255),
        shadow_size=0,
        shadow_color=(0, 0, 0),
        shadow_transparency=100,
        shadow_blur_strength=6,
        padding=20,
        bg_color=(255, 255, 255, 255),
        bg_transparent=True,
        crop=True,
        font_path: str = None, 
        font_size: int = 100,  
        text_color: tuple = (0, 0, 0, 255) 
    ):

        self.alpha_threshold = alpha_threshold
        self.border_size = border_size
        self.border_color = border_color
        self.shadow_size = shadow_size
        self.shadow_color = shadow_color
        self.shadow_transparency = shadow_transparency
        self.shadow_blur_strength = shadow_blur_strength
        self.padding = padding
        self.bg_color = bg_color
        self.bg_transparent = bg_transparent
        self.crop = crop
        
        self.font_path = font_path
        self.font_size = font_size
        self.text_color = text_color
        
        if self.font_path:
            try:
                self.font = ImageFont.truetype(self.font_path, self.font_size)
                self.ttfont = TTFont(self.font_path)
                with open(self.font_path, 'rb') as f:
                    self.hb_font_data = f.read()
                self.hb_font = hb.Font(hb.Face(self.hb_font_data))
            except IOError:
                self.font = ImageFont.load_default()
                self.ttfont = None
                self.hb_font = None
        else:
            self.font = ImageFont.load_default()
            self.ttfont = None
            self.hb_font = None

    def _to_hex_color(self, rgba):
        return f"#{rgba[0]:02x}{rgba[1]:02x}{rgba[2]:02x}"

    def crop_transparent(self, image: Image.Image) -> Image.Image:
        if image.mode != "RGBA":
            raise ValueError("Image must be in RGBA mode for transparency detection.")
            
        bbox = image.getbbox()

        if bbox:
            left, upper, right, lower = bbox
            left = max(0, left - self.padding)
            upper = max(0, upper - self.padding)
            right = min(image.width, right + self.padding)
            lower = min(image.height, lower + self.padding)
            return image.crop((left, upper, right, lower))
        else:
            print("Image is fully transparent.")
            return image
    

    def _render_text_as_svg_paths(self, script_text: str, font_size_units: int) -> str:
        if not self.ttfont or not self.hb_font:
            return ""

        upem = self.ttfont['head'].unitsPerEm
        gs = self.ttfont.getGlyphSet()
        
        try:
            ascender = self.ttfont['hhea'].ascender
            descender = self.ttfont['hhea'].descender
        except:
            ascender = upem * 0.8
            descender = -upem * 0.2
            
        svg_visual_padding = self.padding + self.border_size 
        scale = font_size_units / upem
        
        scaled_font_height = (ascender - descender) * scale
        final_svg_height = scaled_font_height + (svg_visual_padding * 2)
        baseline_y_translation = svg_visual_padding + (ascender * scale)
        
        buf = hb.Buffer()
        buf.add_str(script_text)
        buf.guess_segment_properties()
        hb.shape(self.hb_font, buf, {})
        
        glyph_infos = buf.glyph_infos
        glyph_positions = buf.glyph_positions
        
        fill_pen = SVGPen(gs)
        border_pen = SVGPen(gs)
        current_x_offset_upem = 0 
        
        for info, pos in zip(glyph_infos, glyph_positions):
            glyph_name = self.ttfont.getGlyphName(info.codepoint)
            
            if glyph_name == '.notdef':
                current_x_offset_upem += pos.x_advance
                continue
            
            try:
                glyph = gs[glyph_name]
            except Exception:
                current_x_offset_upem += pos.x_advance
                continue
                
            tx = current_x_offset_upem + pos.x_offset
            ty = pos.y_offset
            
            try:
                tp_fill = TransformPen(fill_pen, Transform().translate(tx, ty))
                glyph.draw(tp_fill)
                
                tp_border = TransformPen(border_pen, Transform().translate(tx, ty))
                glyph.draw(tp_border)
                
            except Exception:
                pass
            
            current_x_offset_upem += pos.x_advance
            
        combined_path_data = fill_pen.getCommands()
        combined_path_data_border = border_pen.getCommands()
        
        if not combined_path_data:
            dwg = svgwrite.Drawing(size=('10px', '10px'), debug=True)
            return dwg.tostring()
            
        actual_path_width = current_x_offset_upem * scale
        final_svg_width = actual_path_width + (svg_visual_padding * 2)
        
        dwg = svgwrite.Drawing(size=(f'{final_svg_width}px', f'{final_svg_height}px'), debug=True)
        
        x_translation_svg = svg_visual_padding
        y_translation_svg = baseline_y_translation
        
        final_transform = Transform(scale, 0, 0, -scale, x_translation_svg, y_translation_svg)

        a, b, c, d, e, f = final_transform
        transform_string = f"matrix({a:.6f},{b:.6f},{c:.6f},{d:.6f},{e:.6f},{f:.6f})"
        
        if self.border_size < 23:
            bordersize = 23
        else:
            bordersize = self.border_size

        border_path_elem = dwg.path(
            d=combined_path_data_border,
            fill='none',
            stroke=self._to_hex_color((192, 192, 192, 255),),
            stroke_width=bordersize,
            stroke_linejoin='round',
            stroke_linecap='round',
            transform=transform_string
        )
        dwg.add(border_path_elem)

        text_path_elem = dwg.path(
            d=combined_path_data,
            fill=self._to_hex_color(self.text_color),
            transform=transform_string
        )
        dwg.add(text_path_elem)

        return dwg.tostring()

    def render_text_to_svg(self, text: str, scheme_name: str) -> str:
        script_text = ScriptConverter.convert_to_script(text, scheme_name=scheme_name)
        svg_unit_size = 200 
        return self._render_text_as_svg_paths(script_text, svg_unit_size)

    def _make_sticker_from_img(self, img: Image.Image, scale_factor: float = 1.0) -> Image.Image:
        if img.mode != "RGBA":
             img = img.convert("RGBA")

        if self.crop:
            img = self.crop_transparent(img)
        
        scaled_border_size = int(self.border_size * scale_factor)
        scaled_shadow_blur = self.shadow_blur_strength * scale_factor

        alpha = img.getchannel("A")
        mask = alpha.point(lambda p: 255 if p > self.alpha_threshold else 0)

        dilated = mask.filter(ImageFilter.MaxFilter(scaled_border_size * 2 + 1))
        border_mask = ImageChops.subtract(dilated, mask)
        border_mask = border_mask.filter(ImageFilter.GaussianBlur(radius=1.5)) 

        white_border_layer = Image.new("RGBA", img.size, self.border_color) 
        white_border_layer.putalpha(border_mask)
        
        shadow_layer = Image.new("RGBA", img.size, (*self.shadow_color, int(255 * (self.shadow_transparency/100))))
        shadow_mask = dilated.filter(ImageFilter.GaussianBlur(radius=scaled_shadow_blur))
        shadow_layer.putalpha(shadow_mask)

        final = Image.new("RGBA", img.size, (0, 0, 0, 0))
        final = Image.alpha_composite(final, shadow_layer)
        final = Image.alpha_composite(final, white_border_layer)
        final = Image.alpha_composite(final, img)

        return final

    def make_image_sticker(self, image_path: Path, scale_factor: float = 1.0) -> Image.Image:
        img = Image.open(image_path).convert("RGBA")
        
        if scale_factor != 1.0:
            new_width = int(img.width * scale_factor)
            new_height = int(img.height * scale_factor)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        return self._make_sticker_from_img(img, scale_factor=1.0)

    def make_sticker_from_image(self, img: Image.Image, scale_factor: float = 1.0) -> Image.Image:
        if img.mode != "RGBA":
             img = img.convert("RGBA")

        if self.crop:
            img = self.crop_transparent(img)
        
        scaled_border_size = int(self.border_size * scale_factor)
        scaled_shadow_blur = self.shadow_blur_strength * scale_factor

        alpha = img.getchannel("A")
        mask = alpha.point(lambda p: 255 if p > self.alpha_threshold else 0)

        dilated = mask.filter(ImageFilter.MaxFilter(scaled_border_size * 2 + 1))
        border_mask = ImageChops.subtract(dilated, mask)
        
        border_mask = border_mask.filter(ImageFilter.GaussianBlur(radius=1.5)) 

        white_border_layer = Image.new("RGBA", img.size, self.border_color) 
        white_border_layer.putalpha(border_mask)
        
        shadow_layer = Image.new("RGBA", img.size, (*self.shadow_color, int(255 * (self.shadow_transparency/100))))

        shadow_mask = dilated.filter(ImageFilter.GaussianBlur(radius=scaled_shadow_blur))
        shadow_layer.putalpha(shadow_mask)

        final = Image.new("RGBA", img.size, (0, 0, 0, 0))
        
        final = Image.alpha_composite(final, shadow_layer)
        
        final = Image.alpha_composite(final, white_border_layer)
        
        final = Image.alpha_composite(final, img)

        if not self.bg_transparent:
            solid_bg = Image.new("RGBA", final.size, self.bg_color)
            solid_bg.paste(final, (0, 0), final)
            return solid_bg

        return final

    def render_text_to_image(self, text: str, scheme_name: str, scale_factor: float = 1.0) -> Image.Image:
        script_text = ScriptConverter.convert_to_script(text, scheme_name=scheme_name)
        
        scaled_font_size = int(self.font_size * scale_factor)
        scaled_border_size = int(self.border_size * scale_factor)
        scaled_padding = int(self.padding * scale_factor)
        scaled_shadow_blur = int(self.shadow_blur_strength * scale_factor)
        
        if self.font_path:
            font = ImageFont.truetype(self.font_path, scaled_font_size)
        else:
            font = ImageFont.load_default()

        temp_img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        
        mask = font.getmask(script_text, "L")

        text_left, text_upper, text_right, text_lower = mask.getbbox()
        text_width = text_right - text_left
        text_height = text_lower - text_upper            
        
        buffer_padding = (scaled_border_size * 2) + (scaled_shadow_blur * 2) + scaled_padding
        canvas_width = max(1, text_width + (buffer_padding * 2))
        canvas_height = max(1, text_height + (buffer_padding * 2))
        
        img = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        x = (canvas_width // 2) - (text_width // 2) - text_left
        y = (canvas_height // 2) - (text_height // 2) - text_upper
        
        draw.text((x, y), script_text, font=font, fill=self.text_color)
        return img
    
    def render_text_sticker(self, text: str, scheme_name: str, scale_factor: float = 1.0) -> Image.Image:
        svg_content = self.render_text_to_svg(text, scheme_name)
        
        try:
            import cairosvg 
            png_data = cairosvg.svg2png(
                bytestring=svg_content.encode('utf-8'),
                output_width=3000, 
                output_height=3000,
            )
            
            text_img = Image.open(io.BytesIO(png_data)).convert("RGBA")
            
        except Exception as e:
            from PIL import ImageDraw 
            print(f"Warning: SVG to PNG conversion failed ({e}). Falling back to robust PIL text rendering.")                        

            script_text = ScriptConverter.convert_to_script(text, scheme_name=scheme_name)
            
            font = ImageFont.truetype(self.font_path, self.font_size)

            text_bbox = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), script_text, font=font)
            
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            buffer_padding = self.border_size + self.shadow_blur_strength + self.padding
            canvas_width = max(1, text_width + (buffer_padding * 2))
            canvas_height = max(1, text_height + (buffer_padding * 2))
            
            text_img = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(text_img)
            x_pos = buffer_padding - text_bbox[0]
            y_pos = buffer_padding - text_bbox[1]
            
            draw.text((x_pos, y_pos), script_text, font=font, fill=self.text_color)

        if scale_factor != 1.0:
            new_width = int(text_img.width * scale_factor)
            new_height = int(text_img.height * scale_factor)
            text_img = text_img.resize((new_width, new_height), Image.LANCZOS)
        return self._make_sticker_from_img(text_img, scale_factor=scale_factor)

    def _create_placeholder_image_from_svg(self, svg_string):
        root = ET.fromstring(svg_string)
        width = int(float(root.attrib.get('width', '10px').replace('px', '')))
        height = int(float(root.attrib.get('height', '10px').replace('px', '')))
        return Image.new("RGBA", (max(width, 100), max(height, 50)), (0, 0, 0, 0))
    
    def combine_elements(self, 
                         img_element: Image.Image, 
                         text_element: Image.Image, 
                         mode: str, 
                         scale: float = 1.0) -> Image.Image:
        w_img, h_img = img_element.size
        w_txt, h_txt = text_element.size
        
        final_scale = max(1, int(scale))
        
        if final_scale != 1:
             img_element = img_element.resize((w_img * final_scale, h_img * final_scale), Image.LANCZOS)
             text_element = text_element.resize((w_txt * final_scale, h_txt * final_scale), Image.LANCZOS)
             w_img, h_img = img_element.size
             w_txt, h_txt = text_element.size
        
        if mode == 'v_image_text' or mode == 'v_text_image':
            final_width = max(w_img, w_txt)
            final_height = h_img + h_txt
            
            final_canvas = Image.new("RGBA", (final_width, final_height), (0, 0, 0, 0))
            
            x_img = (final_width - w_img) // 2
            x_txt = (final_width - w_txt) // 2
            
            if mode == 'v_image_text':
                final_canvas.paste(img_element, (x_img, 0), img_element)
                final_canvas.paste(text_element, (x_txt, h_img), text_element)
            else: 
                final_canvas.paste(text_element, (x_txt, 0), text_element)
                final_canvas.paste(img_element, (x_img, h_txt), img_element)

        elif mode == 'over':
            final_width = w_img
            final_height = h_img
            
            max_text_width = int(final_width * 0.8) 
            
            if w_txt > max_text_width:
                resize_factor = max_text_width / w_txt
                new_w_txt = max_text_width
                new_h_txt = int(h_txt * resize_factor)
                
                text_element = text_element.resize((new_w_txt, new_h_txt), Image.LANCZOS)
                w_txt, h_txt = text_element.size 
            
            final_canvas = img_element.copy()            
            
            x_txt = (final_width - w_txt) // 2
            y_txt = (final_height - h_txt) // 2
            
            final_canvas.paste(text_element, (x_txt, y_txt), text_element)

        else:
            raise ValueError("Invalid combination mode. Use 'over', 'v_image_text', or 'v_text_image'.")

        if not self.bg_transparent:
            solid_bg = Image.new("RGBA", final_canvas.size, self.bg_color)
            solid_bg.paste(final_canvas, (0, 0), final_canvas)
            return solid_bg
            
        return final_canvas

    def process_combined_sticker(self, 
                                 image_path: Path, 
                                 input_text: str, 
                                 scheme_name: str, 
                                 mode: str, 
                                 scale: float, 
                                 output_path: Path):
        
        img_sticker = self.make_image_sticker(image_path, scale_factor=scale) 
        text_sticker = self.render_text_sticker(input_text, scheme_name, scale_factor=scale) 
        
        final_img = self.combine_elements(img_sticker, text_sticker, mode, scale=1.0)
        
        final_img.save(output_path, format="PNG")
        
        return output_path
    
    def process_request(self, input_text: str, scheme_name: str, output_type: str):
        if output_type == 'png_high':
            scale = 4.0 
        else: 
            scale = 1.0 

        if output_type in ('png_small', 'png_high'):
            text_image = self.render_text_to_image(input_text, scheme_name, scale_factor=scale)
            
            final_img = self.make_sticker_from_image(text_image, scale_factor=scale)
            
            buffer = io.BytesIO()
            final_img.save(buffer, format="PNG")
            return buffer.getvalue(), 'image/png'

        elif output_type == 'svg':
            svg_string_content = self.render_text_to_svg(input_text, scheme_name)
            return svg_string_content.encode('utf-8'), 'image/svg+xml'
        
        return None, None