bat_content = """@echo off
title Dimensionamento Pluvial NBR 10844
echo Iniciando o servidor do Streamlit...

:: Caso utilize um ambiente virtual local, remova o "::" da linha abaixo e ajuste o nome da pasta se necessario
:: call venv\\Scripts\\activate

streamlit run app.py
pause
"""

file_path = "iniciar_app.bat"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(bat_content)

print(file_path)