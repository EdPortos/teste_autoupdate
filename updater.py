import urllib.request
import os
import sys

GITHUB_USER = "EdPortos"
GITHUB_REPO = "teste_autoupdate"
BRANCH = "main"

RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}"

VERSION_URL = f"{RAW_BASE}/version.txt"
MAIN_URL    = f"{RAW_BASE}/main.py"


def fetch_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=5) as resp:
        return resp.read().decode("utf-8").strip()


def check_and_update(current_version: str):
    print(f"Versão local: v{current_version}")

    try:
        remote_version = fetch_text(VERSION_URL)
        print(f"Versão remota: v{remote_version}")
    except Exception as e:
        print(f"[updater] Não foi possível verificar atualizações: {e}")
        return

    if remote_version == current_version:
        print("[updater] Aplicação já está na versão mais recente.\n")
        return

    print(f"[updater] Nova versão encontrada! Baixando v{remote_version}...")

    try:
        new_code = fetch_text(MAIN_URL)
    except Exception as e:
        print(f"[updater] Falha ao baixar atualização: {e}")
        return

    # Substitui o próprio main.py
    script_path = os.path.abspath(__file__)
    main_path   = os.path.join(os.path.dirname(script_path), "main.py")

    with open(main_path, "w", encoding="utf-8") as f:
        f.write(new_code)

    print(f"[updater] Atualizado para v{remote_version}! Reiniciando...\n")

    # Reinicia o processo com os mesmos argumentos
    # Usa subprocess no Windows para lidar com caminhos com espaços
    if sys.platform == "win32":
        import subprocess
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit(0)
    else:
        os.execv(sys.executable, [sys.executable] + sys.argv)