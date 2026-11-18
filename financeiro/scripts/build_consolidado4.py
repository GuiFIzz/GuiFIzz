# -*- coding: utf-8 -*-
import json, datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, BarChart, Reference
L=json.load(open("extrato.json"))
OUT="../Fotovolt_Curral_Novo_Consolidado.xlsx"; wb=load_workbook(OUT)
F="Arial"
H=Font(name=F,bold=True,color="FFFFFF",size=10); HF=PatternFill("solid",fgColor="1F3864")
TIT=Font(name=F,bold=True,size=16,color="1F3864"); SUB=Font(name=F,bold=True,size=11,color="1F3864")
N=Font(name=F,size=10); NB=Font(name=F,size=10,bold=True); SM=Font(name=F,size=9,color="404040")
AZ=Font(name=F,size=10,color="0000FF"); KPI=Font(name=F,size=13,bold=True,color="1F3864")
VM=Font(name=F,size=13,bold=True,color="C00000")
OKF=PatternFill("solid",fgColor="E2EFDA"); WARN=PatternFill("solid",fgColor="FFF2CC")
ALERT=PatternFill("solid",fgColor="FCE4E4"); THIN=Border(*[Side(style="thin",color="BFBFBF")]*4)
R2='R$ #,##0.00;[Red](R$ #,##0.00);-'; PC='0.0%'; PC2='0.00%'; DT='dd/mm/yyyy'
MS=sorted({l["data"][:7] for l in L})
fm=wb["Fluxo_Mensal"]
# localizar linhas de interesse no Fluxo_Mensal
def achaFM(txt):
    for r in range(5,60):
        v=fm.cell(r,1).value
        if isinstance(v,str) and v.strip()==txt: return r
    return None
REC=achaFM("Receita Energia"); RES=achaFM("RESULTADO DO MÊS"); SAL=achaFM("SALDO ACUMULADO")
DIST=[achaFM(f"Dist. Sócio - {s}") for s in ["Guilherme","Luiz Felipe","Ricardo","Lucas"]]
rs=wb["Retorno_Socios"]
TOTP=[i for i in range(4,30) if rs.cell(i,1).value=="TOTAL"][0]
def acha(aba,txt,ate=40):
    """Procura o RÓTULO na coluna A, a partir da linha 4 e ignorando frases longas."""
    w=wb[aba]
    for r in range(4,ate):
        v=w.cell(r,1).value
        if isinstance(v,str) and len(v)<60 and txt.lower() in v.lower(): return r
    raise SystemExit(f"nao achei '{txt}' em {aba}")
CEN_TIR=acha("Cenarios","TIR projetada"); CEN_ANOS=acha("Cenarios","Anos até recuperar")
CEN_PREM=acha("Cenarios","Prêmio sobre o CDI")
AT_PROV=acha("Ativo_Reposicao","Provisão que deveria existir hoje")
AT_CAPEX=acha("Ativo_Reposicao","CAPEX da usina")
CX_SALDO=acha("Caixa_Sustentacao","Saldo em caixa"); CX_FOL=acha("Caixa_Sustentacao","Fôlego de caixa")
CX_REC=acha("Caixa_Sustentacao","Receita média mensal"); CX_DIST=acha("Caixa_Sustentacao","Distribuição média mensal")
print(f"refs: TIR={CEN_TIR} anos={CEN_ANOS} premio={CEN_PREM} prov={AT_PROV} saldo={CX_SALDO}")

