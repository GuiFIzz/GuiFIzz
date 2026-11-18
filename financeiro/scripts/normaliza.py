import json
ABREV={"jan":1,"fev":2,"mar":3,"abr":4,"mai":5,"jun":6,"jul":7,"ago":8,"set":9,"out":10,"nov":11,"dez":12}
def norm(ref, fallback):
    if ref is None: return fallback
    if "-" in ref and len(ref)==6:            # ex: mar-26
        a,b=ref.split("-")
        if a.lower() in ABREV: return f"20{b}-{ABREV[a.lower()]:02d}"
    return ref
d=json.load(open("dados.json"))
for r in d["rows"]:
    r["ref"]=norm(r["ref"], r["relatorio"])
# regra: "neg x/y" = parcela de divida negociada; a linha com kWh fixa a competencia
ult={}
for r in sorted(d["rows"],key=lambda x:x["relatorio"]):
    if r.get("neg"):
        if r.get("injetada") is not None: ult[r["uc"]]=r["relatorio"]
        r["ref"]=ult.get(r["uc"],r["relatorio"])+"-neg"
json.dump(d,open("dados.json","w"),ensure_ascii=False,indent=1)
print("refs normalizadas:", sorted({r["ref"] for r in d["rows"]}))
