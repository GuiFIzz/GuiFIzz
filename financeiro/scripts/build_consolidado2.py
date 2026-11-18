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
def lin(ws,r,lbl,val=None,fmt=R2,fonte=None,fill=None,obs=None):
    ws.cell(r,1,lbl).font=fonte or N
    if val is not None:
        x=ws.cell(r,2,val); x.font=fonte or N; x.number_format=fmt
        if fill: x.fill=fill
    if obs: ws.cell(r,3,obs).font=SM
    return r+1

ex=wb["Extrato"]; last_e=ex.max_row-1
E="Extrato!"; FE=f"{E}$D$5:$D${last_e}"; FC=f"{E}$C$5:$C${last_e}"; FD=f"{E}$A$5:$A${last_e}"
MS=sorted({l["data"][:7] for l in L}); u12=MS[-12:]
d0=f'DATE({u12[0][:4]},{int(u12[0][5:])},1)'

# ================= CAIXA E SUSTENTACAO =================
wb.remove(wb["Caixa_Sustentacao"]) if "Caixa_Sustentacao" in wb.sheetnames else None
ws=wb.create_sheet("Caixa_Sustentacao"); head(ws,"Caixa e sustentação",
  "A empresa distribui até quase zerar o caixa e depois pede aporte aos sócios. Esta aba dimensiona isso.")
for c,w in [("A",46),("B",18),("C",64)]: ws.column_dimensions[c].width=w
r=4
r=lin(ws,r,"Saldo em caixa (31/10/2026)",f"={E}$E${last_e}",R2,KPI,WARN,"Último saldo do extrato.")
r=lin(ws,r,"Receita média mensal (últimos 12 meses)",
      f'=SUMIFS({FE},{FC},"Receita Energia",{FD},">="&{d0})/12',R2,N,None,"Repasse da Bro que entrou na conta.")
CUSTO=r
r=lin(ws,r,"Custo fixo médio mensal (últimos 12 meses)",
      f'=-(SUMIFS({FE},{FC},"Impostos (DARF)",{FD},">="&{d0})+SUMIFS({FE},{FC},"Contabilidade",{FD},">="&{d0})'
      f'+SUMIFS({FE},{FC},"O&M / Manutenção",{FD},">="&{d0})+SUMIFS({FE},{FC},"Outras Despesas",{FD},">="&{d0}))/12',
      R2,N,None,"Impostos, contabilidade, O&M e outras despesas.")
r=lin(ws,r,"Distribuição média mensal (últimos 12 meses)",
      f'=-(SUMIFS({FE},{FC},"Dist. Sócio - Guilherme",{FD},">="&{d0})+SUMIFS({FE},{FC},"Dist. Sócio - Luiz Felipe",{FD},">="&{d0})'
      f'+SUMIFS({FE},{FC},"Dist. Sócio - Ricardo",{FD},">="&{d0})+SUMIFS({FE},{FC},"Dist. Sócio - Lucas",{FD},">="&{d0}))/12',
      R2,N,None,"O que sai para os sócios todo mês.")
FOLEGO=r
r=lin(ws,r,"Fôlego de caixa (meses de custo fixo)",f"=IFERROR(B4/B{CUSTO},0)",'0.0" meses"',VM,ALERT,
      "Quantos meses a empresa paga as contas sem receber nada.")
r+=1
ws.cell(r,1,"O problema dos aportes de emergência").font=SUB; r+=1
r=lin(ws,r,"Aportes de sócio para cobrir furos de caixa",f'=SUMIFS({FE},{FC},"Aporte Sócio")',R2,N,None,
      "Dinheiro que os sócios tiveram que devolver para a empresa.")
r=lin(ws,r,"Quantas vezes isso aconteceu",f'=COUNTIFS({FC},"Aporte Sócio")','0',N,None,
      "Cada ocorrência é um mês em que a distribuição foi grande demais.")
r+=1
ws.cell(r,1,"Política de caixa mínimo que a empresa não tem (edite o azul)").font=SUB; r+=1
MESES_MIN=r
r=lin(ws,r,"Meses de custo fixo a manter em caixa",3,'0.0',AZ,None,"Premissa editável.")
RESERVA=r
r=lin(ws,r,"Caixa mínimo recomendado",f"=B{MESES_MIN}*B{CUSTO}",R2,NB,WARN)
r=lin(ws,r,"Falta para atingir o caixa mínimo",f"=MAX(0,B{RESERVA}-B4)",R2,VM,ALERT,
      "Reter este valor da próxima distribuição resolve.")
