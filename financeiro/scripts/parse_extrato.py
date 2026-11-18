# -*- coding: utf-8 -*-
"""Consolida o extrato bancario da SPE: historico do xlsx + PDFs do Banco Inter."""
import os, re, json, glob, subprocess, datetime
from openpyxl import load_workbook

AQUI=os.path.dirname(os.path.abspath(__file__))
EXT=os.path.join(AQUI,"..","extratos")
MES={"janeiro":1,"fevereiro":2,"marco":3,"março":3,"abril":4,"maio":5,"junho":6,
     "julho":7,"agosto":8,"setembro":9,"outubro":10,"novembro":11,"dezembro":12}

def categoriza(desc, valor):
    d=desc.upper()
    if "DARF" in d: return "Impostos (DARF)"
    if "COLETIVA" in d: return "Contabilidade"
    if "SOLCARE" in d or "RETROFIT" in d: return "O&M / Manutenção"
    if "SPE POCOES" in d or "SPE POÇÕES" in d: return "Ressarcimento - SPE Poções"
    if "BRO ENERGY" in d: return "Receita Energia" if valor>0 else "Investimento - Usina (BRO Energy)"
    for n,c in [("GUILHERME","Guilherme"),("LUIZ FELIPE","Luiz Felipe"),
                ("RICARDO","Ricardo"),("LUCAS","Lucas")]:
        if n in d: return ("Aporte de Capital" if valor>0 else f"Dist. Sócio - {c}")
    if "APLICA" in d: return "Aplicação Financeira" if valor<0 else "Resgate Aplicação"
    return "Outras Despesas" if valor<0 else "Outras Entradas"

def do_xlsx():
    f=glob.glob(os.path.join(EXT,"*.xlsx"))
    if not f: return []
    ws=load_workbook(f[0],data_only=True)["Extrato Bancário"]
    out=[]
    for r in range(7,ws.max_row+1):
        d=ws.cell(r,1).value
        if not isinstance(d,datetime.datetime): continue
        e=ws.cell(r,4).value; s=ws.cell(r,5).value
        e=float(e) if isinstance(e,(int,float)) else 0.0
        s=float(s) if isinstance(s,(int,float)) else 0.0
        out.append({"data":d.strftime("%Y-%m-%d"),"desc":str(ws.cell(r,2).value),
                    "cat":str(ws.cell(r,3).value),"valor":round(e-s,2),"fonte":"xlsx"})
    return out

def do_pdf(p):
    txt=subprocess.run(["pdftotext","-layout",p,"-"],capture_output=True,text=True).stdout
    ano=re.search(r"Período:\s*\d{2}/\d{2}/(\d{4})",txt)
    ano=int(ano.group(1)) if ano else datetime.date.today().year
    out=[]; dia=None
    for ln in txt.splitlines():
        s=ln.strip()
        m=re.match(r"^(\d{1,2}) de (\w+) de (\d{4})",s)
        if m:
            dia=datetime.date(int(m.group(3)),MES[m.group(2).lower()],int(m.group(1))); continue
        mv=re.search(r"(-?R\$\s*[\d.]+,\d{2})\s+R\$\s*[\d.]+,\d{2}\s*$",s)
        if not (mv and dia): continue
        bruto=mv.group(1)
        val=float(bruto.replace("R$","").replace(".","").replace(",",".").replace(" ",""))
        desc=s[:mv.start()].strip().strip('"')
        out.append({"data":dia.strftime("%Y-%m-%d"),"desc":desc,
                    "cat":categoriza(desc,val),"valor":round(val,2),"fonte":os.path.basename(p)})
    return out

linhas=do_xlsx()
vistos={(l["data"],l["desc"][:40],l["valor"]) for l in linhas}
for p in sorted(glob.glob(os.path.join(EXT,"*.pdf"))):
    for l in do_pdf(p):
        k=(l["data"],l["desc"][:40],l["valor"])
        if k not in vistos: linhas.append(l); vistos.add(k)
linhas.sort(key=lambda x:(x["data"],x["desc"]))
json.dump(linhas,open("extrato.json","w"),ensure_ascii=False,indent=1)
saldo=sum(l["valor"] for l in linhas)
print(f"{len(linhas)} lançamentos | {linhas[0]['data']} a {linhas[-1]['data']} | saldo acumulado R$ {saldo:,.2f}")
