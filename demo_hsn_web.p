# demo_hsn_web.py

from doffler_engine_hsn import HSNRegistry
from hsn_loader import register_hsn_file
from hsn_web_inspector import start_hsn_web_inspector

def main():
    registry = HSNRegistry()
    register_hsn_file(registry, "./hsn_modules/ramanujan_custom.hsn")
    register_hsn_file(registry, "./hsn_modules/phi_bridge.hsn")

    start_hsn_web_inspector(registry, port=8080)
    input("HSN Web Inspector running. Open http://127.0.0.1:8080 and press Enter to exit...\n")

if __name__ == "__main__":
    main()
