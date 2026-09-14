#!/usr/bin/env python
import sys
import subprocess
import re

def get_issue_from_branch():
    """Extrai o número do ticket do nome do branch."""
    # Obtém o nome do branch atual
    branch = subprocess.check_output(
        ["git", "symbolic-ref", "--short", "HEAD"]
    ).strip().decode("utf-8")
    
    # Exemplo: branch 'issue-123-fix-bug' -> '123'
    match = re.match(r'issue-(\d+)', branch)
    if match:
        return match.group(1)
    return None

def main():
    # Verifica se o hook foi chamado com a opção -m (mensagem fornecida pelo usuário)
    # Se sim, evita sobrescrever a mensagem manualmente inserida
    commit_type = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if commit_type == "message":
        return

    commit_msg_filepath = sys.argv[1]
    issue_number = get_issue_from_branch()

    if issue_number:
        header = f"[ISSUE-{issue_number}] "
        
        with open(commit_msg_filepath, "r+") as f:
            content = f.read()
            # Prependa o header se não existir já
            if not content.startswith(header):
                f.seek(0, 0)
                f.write(header + content)

if __name__ == "__main__":
    main()   