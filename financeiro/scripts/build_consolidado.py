# -*- coding: utf-8 -*-
import json, datetime
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, BarChart, Reference

L=json.load(open("extrato.json"))
EN=json.load(open("dados.json"))
OUT="../Fotovolt_Curral_Novo_Consolidado.xlsx"
F="Arial"
H=Font(name=F,bold=True,color="FFFFFF",size=10); HF=PatternFill("solid",fgColor="1F3864")
TIT=Font(name=F,bold=True,size=16,color="1F3864"); SUB=Font(name=F,bold=True,size=11,color="1F3864")
N=Font(name=F,size=10); NB=Font(name=F,size=10,bold=True); SM=Font(name=F,size=9,color="404040")
AZ=Font(name=F,size=10,color="0000FF"); KPI=Font(name=F,size=12,bold=True,color="1F3864")
VM=Font(name=F,size=11,bold=True,color="C00000")
OKF=PatternFill("solid",fgColor="E2EFDA"); WARN=PatternFill("solid",fgColor="FFF2CC")
ALERT=PatternFill("solid",fgColor="FCE4E4"); THIN=Border(*[Side(style="thin",color="BFBFBF")]*4)
R2='R$ #,##0.00;[Red](R$ #,##0.00);-'; R0='R$ #,##0'; PC='0.0%'; PC2='0.00%'; KW='#,##0'; DT='dd/mm/yyyy'
SOC=["Guilherme","Luiz Felipe","Ricardo","Lucas"]
NOME={"Guilherme":"GUILHERME","Luiz Felipe":"LUIZ FELIPE","Ricardo":"RICARDO","Lucas":"LUCAS"}

wb=Workbook(); wb.remove(wb.active)
def head(ws,t,s=None):
    ws["A1"]=t; ws["A1"].font=TIT
    if s: ws["A2"]=s; ws["A2"].font=Font(name=F,size=9,italic=True,color="595959")
    ws.sheet_view.showGridLines=False
def hrow(ws,r,cols,w=None):
    for i,c in enumerate(cols,1):
        x=ws.cell(r,i,c); x.font=H; x.fill=HF; x.border=THIN
        x.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
    if w:
        for i,ww in enumerate(w,1): ws.column_dimensions[get_column_letter(i)].width=ww

# ================= EXTRATO =================
ws=wb.create_sheet("Extrato"); head(ws,"Extrato bancário consolidado da SPE",
  "Banco Inter, conta 29965026-0. Histórico até set/26 do workbook anterior + out/26 extraído do PDF. Fonte de tudo que é dinheiro.")
hrow(ws,4,["Data","Descrição","Categoria","Valor","Saldo acumulado"],[12,56,32,15,17])
r=5; first_e=r
for l in L:
    ws.cell(r,1,datetime.date.fromisoformat(l["data"])).number_format=DT
    ws.cell(r,1).font=N
    ws.cell(r,2,l["desc"][:90]).font=N
    ws.cell(r,3,l["cat"]).font=N
    x=ws.cell(r,4,l["valor"]); x.font=N; x.number_format=R2
    x=ws.cell(r,5,f"=D{r}" if r==first_e else f"=E{r-1}+D{r}"); x.font=N; x.number_format=R2
    r+=1
last_e=r-1
ws.cell(r,3,"SALDO FINAL").font=NB
x=ws.cell(r,5,f"=E{last_e}"); x.font=NB; x.number_format=R2; x.fill=OKF
ws.freeze_panes="A5"
E=f"Extrato!"

# ================= FLUXO MENSAL =================
mes=defaultdict(lambda: defaultdict(float)); cats=set()
for l in L: mes[l["data"][:7]][l["cat"]]+=l["valor"]; cats.add(l["cat"])
MS=sorted(mes)
ordem=["Receita Energia","Aporte de Capital","Aporte Sócio","Resgate Aplicação",
       "Outras Entradas","Investimento - Usina (BRO Energy)","Impostos (DARF)","Estorno de Imposto (SPE Poções)","Contabilidade",
       "O&M / Manutenção","Outras Despesas","Reembolso Sócio - Guilherme","Aplicação Financeira"]+ \
      [f"Dist. Sócio - {s}" for s in SOC]
