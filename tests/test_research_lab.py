import unittest

from analisador_base import anonymize_text
from analisador_regras import classify_document, detect_chapters, detect_risks

class ResearchLabTests(unittest.TestCase):
    def test_anonymizes_common_identifiers(self):
        text = "CPF 123.456.789-00 CNPJ 12.345.678/0001-90 processo 1234567-89.2026.5.04.0001"
        safe = anonymize_text(text)
        self.assertNotIn("123.456.789-00", safe)
        self.assertNotIn("12.345.678/0001-90", safe)
        self.assertIn("[CPF_REMOVIDO]", safe)
        self.assertIn("[CNPJ_REMOVIDO]", safe)
        self.assertIn("[PROCESSO]", safe)

    def test_classifies_insalubridade_report(self):
        category, _, confidence, _ = classify_document(
            "laudo.docx",
            "Laudo pericial da Vara do Trabalho. Análise de insalubridade conforme NR-15."
        )
        self.assertEqual(category, "laudo judicial de insalubridade")
        self.assertGreaterEqual(confidence, 90)

    def test_detects_risk_and_chapter_signals(self):
        text = "Metodologia com dosimetria de ruído. Conclusão e quesitos do juízo."
        self.assertIn("R-FIS-01", detect_risks(text))
        self.assertIn("metodologia", detect_chapters(text))
        self.assertIn("conclusao", detect_chapters(text))

if __name__ == "__main__":
    unittest.main()
