"""Tools the agent can call. Each tool takes a string and returns a string."""
import ast
import operator

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("exponent too large")
        return _OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


def calculate(expression: str) -> str:
    """Safely evaluate basic arithmetic (+ - * / ** %). No eval()."""
    try:
        result = _eval(ast.parse(expression.strip(), mode="eval").body)
    except ZeroDivisionError:
        return "error: division by zero"
    except (ValueError, SyntaxError) as exc:
        return f"error: {exc}"
    return str(int(result)) if float(result).is_integer() else str(round(result, 6))


def word_count(text: str) -> str:
    """Count words and characters in a piece of text."""
    words = text.split()
    return f"{len(words)} words, {len(text)} characters"


def reverse(text: str) -> str:
    """Reverse a string."""
    return text[::-1]


TOOLS = {
    "calculate": calculate,
    "word_count": word_count,
    "reverse": reverse,
}
