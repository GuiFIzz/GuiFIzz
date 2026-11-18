# -*- coding: utf-8 -*-
import json, datetime
from collections import defaultdict
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, BarChart, Reference

L=json.load(open("extrato.json")); EN=json.load(open("dados.json"))
OUT="../Fotovolt_Curral_Novo_Consolidado.xlsx"; wb=load_workbook(OUT)
F="Arial"
H=Font(name=F,bold=True,color="FFFFFF",size=10); HF=PatternFill("solid",fgColor="1F3864")
TIT=Font(name=F,bold=True,size=16,color="1F3864"); SUB=Font(name=F,bold=True,size=11,color="1F3864")
N=Font(name=F,size=10); NB=Font(name=F,size=10,bold=True); SM=Font(name=F,size=9,color="404040")
AZ=Font(name=F,size=10,color="0000FF"); KPI=Font(name=F,size=12,bold=True,color="1F3864")
VM=Font(name=F,size=11,bold=True,color="C00000")
OKF=PatternFill("solid",fgColor="E2EFDA"); WARN=PatternFill("solid",fgColor="FFF2CC")
ALERT=PatternFill("solid",fgColor="FCE4E4"); THIN=Border(*[Side(style="thin",color="BFBFBF")]*4)
R2='R$ #,##0.00;[Red](R$ #,##0.00);-'; PC='0.0%'; PC2='0.00%'; KW='#,##0'; DT='dd/mm/yyyy'
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

ex=wb["Extrato"]; last_e=ex.max_row-1
E="Extrato!"; FE=f"{E}$D$5:$D${last_e}"; FC=f"{E}$C$5:$C${last_e}"; FD=f"{E}$A$5:$A${last_e}"
MS=sorted({l["data"][:7] for l in L})
rs=wb["Retorno_Socios"]
FLUXO_INI, FLUXO_FIM = 100, 142
TOTP=[i for i in range(4,30) if rs.cell(i,1).value=="TOTAL"][0]
print("Retorno_Socios TOTAL na linha",TOTP)

# ================= ENERGIA RESUMO =================
wb.remove(wb["Energia_Resumo"]) if "Energia_Resumo" in wb.sheetnames else None
ws=wb.create_sheet("Energia_Resumo"); head(ws,"Energia e dinheiro na mesma linha",
  "Liga o kWh ao caixa. O detalhe por cliente fica na planilha LF_Agropastoril_Analise_Relatorios_2026.xlsx.")
hrow(ws,4,["Competência","Produção kWh","Consumo kWh","Resultado kWh","Saldo créditos kWh",
           "Repasse R$","R$/kWh produzido","R$/kWh consumido"],[14,14,14,14,17,15,17,17])
r=5; fe=r
for m in EN["meta"]:
    c=m["competencia"]
    inj=sum(x.get("injetada") or 0 for x in EN["rows"] if x["relatorio"]==c)
    cmp_=sum(x.get("compensada") or 0 for x in EN["rows"] if x["relatorio"]==c)
    sal=sum(x.get("saldo_atual") or 0 for x in EN["rows"] if x["relatorio"]==c)
    ws.cell(r,1,c).font=NB
    for ci,v in [(2,inj),(3,cmp_),(5,sal)]:
        x=ws.cell(r,ci,v); x.font=N; x.number_format=KW
    x=ws.cell(r,4,f"=B{r}-C{r}"); x.font=N; x.number_format=KW
    x=ws.cell(r,6,m["valor_repasse"]); x.font=AZ; x.number_format=R2
    x=ws.cell(r,7,f"=IFERROR(F{r}/B{r},0)"); x.font=N; x.number_format='R$ 0.0000'
    x=ws.cell(r,8,f"=IFERROR(F{r}/C{r},0)"); x.font=N; x.number_format='R$ 0.0000'
    r+=1
le=r-1
ws.cell(r,1,"TOTAL").font=NB
for ci in (2,3,4,6):
    Lc=get_column_letter(ci); x=ws.cell(r,ci,f"=SUM({Lc}{fe}:{Lc}{le})"); x.font=NB
    x.number_format=KW if ci!=6 else R2; x.fill=OKF
x=ws.cell(r,7,f"=IFERROR(F{r}/B{r},0)"); x.font=NB; x.number_format='R$ 0.0000'; x.fill=OKF
x=ws.cell(r,8,f"=IFERROR(F{r}/C{r},0)"); x.font=NB; x.number_format='R$ 0.0000'; x.fill=OKF
ETOT=r; r+=2
ws.cell(r,1,"Leitura").font=SUB; r+=1
for t in ["Cada kWh produzido pela usina virou menos de R$ 0,75 de caixa líquido para a SPE.",
          "O consumo superou a produção em 2026 porque o negócio viveu do estoque de créditos acumulado.",
          "Em out/26 sumiram 17.348 kWh do saldo sem contrapartida de consumo — cobrança aberta com a Bro."]:
    ws.cell(r,1,"• "+t).font=N; r+=1

# ================= CENARIOS =================
wb.remove(wb["Cenarios"]) if "Cenarios" in wb.sheetnames else None
ws=wb.create_sheet("Cenarios"); head(ws,"Cenários — quando o capital volta e a que taxa",
  "Edite as células azuis. A TIR projetada considera o fluxo real já ocorrido mais a projeção à frente.")