# ============== DASHBOARD FINANCEIRO ==============
wb.remove(wb["Dashboard_Financeiro"]) if "Dashboard_Financeiro" in wb.sheetnames else None
ws=wb.create_sheet("Dashboard_Financeiro")
ws.sheet_view.showGridLines=False
ws["A1"]="Dashboard financeiro — Fotovolt Curral Novo SPE"; ws["A1"].font=TIT
ws["A2"]="Tudo calculado a partir do extrato bancário e dos relatórios da Bro. Atualiza ao rodar atualizar_consolidado.py."
ws["A2"].font=Font(name=F,size=9,italic=True,color="595959")
for c,w in [("A",40),("B",18),("C",3)]: ws.column_dimensions[c].width=w
kpis=[("Capital investido pelos sócios",f"=Retorno_Socios!$B${TOTP}",R2,None),
      ("Já devolvido aos sócios",f"=Retorno_Socios!$C${TOTP}",R2,None),
      ("% do capital recuperado",f"=IFERROR(Retorno_Socios!$C${TOTP}/Retorno_Socios!$B${TOTP},0)",PC,WARN),
      ("Falta recuperar",f"=Retorno_Socios!$B${TOTP}-Retorno_Socios!$C${TOTP}",R2,ALERT),
      ("TIR projetada — cenário base",f"=Cenarios!$C${CEN_TIR}",PC2,OKF),
      ("Anos até recuperar o capital",f"=Cenarios!$C${CEN_ANOS}",'0.0" anos"',None),
      ("Caixa hoje",f"=Caixa_Sustentacao!$B${CX_SALDO}",R2,WARN),
      ("Fôlego de caixa",f"=Caixa_Sustentacao!$B${CX_FOL}",'0.0" meses"',ALERT),
      ("Receita média mensal",f"=Caixa_Sustentacao!$B${CX_REC}",R2,None),
      ("Distribuição média mensal",f"=Caixa_Sustentacao!$B${CX_DIST}",R2,None),
      ("Provisão de inversor que deveria existir",f"=Ativo_Reposicao!$B${AT_PROV}",R2,ALERT),
      ("Receita por kWh produzido","=Energia_Resumo!$G$15",'R$ 0.0000',None)]
r=4
ws.cell(r,1,"Indicadores-chave").font=SUB; r+=1
for lbl,f_,fmt,fill in kpis:
    ws.cell(r,1,lbl).font=N
    x=ws.cell(r,2,f_); x.number_format=fmt
    x.font=VM if fill is ALERT else KPI
    if fill: x.fill=fill
    r+=1
# dados para graficos
G0=r+2
ws.cell(G0-1,1,"Série mensal (base dos gráficos)").font=SUB
for i,t in enumerate(["Mês","Receita","Distribuído","Saldo de caixa"]):
    x=ws.cell(G0,1+i,t); x.font=H; x.fill=HF
rr=G0+1; fg=rr
for i,m in enumerate(MS):
    Lc=get_column_letter(2+i)
    ws.cell(rr,1,m).font=SM
    x=ws.cell(rr,2,f"=Fluxo_Mensal!{Lc}{REC}"); x.font=SM; x.number_format=R2
    soma="+".join(f"Fluxo_Mensal!{Lc}{d}" for d in DIST if d)
    x=ws.cell(rr,3,f"=-({soma})"); x.font=SM; x.number_format=R2
    x=ws.cell(rr,4,f"=Fluxo_Mensal!{Lc}{SAL}"); x.font=SM; x.number_format=R2
    rr+=1
lg=rr-1
for c,w in [("B",14),("C",14),("D",16)]: ws.column_dimensions[c].width=w
def arruma(ch,t,y):
    ch.title=t; ch.style=2; ch.roundedCorners=False
    ch.y_axis.title=y; ch.x_axis.title="Mês"
    ch.x_axis.delete=False; ch.y_axis.delete=False
    if ch.legend: ch.legend.position="b"; ch.legend.overlay=False
    ch.height=8.5; ch.width=20
cats=Reference(ws,min_col=1,min_row=fg,max_row=lg)
c1=BarChart(); c1.type="col"
c1.add_data(Reference(ws,min_col=2,max_col=3,min_row=G0,max_row=lg),titles_from_data=True)
c1.set_categories(cats); arruma(c1,"Receita recebida x distribuído aos sócios","R$")
ws.add_chart(c1,"F4")
c2=LineChart()
c2.add_data(Reference(ws,min_col=4,min_row=G0,max_row=lg),titles_from_data=True)
c2.set_categories(cats); arruma(c2,"Evolução do saldo de caixa","R$")
for s in c2.series: s.smooth=False
ws.add_chart(c2,"F22")

