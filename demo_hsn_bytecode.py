# demo_hsn_bytecode.py

from doffler_engine_hsn import HSNRegistry, DofflerEngine, DofflerContext
from hsn_bytecode_integration import make_bytecode_builder_from_hsn
import math

def main():
    registry = HSNRegistry()

    expr_str = "(pi * sqrt(163))^(1/(pi * sqrt(163)))"
    builder = make_bytecode_builder_from_hsn(expr_str)
    registry.register("ramanujan_163_bc", builder, "Ramanujan 163 via bytecode")

    ctx = DofflerContext()
    engine = DofflerEngine(ctx)

    expr = registry.build("ramanujan_163_bc")
    val = engine.eval_expr(expr).value
    print("Bytecode value:", val)
    print("vs e:", engine.compare_to_constant(val, math.e, "e").meta)

if __name__ == "__main__":
    main()
