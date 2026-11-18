# -*- coding: utf-8 -*-
import json, os
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

D = json.load(open("dados.json")); ROWS = D["rows"]; META = D["meta"]
COMPS = [m["competencia"] for m in META]
NOME = {m["competencia"]: m["mes_nome"] for m in META}
OUT = "/home/user/GuiFIzz/financeiro/LF_Agropastoril_Analise_Relatorios_2026.xlsx"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

F="Arial"
H  = Font(name=F, bold=True, color="FFFFFF", size=10)
HF = PatternFill("solid", fgColor="1F3864")
TIT= Font(name=F, bold=True, size=14, color="1F3864")
SUB= Font(name=F, bold=True, size=11, color="1F3864")
N  = Font(name=F, size=10)
NB = Font(name=F, size=10, bold=True)
AZ = Font(name=F, size=10, color="0000FF")      # input digitado da fonte
VD = Font(name=F, size=10, color="008000")      # link entre abas
VM = Font(name=F, size=10, bold=True, color="C00000")
ALERT = PatternFill("solid", fgColor="FCE4E4")
OKF   = PatternFill("solid", fgColor="E2EFDA")
WARN  = PatternFill("solid", fgColor="FFF2CC")
THIN  = Border(*[Side(style="thin", color="BFBFBF")]*4)
R2 = 'R$ #,##0.00;[Red](R$ #,##0.00);-'
R4 = 'R$ 0.0000'
KW = '#,##0;[Red](#,##0);-'
PC = '0.0%'

wb = Workbook(); wb.remove(wb.active)

def head(ws, titulo, sub=None):
    ws["A1"]=titulo; ws["A1"].font=TIT
    if sub: ws["A2"]=sub; ws["A2"].font=Font(name=F,size=9,italic=True,color="595959")
    return 4

def hrow(ws, r, cols, widths=None):
    for i,c in enumerate(cols,1):
        cell=ws.cell(r,i,c); cell.font=H; cell.fill=HF; cell.border=THIN
        cell.alignment=Alignment(horizontal="center", vertical="center", wrap_text=True)
    if widths:
        for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    ws.freeze_panes=ws.cell(r+1,1)

# ============================ 1. BASE ============================
ws = wb.create_sheet("Base_Lancamentos")
r0 = head(ws,"Base de lançamentos — extraída dos 9 relatórios PDF",
          "Fonte única da planilha. Toda outra aba lê daqui por SUMIFS/COUNTIFS. Não editar à mão.")
cols=["Relatório","UC / Instalação","Competência ref.","Tipo","Injetada kWh","Compensada kWh",
      "Saldo transf. kWh","Saldo atual kWh","Tarifa CEMIG","Tarifa Consórcio","Boleto Bro",
      "Valor Pago","Em aberto","Devido (tabela inadimpl.)"]
hrow(ws,r0,cols,[11,16,16,22,12,13,13,13,12,13,13,13,13,15])
r=r0+1
for x in sorted(ROWS,key=lambda z:(z["relatorio"],z["uc"],z["ref"])):
    tipo = x["tipo"] if not x.get("neg") else "parcela negociada"
    ws.cell(r,1,x["relatorio"]).font=N
    ws.cell(r,2,x["uc"]).font=N
    ws.cell(r,3,x["ref"]).font=N
    ws.cell(r,4,tipo).font=N
    for ci,key in [(5,"injetada"),(6,"compensada"),(7,"transferido"),(8,"saldo_atual")]:
        v=x.get(key)
        if v is not None: c=ws.cell(r,ci,v); c.font=N; c.number_format=KW
    for ci,key,fmt in [(9,"tarifa_cemig",R4),(10,"tarifa_consorcio",R4),(11,"boleto",R2),(12,"pago",R2)]:
        v=x.get(key)
        if v is not None: c=ws.cell(r,ci,v); c.font=N; c.number_format=fmt
    if x.get("boleto") is not None and x["tipo"]!="inadimplencia_anterior":
        c=ws.cell(r,13,f"=IFERROR(K{r}-N({chr(76)}{r}),0)"); c.font=N; c.number_format=R2
    if x.get("valor_devido") is not None:
        c=ws.cell(r,14,x["valor_devido"]); c.font=N; c.number_format=R2
    r+=1
