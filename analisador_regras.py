from __future__ import annotations

import re
from typing import List, Tuple

CHAPTER_PATTERNS = [
    ("identificacao_processo", [r"processo\s+n[ºo.]?", r"autos\s+n[ºo.]?"]),
    ("objetivo", [r"objetivo\s+da\s+per[ií]cia", r"finalidade"]),
    ("data_horario_local", [r"data[,\s]+hor[aá]rio\s+e\s+local", r"dilig[eê]ncia", r"inspe[cç][aã]o\s+pericial"]),
    ("cargo_funcao", [r"cargo\s+e\s+fun[cç][aã]o", r"fun[cç][aã]o\s+exercida"]),
    ("setor_ambiente", [r"descri[cç][aã]o\s+do\s+ambiente", r"local\s+de\s+trabalho"]),
    ("metodologia", [r"metodologia", r"crit[eé]rios\s+t[eé]cnicos", r"normas\s+aplic[aá]veis"]),
    ("atividades_reclamante", [r"atividades\s+segundo\s+o\s+reclamante", r"vers[aã]o\s+do\s+autor"]),
    ("atividades_reclamada", [r"atividades\s+segundo\s+a\s+reclamada", r"vers[aã]o\s+da\s+empresa"]),
    ("divergencias", [r"diverg[eê]ncias", r"controv[eé]rsias", r"pontos\s+controvertidos"]),
    ("riscos_fisicos", [r"riscos\s+f[ií]sicos", r"ru[ií]do", r"calor", r"vibra[cç][aã]o"]),
    ("riscos_quimicos", [r"riscos\s+qu[ií]micos", r"hidrocarbonetos", r"poeiras", r"fumos\s+de\s+solda"]),
    ("riscos_biologicos", [r"riscos\s+biol[oó]gicos", r"lixo\s+urbano", r"esgoto", r"hospital"]),
    ("periculosidade", [r"periculosidade", r"inflam[aá]veis", r"eletricidade", r"explosivos"]),
    ("epis", [r"equipamentos\s+de\s+prote[cç][aã]o\s+individual", r"ficha\s+de\s+epi"]),
    ("conclusao", [r"conclus[aã]o", r"parecer\s+conclusivo", r"enquadramento\s+t[eé]cnico"]),
    ("quesitos", [r"quesitos\s+do\s+ju[ií]zo", r"quesitos\s+do\s+reclamante", r"quesitos\s+da\s+reclamada"]),
    ("fotografias", [r"fotografias", r"relat[oó]rio\s+fotogr[aá]fico", r"registro\s+fotogr[aá]fico"]),
]

RISK_CATALOG = {
    "R-FIS-01": {
        "nome": "Ruído Contínuo ou Intermitente",
        "cat": "Físico",
        "referencia": "NR-15 Anexo 1 / NHO-01",
        "keywords": ["ruído", "ruido", "dosimetria", "dosímetro", "nen", "laeq", "db(a)"],
    },
    "R-FIS-03": {
        "nome": "Calor / Sobrecarga Térmica",
        "cat": "Físico",
        "referencia": "NR-15 Anexo 3 / NHO-06",
        "keywords": ["calor", "ibutg", "termômetro de globo", "taxa metabólica", "forno"],
    },
    "R-FIS-07": {
        "nome": "Vibrações",
        "cat": "Físico",
        "referencia": "NR-15 Anexo 8 / NHO-09 / NHO-10",
        "keywords": ["vibração", "vibrações", "corpo inteiro", "mãos e braços", "aren", "vdvr"],
    },
    "R-QUI-01": {
        "nome": "Poeiras Minerais",
        "cat": "Químico",
        "referencia": "NR-15 Anexo 12 / NHO-08",
        "keywords": ["sílica", "silica", "poeira mineral", "amianto", "manganês", "granito"],
    },
    "R-QUI-03": {
        "nome": "Hidrocarbonetos e outros químicos",
        "cat": "Químico",
        "referencia": "NR-15 Anexo 13",
        "keywords": ["hidrocarbonetos", "óleo mineral", "graxa", "solvente", "gasolina", "tintas"],
    },
    "R-BIO-01": {
        "nome": "Agentes Biológicos",
        "cat": "Biológico",
        "referencia": "NR-15 Anexo 14",
        "keywords": ["biológico", "lixo urbano", "esgoto", "hospital", "sangue", "perfurocortante"],
    },
    "R-PER-01": {
        "nome": "Periculosidade por Inflamáveis",
        "cat": "Periculosidade",
        "referencia": "NR-16 Anexo 2",
        "keywords": ["inflamáveis", "tanque de combustível", "abastecimento", "glp"],
    },
    "R-PER-02": {
        "nome": "Periculosidade por Eletricidade",
        "cat": "Periculosidade",
        "referencia": "NR-16 Anexo 4",
        "keywords": ["eletricidade", "alta tensão", "subestação", "quadro de distribuição", "eletricista"],
    },
    "R-ERG-01": {
        "nome": "Ergonomia",
        "cat": "Ergonômico",
        "referencia": "NR-17",
        "keywords": ["ergonomia", "levantamento manual de cargas", "postura inadequada", "movimentos repetitivos"],
    },
}

