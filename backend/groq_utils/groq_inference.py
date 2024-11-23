from groq import Groq

client = Groq()

def get_completion(text: str, image_data_url: str, temperature: float = 1.0, max_tokens: int = 1024, top_p: float = 1.0) -> str:
    completion = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_url
                        }
                    }
                ]
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=True,
        stop=None,
    )

    return completion.choices[0].message
