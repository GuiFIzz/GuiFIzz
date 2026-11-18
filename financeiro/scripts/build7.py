# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, BarChart, Reference, Series

D=json.load(open("dados.json")); ROWS=D["rows"]; META=D["meta"]; R=json.load(open("ref.json"))
NM=len(META); BL=R["base_last"]; B="Base_Lancamentos!"
OUT="/home/user/GuiFIzz/financeiro/LF_Agropastoril_Analise_Relatorios_2026.xlsx"
wb=load_workbook(OUT)
F="Arial"
H=Font(name=F,bold=True,color="FFFFFF",size=10); HF=PatternFill("solid",fgColor="1F3864")
TIT=Font(name=F,bold=True,size=16,color="1F3864"); SUB=Font(name=F,bold=True,size=11,color="1F3864")
N=Font(name=F,size=10); NB=Font(name=F,size=10,bold=True); SM=Font(name=F,size=9,color="404040")
VM=Font(name=F,size=11,bold=True,color="C00000"); KPI=Font(name=F,size=12,bold=True,color="1F3864")
OKF=PatternFill("solid",fgColor="E2EFDA"); WARN=PatternFill("solid",fgColor="FFF2CC"); ALERT=PatternFill("solid",fgColor="FCE4E4")
THIN=Border(*[Side(style="thin",color="BFBFBF")]*4)
KW='#,##0'; PC='0.0%'; R2='R$ #,##0.00'

if "Dashboard_Energia" in wb.sheetnames: del wb["Dashboard_Energia"]
ws=wb.create_sheet("Dashboard_Energia")
ws.sheet_view.showGridLines=False
for col,w in [("A",38),("B",16),("C",18),("D",15),("E",18),("F",18),("G",18),("H",22),("I",13),("J",3)]:
    ws.column_dimensions[col].width=w
ws["A1"]="Dashboard energético da usina — produção e consumo"; ws["A1"].font=TIT
ws["A2"]="Produção = energia injetada pela usina. Consumo = energia compensada nas unidades consumidoras. Atualiza sozinho a cada relatório novo incluído na Base."
ws["A2"].font=Font(name=F,size=9,italic=True,color="595959")

# ---------- série mensal (tabela que alimenta os gráficos) ----------
NKPI=12
TR0=5+NKPI+2
ws.cell(TR0-1,1,"Série mensal — produção, consumo e estoque").font=SUB
cols=["Competência","Produção kWh","Consumo kWh","Resultado kWh","Saldo de créditos kWh","Piso contratual 80% kWh","Variação do saldo kWh","Diferença não explicada kWh","Controle"]
for i,c in enumerate(cols,1):
    x=ws.cell(TR0,i,c); x.font=H; x.fill=HF; x.border=THIN
    x.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
r=TR0+1; first=r
for m in META:
    c_=m["competencia"]
    ws.cell(r,1,f'{m["mes_nome"][:3]}/{c_[2:4]}').font=N
    for ci,col in [(2,"E"),(3,"F"),(5,"H")]:
        x=ws.cell(r,ci,f'=SUMIFS({B}${col}$5:${col}${BL},{B}$A$5:$A${BL},"{c_}")'); x.font=N; x.number_format=KW
    x=ws.cell(r,4,f"=B{r}-C{r}"); x.font=N; x.number_format=KW
    x=ws.cell(r,6,f"=$B${first+NM+1}*0.8"); x.font=N; x.number_format=KW
    if r>first:
        x=ws.cell(r,7,f"=E{r}-E{r-1}"); x.font=N; x.number_format=KW
        x=ws.cell(r,8,f"=G{r}-D{r}"); x.font=N; x.number_format=KW
        x=ws.cell(r,9,f'=IF(ABS(H{r})<1000,"ok","INVESTIGAR")'); x.font=N
        x.alignment=Alignment(horizontal="center")
    else:
        ws.cell(r,7,"—").font=N; ws.cell(r,8,"—").font=N; ws.cell(r,9,"—").font=N
    r+=1