# ============== RESUMO ==============
wb.remove(wb["Resumo"]) if "Resumo" in wb.sheetnames else None
ws=wb.create_sheet("Resumo")
ws.sheet_view.showGridLines=False
for c,w in [("A",52),("B",20),("C",76)]: ws.column_dimensions[c].width=w
ws["A1"]="Fotovolt Curral Novo SPE — posição consolidada"; ws["A1"].font=TIT
ws["A2"]="CNPJ 51.245.620/0001-21 · extrato de jul/2023 a out/2026 · relatórios de energia de jan a out/2026"
ws["A2"].font=Font(name=F,size=9,italic=True,color="595959")
r=4
ws.cell(r,1,"O investimento").font=SUB; r+=1
for lbl,f_,fmt,obs in [
  ("Capital aportado por 4 sócios",f"=Retorno_Socios!$B${TOTP}",R2,"R$ 90.000 cada, entre jul e set/2023. A LF Agropastoril não aportou."),
  ("Pago à Bro Energy pela usina",f'=Ativo_Reposicao!$B${AT_CAPEX}',R2,"Todo o capital foi para o ativo."),
  ("Já devolvido aos sócios",f"=Retorno_Socios!$C${TOTP}",R2,"Em 33 meses de operação."),
  ("% do capital recuperado",f"=IFERROR(Retorno_Socios!$C${TOTP}/Retorno_Socios!$B${TOTP},0)",PC,"Passou da metade."),
  ("Falta recuperar",f"=Retorno_Socios!$B${TOTP}-Retorno_Socios!$C${TOTP}",R2,"Cerca de 2 anos no ritmo atual."),
  ("TIR projetada — cenário base",f"=Cenarios!$C${CEN_TIR}",PC2,"Com 22 anos de operação à frente. Veja a aba Cenarios."),
  ("Prêmio sobre o CDI",f"=Cenarios!$C${CEN_PREM}",PC2,"Quanto o projeto rende acima de deixar o dinheiro no banco."),
 ]:
    ws.cell(r,1,lbl).font=N
    x=ws.cell(r,2,f_); x.font=KPI; x.number_format=fmt
    ws.cell(r,3,obs).font=SM; r+=1
r+=1
ws.cell(r,1,"As três decisões que precisam ser tomadas").font=SUB; r+=1
for i,(t,d) in enumerate([
  ("1. Caixa mínimo","A empresa opera com fôlego de poucos meses e já precisou de 14 aportes dos sócios para cobrir furos. Definir quanto fica retido antes de distribuir."),
  ("2. Provisão de inversor","Um inversor falhou com 3 anos e não havia reserva. Definir a retenção mensal — é pequena perto da distribuição."),
  ("3. Acerto entre sócios","Os quatro têm 25% e aportaram igual, mas receberam valores diferentes. Acertar a diferença acumulada."),
 ],1):
    ws.cell(r,1,t).font=NB; ws.cell(r,3,d).font=N; ws.row_dimensions[r].height=28
    ws.cell(r,3).alignment=Alignment(wrap_text=True,vertical="top"); r+=1
r+=1
ws.cell(r,1,"Pendências com a Bro Energy").font=SUB; r+=1
for t in ["17.348 kWh sumiram do saldo de créditos em out/26 sem contrapartida de consumo (~R$ 12.020).",
          "R$ 6.076,57 de boletos em aberto na carteira, sendo R$ 5.422,69 de um único cliente.",
          "Nenhum cliente novo em 10 relatórios e duas instalações perdidas.",
          "E-mail com os oito questionamentos está em comunicacao/email_bro_energy_nov2026.md."]:
    ws.cell(r,1,"• "+t).font=N; r+=1
r+=1
ws.cell(r,1,"Como esta planilha funciona").font=SUB; r+=1
for t in ["Nenhum número foi digitado: tudo sai do extrato bancário e dos PDFs dos relatórios.",
          "O saldo final da aba Extrato bate com o extrato do Banco Inter de 31/10/2026.",
          "Azul é premissa editável. Preto é fórmula. Verde confere. Vermelho exige ação.",
          "Para atualizar: solte o novo extrato em financeiro/extratos/ e rode financeiro/scripts/atualizar_consolidado.py.",
          "O detalhe por cliente e por unidade consumidora fica na planilha LF_Agropastoril_Analise_Relatorios_2026.xlsx."]:
    ws.cell(r,1,"• "+t).font=N; r+=1

ordem=["Resumo","Dashboard_Financeiro","Conciliacao","Energia_Resumo","Retorno_Socios",
       "Cenarios","Caixa_Sustentacao","Ativo_Reposicao","Fluxo_Mensal","Extrato"]
wb._sheets=[wb[s] for s in ordem]
wb.save(OUT); print("parte 4 ok | abas:",wb.sheetnames)
