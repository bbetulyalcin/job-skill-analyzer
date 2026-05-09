import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import os

raw_query = input("Which position's skill analysis do you want to see? (e.g., AI Developer): ")

formatted_query = raw_query.replace(" ", "_")
FILENAME = f"dice_{formatted_query}_jobs_with_skills.csv" 

print(f"\nReading {FILENAME}...\n")

# 2. File Check
if not os.path.exists(FILENAME):
    print(f"❌ Error: '{FILENAME}' not found!")
    print("Please ensure you have run the scraper code to fetch data for this position and that the filename is correct.")
    exit()

try:
    df = pd.read_csv(FILENAME, sep=";")
except Exception as e:
    print(f"CSV reading error: {e}")
    exit()

all_skills = []

if 'Extracted_Skills' in df.columns:
    column_name = 'Extracted_Skills'
elif 'Required_Skills' in df.columns:
    column_name = 'Required_Skills'
else:
    print(f"❌ Error: Skill column not found. Available columns: {list(df.columns)}")
    exit()

for skills_string in df[column_name].dropna():
    if "LLM" in str(skills_string) or "Rate Limit" in str(skills_string) or not str(skills_string).strip():
        continue
    
    clean_skills = str(skills_string).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
    
    skills_list = [s.strip() for s in clean_skills.split(",") if s.strip()]
    all_skills.extend(skills_list)

if not all_skills:
    print("❌ No valid skills found to plot! Please check the contents of your CSV file.")
    exit()

print(f"Total extracted skills: {len(all_skills)}")

skill_counts = Counter(all_skills)
top_10_skills = skill_counts.most_common(10)

skills, counts = zip(*top_10_skills)

print("Generating plot...")
plt.figure(figsize=(12, 6))
bars = plt.bar(skills, counts, color='skyblue', edgecolor='black')

plt.title(f"Dice.com - Top 10 Most In-Demand Skills for '{raw_query.title()}'", fontsize=14, fontweight='bold')
plt.ylabel("Number of Job Postings")
plt.xticks(rotation=45, ha='right')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()