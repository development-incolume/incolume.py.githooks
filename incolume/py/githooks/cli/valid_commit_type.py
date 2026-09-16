#!/usr/bin/env python
import sys

commit_msg_file = sys.argv[1]

with open(commit_msg_file, "r") as f:
    commit_msg = f.read()

if not commit_msg.startswith("feat") and not commit_msg.startswith("fix"):
    print("Erros: Mensagens devem começar com 'feat' ou 'fix'")
    sys.exit(1)

print("Mensagem validada com sucesso.")
sys.exit(0)   