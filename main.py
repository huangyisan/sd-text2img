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
    "prompt": "((masterpiece,best quality)),photon mapping, physically-based rendering, highly detailed background, high res, perspective,(1 girl),detailed clothes, white clothes, blunt bangs, braid, fine fabric emphasis,(large breasts:1.4), cleavage, wide-sleeved kimono, hair ornament, white japanese clothes,(bare leg:1.2), (pink hair:1.4),long hair, straight hair, detailed face, cool face, (smail:0.8),looking at viewer, beautiful eyes,detailed eyes, skirt, from side, (sea:1.4), (beach:0.9), sunshine,(hand between legs:1.7),standing,(ulzzang-6500:0.7),<lora:koreanDollLikeness_v15:0.4> <lora:yaeMikoRealistic_yaemikoMixed:0.7>",

    "negative_prompt": "EasyNegative, extra fingers, fewer fingers, nsfw, bad anatomy, low-res, (watermarks:1.2), username, paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), monochrome, grayscale, easynegative, ng_deepnegative_v1_75t, bad anatomy, low-res, poorly drawn face, disfigured hands, poorly drawn eyebrows, bad body perspective, animal tail, anime, nipples, pussy, wrong anatomy, poorly drawn legs, wrong perspective legs, extra legs,poorly drawn hands, (bad-hands-5:1.8), wrong hand",
    "seed": -1,
    "Model": "CounterfeitV25_25",
    "cfg_scale": 6.5,
    "sampler_name": "DPM++ 2M Karras",
    "width": 600,
    "height": 900,
    "steps": 30,
    "s_noise": 1337,
    
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
    for i in range(0,100):
        try:
            make_pic()
        except BaseException:
            pass
        time.sleep(1)
            

main()

