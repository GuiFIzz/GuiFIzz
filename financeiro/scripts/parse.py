import re, json, subprocess, glob, os

import os
SRC = os.environ.get("RELATORIOS_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "relatorios"))
MESES = {"Janeiro":1,"Fevereiro":2,"Março":3,"Marco":3,"Abril":4,"Maio":5,"Junho":6,
         "Julho":7,"Agosto":8,"Setembro":9,"Outubro":10,"Novembro":11,"Dezembro":12}

def money(tok):
    t = tok.replace("R$","").strip().replace(".","").replace(",",".")
    return float(t)

rows, meta = [], []
for f in sorted(glob.glob(os.path.join(SRC,"*.pdf"))):
    txt = subprocess.run(["pdftotext","-layout",f,"-"],capture_output=True,text=True).stdout
    m = re.search(r"Relat[óo]rio\s+(\w+)/(\d{4})", txt)
    mes_nome, ano = m.group(1), int(m.group(2))
    mes = MESES[mes_nome]; comp = f"{ano}-{mes:02d}"

    def grab(label):
        mm = re.search(label + r"\s*:?\s*R\$\s*([\d.,]+)", txt)
        return money("R$"+mm.group(1)) if mm else None

    meta.append({"competencia":comp,"mes_nome":mes_nome,"ano":ano,"arquivo":os.path.basename(f),
                 "administracao":grab("Administração"),
                 "fatura_concessionaria":grab("Fatura Concessionária"),
                 "valor_repasse":grab("Valor Repasse"),
                 "inadimplencia_total":grab("Inadimplência Total"),
                 "observacao":"retida" if "CEMIG retida" in txt else ("paga pela Bro" if "paga pela Bro" in txt else None)})

    in_inad = False
    for line in txt.splitlines():
        s = line.strip()
        if s.startswith("Inadimplência meses anteriores"): in_inad = True; continue
        if s.startswith("Inadimplência Total"): in_inad = False; continue
        mrow = re.match(r"^(\d{10})\s*(?:\((\w{3}-\d{2})\)|(neg \d/\d))?\s*(.*)$", s)
        if not mrow: continue
        uc, tag, neg, rest = mrow.group(1), mrow.group(2), mrow.group(3), mrow.group(4)
        monies = re.findall(r"R\$\s*[\d.,]+", rest)
        ints = [int(x) for x in re.findall(r"(?<![\d,.])-?\d{1,6}(?![\d,.])", rest.split("R$")[0])]
        if in_inad:
            if monies:
                rows.append({"relatorio":comp,"uc":uc,"ref":tag or comp,"tipo":"inadimplencia_anterior",
                             "valor_devido":money(monies[0])})
            continue
        rec = {"relatorio":comp,"uc":uc,"ref":tag or comp,"neg":neg,
               "tipo":"corrente" if (tag is None) else "atrasado"}
        if len(ints) >= 4:
            rec.update(injetada=ints[0],compensada=ints[1],transferido=ints[2],saldo_atual=ints[3])
        if len(monies) >= 3:
            rec.update(tarifa_cemig=money(monies[0]),tarifa_consorcio=money(monies[1]),
                       boleto=money(monies[2]))
            if len(monies) >= 4: rec["pago"]=money(monies[3])
        elif len(monies) >= 1:
            rec["boleto"]=money(monies[0])
            if len(monies) >= 2: rec["pago"]=money(monies[1])
        rows.append(rec)

out = {"meta":sorted(meta,key=lambda x:x["competencia"]),"rows":rows}
json.dump(out,open("dados.json","w"),ensure_ascii=False,indent=1)
print("relatorios:",len(meta))
for mt in out["meta"]: print(mt["competencia"], mt["administracao"], mt["fatura_concessionaria"], mt["valor_repasse"], mt["observacao"])
print("linhas:",len(rows))
