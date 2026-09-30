from pathlib import Path
import re
import unicodedata

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "sample_contacts.csv"
OUTPUT_DIR = BASE_DIR / "output"


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", text).upper()


def normalize_email(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def is_valid_email(email: str) -> bool:
    pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return bool(re.match(pattern, email))


def classify_role(role: object) -> str:
    normalized = normalize_text(role)

    if normalized.startswith("PROP"):
        return "Proprietario"
    if normalized.startswith("DIR"):
        return "Diretor"
    if normalized.startswith("GER"):
        return "Gerente"
    return "Outros"


def add_segment_flags(df: pd.DataFrame) -> pd.DataFrame:
    interest = df["SetorInteresse"].map(normalize_text)
    activity = df["Atividade"].map(normalize_text)
    combined = interest + " " + activity

    df["Interesse_Alimentos"] = combined.str.contains("ALIMENTO", na=False)
    df["Interesse_Pizza"] = combined.str.contains("PIZZA", na=False)
    df["Interesse_Confeitaria"] = combined.str.contains("CONFEIT", na=False)
    df["Interesse_Cafe"] = combined.str.contains("CAFE", na=False)
    return df


def clean_contacts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [normalize_text(column).title().replace(" ", "") for column in df.columns]

    expected_columns = {
        "Email",
        "Empresa",
        "Cargo",
        "Atividade",
        "Departamento",
        "Setorinteresse",
    }
    missing = expected_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes: {sorted(missing)}")

    df = df.rename(columns={"Setorinteresse": "SetorInteresse"})

    df["Email"] = df["Email"].map(normalize_email)
    df = df[df["Email"].map(is_valid_email)].copy()
    df = df.drop_duplicates(subset=["Email"], keep="first")

    for column in ["Empresa", "Cargo", "Atividade", "Departamento", "SetorInteresse"]:
        df[column] = df[column].fillna("").astype(str).str.strip()

    df["NivelCargo"] = df["Cargo"].map(classify_role)
    df = add_segment_flags(df)

    return df.sort_values(["Empresa", "Email"], kind="stable").reset_index(drop=True)


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("Registros validos", len(df)),
        ("Empresas unicas", df["Empresa"].nunique()),
        ("Proprietarios", (df["NivelCargo"] == "Proprietario").sum()),
        ("Diretores", (df["NivelCargo"] == "Diretor").sum()),
        ("Gerentes", (df["NivelCargo"] == "Gerente").sum()),
        ("Interesse em alimentos", df["Interesse_Alimentos"].sum()),
        ("Interesse em pizza", df["Interesse_Pizza"].sum()),
        ("Interesse em confeitaria", df["Interesse_Confeitaria"].sum()),
        ("Interesse em cafe", df["Interesse_Cafe"].sum()),
    ]
    return pd.DataFrame(rows, columns=["Indicador", "Valor"])


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    raw = pd.read_csv(INPUT_FILE)
    cleaned = clean_contacts(raw)
    summary = build_summary(cleaned)

    cleaned.to_csv(OUTPUT_DIR / "contacts_clean.csv", index=False, encoding="utf-8-sig")
    summary.to_csv(OUTPUT_DIR / "summary.csv", index=False, encoding="utf-8-sig")

    print(f"Entrada: {len(raw)} registros")
    print(f"Saida: {len(cleaned)} registros")
    print(f"Arquivos gerados em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
