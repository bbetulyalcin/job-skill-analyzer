import time
import requests
import pandas as pd
import os
import json
from bs4 import BeautifulSoup
from groq import Groq
from dotenv import load_dotenv


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def load_skills_map(filepath="skill.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"\n[ERROR] '{filepath}' not found! Please create the file.")
        return {}
    except json.JSONDecodeError:
        print(f"\n[ERROR] '{filepath}' has an invalid format! Ensure it is a valid JSON.")
        return {}

def extract_skills_with_llm(job_description, role_name, skills_map):
    allowed_skills = skills_map.get(role_name, [])
    if not allowed_skills or not job_description.strip():
        return ""

    allowed_skills_str = ", ".join(allowed_skills)
    clean_text = " ".join(job_description.split())

    prompt = f"""
TASK:
Analyze the provided "JOB DESCRIPTION" and extract ONLY the technical skills that are actually present in the text, cross-referencing them with the "ALLOWED SKILLS" list.

ALLOWED SKILLS ({role_name}):
{allowed_skills_str}

STRICT RULES:
1. DO NOT hallucinate. DO NOT output the entire allowed skills list.
2. ONLY output a skill if it is explicitly mentioned OR strongly implied by a direct synonym in the text (e.g., "Azure OpenAI" -> LLMs, "Agent based" -> Agentic Workflows).
3. Ignore any skill from the allowed list that is NOT present in the job description.
4. Output format MUST be a single line of comma-separated values.
5. NO conversational text, NO explanations, NO bullet points.
6. If absolutely no matches are found, output exactly: Not Found

JOB DESCRIPTION:
{clean_text[:4000]}
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a strict data extraction parser. Your ONLY job is to identify matching skills without hallucinating. You never add conversational filler."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0
        )
        response = chat_completion.choices[0].message.content.strip()
        
        
        if response.lower() == "not found":
            return ""
            
        return response.replace("[", "").replace("]", "").replace('"', "").replace("'", "")
    except Exception as e:
        print(f"LLM Error: {e}")
        return ""

def main():
  
    SKILLS_MAP = load_skills_map()
    if not SKILLS_MAP:
        return 

    raw_query = input("Which position are you looking for? (e.g., AI Developer): ")
    SEARCH_QUERY = raw_query.replace(" ", "%20") 
    PAGE_LIMIT = int(input("How many pages do you want to scrape?: "))
    POSTED_DAYS = 7

    valid_roles_lower = {k.lower(): k for k in SKILLS_MAP.keys()}
    role_key = valid_roles_lower.get(raw_query.lower(), None)

    if not role_key:
        print(f"\n[WARNING] '{raw_query}' not found in skill.json! LLM Skill extraction will be skipped.\n")

    scraped_jobs = []
    print(f"\nScanning job postings from the last {POSTED_DAYS} days...\n")
    
    for page in range(1, PAGE_LIMIT + 1):
        url = f"https://www.dice.com/jobs?q={SEARCH_QUERY}&countryCode=US&radius=30&radiusUnit=mi&page={page}&pageSize=20&filters.workplaceTypes=Remote&language=en&postedDate={POSTED_DAYS}"
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            job_cards = soup.find_all('div', attrs={'data-testid': 'job-card'})
            
            if not job_cards:
                print(f"No job postings found on page {page}.")
                continue

            for card in job_cards:
                link_tag = card.find('a', attrs={'data-testid': 'job-search-job-card-link'})
                if not link_tag: continue
                
                job_link = link_tag.get('href')
                clean_title = link_tag.get('aria-label', '').replace("View Details for ", "").strip()
                
                company_tag = card.find('span', class_='logo')
                company_name = company_tag.text.strip() if company_tag else "Not Found"
                
                location_tag = card.find('p', class_='text-zinc-600')
                location = location_tag.text.strip() if location_tag else "Not Found"
                
                print(f"Inspecting: {clean_title} | {company_name}")
                
                extracted_skills = ""
                if role_key:
                    try:
                        detail_res = requests.get(job_link, headers=headers, timeout=10)
                        detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
                        
                        desc_div = detail_soup.find('div', id='jobDescription') or \
                                   detail_soup.find('div', id='jobdoc') or \
                                   detail_soup.find('div', attrs={'data-testid': 'jobDescriptionHtml'})
                        
                        job_desc_text = desc_div.text.strip() if desc_div else " ".join([p.text for p in detail_soup.find_all('p')])
                        
                        # Send the extracted text and the loaded SKILLS_MAP to the LLM
                        extracted_skills = extract_skills_with_llm(job_desc_text, role_key, SKILLS_MAP)
                        
                    except Exception as e:
                        print(f"  -> Failed to read details page: {e}")
                    
                    time.sleep(1)
                
                scraped_jobs.append({
                    "Title": clean_title,
                    "Company": company_name,
                    "Location": location,
                    "Link": job_link,
                    "Extracted_Skills": extracted_skills
                })
                
            time.sleep(1.5)  
            
        except Exception as e:
            print(f"Error occurred while processing page {page}: {e}")
            
    if scraped_jobs:
        df = pd.DataFrame(scraped_jobs)
        csv_filename = f"dice_{raw_query.replace(' ', '_')}_jobs_with_skills.csv"
        df.to_csv(csv_filename, index=False, encoding="utf-8-sig", sep=";")
        print(f"\n✅ Process Complete! AI-enriched job postings saved to '{csv_filename}'.")
    else:
        print("\nWarning: No job postings found matching the criteria.")

if __name__ == "__main__":
    main()