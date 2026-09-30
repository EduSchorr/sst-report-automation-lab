from __future__ import annotations

import os
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_DIR = Path(os.environ.get("SST_LAB_CORPUS_DIR", ROOT / "corpus")).expanduser().resolve()
OUTPUT_DIR = Path(os.environ.get("SST_LAB_OUTPUT_DIR", ROOT / "output")).expanduser().resolve()
DB_PATH = Path(os.environ.get("SST_LAB_DB_PATH", ROOT / "data" / "checkpoint_sst.db")).expanduser().resolve()

CPF_REGEX = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}[-.]?\d{2}\b")
CNPJ_REGEX = re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}/\d{4}[-.]?\d{2}\b")
PROCESSO_REGEX = re.compile(r"\b\d{7}[-.]\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b|\b\d{4,7}/\d{4}\b")
RG_REGEX = re.compile(r"\bRG[:\s]*\d{1,2}\.?\d{3}\.?\d{3}[-.]?[0-9xX]?\b", re.IGNORECASE)
PIS_REGEX = re.compile(r"\b(?:PIS|PASEP|NIT)[:\s]*\d{3}\.?\d{5}\.?\d{2}[-.]?\d\b", re.IGNORECASE)

def anonymize_text(text: str) -> str:
    if not text:
        return ""
    text = CPF_REGEX.sub("[CPF_REMOVIDO]", text)
    text = CNPJ_REGEX.sub("[CNPJ_REMOVIDO]", text)
    text = PROCESSO_REGEX.sub("[PROCESSO]", text)
    text = RG_REGEX.sub("[RG_REMOVIDO]", text)
    text = PIS_REGEX.sub("[PIS_REMOVIDO]", text)
    return text

def init_db(db_path: str | Path = DB_PATH) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem TEXT,
            caminho_relativo TEXT,
            nome_arquivo TEXT,
            extensao TEXT,
            tamanho_bytes INTEGER,
            sha256 TEXT,
            is_duplicata INTEGER,
            duplicata_de TEXT,
            categoria_principal TEXT,
            categorias_secundarias TEXT,
            confianca INTEGER,
            justificativa TEXT,
            paginas INTEGER,
            tem_texto INTEGER,
            tem_imagens INTEGER,
            num_imagens INTEGER,
            tem_tabelas INTEGER,
            num_tabelas INTEGER,
            precisou_ocr INTEGER,
            erro TEXT,
            processado INTEGER DEFAULT 0
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_documentos_sha256 ON documentos(sha256)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_documentos_processado ON documentos(processado)")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS extracao_detalhada (
            doc_id INTEGER PRIMARY KEY,
            dados_json TEXT NOT NULL,
            FOREIGN KEY (doc_id) REFERENCES documentos(id)
        )
    """)
    conn.commit()
    return conn
