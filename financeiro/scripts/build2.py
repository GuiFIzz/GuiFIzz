# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
D=json.load(open("dados.json")); ROWS=D["rows"]; META=D["meta"]; R=json.load(open("ref.json"))
COMPS=[m["competencia"] for m in META]; NM=len(META)
OUT="/home/user/GuiFIzz/financeiro/LF_Agropastoril_Analise_Relatorios_2026.xlsx"
wb=load_workbook(OUT)
F="Arial"
H=Font(name=F,bold=True,color="FFFFFF",size=10); HF=PatternFill("solid",fgColor="1F3864")
TIT=Font(name=F,bold=True,size=14,color="1F3864"); SUB=Font(name=F,bold=True,size=11,color="1F3864")
N=Font(name=F,size=10); NB=Font(name=F,size=10,bold=True); AZ=Font(name=F,size=10,color="0000FF")
VM=Font(name=F,size=10,bold=True,color="C00000"); SM=Font(name=F,size=9,color="404040")
ALERT=PatternFill("solid",fgColor="FCE4E4"); OKF=PatternFill("solid",fgColor="E2EFDA")
WARN=PatternFill("solid",fgColor="FFF2CC"); THIN=Border(*[Side(style="thin",color="BFBFBF")]*4)
R2='R$ #,##0.00;[Red](R$ #,##0.00);-'; R4='R$ 0.0000'; KW='#,##0;[Red](#,##0);-'; PC='0.0%'
BL=R["base_last"]; B="Base_Lancamentos!"
def head(ws,t,s=None):
    ws["A1"]=t; ws["A1"].font=TIT
    if s: ws["A2"]=s; ws["A2"].font=Font(name=F,size=9,italic=True,color="595959")
    return 4
def hrow(ws,r,cols,widths=None):
    for i,c in enumerate(cols,1):
        c_=ws.cell(r,i,c); c_.font=H; c_.fill=HF; c_.border=THIN
        c_.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
    if widths:
        for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w

# razao (uc, ref)
raz=defaultdict(lambda:{"fat":0.0,"pago":0.0,"fat_em":None})
for x in ROWS:
    if x["tipo"]=="inadimplencia_anterior": continue
    k=(x["uc"],x["ref"])
    if x.get("boleto") is not None and raz[k]["fat_em"] is None:
        raz[k]["fat"]=x["boleto"]; raz[k]["fat_em"]=x["relatorio"]
    if x.get("pago") is not None: raz[k]["pago"]+=x["pago"]
def mi(c): return int(c[:4])*12+int(c[5:7])
ult=mi(COMPS[-1])
abertos=sorted([(uc,ref,round(v["fat"]-v["pago"],2),v["fat_em"])
                for (uc,ref),v in raz.items() if round(v["fat"]-v["pago"],2)>0.009],
               key=lambda x:-x[2])
# divida antiga que so aparece na tabela de inadimplencia (nunca foi faturada na janela)
extra=[("3002347701","2025-08",30.66,"Listada em TODOS os relatórios sem baixa")]

ws=wb.create_sheet("Contas_a_Receber")
r0=head(ws,"Dinheiro devido à empresa — posição após o fechamento de outubro/2026",
        "Consolidado da aba Inadimplência. Com o relatório de fevereiro em mãos, a série está completa e não há mais pendência de conciliação.")
r=r0
ws.cell(r,1,"Boletos em aberto").font=SUB; r+=1
hrow(ws,r,["UC","Competência","Valor em aberto","Meses de atraso","Origem"],[15,15,17,15,52]); r+=1
first=r
for uc,ref,val,fat_em in abertos:
    ws.cell(r,1,uc).font=N; ws.cell(r,2,ref).font=N
    c=ws.cell(r,3,val); c.font=AZ; c.number_format=R2
    ws.cell(r,4,ult-mi(ref.replace("-neg",""))).font=N
    ws.cell(r,5,"Boleto sem pagamento até o relatório de out/26").font=SM
    r+=1
for uc,ref,val,obs in extra:
    ws.cell(r,1,uc).font=N; ws.cell(r,2,ref).font=N
    c=ws.cell(r,3,val); c.font=AZ; c.number_format=R2; c.fill=ALERT
    ws.cell(r,4,ult-mi(ref)).font=N; ws.cell(r,5,obs).font=SM
    r+=1
