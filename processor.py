import pandas as pd
import os
import re
from utils import extract_root_domain, extract_subdomain


def read_input_file(input_path):
    ext = os.path.splitext(input_path)[1].lower()

    if ext in [".xlsx", ".xls"]:
        return pd.read_excel(input_path)

    elif ext == ".csv":
        # Use python engine for better handling of messy CSV
        return pd.read_csv(input_path, encoding="utf-8", engine="python")

    else:
        raise ValueError("Unsupported file format. Use Excel or CSV.")


def clean_text(text):
    """
    Normalize messy CSV/Excel cell content
    """
    text = str(text)

    # Replace newlines and tabs with space
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # Remove duplicate spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_domains(cell_value):
    """
    Extract valid domains from a cell.
    Works even if input is messy.
    """
    if pd.isna(cell_value):
        return []

    text = clean_text(cell_value)

    # Extract domains (supports normal + wildcard like *.abc.com)
    domains = re.findall(
        r"(?:\*\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}",
        text
    )

    return domains


def process_file(input_path, output_path, column_name="Domain"):
    df = read_input_file(input_path)

    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found.")

    # Step 1: extract domains into list
    df["Split Domains"] = df[column_name].apply(split_domains)

    # Step 2: explode into rows
    df = df.explode("Split Domains")

    # Step 3: drop empty rows
    df = df[df["Split Domains"].notna()]

    # Step 4: normalize domain
    df["Domain Cleaned"] = df["Split Domains"].str.lower().str.strip()

    # Step 5: extract root + subdomain
    df["Root Domain"] = df["Domain Cleaned"].apply(extract_root_domain)
    df["Subdomain"] = df["Domain Cleaned"].apply(extract_subdomain)

    # Optional: remove duplicates
    df = df.drop_duplicates(subset=["Domain Cleaned"])

    # Clean up
    df = df.drop(columns=["Split Domains"])

    # Output format
    if output_path.endswith(".csv"):
        df.to_csv(output_path, index=False)
    else:
        df.to_excel(output_path, index=False)