BASE_LAST=r-1
B=f"Base_Lancamentos!"
print("Base:",BASE_LAST-r0,"linhas")

# ============================ 2. RELATORIOS ============================
ws = wb.create_sheet("Relatorios")
r0 = head(ws,"Identificação dos relatórios recebidos",
          "Um relatório por mês emitido pela Bro (vendedora/gestora de energia). Azul = valor lido do PDF. Preto = fórmula.")
cols=["Competência","Mês","Arquivo PDF","UCs no relatório","Injetada kWh","Compensada kWh",
      "Saldo final kWh","Faturado mês (boletos)","Recebido no mês","Administração (PDF)",
      "Fatura concessionária (PDF)","Repasse declarado (PDF)","Repasse recalculado","Confere?","Obs. fatura CEMIG"]
hrow(ws,r0,cols,[12,11,42,10,12,13,13,16,15,15,16,16,16,10,20])
r=r0+1; first=r
for m in META:
    c=m["competencia"]
    ws.cell(r,1,c).font=NB
    ws.cell(r,2,m["mes_nome"]).font=N
    ws.cell(r,3,m["arquivo"]).font=Font(name=F,size=8)
    ws.cell(r,4,f'=COUNTIFS({B}$A$5:$A${BASE_LAST},$A{r},{B}$D$5:$D${BASE_LAST},"corrente")').font=N
    for ci,col in [(5,"E"),(6,"F"),(7,"H")]:
        cc=ws.cell(r,ci,f'=SUMIFS({B}${col}$5:${col}${BASE_LAST},{B}$A$5:$A${BASE_LAST},$A{r})')
        cc.font=N; cc.number_format=KW
    for ci,col in [(8,"K"),(9,"L")]:
        cc=ws.cell(r,ci,f'=SUMIFS({B}${col}$5:${col}${BASE_LAST},{B}$A$5:$A${BASE_LAST},$A{r})')
        cc.font=N; cc.number_format=R2
    for ci,key in [(10,"administracao"),(11,"fatura_concessionaria"),(12,"valor_repasse")]:
        cc=ws.cell(r,ci,m[key]); cc.font=AZ; cc.number_format=R2
    cc=ws.cell(r,13,f"=I{r}-J{r}-K{r}"); cc.font=N; cc.number_format=R2
    cc=ws.cell(r,14,f'=IF(ABS(M{r}-L{r})<0.02,"OK","VERIFICAR")'); cc.font=N
    cc.alignment=Alignment(horizontal="center")
    ws.cell(r,15,m["observacao"]).font=N
    r+=1
last=r-1
ws.cell(r,1,"TOTAL").font=NB
for ci in [5,6,8,9,10,11,12,13]:
    L=get_column_letter(ci); cc=ws.cell(r,ci,f"=SUM({L}{first}:{L}{last})")
    cc.font=NB; cc.number_format=KW if ci in (5,6) else R2
ws.cell(r,7,"—").font=N
for ci in range(1,16): ws.cell(r,ci).fill=OKF
TOTROW=r
r+=3
ws.cell(r,1,"Leitura do mecanismo financeiro").font=SUB; r+=1
for t in [
 "Repasse = Valor Pago − Administração − Fatura da concessionária. A fórmula fecha nos 9 meses (coluna Confere?).",
 "Administração da Bro = 10,0% do valor EFETIVAMENTE PAGO, não do faturado. A Bro só ganha sobre o que arrecada.",
 "Consequência: quem absorve 100% do risco de inadimplência é a LF Agropastoril, não a Bro.",
 "A partir de junho/2026 a observação muda de \"Fatura CEMIG paga pela Bro\" para \"Fatura CEMIG retida\" — mudança não explicada.",
 "O relatório de fevereiro/2026 foi entregue fora da remessa original, depois de cobrado. A série agora está completa.",
]:
    ws.cell(r,1,"• "+t).font=N; r+=1

# ============================ 3. CLIENTES ============================
ucs_pres=defaultdict(set)
for x in ROWS:
    if x["tipo"]=="corrente" and not x.get("neg"): ucs_pres[x["uc"]].add(x["relatorio"])
