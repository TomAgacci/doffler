# demo_hsn_live.py

import threading
import math
from doffler_engine_hsn import HSNRegistry, DofflerEngine, DofflerContext
from hsn_live_reload import HSNLiveReloader
from hsn_visual_inspector import visual_registry_inspector

def main():
    registry = HSNRegistry()
    ctx = DofflerContext()
    engine = DofflerEngine(ctx)

    reloader = HSNLiveReloader(registry, directory="./hsn_modules", interval=1.0)
    t = threading.Thread(target=reloader.run_forever, daemon=True)
    t.start()

    print("HSN LiveReload running. Edit/add .hsn files in ./hsn_modules.")
    while True:
        input("Press Enter to inspect and test a module...\n")
        visual_registry_inspector(registry)
        if "ramanujan_custom" in registry.list_modules():
            expr = registry.build("ramanujan_custom")
            res = engine.eval_expr(expr)
            print("ramanujan_custom value:", res.value)
            print("vs e:", engine.compare_to_constant(res.value, math.e, "e").meta)

if __name__ == "__main__":
    main()
