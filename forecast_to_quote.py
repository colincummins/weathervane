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
        "Always output quotes in JSON format with a 'body' and 'author' attribute. Limit quote length to 150 characters. Quotes must be real and attributable to author. No quotes with unknown authors.",
        "input: rain showers likely",
        "output: {\"body\": \"Rainy days should be spent at home with a cup of tea and a good book\", \"author\":\"Bill Watterston\"}",
        "input: Windy with strong thunderstorms early, mainly cloudy overnight with a few showers. Damaging winds, large hail and possibly a tornado with some storms. Low around 60F. ENE winds at 20 to 30 mph, decreasing to 10 to 15 mph. Chance of rain 100%.",
        "output: { \"body\": \"Insults are pouring down on me as thick as hail.\", \"author\": \"Edouard Manet\"}",
        "input: Sunshine and clouds mixed. High 103F. Winds SSE at 10 to 15 mph.Mostly clear.",
        "output: { \"body\": \"Keep your face to the sunshine and you cannot see the shadows.\", \"author\": \"Helen Keller\"}",
        "input: Windy...strong thunderstorms during the evening will give way to cloudy skies after midnight. Damaging winds, large hail and possibly a tornado with some storms. Low 61F. ENE winds at 25 to 35 mph, decreasing to 10 to 15 mph. Chance of rain 100%.",
        "output: { \"body\": \"There is a safe spot in every tornado. My job is to find it\", \"author\": \"David Copperfield\"}",
        "input: Partly Cloudy\nDay 106° • Night 79°",
        "output: { \"body\": \"God, it was hot! Forget about frying an egg on the sidewalk; this kind of heat would fry an egg inside the chicken.\", \"author\": \"Rachel Caine\n\"}",
        "input: Generally sunny despite a few afternoon clouds. High 104F. Winds SSE at 10 to 15 mph.",
        "output: { \"body\": \"A cloudy day is no match for a sunny disposition.\", \"author\": \"William Arthur Ward\"}",
        "input: patchy fog after 3am. mostly cloudy, with a low around 40. southeast wind 3 to 7 mph.",
        "output: { \"body\": \"The fog comes on little cat feet.\", \"author\": \"Carl Sandburg\"}",
        "input: Plentiful sunshine. High 104F. Winds W at 10 to 15 mph.",
        "output: { \"body\": \"It ain't the heat, it's the humility.\", \"author\":\"Yogi Berra\"}",
        "input: Cloudy. High 72F. Winds WSW at 5 to 10 mph.",
        "output: { \"body\": \"Cloudy days are the best for catching up on reading.\", \"author\": \"Unknown\"}",
        "input: Showers early then scattered thunderstorms developing later in the day. High 86F. Winds E at 10 to 20 mph. Chance of rain 40%.",
        "output: { \"body\": \"It is not light that we need, but fire; it is not the gentle shower, but thunder. We need the storm, the whirlwind, and the earthquake.\", \"author\": \"Frederick Douglass\"}",
        "input: Abundant sunshine. High 56F. Winds N at 10 to 15 mph.",
        "output: { \"body\": \"Her angel's face, As the great eye of heaven shined bright, And made a sunshine in the shady place.\", \"author\": \"Edmund Spenser\"}",
        "input: Humid; overcast with a shower in spots late this morning, then times of sun and clouds this afternoon with a heavy thunderstorm",
        "output: { \"body\": \"It ain't the heat, it's the humility.\", \"author\":\"Yogi Berra\"}",
        "input: Mostly sunny; a beautiful start to the weekend. Hi 76",
        "output: { \"body\": \"Be noble like the sun; let even those who resent you for shinning benefit from your warmth.\", \"author\": \"Matshona Dhliwayo\"}",
        "input: Cloudy with a shower in places this afternoon. High 67",
        "output: { \"body\": \"How beautiful it is outside when everything is wet from the rain\", \"author\": \"Vincent Van Gogh\"}",
        "input: Breezy this morning; otherwise, mostly cloudy. High 58",
        "output: { \"body\": \"Summer bachelors, like summer breezes, are never as cool as they pretend to be.\", \"author\": \"Nora Ephron\"}"
    ]

    prompt_parts.append("input: " + forecast)

    response = model.generate_content(prompt_parts)
    json_quote = json.loads(response.text.strip("\n"))
    return json_quote['body'], json_quote['author']


if __name__ == "__main__":
    result = forecast_to_quote("Mostly sunny. Slight chance of a shower. Light winds becoming southeasterly 15 to 20 km/h "
                      "during the morning.")
    print(result)