import subprocess
import os
import json
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from core.database import LogModel
from core.security import sanitize_param

logger = logging.getLogger(__name__)

SCRIPTS_DIR = os.getenv("SCRIPTS_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))


def run_script(script_filename: str, args: list[str], db: Session) -> dict:
    script_path = os.path.join(SCRIPTS_DIR, script_filename)
    params_str = " ".join(args)

    # Sanitizar todos os parâmetros antes de qualquer execução
    safe_args = []
    for arg in args:
        safe_args.append(sanitize_param(str(arg)))

    status = "error"
    output = None
    error = None
    result_data = {}

    if not os.path.isfile(script_path):
        error = f"Script '{script_filename}' não encontrado em {SCRIPTS_DIR}"
        logger.error(error)
        result_data = {"status": "error", "message": error}
    else:
        if not os.access(script_path, os.X_OK):
            os.chmod(script_path, 0o755)

        try:
            result = subprocess.run(
                ["bash", script_path] + safe_args,
                capture_output=True,
                text=True,
                timeout=60,
            )

            output = result.stdout.strip()
            error = result.stderr.strip() if result.stderr.strip() else None

            if result.returncode == 0:
                status = "success"
            else:
                status = "error"

            try:
                result_data = json.loads(output) if output else {}
            except json.JSONDecodeError:
                result_data = {
                    "status": status,
                    "output": output,
                    "exit_code": result.returncode,
                }

        except subprocess.TimeoutExpired:
            error = "Script excedeu o tempo limite de 60 segundos"
            result_data = {"status": "error", "message": error}

        except Exception as e:
            error = str(e)
            logger.exception(f"Erro ao executar {script_filename}: {e}")
            result_data = {"status": "error", "message": f"Erro interno: {error}"}

    # Persistir log no banco independentemente do resultado
    log = LogModel(
        script_name=script_filename,
        parameters=params_str if params_str else None,
        status=status,
        output=output,
        error=error,
        executed_at=datetime.utcnow(),
    )
    db.add(log)
    db.commit()

    return result_data
