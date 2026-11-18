#!/usr/bin/env python3
"""Reconstrói a planilha consolidada (energia + dinheiro) do zero.

Uso:  cd financeiro/scripts && python3 atualizar_consolidado.py

Fontes: financeiro/relatorios/*.pdf (energia) e financeiro/extratos/* (dinheiro).
Para incluir um extrato novo, solte o PDF em financeiro/extratos/ e rode este script.
"""
import os, subprocess, sys, glob, shutil
AQUI=os.path.dirname(os.path.abspath(__file__))
XLSX=os.path.join(AQUI,"..","Fotovolt_Curral_Novo_Consolidado.xlsx")
ETAPAS=["parse.py","normaliza.py","parse_extrato.py","build_consolidado.py",
        "build_consolidado2.py","build_consolidado3.py","build_consolidado4.py"]
def main():
    os.chdir(AQUI)
    ex=glob.glob(os.path.join(AQUI,"..","extratos","*"))
    if not ex: sys.exit("Nenhum extrato em financeiro/extratos/.")
    print(f"{len(ex)} arquivos de extrato encontrados.")
    if os.path.exists(XLSX):
        shutil.copy(XLSX,XLSX+".bak"); os.remove(XLSX)
    for e in ETAPAS:
        print(f"  → {e}")
        r=subprocess.run([sys.executable,"-I",e],capture_output=True,text=True)
        if r.returncode: sys.exit(f"FALHOU em {e}:\n{r.stdout}\n{r.stderr}")
    cand=glob.glob(os.path.expanduser("~/.claude/skills/synced/*/xlsx/scripts/recalc.py"))
    if cand:
        print("  → recalculando fórmulas")
        r=subprocess.run([sys.executable,cand[0],os.path.abspath(XLSX),"240"],
                         capture_output=True,text=True)
        print(r.stdout.strip())
        if '"total_errors": 0' not in r.stdout:
            sys.exit("ATENÇÃO: saiu com erro de fórmula. Não entregue assim.")
    else:
        print("  ! recalc.py não encontrado — abra no Excel para calcular.")
    print(f"\nPronto: {os.path.abspath(XLSX)}")
if __name__=="__main__": main()