ws.cell(r,2,"TOTAL A RECEBER").font=NB
c=ws.cell(r,3,f"=SUM(C{first}:C{r-1})"); c.font=Font(name=F,size=12,bold=True,color="C00000")
c.number_format=R2; c.fill=ALERT
TOTREC=r; r+=2
ws.cell(r,1,"O que o relatório de fevereiro resolveu").font=SUB; r+=1
for t in ["As três dívidas de janeiro/2026 (R$ 5.450,90 + R$ 483,14 + R$ 122,02 = R$ 6.056,06) foram integralmente quitadas em fevereiro.",
          "Elas apareciam como 'em aberto' enquanto o relatório de fevereiro não existia na série. Estão liquidadas.",
          "A dívida real da empresa hoje é somente a listada acima."]:
    ws.cell(r,1,"• "+t).font=N; r+=1
r+=1
ws.cell(r,1,"O erro que esta aba corrige").font=SUB; r+=1
for t in ['O relatório de outubro declara "Inadimplência Total: R$ 311,15".',
          'Esse número só conta meses ANTERIORES. Ele ignora os boletos do próprio mês que ficaram sem pagamento — R$ 5.765,42 em out/26.',
          'A dívida real no fechamento de outubro é 19,5x maior do que o relatório informa.',
          'Isso não é detalhe de apresentação: é o indicador usado para decidir se alguém precisa ser cobrado.']:
    ws.cell(r,1,"• "+t).font=N; r+=1
r+=1
ws.cell(r,1,"Comparativo: inadimplência declarada x real, mês a mês").font=SUB; r+=1
hrow(ws,r,["Competência","Declarada no PDF","Boletos do mês não pagos","Posição real no fechamento","Subdeclaração"],[14,18,24,22,14]); r+=1
naopago=defaultdict(float)
for x in ROWS:
    if x["tipo"]=="inadimplencia_anterior": continue
    if x.get("boleto") is not None and x.get("pago") is None: naopago[x["relatorio"]]+=x["boleto"]
fr=r
for m in META:
    c_=m["competencia"]
    ws.cell(r,1,c_).font=N
    x=ws.cell(r,2,m["inadimplencia_total"]); x.font=AZ; x.number_format=R2
    x=ws.cell(r,3,round(naopago[c_],2)); x.font=N; x.number_format=R2
    x=ws.cell(r,4,f"=B{r}+C{r}"); x.font=NB; x.number_format=R2
    x=ws.cell(r,5,f'=IFERROR(D{r}/B{r},"—")'); x.font=N; x.number_format='0.0"x"'
    r+=1
for ci,L in [(2,"B"),(3,"C"),(4,"D")]:
    x=ws.cell(r,ci,f"=SUM({L}{fr}:{L}{r-1})"); x.font=NB; x.number_format=R2
ws.cell(r,1,"TOTAL").font=NB
for ci in range(1,6): ws.cell(r,ci).fill=OKF

# ===================== ENERGIA =====================
ws=wb.create_sheet("Energia")
r0=head(ws,"Energia — queda explicada por inversor parado, e o estoque de créditos que ela consumiu",
        "Saldo atual = banco de créditos acumulado. Enquanto a compensação for maior que a injeção, o estoque cai.")
hrow(ws,r0,["Competência","Mês","Injetada kWh","Compensada kWh","Resultado do mês kWh",
            "Saldo final kWh","Meses de estoque restante","Faturado / kWh compensado"],[13,12,14,16,18,15,22,22])
r=r0+1; fr=r
for m in META:
    c_=m["competencia"]
    ws.cell(r,1,c_).font=NB; ws.cell(r,2,m["mes_nome"]).font=N
    for ci,col in [(3,"E"),(4,"F"),(6,"H")]:
        x=ws.cell(r,ci,f'=SUMIFS({B}${col}$5:${col}${BL},{B}$A$5:$A${BL},$A{r})'); x.font=N; x.number_format=KW
    x=ws.cell(r,5,f"=C{r}-D{r}"); x.font=N; x.number_format=KW
    x=ws.cell(r,7,f'=IF(E{r}>=0,"estoque crescendo",IFERROR(F{r}/-E{r},0))'); x.font=N; x.number_format='0.0'
    x=ws.cell(r,8,f'=IFERROR(SUMIFS({B}$K$5:$K${BL},{B}$A$5:$A${BL},$A{r},{B}$D$5:$D${BL},"corrente")/D{r},0)')
    x.font=N; x.number_format=R4
    r+=1
