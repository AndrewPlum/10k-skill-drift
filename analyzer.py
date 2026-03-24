import requests
import json

import config

def analyze_labor_drift(extracted_text, ticker, year):
    prompt = f"""
    As a Labor Economist at the Federal Reserve, analyze the following Human Capital Disclosure from a 10-K filing. 

    Your goal is to quantify "Skill Drift" by extracting specific competencies and mapping them to standardized categories.

    ### INSTRUCTIONS:
    1. EXTRACT HEADCOUNT: Find the total number of employees.
    2. CATEGORIZE SKILLS: 
    - 'Traditional': Manual labor, basic retail/manufacturing, general administration.
    - 'Technical': Data science, software, automation, advanced analytics.
    3. NORMALIZE TO O*NET: If a technical skill is a variant (e.g., "Pythonic scripting"), map it to the official O*NET "Hot Technology" name (e.g., "Python").
    4. NARRATIVE SCORE: Determine if technology is used for 'Substitution' (replacing humans) or 'Augmentation' (making humans more productive).
    5. CALCULATE INTENSITY: The tech_intensity_score must be calculated as: (Number of Unique Technical Skills) / (Total Number of Unique Technical and Traditional Skills). If no skills are found, return 0.
    
    ### OUTPUT FORMAT:
    Return a JSON object following this exact structure:
    
    {{
        "company_metadata": {{
            "ticker": "{ticker}",
            "fiscal_year": "{year}",
            "headcount": "integer or null"
        }},
        "skill_extraction": {{
            "traditional_skills": ["list"],
            "technical_skills_onet": ["list of O*NET standardized names"],
            "tech_intensity_score": "float between 0 and 1"
        }},
        "economic_narrative": {{
            "stance": "Substitution | Augmentation | Neutral",
            "justification": "string"
        }}
    }}

    TEXT TO ANALYZE: 
    {extracted_text}
    """

    response = requests.post(
        url=config.OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": config.OPENROUTER_MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": { "type": "json_object" } # Forces JSON output
        })
    )
    
    try:
        result = response.json()
        content = result['choices'][0]['message']['content']
        return json.loads(content)
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing LLM response for {ticker} {year}: {e}")
        return None