last=r-1
ws.cell(r,1,"TOTAL").font=NB
for ci in (2,3,4):
    L=get_column_letter(ci); x=ws.cell(r,ci,f"=SUM({L}{first}:{L}{last})"); x.font=NB; x.number_format=KW
ws.cell(r,5,"—").font=NB
for ci in range(1,10): ws.cell(r,ci).fill=OKF
TOT=r
ws.cell(r+1,1,"Média mensal").font=NB
x=ws.cell(r+1,2,f"=AVERAGE(B{first}:B{last})"); x.font=NB; x.number_format=KW
x=ws.cell(r+1,3,f"=AVERAGE(C{first}:C{last})"); x.font=NB; x.number_format=KW
MED=r+1

# ---------- KPIs ----------
ws.cell(4,1,"Indicadores da usina").font=SUB
kpis=[("Produção total no período (kWh)",f"=B{TOT}",KW,None),
      ("Produção média mensal (kWh)",f"=B{MED}",KW,None),
      ("Melhor mês de produção",f'=INDEX($A${first}:$A${last},MATCH(MAX($B${first}:$B${last}),$B${first}:$B${last},0))&" — "&TEXT(MAX($B${first}:$B${last}),"#,##0")&" kWh"',None,OKF),
      ("Pior mês de produção",f'=INDEX($A${first}:$A${last},MATCH(MIN($B${first}:$B${last}),$B${first}:$B${last},0))&" — "&TEXT(MIN($B${first}:$B${last}),"#,##0")&" kWh"',None,ALERT),
      ("Consumo total compensado (kWh)",f"=C{TOT}",KW,None),
      ("Taxa de aproveitamento (consumo / produção)",f"=IFERROR(C{TOT}/B{TOT},0)",PC,None),
      ("Saldo de créditos no último relatório",f"=E{last}",KW,WARN),
      ("Meses abaixo do piso contratual de 80%",f"=SUMPRODUCT(--($B${first}:$B${last}<$F${first}:$F${last}))",'0',ALERT),
      ("Créditos que sumiram sem consumo (kWh)",f"=-SUMIF($H${first+1}:$H${last},\"<-1000\")",KW,ALERT),
      ("Valor estimado desses créditos",f"=IFERROR(-SUMIF($H${first+1}:$H${last},\"<-1000\")*Indicadores!$B$8,0)",R2,ALERT),
      ("Potência implícita na produção média (kWp)",f"=IFERROR(B{MED}/(4.7*30.4),0)",KW,None),
      ("Receita por kWh consumido",f"=IFERROR(Indicadores!$B$5/C{TOT},0)",'R$ 0.0000',None)]
rr=5
for lbl,f_,fmt,fill in kpis:
    ws.cell(rr,1,lbl).font=N
    x=ws.cell(rr,2,f_); x.font=KPI
    if fmt: x.number_format=fmt
    if fill: x.fill=fill
    rr+=1

# ---------- consumo por UC ----------
pres=defaultdict(dict)
for x in ROWS:
    if x["tipo"]=="corrente" and not x.get("neg"): pres[x["uc"]][x["relatorio"]]=x
ucs=sorted(pres,key=lambda u:-sum((pres[u][c].get("compensada") or 0) for c in pres[u]))
UR0=TOT+4
ws.cell(UR0-1,1,"Consumo por unidade consumidora (kWh compensados)").font=SUB
hdr=["UC / Instalação"]+[f'{m["mes_nome"][:3]}/{m["competencia"][2:4]}' for m in META]+["Total no período","% do consumo"]
for i,c in enumerate(hdr,1):
    x=ws.cell(UR0,i,c); x.font=H; x.fill=HF; x.border=THIN
    x.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
    if i>1: ws.column_dimensions[get_column_letter(i)].width=10
