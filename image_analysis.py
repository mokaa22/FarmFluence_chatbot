<<<<<<< HEAD
import base64
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_plant_image(image_path):
    """
    Real image analysis using Groq LLaVA (vision-capable model)
    """

    # Read and encode image
    with open(image_path, "rb") as img:
        image_base64 = base64.b64encode(img.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="llava-v1.5-7b-4096",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert agricultural advisor.\n"
                    "Analyze the plant image carefully and:\n"
                    "1. Identify the crop if possible\n"
                    "2. Identify visible problems (disease, pest, deficiency, stress)\n"
                    "3. Explain in simple farmer-friendly language\n"
                    "4. Give practical next steps\n"
                    "5. If unsure, clearly say so\n\n"
                    "Do NOT be generic. Be specific and helpful."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this crop image and help the farmer."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500,
        temperature=0.2
    )

    return response.choices[0].message.content
=======
import base64
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_plant_image(image_path):
    """
    Real image analysis using Groq LLaVA (vision-capable model)
    """

    # Read and encode image
    with open(image_path, "rb") as img:
        image_base64 = base64.b64encode(img.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="llava-v1.5-7b-4096",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert agricultural advisor.\n"
                    "Analyze the plant image carefully and:\n"
                    "1. Identify the crop if possible\n"
                    "2. Identify visible problems (disease, pest, deficiency, stress)\n"
                    "3. Explain in simple farmer-friendly language\n"
                    "4. Give practical next steps\n"
                    "5. If unsure, clearly say so\n\n"
                    "Do NOT be generic. Be specific and helpful."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this crop image and help the farmer."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500,
        temperature=0.2
    )

    return response.choices[0].message.content
>>>>>>> c9f2407 (Fix project structure for Render deployment)
