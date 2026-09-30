from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from analisador_base import BASE_DIR, DB_PATH, anonymize_text, init_db
from analisador_extrator import calculate_sha256, extract_docx_details, extract_pdf_details, extract_xlsx_details
from analisador_regras import classify_document, detect_chapters, detect_risks

SUPPORTED = {".docx", ".pdf", ".xlsx"}

def extract_details(path: Path) -> dict:
    data = path.read_bytes()
    suffix = path.suffix.lower()
    if suffix == ".docx":
        details = extract_docx_details(data, path.name)
    elif suffix == ".pdf":
        details = extract_pdf_details(data, path.name)
    elif suffix == ".xlsx":
        details = extract_xlsx_details(data, path.name)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
    return {"data": data, "details": details}

def process_directory(base_dir: Path = BASE_DIR, db_path: Path = DB_PATH) -> dict:
    base_dir = Path(base_dir).expanduser().resolve()
    conn = init_db(db_path)
    known = {
        row[0]: row[1]
        for row in conn.execute("SELECT sha256,nome_arquivo FROM documentos WHERE processado=1 AND sha256<>''")
    }

    stats = {"processed": 0, "duplicates": 0, "errors": 0, "skipped": 0}

    for path in sorted(base_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED:
            stats["skipped"] += 1
            continue

        relative = str(path.relative_to(base_dir))
        try:
            extracted = extract_details(path)
            data, details = extracted["data"], extracted["details"]
            sha = calculate_sha256(data)
            duplicate_of = known.get(sha)
            if duplicate_of:
                stats["duplicates"] += 1
            else:
                known[sha] = path.name

            sample = anonymize_text(details.get("text_sample", ""))
            category, secondary, confidence, justification = classify_document(
                path.name,
                sample,
                is_docx=path.suffix.lower() == ".docx",
                has_tables=details.get("tables_count", 0) > 0,
                has_images=details.get("images_count", 0) > 0,
            )

            payload = {
                "headings": [anonymize_text(x) for x in details.get("headings", [])],
                "detected_chapters": detect_chapters(sample),
                "detected_risks": detect_risks(sample),
                "text_sample": sample[:2500],
            }

            cursor = conn.execute(
                """INSERT INTO documentos(
                   origem,caminho_relativo,nome_arquivo,extensao,tamanho_bytes,sha256,
                   is_duplicata,duplicata_de,categoria_principal,categorias_secundarias,
                   confianca,justificativa,paginas,tem_texto,tem_imagens,num_imagens,
                   tem_tabelas,num_tabelas,precisou_ocr,erro,processado
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
                (
                    str(base_dir),
                    relative,
                    path.name,
                    path.suffix.lower(),
                    path.stat().st_size,
                    sha,
                    int(bool(duplicate_of)),
                    duplicate_of or "",
                    category,
                    json.dumps(secondary, ensure_ascii=False),
                    confidence,
                    justification,
                    details.get("num_pages", 1),
                    int(details.get("full_text_len", 0) > 50),
                    int(details.get("images_count", 0) > 0),
                    details.get("images_count", 0),
                    int(details.get("tables_count", 0) > 0),
                    details.get("tables_count", 0),
                    int(details.get("is_scanned", False)),
                    "",
                ),
            )
            conn.execute(
                "INSERT OR REPLACE INTO extracao_detalhada(doc_id,dados_json) VALUES(?,?)",
                (cursor.lastrowid, json.dumps(payload, ensure_ascii=False)),
            )
            stats["processed"] += 1
        except Exception as exc:
            stats["errors"] += 1
            conn.execute(
                """INSERT INTO documentos(
                   origem,caminho_relativo,nome_arquivo,extensao,tamanho_bytes,sha256,
                   is_duplicata,duplicata_de,categoria_principal,categorias_secundarias,
                   confianca,justificativa,paginas,tem_texto,tem_imagens,num_imagens,
                   tem_tabelas,num_tabelas,precisou_ocr,erro,processado
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
                (
                    str(base_dir), relative, path.name, path.suffix.lower(), path.stat().st_size,
                    "", 0, "", "erro na leitura", "[]", 0, "Falha de processamento",
                    0, 0, 0, 0, 0, 0, 0, str(exc)[:300],
                ),
            )

        if (stats["processed"] + stats["errors"]) % 100 == 0:
            conn.commit()

    conn.commit()
    conn.close()
    return stats

def main():
    parser = argparse.ArgumentParser(description="Analyze a local SST report corpus without publishing source documents.")
    parser.add_argument("directory", nargs="?", default=str(BASE_DIR))
    parser.add_argument("--db", default=str(DB_PATH))
    args = parser.parse_args()
    print(json.dumps(process_directory(Path(args.directory), Path(args.db)), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