for c,w in [("A",44),("B",16),("C",16),("D",16),("E",52)]: ws.column_dimensions[c].width=w
r=4
hrow(ws,r,["Premissa","Pessimista","Base","Otimista","Observação"]); r+=1
DM=r
ws.cell(r,1,"Distribuição mensal futura").font=N
for i,v in enumerate([4400,6288,8174]):
    x=ws.cell(r,2+i,v); x.font=AZ; x.number_format=R2
ws.cell(r,5,"Base = média dos últimos 12 meses. Pessimista −30%, otimista +30%.").font=SM; r+=1
ANOS=r
ws.cell(r,1,"Anos de operação à frente").font=N
for i,v in enumerate([22,22,22]):
    x=ws.cell(r,2+i,v); x.font=AZ; x.number_format='0'
ws.cell(r,5,"Painéis com 25 anos de vida, usina em operação desde nov/2023.").font=SM; r+=1
RESID=r
ws.cell(r,1,"Valor residual ao fim").font=N
for i,v in enumerate([0,0,54000]):
    x=ws.cell(r,2+i,v); x.font=AZ; x.number_format=R2
ws.cell(r,5,"Otimista assume 15% do CAPEX de valor residual.").font=SM; r+=2

ws.cell(r,1,"Resultado").font=SUB; r+=1
hrow(ws,r,["Indicador","Pessimista","Base","Otimista","Observação"]); r+=1
TIRROW=r
ws.cell(r,1,"TIR projetada (a.a.)").font=NB
for i,col in enumerate(["H","I","J"]):
    x=ws.cell(r,2+i,f'=IFERROR(XIRR(${col}$100:${col}$500,$G$100:$G$500),"")')
    x.font=VM; x.number_format=PC2; x.fill=OKF
ws.cell(r,5,"Inclui os R$ 360.000 já aportados e tudo que já foi distribuído.").font=SM; r+=1
PBROW=r
ws.cell(r,1,"Meses até recuperar o capital").font=NB
for i in range(3):
    Lc=get_column_letter(2+i)
    x=ws.cell(r,2+i,f"=IFERROR((Retorno_Socios!$B${TOTP}-Retorno_Socios!$C${TOTP})/{Lc}{DM},0)")
    x.font=N; x.number_format='0.0'
ws.cell(r,5,"A partir de hoje, ao ritmo de distribuição de cada cenário.").font=SM; r+=1
ws.cell(r,1,"Anos até recuperar o capital").font=N
for i in range(3):
    Lc=get_column_letter(2+i); x=ws.cell(r,2+i,f"={Lc}{PBROW}/12"); x.font=N; x.number_format='0.0'
r+=1
ws.cell(r,1,"Distribuição por sócio nos próximos 12 meses").font=N
for i in range(3):
    Lc=get_column_letter(2+i); x=ws.cell(r,2+i,f"={Lc}{DM}*12/4"); x.font=N; x.number_format=R2
r+=1
CDI=r
ws.cell(r,1,"CDI de referência (a.a.)").font=N
x=ws.cell(r,2,0.105); x.font=AZ; x.number_format=PC2
ws.cell(r,5,"ESTIMATIVA — ajuste para o CDI corrente.").font=SM; r+=1
ws.cell(r,1,"Prêmio sobre o CDI").font=NB
for i in range(3):
    Lc=get_column_letter(2+i); x=ws.cell(r,2+i,f'=IFERROR({Lc}{TIRROW}-$B${CDI},"")'); x.font=N; x.number_format=PC2
r+=2
ws.cell(r,1,"Como ler estes números").font=SUB; r+=1
for t in ["A TIR realizada de −24% da aba Retorno_Socios mede só o passado: o capital ainda não voltou.",
          "Estes cenários somam o futuro ao passado e dão a taxa do investimento inteiro.",
          "No cenário base o capital volta em cerca de 2 anos e o projeto rende acima de 20% ao ano.",
          "Mesmo no cenário pessimista o retorno supera com folga o CDI — o ativo é bom, a gestão do caixa é que está apertada."]:
    ws.cell(r,1,"• "+t).font=N; r+=1

# fluxo para XIRR (G=data, H/I/J = cenarios)
ws.cell(99,7,"Data").font=H; ws.cell(99,7).fill=HF
for i,nm in enumerate(["Pessimista","Base","Otimista"]):
    c=ws.cell(99,8+i,nm); c.font=H; c.fill=HF
rr=100
for i in range(FLUXO_INI,FLUXO_FIM+1):
    d=rs.cell(i,1).value
    if d is None: continue
    ws.cell(rr,7,d).number_format=DT; ws.cell(rr,7).font=SM
    for k in range(3):
        x=ws.cell(rr,8+k,f"=Retorno_Socios!$F${i}"); x.font=SM; x.number_format=R2
    rr+=1
base=datetime.date(2026,10,31)
MAXM=22*12
for j in range(1,MAXM+1):
    d=base+datetime.timedelta(days=int(30.44*j))
    ws.cell(rr,7,d).number_format=DT; ws.cell(rr,7).font=SM
    for k,Lc in enumerate(["B","C","D"]):
        x=ws.cell(rr,8+k,f'=IF({j}<= ${Lc}${ANOS}*12,${Lc}${DM},0)+IF({j}=${Lc}${ANOS}*12,${Lc}${RESID},0)')
        x.font=SM; x.number_format=R2
    rr+=1
print("fluxo cenarios ate linha",rr-1)
wb.save(OUT); print("parte 3 ok")
