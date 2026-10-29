import pandas as pd
import pytest
from src.pipeline import normalize_text, normalize_email, classify_role, clean_contacts

def test_normalizacao():
    assert normalize_text(" Proprietária ") == "PROPRIETARIA"
    assert normalize_email(" ANA@EXAMPLE.COM ") == "ana@example.com"
    assert classify_role("Gerente Comercial") == "Gerente"

def test_limpeza():
    data = pd.DataFrame([
        ["ANA@EXAMPLE.COM", "Empresa A", "Gerente", "Pizzaria", "Comercial", "Alimentos"],
        ["ana@example.com", "Empresa A", "Gerente", "Pizzaria", "Comercial", "Alimentos"],
        ["invalido", "Empresa B", "Diretor", "Servicos", "Diretoria", "Outros"],
        ["bia@example.com", "Empresa C", "Proprietaria", "Confeitaria", "Diretoria", "Cafe"],
    ], columns=["Email", "Empresa", "Cargo", "Atividade", "Departamento", "SetorInteresse"])
    cleaned = clean_contacts(data)
    assert len(cleaned) == 2
    assert set(cleaned["Email"]) == {"ana@example.com", "bia@example.com"}
    assert bool(cleaned.loc[cleaned["Email"] == "ana@example.com", "Interesse_Pizza"].iloc[0])

def test_colunas_obrigatorias():
    with pytest.raises(ValueError, match="Colunas ausentes"):
        clean_contacts(pd.DataFrame({"Email": ["ana@example.com"]}))
