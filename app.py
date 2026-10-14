"""
Ponto de entrada principal da aplicação PDP 2025 (Streamlit).
Permite a execução direta via 'streamlit run app.py' ou integração com plataformas de deploy.
"""

import sys
from pathlib import Path

# Adiciona o diretório src ao sys.path para importação dos módulos internos
src_dir = Path(__file__).resolve().parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from dashboard import main

if __name__ == "__main__":
    main()
