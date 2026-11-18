#!/usr/bin/env python3
"""Refaz a planilha inteira a partir dos PDFs em financeiro/relatorios/.

Uso:  cd financeiro/scripts && python3 atualizar.py

Passo 1 da regra do repositório (ver CLAUDE.md). Para incluir um relatório novo,
basta soltar o PDF em financeiro/relatorios/ e rodar este script: tudo é
recalculado do zero, inclusive o dashboard energético.
"""
import os, subprocess, sys, glob, shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(AQUI, "..", "LF_Agropastoril_Analise_Relatorios_2026.xlsx")
ETAPAS = ["parse.py","normaliza.py","build.py","build2.py","build3.py",
          "build4.py","build5.py","build6.py","build7.py","fix_final.py"]

def main():
    os.chdir(AQUI)
    pdfs = sorted(glob.glob(os.path.join(AQUI,"..","relatorios","*.pdf")))
    if not pdfs:
        sys.exit("Nenhum PDF em financeiro/relatorios/.")
    print(f"{len(pdfs)} relatórios encontrados.")
    if os.path.exists(XLSX):
        shutil.copy(XLSX, XLSX + ".bak")
        os.remove(XLSX)
    for e in ETAPAS:
        print(f"  → {e}")
        r = subprocess.run([sys.executable,"-I",e],capture_output=True,text=True)
        if r.returncode:
            sys.exit(f"FALHOU em {e}:\n{r.stdout}\n{r.stderr}")
    recalc = os.path.expanduser("~/.claude/skills/synced")
    cand = glob.glob(os.path.join(recalc,"*","xlsx","scripts","recalc.py"))
    if cand:
        print("  → recalculando fórmulas")
        r = subprocess.run([sys.executable,cand[0],os.path.abspath(XLSX),"180"],
                           capture_output=True,text=True)
        print(r.stdout.strip())
        if '"total_errors": 0' not in r.stdout:
            sys.exit("ATENÇÃO: a planilha saiu com erros de fórmula. Não entregue assim.")
    else:
        print("  ! recalc.py não encontrado — abra a planilha no Excel para calcular as fórmulas.")
    print(f"\nPronto: {os.path.abspath(XLSX)}")

if __name__ == "__main__":
    main()
