#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    import main_new
    print("✓ Importaciones de main_new.py exitosas")
except Exception as e:
    print(f"✗ Error en importaciones: {e}")
    import traceback
    traceback.print_exc()