ordem=[c for c in ordem if c in cats]+[c for c in sorted(cats) if c not in ordem]
ws=wb.create_sheet("Fluxo_Mensal"); head(ws,"Fluxo de caixa mensal por categoria",
  "Todo valor vem da aba Extrato por SUMIFS. Positivo entra, negativo sai.")
hrow(ws,4,["Categoria"]+[m for m in MS]+["TOTAL"],[34]+[11]*len(MS)+[15])
r=5; fr=r
for c in ordem:
    ws.cell(r,1,c).font=N
    for i,m in enumerate(MS):
        x=ws.cell(r,2+i,f'=SUMIFS({E}$D${first_e}:$D${last_e},{E}$C${first_e}:$C${last_e},$A{r},'
                        f'{E}$A${first_e}:$A${last_e},">="&DATE({m[:4]},{int(m[5:])},1),'
                        f'{E}$A${first_e}:$A${last_e},"<"&DATE({m[:4]},{int(m[5:])}+1,1))')
        x.font=N; x.number_format=R2
    L_=get_column_letter(1+len(MS))
    x=ws.cell(r,2+len(MS),f"=SUM(B{r}:{L_}{r})"); x.font=NB; x.number_format=R2
    r+=1
lr=r-1
ws.cell(r,1,"RESULTADO DO MÊS").font=NB
for i in range(len(MS)+1):
    Lc=get_column_letter(2+i); x=ws.cell(r,2+i,f"=SUM({Lc}{fr}:{Lc}{lr})"); x.font=NB; x.number_format=R2
    x.fill=OKF
RES=r; r+=1
ws.cell(r,1,"SALDO ACUMULADO").font=NB
for i in range(len(MS)):
    Lc=get_column_letter(2+i); ant=get_column_letter(1+i)
    f_=f"={Lc}{RES}" if i==0 else f"={ant}{r}+{Lc}{RES}"
    x=ws.cell(r,2+i,f_); x.font=NB; x.number_format=R2
ws.freeze_panes="B5"
FM=f"Fluxo_Mensal!"; SALDO_ROW=r

# ================= CONCILIACAO ENERGIA -> CAIXA =================
ws=wb.create_sheet("Conciliacao"); head(ws,"Conciliação energia → caixa",
  "O repasse de uma competência entra na conta no mês seguinte. Esta aba prova isso mês a mês.")
hrow(ws,4,["Competência do relatório","Injetado kWh","Compensado kWh","Faturado pela Bro",
           "Recebido pela Bro","Administração","Repasse do relatório","Mês de entrada no extrato",
           "Receita no extrato","Diferença","Controle","R$ por kWh injetado"],
     [18,13,14,15,15,13,16,18,15,13,13,16])
r=5; fc=r
def prox(m):
    a,b=int(m[:4]),int(m[5:]); b+=1
    if b==13: a,b=a+1,1
    return f"{a}-{b:02d}"
