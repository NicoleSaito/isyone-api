import subprocess
import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")


def run_script(script_name: str, args: list[str] = []) -> dict:
    """
    Executa um shell script e retorna o resultado como dict.
    O script deve retornar JSON válido no stdout.
    """
    script_path = os.path.join(SCRIPTS_DIR, script_name)

    if not os.path.isfile(script_path):
        logger.error(f"Script não encontrado: {script_path}")
        return {"status": "error", "message": f"Script '{script_name}' não encontrado"}

    if not os.access(script_path, os.X_OK):
        os.chmod(script_path, 0o755)

    try:
        result = subprocess.run(
            ["bash", script_path] + [str(a) for a in args],
            capture_output=True,
            text=True,
            timeout=30,
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if stderr:
            logger.warning(f"[{script_name}] stderr: {stderr}")

        if not stdout:
            return {
                "status": "error",
                "message": "Script não retornou saída",
                "exit_code": result.returncode,
            }

        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return {
                "status": "success" if result.returncode == 0 else "error",
                "output": stdout,
                "exit_code": result.returncode,
            }

    except subprocess.TimeoutExpired:
        logger.error(f"[{script_name}] Timeout após 30s")
        return {"status": "error", "message": "Script excedeu o tempo limite de 30 segundos"}

    except Exception as e:
        logger.exception(f"[{script_name}] Erro inesperado: {e}")
        return {"status": "error", "message": f"Erro interno: {str(e)}"}
