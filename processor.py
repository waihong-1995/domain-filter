import pandas as pd
from utils import extract_root_domain, extract_subdomain

def process_file(input_path, output_path, column_name="Domain"):
    df = pd.read_excel(input_path)

    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in Excel.")

    df["Root Domain"] = df[column_name].astype(str).apply(extract_root_domain)
    df["Subdomain"] = df[column_name].astype(str).apply(extract_subdomain)

    df.to_excel(output_path, index=False)