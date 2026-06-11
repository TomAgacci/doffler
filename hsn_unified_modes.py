# hsn_unified_modes.py

import math
import ast
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Dict, Optional

# --- from your existing engine stack ---
from doffler_engine import (
    Expr, Const, add, sub, mul, div, pow_, sqrt,
    DofflerEngine, DofflerContext
)
from doffler_engine_hsn import HSNRegistry as BaseHSNRegistry, HSNModule as BaseHSNModule
from hsn_bytecode import HSNBytecodeVM, HSNBytecodeProgram
from hsn_bytecode_compiler import compile_hsn_expr_to_bytecode


# =========================
# Engine modes
# =========================

class EngineMode(str, Enum):
    DIRECT = "direct"      # direct-float via eval
    AST = "ast"            # Expr tree via AST
    BYTECODE = "bytecode"  # VM bytecode


@dataclass
class HSNModeModule:
    """Module that can be executed under multiple engine modes."""
    name: str
    expr_str: str          # HSN DSL expression
    description: str
    default_mode: EngineMode = EngineMode.AST


# =========================
# AST -> Expr compiler
# =========================

def compile_hsn_expr_to_ast_expr(expr: str) -> Expr:
    """
    Compile HSN DSL to your Expr tree.
    DSL: pi, e, sqrt(), + - * / ^, parentheses.
    """
    expr_py = expr.replace("^", "**")
    expr_py = expr_py.replace("pi", "math.pi")
    expr_py = expr_py.replace("e", "math.e")
    expr_py = expr_py.replace("sqrt", "math.sqrt")

    tree = ast.parse(expr_py, mode="eval")

    def compile_node(node) -> Expr:
        if isinstance(node, ast.Expression):
            return compile_node(node.body)

        if isinstance(node, ast.Constant):
            return Const(float(node.value))

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                inner = compile_node(node.operand)
                return mul(Const(-1.0), inner)
            raise ValueError("Unsupported unary op")

        if isinstance(node, ast.BinOp):
            left = compile_node(node.left)
            right = compile_node(node.right)

            if isinstance(node.op, ast.Add):
                return add(left, right)
            if isinstance(node.op, ast.Sub):
                return sub(left, right)
            if isinstance(node.op, ast.Mult):
                return mul(left, right)
            if isinstance(node.op, ast.Div):
                return div(left, right)
            if isinstance(node.op, ast.Pow):
                return pow_(left, right)
            raise ValueError("Unsupported binary op")

        if isinstance(node, ast.Call):
            # only math.sqrt
            if not isinstance(node.func, ast.Attribute):
                raise ValueError("Unsupported call")
            if not (isinstance(node.func.value, ast.Name) and node.func.value.id == "math"):
                raise ValueError("Unsupported namespace")
            if node.func.attr != "sqrt":
                raise ValueError("Only math.sqrt
