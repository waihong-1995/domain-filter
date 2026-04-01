import tldextract

def extract_root_domain(domain):
    extracted = tldextract.extract(domain)
    return f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain

def extract_subdomain(domain):
    extracted = tldextract.extract(domain)
    return extracted.subdomain if extracted.subdomain else ""