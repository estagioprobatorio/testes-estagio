"""
Testes automatizados para filtragem de dados e integridade da modalidade DOCENTE.
Atende a task2.md (item 2.8).
"""

import os
import tempfile
import unittest
import pandas as pd
from pathlib import Path
import sys

# Adiciona o diretório src ao path de importação
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from data_loader import (
    load_and_filter_docentes,
    find_modality_column,
    get_criteria_metadata,
    get_docente_evaluations
)

class TestDataFiltering(unittest.TestCase):
    def setUp(self):
        # Criação de um conjunto de dados controlado para teste
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mock_csv = os.path.join(self.temp_dir.name, "test_data.csv")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_find_modality_column_success(self):
        df = pd.DataFrame({
            "Carimbo": ["2025/10/14"],
            "Nome": ["PROFESSOR TESTE"],
            "2º ANO - Selecione a modalidade do cursista": ["Docentes"]
        })
        col = find_modality_column(df)
        self.assertEqual(col, "2º ANO - Selecione a modalidade do cursista")

    def test_find_modality_column_missing_raises_error(self):
        df = pd.DataFrame({
            "Carimbo": ["2025/10/14"],
            "Nome": ["PROFESSOR TESTE"]
        })
        with self.assertRaises(ValueError) as context:
            find_modality_column(df)
        self.assertIn("Coluna de modalidade não encontrada", str(context.exception))

    def test_filter_docentes_excludes_other_modalities(self):
        df = pd.DataFrame({
            "Carimbo": ["1", "2", "3", "4"],
            "Nome": ["DOC1", "GESTOR", "TECNICO", "DOC2"],
            "2º ANO - Selecione a modalidade do cursista": ["Docentes", "Equipe Gestora", "Técnico", "Docentes"]
        })
        df.to_csv(self.mock_csv, index=False, encoding='utf-8')
        
        filtered_df, err = load_and_filter_docentes(self.mock_csv)
        self.assertIsNone(err)
        self.assertEqual(len(filtered_df), 2)
        self.assertListEqual(list(filtered_df["Nome"]), ["DOC1", "DOC2"])
        # Garante que não há mistura de modalidades
        modalidades = filtered_df["2º ANO - Selecione a modalidade do cursista"].unique()
        self.assertEqual(list(modalidades), ["Docentes"])

    def test_empty_csv_behavior(self):
        empty_csv = os.path.join(self.temp_dir.name, "empty.csv")
        with open(empty_csv, "w", encoding="utf-8") as f:
            f.write("")
            
        df, msg = load_and_filter_docentes(empty_csv)
        self.assertTrue(df.empty)
        self.assertIn("vazio", msg.lower())

    def test_no_docentes_found_behavior(self):
        df = pd.DataFrame({
            "Nome": ["GESTOR 1", "TECNICO 1"],
            "2º ANO - Selecione a modalidade do cursista": ["Equipe Gestora", "Técnico Pedagógico"]
        })
        df.to_csv(self.mock_csv, index=False, encoding='utf-8')
        
        filtered_df, msg = load_and_filter_docentes(self.mock_csv)
        self.assertTrue(filtered_df.empty)
        self.assertIn("nenhum registro da modalidade docente", msg.lower())

    def test_treatment_of_empty_or_nan_fields(self):
        # Testa a extração de avaliações quando campos de nível são NaN
        cols = [f"Col_{i}" for i in range(100)]
        cols[2] = "Nome"
        cols[33] = "2º ANO - Selecione a modalidade do cursista"
        cols[34] = "Componente"
        cols[86] = "Tema"
        cols[82] = "Nivel_T1_Plan"
        cols[84] = "Nivel_T1_Prat"
        
        df = pd.DataFrame(columns=cols)
        df.loc[0, "Nome"] = "PROFESSOR TESTE"
        df.loc[0, cols[33]] = "Docentes"
        df.loc[0, "Componente"] = "Matemática"
        df.loc[0, "Tema"] = "Tema I"
        df.loc[0, "Nivel_T1_Plan"] = None  # Vazio
        df.loc[0, "Nivel_T1_Prat"] = "Atende integralmente"
        
        evals = get_docente_evaluations(df)
        self.assertEqual(len(evals), 2)
        # O campo vazio deve ser marcado como 'Pendente' e nunca 'Não atende' artificial
        plan_eval = evals[evals['dimensao'] == 'Planejamento'].iloc[0]
        self.assertEqual(plan_eval['nivel_atendimento'], 'Pendente')
        self.assertEqual(plan_eval['situacao'], 'Pendente')

    def test_criteria_metadata_completeness(self):
        meta = get_criteria_metadata()
        self.assertEqual(len(meta), 27)  # 14 Tema I + 13 Tema II
        # Verificar categorias de Bloom permitidas
        allowed_bloom = {"Lembrar", "Compreender", "Aplicar", "Analisar", "Avaliar", "Criar"}
        for cat in meta['categoria_bloom']:
            self.assertIn(cat, allowed_bloom)

if __name__ == '__main__':
    unittest.main()
