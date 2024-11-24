from groq import Groq
from groq_utils.system_prompts import GROQ_SYSTEM_PROMPT, format_system_prompt
import base64

from typing import Optional

client = Groq()


def get_completion(
    text: Optional[str],
    image_filepath: str,
    temperature: float = 1.0,
    max_tokens: int = 1024,
    top_p: float = 1.0,
) -> str:
    def encode_image(filepath: str) -> str:
        with open(filepath, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    image_base64 = encode_image(image_filepath)

    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": format_system_prompt(text)},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    },
                ],
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message


def test_images():
    import os
    from pathlib import Path

    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent

    image_dir = project_root / "images" / "house1"

    image_extensions = (".jpg", ".jpeg", ".png")

    image_files = [
        str(f) for f in image_dir.iterdir() if f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print(f"No images found in {image_dir}")
        return

    prompt = "Can you describe this property in detail?"

    for image_path in image_files:
        print(f"\nProcessing image: {os.path.basename(image_path)}")
        try:
            response = get_completion(prompt, image_path)
            print(f"Response: {response.content}")
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")


if __name__ == "__main__":
    test_images()
