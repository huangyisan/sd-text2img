import json
import time
import requests
import io
import os
import base64
from PIL import Image, PngImagePlugin

def get_timestamp():
    return str(int(time.time()))

url = os.getenv("STABLE_DIFFUSION_API")

payload = {
    "prompt": "((masterpiece, best quality)),close-up, facing viewer,straight on, face focus,((1 girl)), {long hair}, (medium breasts:1.4),(photo realistic:0.8), standing,  hair ornamen, gloves, (smile:1.2), (detailed light),lighting, colorful, layered backgrounds, (gorgeous background), dynamic angle, (shine),keqing \(genshin impact\),twintail, purple hair,(purple eyes:1.2),(outdoor),  physically-based rendering, RAW photo, highly detailed background, (photo realistic:0.8), high res, (black bodystocking),(potted plant:1.2),geyser, park, flower field,<lora:keqingGenshinImpact_10:0.75>  <lora:chilloutmixss_xss10:0.7>",

    "negative_prompt": "EasyNegative, extra fingers, fewer fingers, nsfw, bad anatomy, low-res, (watermarks:1.2), username, paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), monochrome, grayscale, easynegative, ng_deepnegative_v1_75t, bad anatomy, low-res, poorly drawn face, disfigured hands, poorly drawn eyebrows, bad body perspective, animal tail, anime, nipples, pussy, wrong anatomy, poorly drawn legs, wrong perspective legs, extra legs,poorly drawn hands, (bad-hands-5:1.8), wrong hand,EasyNegative, extra fingers, fewer fingers, (worst quality, low quality:1.4), loli",
    "seed": -1,
    "Model": "CounterfeitV25_25",
    "cfg_scale": 4.5,
    "sampler_name": "DPM++ 2M Karras",
    "width": 854,
    "height": 480,
    "steps": 30,
    "s_noise": 31337,
    "enable_hr": True,
    "hr_scale": 2,
    "hr_upscaler": "Latent",
    "hr_resize_x": 1280,
    "hr_resize_y": 720,
    "denoising_strength": 0.6,
    "hr_second_pass_steps": 12,
}

def make_pic():
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save("output/{}.png".format(get_timestamp()), pnginfo=pnginfo)

def main():
    for i in range(0,30):
        try:
            make_pic()
        except BaseException:
            pass
        time.sleep(1)
            

main()