r=UR0+1; ufirst=r
for uc in ucs:
    ws.cell(r,1,uc).font=NB
    for i,m in enumerate(META):
        c_=m["competencia"]
        x=ws.cell(r,2+i,f'=IF(COUNTIFS({B}$A$5:$A${BL},"{c_}",{B}$B$5:$B${BL},$A{r},{B}$D$5:$D${BL},"corrente")=0,"",'
                           f'SUMIFS({B}$F$5:$F${BL},{B}$A$5:$A${BL},"{c_}",{B}$B$5:$B${BL},$A{r},{B}$D$5:$D${BL},"corrente"))')
        x.font=N; x.number_format=KW
    tc=get_column_letter(2+NM); pc=get_column_letter(3+NM)
    x=ws.cell(r,2+NM,f"=SUM(B{r}:{get_column_letter(1+NM)}{r})"); x.font=NB; x.number_format=KW
    x=ws.cell(r,3+NM,f"=IFERROR({tc}{r}/{tc}${ufirst+len(ucs)},0)"); x.font=N; x.number_format=PC
    r+=1
ulast=r-1
ws.cell(r,1,"TOTAL").font=NB
for i in range(NM):
    L=get_column_letter(2+i); x=ws.cell(r,2+i,f"=SUM({L}{ufirst}:{L}{ulast})"); x.font=NB; x.number_format=KW
L=get_column_letter(2+NM); x=ws.cell(r,2+NM,f"=SUM({L}{ufirst}:{L}{ulast})"); x.font=NB; x.number_format=KW
for ci in range(1,4+NM): ws.cell(r,ci).fill=OKF
ws.column_dimensions[get_column_letter(2+NM)].width=16
ws.column_dimensions[get_column_letter(3+NM)].width=13

# ---------- gráficos ----------
def arruma(ch,titulo,ytit):
    ch.title=titulo; ch.style=2; ch.roundedCorners=False
    ch.y_axis.title=ytit; ch.x_axis.title="Competência"
    ch.x_axis.delete=False; ch.y_axis.delete=False
    if ch.legend: ch.legend.position="b"; ch.legend.overlay=False
    ch.height=8.5; ch.width=19

cats=Reference(ws,min_col=1,min_row=first,max_row=last)

c1=LineChart()
c1.add_data(Reference(ws,min_col=2,max_col=3,min_row=TR0,max_row=last),titles_from_data=True)
c1.add_data(Reference(ws,min_col=6,min_row=TR0,max_row=last),titles_from_data=True)
c1.set_categories(cats)
arruma(c1,"Produção x consumo x piso contratual","kWh")
for s in c1.series: s.smooth=False
ws.add_chart(c1,"L4")

c2=LineChart()
c2.add_data(Reference(ws,min_col=5,min_row=TR0,max_row=last),titles_from_data=True)
c2.set_categories(cats)
arruma(c2,"Estoque de créditos de energia","kWh acumulados")
for s in c2.series: s.smooth=False
ws.add_chart(c2,"L22")

c3=BarChart(); c3.type="col"
c3.add_data(Reference(ws,min_col=4,min_row=TR0,max_row=last),titles_from_data=True)
c3.set_categories(cats)
arruma(c3,"Resultado mensal — produção menos consumo","kWh")
ws.add_chart(c3,"L40")

c4=BarChart(); c4.type="bar"
c4.add_data(Reference(ws,min_col=2+NM,min_row=UR0,max_row=ulast),titles_from_data=True)
c4.set_categories(Reference(ws,min_col=1,min_row=ufirst,max_row=ulast))
arruma(c4,"Consumo acumulado por unidade consumidora","kWh no período")
c4.x_axis.title="UC"; c4.height=11
ws.add_chart(c4,"L58")

ordem=["Leia-me","Dashboard_Energia","Relatorios","Clientes_Comparativo","Inadimplencia",
       "Contas_a_Receber","Energia","Indicadores","Contrato_Bro","Perguntas_Bro","Plano_de_Acao","Base_Lancamentos"]
wb._sheets=[wb[s] for s in ordem]
lm=wb["Leia-me"]
rowi=[x for x in range(10,45) if lm.cell(x,1).value=="Relatorios"][0]
lm.insert_rows(rowi)
lm.cell(rowi,1,"Dashboard_Energia").font=NB
lm.cell(rowi,3,"Histórico completo de produção e consumo da usina, com gráficos e consumo por unidade consumidora.").font=N
wb.save(OUT); print(f"dashboard ok | serie {first}-{last} | ucs {ufirst}-{ulast}")
