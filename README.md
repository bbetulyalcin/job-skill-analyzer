# LLM-Powered Job Skill Analyzer
Built an AI-assisted market intelligence pipeline that combines web scraping, LLM-based information extraction, and data visualization to analyze hiring trends from real-world job postings.

An AI-assisted job market analysis pipeline that scrapes remote job postings from Dice.com, extracts technical skills using LLMs, and visualizes the most in-demand skills for a selected role.

## Features

- Scrapes remote job postings from Dice.com
- Collects:
  - Job title
  - Company name
  - Location
  - Job URL
  - Extracted technical skills
- Uses Groq + Llama 3.3 70B for skill extraction
- Cross-checks extracted skills with a predefined skill map
- Generates CSV datasets automatically
- Visualizes the Top 10 most requested skills using Matplotlib

---

## Project Workflow

### Step 1 — Scrape Jobs & Extract Skills

Run:

```bash
python skill.py
```

This script:

1. Scrapes Dice.com job postings page-by-page
2. Visits each job detail page
3. Extracts the job description
4. Sends the description to an LLM
5. Matches detected skills against a predefined skill map
6. Saves results into a CSV file

Generated CSV includes:

- Title
- Company
- Location
- Link
- Extracted_Skills

---

### Step 2 — Analyze Skill Demand

Run:

```bash
python analysis.py
```

This script:

- Reads the generated CSV
- Counts extracted skills
- Finds the Top 10 most requested skills
- Generates a visualization chart

---

## Tech Stack

- Python
- BeautifulSoup
- Requests
- Pandas
- Matplotlib
- Groq API
- Llama 3.3 70B
- Prompt Engineering

---

## Example Use Cases

- AI Engineer market analysis
- Skill trend analysis
- Resume optimization research
- Hiring market intelligence
- Technical recruitment analytics

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

## Installation

```bash
git clone <your-repo-url>

cd <repo-name>

pip install -r requirements.txt
```

---

## Example Output

### CSV Output

| Title | Company | Location | Link | Required Skills |
|---|---|---|---|---|
| AI Engineer | Company X | Remote | https://... | Python, LangChain, RAG |

### Visualization

Top 10 most in-demand skills chart generated with Matplotlib.

---

## Notes

- The extractor uses strict prompting to minimize hallucinations.
- Only skills included in the predefined `skill.json` map are considered valid.
- Designed for educational and market analysis purposes.

---

# LLM Destekli İş İlanı Beceri Analizörü

Web scraping, LLM tabanlı bilgi çıkarımı ve veri görselleştirmeyi birleştiren AI destekli bir piyasa istihbarat pipeline’ıdır. Gerçek iş ilanları üzerinden işe alım trendlerini analiz eder.

Bu sistem, Dice.com üzerindeki uzaktan iş ilanlarını scrape eder, LLM kullanarak teknik becerileri çıkarır ve seçilen role göre en çok talep edilen becerileri görselleştirir.

---

## Özellikler

- Dice.com üzerinden uzaktan iş ilanlarını scrape eder
- Şunları toplar:
  - İş başlığı
  - Şirket adı
  - Lokasyon
  - İş ilanı URL’i
  - Çıkarılmış teknik beceriler
- Beceri çıkarımı için Groq + Llama 3.3 70B kullanır
- Çıkarılan becerileri önceden tanımlı skill map ile karşılaştırır
- CSV veri seti otomatik oluşturur
- En çok talep edilen Top 10 beceriyi Matplotlib ile görselleştirir

---

## Proje Akışı

### Adım 1 — İş İlanlarını Scrape Etme ve Beceri Çıkarma

```bash
python skill.py
```

Bu script şunları yapar:

1. Dice.com iş ilanlarını sayfa sayfa scrape eder
2. Her iş ilanının detay sayfasına gider
3. İş açıklamasını çıkarır
4. Açıklamayı LLM’e gönderir
5. Tespit edilen becerileri skill map ile eşleştirir
6. Sonuçları CSV dosyasına kaydeder

Oluşturulan CSV şunları içerir:

- Title
- Company
- Location
- Link
- Extracted_Skills

---

### Adım 2 — Beceri Talep Analizi

```bash
python analysis.py
```

Bu script şunları yapar:

- Oluşturulan CSV dosyasını okur
- Çıkarılan becerileri sayar
- En çok geçen Top 10 beceriyi bulur
- Görselleştirme grafiği oluşturur

---

## Teknoloji Yığını

- Python
- BeautifulSoup
- Requests
- Pandas
- Matplotlib
- Groq API
- Llama 3.3 70B
- Prompt Engineering

---

## Örnek Kullanım Alanları

- AI Engineer iş piyasası analizi
- Beceri trend analizi
- CV optimizasyon araştırması
- İşe alım piyasası istihbaratı
- Teknik işe alım analitiği

---

## Ortam Değişkenleri

`.env` dosyası oluştur:

```env
GROQ_API_KEY=your_api_key_here
```

---

## Kurulum

```bash
git clone <repo-url>

cd <repo-adi>

pip install -r requirements.txt
```

---

## Örnek Çıktı

### CSV Çıktısı

| Title | Company | Location | Link | Required Skills |
|---|---|---|---|---|
| AI Engineer | Company X | Remote | https://... | Python, LangChain, RAG |

---

### Görselleştirme

Matplotlib ile oluşturulan en çok talep edilen Top 10 beceri grafiği.

---

## Notlar

- Extractor, hallucination’ı azaltmak için sıkı prompt mantığı kullanır.
- Sadece `skill.json` içinde tanımlı beceriler geçerli kabul edilir.
- Eğitim ve piyasa analizi amacıyla tasarlanmıştır.