ordem=sorted(ucs_pres,key=lambda u:(-len(ucs_pres[u]),u))

ws = wb.create_sheet("Clientes_Comparativo")
r0 = head(ws,"Comparativo de clientes entre relatórios — entradas, saídas e faturamento",
          "Valores = boleto emitido no mês (competência corrente). Célula vazia = UC ausente do relatório.")
cols=["UC / Instalação"]+[NOME[c][:3]+"/"+c[2:4] for c in COMPS]+["Meses ativos","1º relatório","Último relatório","Status","Faturado no período","% do faturamento"]
hrow(ws,r0,cols,[16]+[11]*len(COMPS)+[12,13,15,24,17,15])
r=r0+1; first=r
for uc in ordem:
    ws.cell(r,1,uc).font=NB
    for i,c in enumerate(COMPS):
        cc=ws.cell(r,2+i,f'=IF(COUNTIFS({B}$A$5:$A${BASE_LAST},"{c}",{B}$B$5:$B${BASE_LAST},$A{r},{B}$D$5:$D${BASE_LAST},"corrente")=0,"",'
                            f'SUMIFS({B}$K$5:$K${BASE_LAST},{B}$A$5:$A${BASE_LAST},"{c}",{B}$B$5:$B${BASE_LAST},$A{r},{B}$D$5:$D${BASE_LAST},"corrente"))')
        cc.font=N; cc.number_format=R2
        if c not in ucs_pres[uc]: cc.fill=ALERT
    n=len(ucs_pres[uc]); pres=sorted(ucs_pres[uc])
    ws.cell(r,2+len(COMPS),n).font=NB
    ws.cell(r,3+len(COMPS),pres[0]).font=N
    ws.cell(r,4+len(COMPS),pres[-1]).font=N
    if pres[-1]!=COMPS[-1]:
        st="PERDIDO — saiu após "+pres[-1]; cel=ws.cell(r,5+len(COMPS),st); cel.font=VM; cel.fill=ALERT
    elif pres[0]!=COMPS[0]:
        st="NOVO — entrou em "+pres[0]; cel=ws.cell(r,5+len(COMPS),st); cel.font=Font(name=F,size=10,bold=True,color="C55A11")
    else:
        cel=ws.cell(r,5+len(COMPS),"Base original (ativo desde jan/26)"); cel.font=N
    cc=ws.cell(r,6+len(COMPS),f"=SUM(B{r}:{get_column_letter(1+len(COMPS))}{r})"); cc.font=NB; cc.number_format=R2
    cc=ws.cell(r,7+len(COMPS),f"=IFERROR({get_column_letter(6+len(COMPS))}{r}/{get_column_letter(6+len(COMPS))}${first+len(ordem)},0)")
    cc.font=N; cc.number_format=PC
    r+=1
last=r-1
ws.cell(r,1,"TOTAL").font=NB
for i in range(len(COMPS)):
    L=get_column_letter(2+i); cc=ws.cell(r,2+i,f"=SUM({L}{first}:{L}{last})"); cc.font=NB; cc.number_format=R2
L=get_column_letter(6+len(COMPS)); cc=ws.cell(r,6+len(COMPS),f"=SUM({L}{first}:{L}{last})"); cc.font=NB; cc.number_format=R2
for ci in range(1,8+len(COMPS)): ws.cell(r,ci).fill=OKF
r+=2
ws.cell(r,1,"Conclusão comercial").font=SUB; r+=1
for t in ["NENHUM cliente novo entrou na base em 10 relatórios (jan a out/2026). A Taxa Inicial de 50% do 1º faturamento nunca foi cobrada, porque nunca houve captação.",
          "DOIS clientes saíram: UC 3012593143 (após jun/26) e UC 3012693035 (após jul/26) — a base caiu de 15 para 13 UCs (−13%).",
          "A UC 3012593143 nunca compensou energia em nenhum mês (0 kWh sempre, saldo parado em 732 kWh) e nunca gerou boleto: estava ocupando vaga sem gerar receita.",
          "A UC 3012693035 zerou o saldo em jul/26 (778 kWh compensados, 0 injetados) e sumiu no mês seguinte.",
          "Concentração: a maior UC responde por mais da metade do faturamento do período (ver coluna % do faturamento)."]:
    ws.cell(r,1,"• "+t).font=N; r+=1
