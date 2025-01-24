import os
import uuid
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List
from PIL import Image

app = FastAPI()


class Detection(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    confidence: float
    predicted_class: int
    name: str

    class Config:
        schema_extra = {
            "example": {
                "xmin": 895.28,
                "ymin": 568.59,
                "xmax": 1184.85,
                "ymax": 872.23,
                "confidence": 0.9306,
                "predicted_class": 14,
                "name": "bird"
            }
        }


@app.post("/")
async def process_image( detections: List[Detection] = Body(...) ):
    img = Image.open("artefacts/img/plage.jpg")
    uuid_process = str(uuid.uuid4())
    os.makedirs(f"artefacts/{uuid_process}")

    cropped_images = []
    for i, box in enumerate(detections):
        uuid_file = str(uuid.uuid4())
        xmin, ymin, xmax, ymax = box.xmin, box.ymin, box.xmax, box.ymax

        cropped_img = img.crop((xmin, ymin, xmax, ymax))

        cropped_img_path = f"artefacts/{uuid_process}/{uuid_file}.png"
        cropped_img.save(cropped_img_path)
        cropped_images.append(cropped_img_path)

    return {"cropped_images": cropped_images}