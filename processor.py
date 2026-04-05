import pandas as pd
import os
import re
from utils import extract_root_domain, extract_subdomain


def read_input_file(input_path):
    ext = os.path.splitext(input_path)[1].lower()

    if ext in [".xlsx", ".xls"]:
        return pd.read_excel(input_path)
    elif ext == ".csv":
        return pd.read_csv(input_path)
    else:
        raise ValueError("Unsupported file format. Use Excel or CSV.")


def split_domains(cell_value):
    """
    Split multiple domains in one cell.
    Handles spaces, commas, semicolons, etc.
    """
    if pd.isna(cell_value):
        return []

    # Split by whitespace, comma, semicolon
    domains = re.split(r"[,\s;]+", str(cell_value))

    # Remove empty strings
    return [d.strip() for d in domains if d.strip()]


def process_file(input_path, output_path, column_name="Domain"):
    df = read_input_file(input_path)

    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found.")

    # Step 1: split domains into lists
    df["Split Domains"] = df[column_name].apply(split_domains)

    # Step 2: explode into multiple rows
    df = df.explode("Split Domains")

    # Step 3: rename for clarity
    df["Domain Cleaned"] = df["Split Domains"]

    # Step 4: extract root + subdomain
    df["Root Domain"] = df["Domain Cleaned"].apply(extract_root_domain)
    df["Subdomain"] = df["Domain Cleaned"].apply(extract_subdomain)

    # Optional: drop helper column
    df = df.drop(columns=["Split Domains"])

    # Save output (always Excel for now)
    df.to_excel(output_path, index=False)