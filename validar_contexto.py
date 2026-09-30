from __future__ import annotations

import json
from pathlib import Path

REQUIRED_CONTEXT_FILES = [
    "00_LEIA_ME.md",
    "01_resumo_executivo.md",
    "14_regras_geracao_laudos.md",
    "15_fluxo_sistema.md",
    "16_requisitos_funcionais.md",
    "17_requisitos_nao_funcionais.md",
]

def validate_context(directory: str | Path) -> dict:
    root = Path(directory)
    missing = [name for name in REQUIRED_CONTEXT_FILES if not (root / name).is_file()]
    empty = [name for name in REQUIRED_CONTEXT_FILES if (root / name).is_file() and (root / name).stat().st_size == 0]
    return {"valid": not missing and not empty, "missing": missing, "empty": empty}

if __name__ == "__main__":
    result = validate_context(Path(__file__).resolve().parent / "Contexto_Sistema_Laudos_SST")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["valid"] else 1)