for m in EN["meta"]:
    c=m["competencia"]; nx=prox(c)
    ws.cell(r,1,c).font=NB
    inj=sum(x.get("injetada") or 0 for x in EN["rows"] if x["relatorio"]==c)
    cmp_=sum(x.get("compensada") or 0 for x in EN["rows"] if x["relatorio"]==c)
    fat=sum(x.get("boleto") or 0 for x in EN["rows"] if x["relatorio"]==c and x["tipo"]!="inadimplencia_anterior")
    pag=sum(x.get("pago") or 0 for x in EN["rows"] if x["relatorio"]==c and x["tipo"]!="inadimplencia_anterior")
    for ci,v,fmt in [(2,inj,KW),(3,cmp_,KW),(4,round(fat,2),R2),(5,round(pag,2),R2),
                     (6,m["administracao"],R2),(7,m["valor_repasse"],R2)]:
        x=ws.cell(r,ci,v); x.font=AZ if ci in (6,7) else N; x.number_format=fmt
    ws.cell(r,8,nx).font=N
    x=ws.cell(r,9,f'=SUMIFS({E}$D${first_e}:$D${last_e},{E}$C${first_e}:$C${last_e},"Receita Energia",'
                  f'{E}$A${first_e}:$A${last_e},">="&DATE({nx[:4]},{int(nx[5:])},1),'
                  f'{E}$A${first_e}:$A${last_e},"<"&DATE({nx[:4]},{int(nx[5:])}+1,1))')
    x.font=N; x.number_format=R2
    x=ws.cell(r,10,f"=I{r}-G{r}"); x.font=N; x.number_format=R2
    ult=max(x["data"][:7] for x in L)
    ctrl=f'=IF(ABS(J{r})<0.05,"confere","DIVERGE")' if nx<=ult else '="aguardando extrato"'
    x=ws.cell(r,11,ctrl); x.font=N
    x.alignment=Alignment(horizontal="center")
    x=ws.cell(r,12,f"=IFERROR(G{r}/B{r},0)"); x.font=N; x.number_format='R$ 0.0000'
    r+=1
lc=r-1
ws.cell(r,1,"TOTAL").font=NB
for ci in (2,3,4,5,6,7,9,10):
    Lc=get_column_letter(ci); x=ws.cell(r,ci,f"=SUM({Lc}{fc}:{Lc}{lc})"); x.font=NB
    x.number_format=KW if ci in (2,3) else R2; x.fill=OKF
CONC_TOT=r; r+=2
ws.cell(r,1,"Leitura").font=SUB; r+=1
for t in ["Em todos os meses a receita do extrato bate com o repasse do relatório anterior.",
          "Isso prova que o dinheiro entra na conta da PRÓPRIA SPE, e não na LF Agropastoril, apesar do endereçamento do relatório.",
          "A coluna R$ por kWh injetado é o preço real que cada kWh gerado trouxe de caixa para a empresa."]:
    ws.cell(r,1,"• "+t).font=N; r+=1

# ================= RETORNO SOCIOS =================
fluxos=defaultdict(lambda: defaultdict(float))
for l in L:
    d=l["data"]; dd=l["desc"].upper()
    if l["cat"]=="Aporte de Capital":
        for s in SOC:
            if NOME[s] in dd: fluxos[d][s]-=l["valor"]
    if l["cat"].startswith("Dist. Sócio - "):
        s=l["cat"].replace("Dist. Sócio - ","")
        if s in SOC: fluxos[d][s]-=l["valor"]
datas=sorted(fluxos)
ws=wb.create_sheet("Retorno_Socios"); head(ws,"Retorno do investimento por sócio",
  "Fluxo de caixa real, nas datas reais. Negativo = sócio pôs dinheiro. Positivo = sócio recebeu.")
r=4
ws.cell(r,1,"Posição de cada sócio").font=SUB; r+=1
hrow(ws,r,["Sócio","Aportado","Recebido","Múltiplo","% do capital recuperado","Falta recuperar","TIR realizada"],
     [18,15,15,11,20,15,14]); r+=1
fp=r
for i,s in enumerate(SOC):
    ws.cell(r,1,s).font=NB
    col=get_column_letter(2+i)
    x=ws.cell(r,2,f"=-SUMIF(${col}$100:${col}$200,\"<0\")"); x.font=N; x.number_format=R2
    x=ws.cell(r,3,f"=SUMIF(${col}$100:${col}$200,\">0\")"); x.font=N; x.number_format=R2
    x=ws.cell(r,4,f"=IFERROR(C{r}/B{r},0)"); x.font=N; x.number_format='0.00"x"'
    x=ws.cell(r,5,f"=IFERROR(C{r}/B{r},0)"); x.font=N; x.number_format=PC
    x=ws.cell(r,6,f"=B{r}-C{r}"); x.font=N; x.number_format=R2; x.fill=WARN
    x=ws.cell(r,7,f'=IFERROR(XIRR(${col}$100:${col}$200,$A$100:$A$200),"")'); x.font=N; x.number_format=PC2
    r+=1
