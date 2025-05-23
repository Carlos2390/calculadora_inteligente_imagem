# Importação de bibliotecas
import ast                # Para análise segura de expressões matemáticas
import operator as op     # Operadores matemáticos seguros
from transformers import pipeline  # Pipeline de IA para correção de texto
import gradio as gr       # Framework para interface web
import pytesseract        # OCR para extrair texto de imagens
from PIL import Image     # Manipulação de imagens

# Dicionário de operações matemáticas permitidas (segurança)
OPERATORS = {
    ast.Add: op.add,      # Soma
    ast.Sub: op.sub,      # Subtração
    ast.Mult: op.mul,     # Multiplicação
    ast.Div: op.truediv,  # Divisão
    ast.Pow: op.pow,      # Potência
    ast.Mod: op.mod,      # Módulo
    ast.USub: op.neg,     # Negativo (operador unário)
}

# Função para avaliar expressões matemáticas de forma segura
def eval_expr(expr: str):
    try:
        # Converte a string em Abstract Syntax Tree (AST)
        expr_ast = ast.parse(expr, mode='eval').body
        return eval_ast(expr_ast)
    except Exception as err:
        raise ValueError(f"Erro na análise da expressão: {err}")

# Avalia recursivamente os nós da AST
def eval_ast(node):
    # Caso base: números
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, "n") else node.value

    # Operações binárias (+, -, *, etc)
    elif isinstance(node, ast.BinOp):
        left = eval_ast(node.left)
        right = eval_ast(node.right)
        operator_func = OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Operador não suportado: {node.op}")
        return operator_func(left, right)

    # Operadores unários (ex: -5)
    elif isinstance(node, ast.UnaryOp):
        operand = eval_ast(node.operand)
        operator_func = OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Operador não suportado: {node.op}")
        return operator_func(operand)

    else:
        raise ValueError("Expressão contém elementos não permitidos.")

# Configuração do modelo de correção gramatical em francês (adaptado para matemática)
corrector = pipeline("text2text-generation", model="PoloHuggingface/French_grammar_error_corrector")

# Função para corrigir expressões usando IA
def correct_expression(expression: str) -> str:
    try:
        correction_output = corrector(expression)
        return correction_output[0]['generated_text'].strip()
    except Exception:
        return expression  # Fallback para a expressão original

# Processamento principal da imagem
def process_image(image):
    try:
        # OCR: Extrai texto da imagem com configurações otimizadas para matemática
        text = pytesseract.image_to_string(
            image,
            config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789+-*/.()^%'
        )
        # Limpeza do texto extraído
        text = text.strip().replace(' ', '').replace('\n', '').replace('\x0c', '')

        if not text:
            return "Não foi possível detectar texto na imagem."

        # Tentativa de cálculo direto
        try:
            result = eval_expr(text)
            return f"Expressão detectada:\n{text}\n\nResultado: {result}"

        # Se falhar, tenta correção com IA
        except Exception as err:
            corrected_expression = correct_expression(text)
            try:
                result = eval_expr(corrected_expression)
                return (f"Expressão original (OCR): {text}\n\n"
                        f"Expressão corrigida via IA:\n{corrected_expression}\n\n"
                        f"Resultado: {result}")
            except Exception as err2:
                return (f"Erro na expressão detectada: {err}\n\n"
                        f"Tentativa de correção falhou: {err2}\n"
                        f"Expressão corrigida: {corrected_expression}")

    except Exception as e:
        return f"Erro no processamento da imagem: {str(e)}"

# Interface Gradio
iface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type='pil', label="Envie uma imagem do cálculo escrito à mão"),
    outputs="text",
    title="Calculadora por Imagem com IA",
    description="Sistema que combina OCR e IA para resolver expressões matemáticas manuscritas",
    allow_flagging="never"
)

iface.launch(share=True)