def detect_chapters(text: str) -> list[str]:
    source = (text or "").lower()
    return [
        chapter_id
        for chapter_id, patterns in CHAPTER_PATTERNS
        if any(re.search(pattern, source) for pattern in patterns)
    ]

def detect_risks(text: str) -> list[str]:
    source = (text or "").lower()
    return [
        risk_id
        for risk_id, info in RISK_CATALOG.items()
        if any(keyword in source for keyword in info["keywords"])
    ]

def classify_document(
    filename: str,
    text_sample: str,
    is_docx: bool = False,
    has_tables: bool = False,
    has_images: bool = False,
) -> Tuple[str, List[str], int, str]:
    source = (filename + " " + (text_sample or "")).lower()

    if any(term in source for term in ["questionário de perícia", "formulário de inspeção", "roteiro de perícia"]):
        return "questionário/formulário de perícia", [], 90, "Estrutura típica de coleta em campo."

    if any(term in source for term in ["aposentadoria especial", "decreto 3.048", "perfil profissiográfico", "ltcat"]):
        secondary = ["LTCAT"] if "ltcat" in source else []
        return "laudo previdenciário", secondary, 85, "Conteúdo previdenciário / aposentadoria especial."

    if any(term in source for term in ["programa de gerenciamento de riscos", "inventário de riscos", "pgr"]):
        return "PGR", ["inventário de riscos"], 85, "Estrutura compatível com gerenciamento de riscos."

    if any(term in source for term in ["manifestação ao laudo", "impugnação ao laudo", "parecer técnico divergente", "assistente técnico"]):
        return "manifestação ou impugnação", ["parecer técnico"], 85, "Peça técnica relacionada a laudo/perícia."

    if any(term in source for term in ["laudo pericial", "laudo técnico pericial", "inspeção pericial", "vara do trabalho", "perito do juízo"]):
        has_insal = any(term in source for term in ["insalubridade", "nr-15", "insalubre"])
        has_peric = any(term in source for term in ["periculosidade", "nr-16", "periculoso"])
        if has_insal and has_peric:
            return "laudo combinado", ["insalubridade", "periculosidade"], 95, "Laudo trabalhista combinado."
        if has_insal:
            return "laudo judicial de insalubridade", [], 95, "Laudo focado em insalubridade."
        if has_peric:
            return "laudo judicial de periculosidade", [], 95, "Laudo focado em periculosidade."
        return "laudo pericial genérico", [], 80, "Estrutura geral de laudo pericial."

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        return "fotografia/anexo", [], 95, "Arquivo de imagem."
    if filename.lower().endswith((".xlsx", ".xls", ".csv")):
        return "medição quantitativa", ["inventário de riscos"], 75, "Planilha de medição/cadastro/cálculo."

    return "documento administrativo", [], 60, "Documento acessório de suporte."