r+=1
ws.cell(r,1,"Leitura").font=SUB; r+=1
for t in ["Em outubro não houve distribuição aos sócios e o caixa subiu de R$ 2.373,72 para R$ 5.157,60.",
          "Foi a decisão certa: o mês teve R$ 2.929,89 de DARF (IRPJ e CSLL trimestrais) contra R$ 4.776,66 de receita.",
          "A regra prática: só distribuir o que sobra depois de recompor o caixa mínimo e a provisão de inversor."]:
    ws.cell(r,1,"• "+t).font=N; r+=1

# ================= ATIVO E REPOSICAO =================
wb.remove(wb["Ativo_Reposicao"]) if "Ativo_Reposicao" in wb.sheetnames else None
ws=wb.create_sheet("Ativo_Reposicao"); head(ws,"Ativo e provisão de reposição",
  "Um inversor quebrou em 2026 e não havia um centavo de reserva. Esta aba dimensiona a provisão que deveria existir.")
for c,w in [("A",46),("B",18),("C",64)]: ws.column_dimensions[c].width=w
r=4
CAPEX=r
r=lin(ws,r,"CAPEX da usina",f'=-SUMIFS({FE},{FC},"Investimento - Usina (BRO Energy)")',R2,KPI,None,
      "Pago à Bro Energy entre jul e set/2023, do extrato.")
KWP=r
r=lin(ws,r,"Potência estimada (kWp)",73,KW,AZ,None,"Estimada pela geração observada. Confirmar com o registro da CEMIG.")
r=lin(ws,r,"CAPEX por kWp",f"=IFERROR(B{CAPEX}/B{KWP},0)",R2,NB,None,"Referência para comparar com o mercado.")
r=lin(ws,r,"Entrada em operação",datetime.date(2023,11,1),DT,AZ,None,"Primeira receita de energia no extrato: nov/2023.")
IDADE=r
r=lin(ws,r,"Idade da usina (anos)",'=YEARFRAC(B7,DATE(2026,10,31))','0.0',N)
r+=1
ws.cell(r,1,"Vida útil e reposição (edite o azul)").font=SUB; r+=1
VP=r; r=lin(ws,r,"Vida útil dos painéis (anos)",25,'0',AZ,None,"Padrão de mercado.")
VI=r; r=lin(ws,r,"Vida útil do inversor (anos)",10,'0',AZ,None,"Padrão de mercado; o primeiro falhou com 3 anos.")
NI=r; r=lin(ws,r,"Quantidade de inversores",2,'0',AZ,None,"Confirmado: a usina tem dois.")
CI=r; r=lin(ws,r,"Custo estimado de um inversor",10000,R2,AZ,None,"ESTIMATIVA — pedir orçamento à Solcare e ajustar.")
PROV=r
r=lin(ws,r,"Provisão mensal necessária",f"=IFERROR(B{NI}*B{CI}/(B{VI}*12),0)",R2,VM,WARN,
      "Quanto deveria ser retido todo mês para trocar os inversores no fim da vida.")
r=lin(ws,r,"Provisão que deveria existir hoje",f"=B{PROV}*B{IDADE}*12",R2,VM,ALERT,
      "Acumulado desde a entrada em operação. Hoje é zero.")
r=lin(ws,r,"Gasto real com O&M até agora",f'=-SUMIFS({FE},{FC},"O&M / Manutenção")',R2,N,None,
      "Solcare Retrofit Solar, out/2026 — o reparo do inversor.")
r+=1
ws.cell(r,1,"Leitura").font=SUB; r+=1
for t in ["O primeiro inversor falhou com cerca de 3 anos de uso, bem antes da vida útil esperada.",
          "O reparo custou R$ 600,00 e saiu do caixa corrente, que tinha R$ 2.373,72 no mês anterior.",
          "Se tivesse sido troca e não reparo, a empresa não teria dinheiro e dependeria de aporte dos sócios.",
          "A provisão mensal acima é pequena perto da distribuição e resolve o problema de forma definitiva."]:
    ws.cell(r,1,"• "+t).font=N; r+=1
wb.save(OUT); print("parte 2 ok")
