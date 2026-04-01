# domain-filter - by Tan Wai Hong - 2 Apr 2026 - version 1.0
A Python-based tool for processing and extracting root domain and subdomain from a list of domain provided

# Features
- Process domain list from CSV/ Excel
- GUI interface (Gradio)
- Dockerfile available for containerization

# Installation
```bash
git clone https://github.com/waihong-1995/domain-filter.git
cd domain-filter
pip3 install -r requirement.txt
```

# Usage 
```bash
python3 webapp.py
```
Then open http://127.0.0.1:7860

# Docker usage
```bash
docker build -t domain-filter .
docker run -p 7860:7860 domain-filter
```

# Example Input/ Output
Input:
www.abc.com

Output:
root domain = abc.com
subdomain = www

# Project Structure
- webapp.py
- gui.py
- utils.py
- processor.py

# Dependencies
- Python 3.9
- pandas>=2.0.0
- tldextract>=5.0.0
- openpyxl>=3.1.0
- gradio==3.50.2

# License
MIT License
