"""
Testes automatizados para validação de dados, integridade dos níveis e consistência.
Atende a task2.md (item 2.8) e task4.md.
"""

import os
import tempfile
import unittest
import pandas as pd
from pathlib import Path
import sys

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from data_validation import validate_filled_dataset, ALLOWED_LEVELS
from data_loader import load_and_filter_docentes, get_docente_evaluations

class TestDataValidation(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.orig_csv = self.base_dir / 'data' / 'arquivo_original.csv'
        self.filled_csv = self.base_dir / 'data' / 'arquivo_preenchido.csv'
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_allowed_levels_set(self):
        expected_levels = {'Não atende', 'Atende parcialmente', 'Atende integralmente', 'Supera'}
        self.assertEqual(ALLOWED_LEVELS, expected_levels)

    def test_validate_real_datasets(self):
        # Validação do arquivo real do projeto
        if self.orig_csv.exists() and self.filled_csv.exists():
            res = validate_filled_dataset(str(self.orig_csv), str(self.filled_csv))
            self.assertTrue(res['is_valid'], f"Erros na validação: {res['errors']}")
            self.assertEqual(res['total_rows_original'], 1135)
            self.assertEqual(res['total_rows_filled'], 1135)
            self.assertEqual(res['total_cols_original'], 152)
            self.assertEqual(res['total_cols_filled'], 152)
            self.assertTrue(res['columns_match'])
            self.assertEqual(len(res['invalid_values']), 0)

    def test_validation_detects_row_count_mismatch(self):
        mock_orig = os.path.join(self.temp_dir.name, "orig.csv")
        mock_filled = os.path.join(self.temp_dir.name, "filled.csv")
        
        # Base com 152 colunas mínimas
        cols = [f"Col_{i}" for i in range(152)]
        cols[78] = "Nivel_T2_Plan"
        cols[80] = "Nivel_T2_Prat"
        cols[82] = "Nivel_T1_Plan"
        cols[84] = "Nivel_T1_Prat"
        
        df1 = pd.DataFrame(columns=cols)
        df1.loc[0] = [""] * 152
        df1.to_csv(mock_orig, index=False)
        
        df2 = pd.DataFrame(columns=cols)
        df2.loc[0] = [""] * 152
        df2.loc[1] = [""] * 152  # Linha extra
        df2.to_csv(mock_filled, index=False)
        
        res = validate_filled_dataset(mock_orig, mock_filled)
        self.assertFalse(res['is_valid'])
        self.assertTrue(any("linhas" in e for e in res['errors']))

    def test_validation_detects_invalid_levels(self):
        mock_orig = os.path.join(self.temp_dir.name, "orig.csv")
        mock_filled = os.path.join(self.temp_dir.name, "filled.csv")
        
        cols = [f"Col_{i}" for i in range(152)]
        cols[78] = "Nivel_T2_Plan"
        cols[80] = "Nivel_T2_Prat"
        cols[82] = "Nivel_T1_Plan"
        cols[84] = "Nivel_T1_Prat"
        
        df1 = pd.DataFrame(columns=cols)
        df1.loc[0] = [""] * 152
        df1.to_csv(mock_orig, index=False)
        
        df2 = pd.DataFrame(columns=cols)
        df2.loc[0] = [""] * 152
        df2.loc[0, cols[82]] = "Excelente"  # Rótulo não autorizado
        df2.to_csv(mock_filled, index=False)
        
        res = validate_filled_dataset(mock_orig, mock_filled)
        self.assertFalse(res['is_valid'])
        self.assertIn(cols[82], res['invalid_values'])

    def test_results_update_reflects_data_change(self):
        # Testa a atualização dinâmica após modificação na base
        mock_csv = os.path.join(self.temp_dir.name, "dynamic_test.csv")
        cols = [f"Col_{i}" for i in range(100)]
        cols[2] = "Nome"
        cols[33] = "2º ANO - Selecione a modalidade do cursista"
        cols[34] = "Componente"
        cols[86] = "Tema"
        cols[82] = "Nivel_T1_Plan"
        cols[84] = "Nivel_T1_Prat"
        
        df = pd.DataFrame(columns=cols)
        df.loc[0, "Nome"] = "PROF 1"
        df.loc[0, cols[33]] = "Docentes"
        df.loc[0, cols[86]] = "Tema I"
        df.loc[0, cols[82]] = "Atende parcialmente"
        df.loc[0, cols[84]] = "Atende parcialmente"
        df.to_csv(mock_csv, index=False)
        
        df_loaded, _ = load_and_filter_docentes(mock_csv)
        evals_1 = get_docente_evaluations(df_loaded)
        self.assertEqual(evals_1['nivel_atendimento'].value_counts()['Atende parcialmente'], 2)
        
        # Alteração na base
        df.loc[0, cols[82]] = "Atende integralmente"
        df.to_csv(mock_csv, index=False)
        
        df_reloaded, _ = load_and_filter_docentes(mock_csv)
        evals_2 = get_docente_evaluations(df_reloaded)
        self.assertEqual(evals_2['nivel_atendimento'].value_counts()['Atende integralmente'], 1)
        self.assertEqual(evals_2['nivel_atendimento'].value_counts()['Atende parcialmente'], 1)

if __name__ == '__main__':
    unittest.main()