ws.cell(r,1,"TOTAL").font=NB
for ci,L in [(3,"C"),(4,"D"),(5,"E")]:
    x=ws.cell(r,ci,f"=SUM({L}{fr}:{L}{r-1})"); x.font=NB; x.number_format=KW
ws.cell(r,6,"—").font=NB
for ci in range(1,9): ws.cell(r,ci).fill=OKF
MEDIA_R=r; r+=2
ws.cell(r,1,"A causa, informada pelo sócio em 18/11/2026").font=SUB; r+=1
for t in ["Um dos dois inversores da usina estava quebrado: só um produzia. Os dois voltaram a produzir.",
          "Isso explica a série: out/26 injetou 5.801 kWh, praticamente metade dos ~11.000 kWh dos meses normais.",
          "Também explica por que o estoque de créditos foi consumido: a compensação continuou enquanto a geração caiu pela metade.",
          "Com os dois inversores de volta, a injeção deve retornar ao patamar de 11.000 a 13.000 kWh/mês."]:
    ws.cell(r,1,"• "+t).font=N; r+=1
r+=1
ws.cell(r,1,"O que ainda precisa ser acompanhado").font=SUB; r+=1
for t in ["O saldo total de créditos caiu de 36.430 kWh (jan/26) para 7.823 kWh (out/26): −78%.",
          "A UC 3014144595 fechou out/26 com saldo ZERO (era 26.548 kWh em jan/26). Ela não tem mais colchão.",
          "Confirmar no relatório de novembro se a injeção voltou ao patamar normal.",
          "Quantificar a energia perdida no período em que um inversor esteve parado — é receita que não foi faturada.",
          "Verificar se houve expiração de créditos durante o período de geração reduzida."]:
    ws.cell(r,1,"• "+t).font=N; r+=1
r+=1
ws.cell(r,1,"Projeção do estoque (edite as células azuis para testar cenários)").font=SUB; r+=1
ws.cell(r,1,"Saldo em out/26 (kWh)").font=N; c=ws.cell(r,2,7823); c.font=AZ; c.number_format=KW; SALDO=r; r+=1
ws.cell(r,1,"Injeção mensal assumida (kWh)").font=N; c=ws.cell(r,2,11000); c.font=AZ; c.number_format=KW
ws.cell(r,5,"Patamar esperado com os dois inversores produzindo.").font=SM; INJ=r; r+=1
ws.cell(r,1,"Compensação mensal assumida (kWh)").font=N; c=ws.cell(r,2,10811); c.font=AZ; c.number_format=KW; CMP=r; r+=1
ws.cell(r,1,"Resultado do mês (kWh)").font=N; c=ws.cell(r,2,f"=B{INJ}-B{CMP}"); c.font=N; c.number_format=KW; r+=1
ws.cell(r,1,"Meses até o estoque zerar").font=NB
c=ws.cell(r,2,f'=IF(B{INJ}>=B{CMP},"não zera — estoque volta a crescer",IFERROR(B{SALDO}/(B{CMP}-B{INJ}),0))')
c.font=VM; c.number_format='0.0'; c.fill=WARN; r+=1
ws.cell(r,1,"Faturamento mensal se a compensação cair ao nível da injeção").font=N
c=ws.cell(r,2,f"=B{INJ}*Indicadores!$B$8"); c.font=N; c.number_format=R2; r+=1
ws.cell(r,1,"Faturamento mensal médio do período").font=N
c=ws.cell(r,2,"=Indicadores!$B$6"); c.font=N; c.number_format=R2
R["totrec"]=TOTREC; R["energia_media"]=MEDIA_R
json.dump(R,open("ref.json","w"))
wb.save(OUT); print("parte 2 ok | total a receber na linha",TOTREC)
