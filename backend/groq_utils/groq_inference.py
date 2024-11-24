from groq import Groq
from groq_utils.system_prompts import GROQ_SYSTEM_PROMPT, format_system_prompt
import base64

from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor
import time

client = Groq()


def get_completion(
    text: Optional[str],
    image_filepath: str,
    temperature: float = 1.0,
    max_tokens: int = 1024,
    top_p: float = 1.0,
) -> str:
    def encode_image(img_filepath: str) -> str:
        return base64.b64encode(image_filepath).decode("utf-8")

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


def process_images_batch(images: List[bytes], batch_size: int = 4, max_workers: int = 4) -> List[str]:
    """Process images concurrently using a thread pool"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(get_completion, None, img) 
            for img in images
        ]
        
        results = []
        for future in futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing image: {e}")
                results.append(None)
                
        return results


def get_completion_with_retry(
    text: Optional[str],
    image_filepath: str,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    **kwargs
) -> str:
    """Wrapper around get_completion with retry logic"""
    for attempt in range(max_retries):
        try:
            return get_completion(text, image_filepath, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1: 
                raise e
            time.sleep(retry_delay * (attempt + 1))


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
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        try:
            response = get_completion(prompt, image_data)
            print(f"Response: {response.content}")
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")


if __name__ == "__main__":
    test_images()
