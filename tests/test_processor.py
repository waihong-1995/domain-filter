import pandas as pd
import os
from processor import process_file


def test_process_excel(tmp_path):
    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    df = pd.DataFrame({
        "Domain": ["abc.com www.abc.com"]
    })
    df.to_excel(input_file, index=False)

    process_file(str(input_file), str(output_file), "Domain")

    result = pd.read_excel(output_file)

    assert "Root Domain" in result.columns
    assert "Subdomain" in result.columns
    assert len(result) == 2


def test_process_csv(tmp_path):
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