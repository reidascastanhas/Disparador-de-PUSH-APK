"""
Wrapper para iniciar o bot com tratamento de erros.
Salva qualquer erro em crash-log.txt antes de morrer.
"""
import sys
import os

# Forçar UTF-8 ANTES de qualquer import que use print
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

# Mudar para o diretório do script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Redirecionar stdout/stderr para arquivo se não houver console
log_file = open("bot-output.log", "w", encoding="utf-8")
if sys.stdout is None or not hasattr(sys.stdout, "write"):
    sys.stdout = log_file
else:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        sys.stdout = log_file

if sys.stderr is None or not hasattr(sys.stderr, "write"):
    sys.stderr = log_file
else:
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        sys.stderr = log_file

try:
    # Executar o bot como __main__
    import runpy
    runpy.run_path("rei-castanhas-bot-v2.py", run_name="__main__")
except KeyboardInterrupt:
    pass
except Exception as e:
    with open("crash-log.txt", "w", encoding="utf-8") as f:
        import traceback
        f.write(f"CRASH em {__file__}\n")
        f.write(f"Erro: {e}\n\n")
        traceback.print_exc(file=f)