CLIENTES_TOT=last

# ============================ 4. INADIMPLENCIA ============================
raz=defaultdict(lambda:{"fat":0.0,"pago":0.0,"fat_em":None,"pgtos":[]})
for x in ROWS:
    if x["tipo"]=="inadimplencia_anterior": continue
    k=(x["uc"],x["ref"])
    if x.get("boleto") is not None and raz[k]["fat_em"] is None:
        raz[k]["fat"]=x["boleto"]; raz[k]["fat_em"]=x["relatorio"]
    if x.get("pago") is not None:
        raz[k]["pago"]+=x["pago"]; raz[k]["pgtos"].append((x["relatorio"],x["pago"]))

ws = wb.create_sheet("Inadimplencia")
r0 = head(ws,"Inadimplência — razão por cliente e competência",
          "Cada linha é um boleto. 'Pago em' mostra em que relatório a quitação apareceu. Acréscimo = juros/multa cobrados no atraso.")
cols=["UC","Competência do boleto","Faturado em","Valor faturado","Total pago","Pago em (relatório)",
      "Meses de atraso","Acréscimo cobrado","Em aberto","Situação"]
hrow(ws,r0,cols,[15,18,13,15,15,24,12,15,14,34])
def mi(c):
    a,b=c[:4],c[5:7]; return int(a)*12+int(b)
r=r0+1; first=r
for (uc,ref),v in sorted(raz.items(), key=lambda kv:(kv[0][0], kv[0][1])):
    aberto=round(v["fat"]-v["pago"],2)
    pg=", ".join(p[0] for p in v["pgtos"]) or "—"
    refm = ref.replace("-neg","")
    atraso = max((mi(p[0])-mi(refm) for p in v["pgtos"]), default=(mi(COMPS[-1])-mi(refm) if aberto>0.009 else 0))
    acr = round(v["pago"]-v["fat"],2) if v["pago"]>v["fat"]+0.009 else 0
    ws.cell(r,1,uc).font=N
    ws.cell(r,2,ref).font=N
    ws.cell(r,3,v["fat_em"] or "anterior à base").font=N
    for ci,val in [(4,v["fat"]),(5,v["pago"])]:
        cc=ws.cell(r,ci,val); cc.font=N; cc.number_format=R2
    ws.cell(r,6,pg).font=N
    ws.cell(r,7,atraso).font=N
    cc=ws.cell(r,8,acr); cc.font=N; cc.number_format=R2
    cc=ws.cell(r,9,f"=D{r}-E{r}"); cc.font=N; cc.number_format=R2
    if aberto>0.009:
        if ref=="2026-01":
            s="EM ABERTO na base — provável quitação no relatório de FEV/26 (ausente)"; cel=ws.cell(r,10,s); cel.font=Font(name=F,size=10,color="BF8F00"); cel.fill=WARN
        else:
            s="EM ABERTO — confirmado"; cel=ws.cell(r,10,s); cel.font=VM; cel.fill=ALERT
    elif atraso>0:
        ws.cell(r,10,f"Quitado com {atraso} mês(es) de atraso").font=N
    else:
        cel=ws.cell(r,10,"Quitado no mês"); cel.font=N; cel.fill=OKF
    r+=1
last=r-1
ws.cell(r,1,"TOTAL").font=NB
for ci in [4,5,8,9]:
    L=get_column_letter(ci); cc=ws.cell(r,ci,f"=SUM({L}{first}:{L}{last})"); cc.font=NB; cc.number_format=R2
for ci in range(1,11): ws.cell(r,ci).fill=OKF
INAD_FIRST, INAD_LAST = first, last
json.dump({"inad_first":first,"inad_last":last,"base_last":BASE_LAST,"clientes_tot":CLIENTES_TOT,"tot_rel":TOTROW},
          open("ref.json","w"))
wb.save(OUT); print("parcial salvo:",OUT)
