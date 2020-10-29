# -*- coding: utf-8 -*-

import subprocess

scripts_paths = ("server.py", "network.py")

ps = [subprocess.Popen(["python", script]) for script in scripts_paths]
exit_codes = [p.wait() for p in ps]

if not any(exit_codes):
    print("Todos los procesos terminaron con éxito")
else:
    print("Algunos procesos terminaron de forma inesperada.")
