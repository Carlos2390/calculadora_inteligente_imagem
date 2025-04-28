# Calculadora Inteligente por Imagem

Sistema que combina OCR (Reconhecimento Óptico de Caracteres) e IA para resolver expressões matemáticas manuscritas através de uma interface web amigável.

## Funcionalidades
- Captura de expressões matemáticas via imagem
- Reconhecimento de texto usando Tesseract OCR
- Correção automática de erros de reconhecimento com IA
- Cálculo seguro de expressões matemáticas
- Interface web intuitiva com Gradio

## Pré-requisitos
1. **Tesseract OCR** instalado no sistema:
   - **Windows**: [Instalador](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Linux**: `sudo apt install tesseract-ocr`
   - **Mac**: `brew install tesseract`

2. Ambiente Python 3.8+

## Instalação
```bash
  git clone <URL_DO_REPOSITORIO>
  cd <NOME_DO_REPOSITORIO>
  python -m venv venv && source venv/bin/activate  # Linux/MacOS (ou use "venv\Scripts\activate" no Windows)
  pip install -r requirements.txt
```
## Uso
```bash
  python <nome_do_script>.py
```
O sistema iniciará um servidor local e abrirá automaticamente uma interface no navegador.

## Passo a passo:

  - Tire uma foto da expressão matemática escrita à mão
  - Acesse a interface no link fornecido
  - Clique em "Upload" para enviar a imagem
  - Aguarde o processamento (OCR + IA + Cálculo)
  - Veja o resultado com detalhes do processamento

## Limitações

  - Funciona melhor com texto claro e bem espaçado
  - Suporta apenas operadores básicos (+, -, *, /, **, %)
  - Performance depende da qualidade da imagem


## Autores

  - Carlos Matos | RGM: 29622182
  - Gustavo Taglianetti | RGM: 29649111
