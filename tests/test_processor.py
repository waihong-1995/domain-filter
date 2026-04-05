import sys
import os
import pandas as pd
import pytest

# Fix import path for GitHub Actions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from processor import process_file


def test_process_excel_multiple_domains(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    df = pd.DataFrame({
        "Domain": ["abc.com www.abc.com def.com"]
    })
    df.to_excel(input_file, index=False)

    process_file(str(input_file), str(output_file), "Domain")

    result = pd.read_excel(output_file)

    # Expected 3 domains after split
    assert len(result) == 3

    assert "Root Domain" in result.columns
    assert "Subdomain" in result.columns

    assert "abc.com" in result["Root Domain"].values
    assert "def.com" in result["Root Domain"].values


def test_process_csv_multiple_domains(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.xlsx"

    df = pd.DataFrame({
        "Domain": ["def.com www.def.com"]
    })
    df.to_csv(input_file, index=False)

    process_file(str(input_file), str(output_file), "Domain")

    result = pd.read_excel(output_file)

    assert len(result) == 2
    assert "def.com" in result["Root Domain"].values


def test_single_domain(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    df = pd.DataFrame({
        "Domain": ["www.google.com"]
    })
    df.to_excel(input_file, index=False)

    process_file(str(input_file), str(output_file), "Domain")

    result = pd.read_excel(output_file)

    assert len(result) == 1
    assert result.loc[0, "Root Domain"] == "google.com"
    assert result.loc[0, "Subdomain"] == "www"


def test_empty_cell(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    df = pd.DataFrame({
        "Domain": [None]
    })
    df.to_excel(input_file, index=False)

    process_file(str(input_file), str(output_file), "Domain")

    result = pd.read_excel(output_file)

    # Should result in 0 rows after explode
    assert len(result) == 0


def test_missing_column(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    df = pd.DataFrame({
        "WrongColumn": ["abc.com"]
    })
    df.to_excel(input_file, index=False)

    with pytest.raises(ValueError):
        process_file(str(input_file), str(output_file), "Domain")