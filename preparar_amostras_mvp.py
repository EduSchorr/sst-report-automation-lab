from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from analisador_base import anonymize_text, init_db

def prepare_samples(db_path: Path, output_dir: Path, per_category: int = 5, seed: int = 42) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    conn = init_db(db_path)
    rows = conn.execute(
        """SELECT d.id,d.nome_arquivo,d.categoria_principal,d.confianca,e.dados_json
           FROM documentos d LEFT JOIN extracao_detalhada e ON e.doc_id=d.id
           WHERE d.processado=1 AND d.is_duplicata=0 AND e.dados_json IS NOT NULL"""
    ).fetchall()
    conn.close()

    grouped = {}
    for row in rows:
        grouped.setdefault(row[2], []).append(row)

    rng = random.Random(seed)
    manifest = []
    for category, items in grouped.items():
        items = list(items)
        rng.shuffle(items)
        selected = sorted(items[:per_category], key=lambda row: -int(row[3] or 0))
        for index, row in enumerate(selected, start=1):
            payload = json.loads(row[4])
            safe = {
                "source_id": row[0],
                "category": category,
                "confidence": row[3],
                "headings": [anonymize_text(x) for x in payload.get("headings", [])],
                "detected_chapters": payload.get("detected_chapters", []),
                "detected_risks": payload.get("detected_risks", []),
                "text_sample": anonymize_text(payload.get("text_sample", "")),
            }
            filename = f"{category.replace('/', '-')[:40]}_{index:02d}.json"
            (output_dir / filename).write_text(json.dumps(safe, ensure_ascii=False, indent=2), encoding="utf-8")
            manifest.append({"file": filename, "category": category, "source_id": row[0]})

    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"categories": len(grouped), "samples": len(manifest)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="data/checkpoint_sst.db")
    parser.add_argument("--output", default="output/samples")
    parser.add_argument("--per-category", type=int, default=5)
    args = parser.parse_args()
    print(prepare_samples(Path(args.db), Path(args.output), args.per_category))

if __name__ == "__main__":
    main()
