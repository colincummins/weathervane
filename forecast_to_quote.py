import json
import re

import google.generativeai as genai
from wv_config import gemini_api_key
from re import match


def markdown_to_json(markdown: str):
    json_template = r"\{.*\}"
    matches = re.match(markdown,json_template)
    return matches[0]


def forecast_to_quote(forecast):
    genai.configure(api_key=gemini_api_key)

    # Set up the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    prompt_parts = [
        "Respond with no formatting. Always output quotes in JSON format with a 'body' and 'author' attribute. Limit quote length to 150 characters. Quotes must be real and attributable to author.",
        "input: rain showers likely",
        "output: {body: \"Rainy days should be spent at home with a cup of tea and a good book\", author:\"Bill Watterston\"}",
        "input: Windy with strong thunderstorms early, mainly cloudy overnight with a few showers. Damaging winds, large hail and possibly a tornado with some storms. Low around 60F. ENE winds at 20 to 30 mph, decreasing to 10 to 15 mph. Chance of rain 100%.",
        "output: { \"body\": \"Insults are pouring down on me as thick as hail.\", \"author\": \"Edouard Manet\"}",
        "input: Sunshine and clouds mixed. High 103F. Winds SSE at 10 to 15 mph.Mostly clear.",
        "output: { \"body\": \"Keep your face to the sunshine and you cannot see the shadows.\", \"author\": \"Helen Keller\"}",
        "input: Windy...strong thunderstorms during the evening will give way to cloudy skies after midnight. Damaging winds, large hail and possibly a tornado with some storms. Low 61F. ENE winds at 25 to 35 mph, decreasing to 10 to 15 mph. Chance of rain 100%.",
        "output: { \"body\": \"There is a safe spot in every tornado. My job is to find it\", \"author\": \"David Copperfield\"}",
        "input: Partly Cloudy\nDay 106° • Night 79°",
        "output: { \"body\": \"God, it was hot! Forget about frying an egg on the sidewalk; this kind of heat would fry an egg inside the chicken.\", \"author\": \"Rachel Caine\n\"}",
        "input: Generally sunny despite a few afternoon clouds. High 104F. Winds SSE at 10 to 15 mph.",
        "output: { \"body\": \"The fog comes on little cat feet.\", \"author\": \"Carl Sandburg\"}",
    ]

    response = model.generate_content(prompt_parts)
    json_quote = json.loads(response.text.strip("\n"))
    return json_quote['body'], json_quote['author']


if __name__ == "__main__":
    result = forecast_to_quote("Mostly sunny. Slight chance of a shower. Light winds becoming southeasterly 15 to 20 km/h "
                      "during the morning.")
    print(result)