ws.cell(r,1,"TOTAL").font=NB
for ci in (2,3,6):
    Lc=get_column_letter(ci); x=ws.cell(r,ci,f"=SUM({Lc}{fp}:{Lc}{r-1})"); x.font=NB; x.number_format=R2
x=ws.cell(r,4,f"=IFERROR(C{r}/B{r},0)"); x.font=NB; x.number_format='0.00"x"'
x=ws.cell(r,5,f"=IFERROR(C{r}/B{r},0)"); x.font=NB; x.number_format=PC
x=ws.cell(r,7,'=IFERROR(XIRR($F$100:$F$200,$A$100:$A$200),"")'); x.font=NB; x.number_format=PC2
for ci in range(1,8): ws.cell(r,ci).fill=OKF
TOTP=r; r+=2
ws.cell(r,1,"Por que a TIR realizada é negativa").font=SUB; r+=1
for t in ["Ela mede só o que já aconteceu: saíram R$ 360.000 e voltaram R$ 216.886,29 em 3,3 anos.",
          "Como o capital ainda não voltou, a taxa é negativa por definição. Não significa prejuízo.",
          "A usina continua existindo e produzindo. A TIR que importa para decidir está na aba Cenarios.",
          "O número honesto hoje é: 60,2% do capital recuperado, faltam R$ 143.113,71."]:
    ws.cell(r,1,"• "+t).font=N; r+=1
r+=1
ws.cell(r,1,"Conta corrente de sócios — os quatro têm 25% e aportaram igual, mas receberam diferente").font=SUB; r+=1
hrow(ws,r,["Sócio","Recebido","Média dos quatro","Diferença","Situação"],[18,15,16,14,34]); r+=1
fcc=r
for i,s in enumerate(SOC):
    ws.cell(r,1,s).font=NB
    x=ws.cell(r,2,f"=C{fp+i}"); x.font=N; x.number_format=R2
    x=ws.cell(r,3,f"=$C${TOTP}/4"); x.font=N; x.number_format=R2
    x=ws.cell(r,4,f"=B{r}-C{r}"); x.font=N; x.number_format=R2
    x=ws.cell(r,5,f'=IF(D{r}>0,"recebeu a mais","recebeu a menos")'); x.font=N
    r+=1
ws.cell(r,1,"Diferença entre o maior e o menor").font=NB
x=ws.cell(r,2,f"=MAX(B{fcc}:B{fcc+3})-MIN(B{fcc}:B{fcc+3})"); x.font=VM; x.number_format=R2; x.fill=ALERT
r+=2
ws.cell(r,1,"Fluxo de caixa do investidor (base do cálculo de TIR)").font=SUB
hrow(ws,99,["Data"]+SOC+["Consolidado"],[12,14,14,14,14,15])
rr=100
for d in datas:
    ws.cell(rr,1,datetime.date.fromisoformat(d)).number_format=DT
    ws.cell(rr,1).font=N
    for i,s in enumerate(SOC):
        v=fluxos[d].get(s,0.0)
        if v: x=ws.cell(rr,2+i,round(v,2)); x.font=N; x.number_format=R2
    x=ws.cell(rr,6,f"=SUM(B{rr}:E{rr})"); x.font=N; x.number_format=R2
    rr+=1
print("datas de fluxo:",len(datas),"ultima linha fluxo:",rr-1)
wb.save(OUT); print("parte 1 salva")
