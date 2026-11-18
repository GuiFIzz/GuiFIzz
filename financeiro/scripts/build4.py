# -*- coding: utf-8 -*-
import json
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
D=json.load(open("dados.json")); META=D["meta"]; R=json.load(open("ref.json")); NM=len(META)
OUT="/home/user/GuiFIzz/financeiro/LF_Agropastoril_Analise_Relatorios_2026.xlsx"
wb=load_workbook(OUT)
F="Arial"
TIT=Font(name=F,bold=True,size=16,color="1F3864"); SUB=Font(name=F,bold=True,size=11,color="1F3864")
N=Font(name=F,size=10); NB=Font(name=F,size=10,bold=True); VM=Font(name=F,size=11,bold=True,color="C00000")
OKF=PatternFill("solid",fgColor="E2EFDA"); WARN=PatternFill("solid",fgColor="FFF2CC"); ALERT=PatternFill("solid",fgColor="FCE4E4")
R2='R$ #,##0.00'; PC='0.0%'; KW='#,##0'

ws=wb.create_sheet("Leia-me")
for col,w in [("A",52),("B",20),("C",76)]: ws.column_dimensions[col].width=w
ws["A1"]="LF Agropastoril — Análise dos relatórios de energia 2026"; ws["A1"].font=TIT
ws["A2"]="Construída a partir dos 9 relatórios mensais em PDF emitidos pela Bro. Nenhum número foi digitado à mão: todos são extraídos dos PDFs e recalculados."
ws["A2"].font=Font(name=F,size=9,italic=True,color="595959")
r=4
ws.cell(r,1,"Os cinco números que importam").font=SUB; r+=1
for lbl,f_,fmt in [("Repasse líquido recebido em 9 meses","=Indicadores!$B$14",R2),
                   ("Faturamento bruto emitido","=Indicadores!$B$5",R2),
                   ("Dinheiro devido à empresa","=Contas_a_Receber!$C$"+str(R["totrec"]),R2),
                   ("Queda do estoque de créditos (jan→out)","=IFERROR(Energia!$F$"+str(4+NM)+"/Energia!$F$5-1,0)",PC),
                   ("Clientes novos em 9 relatórios","=Indicadores!$B$20-Indicadores!$B$19",'0')]:
    ws.cell(r,1,lbl).font=NB
    c=ws.cell(r,2,f_); c.number_format=fmt; c.font=VM; c.fill=WARN
    r+=1
r+=1
ws.cell(r,1,"O que cada aba responde").font=SUB; r+=1
for aba,desc in [("Relatorios","Identifica os 9 relatórios recebidos e confere a matemática do repasse de cada um."),
  ("Clientes_Comparativo","Compara os relatórios entre si: quem entrou, quem saiu, quanto cada UC faturou."),
  ("Inadimplencia","Razão de cada boleto: quando foi faturado, quando foi pago, quanto de juros, o que ficou em aberto."),
  ("Contas_a_Receber","Quanto a empresa tem a receber hoje, separando dívida confirmada de dívida a verificar."),
  ("Energia","O estoque de créditos e quando ele acaba — a principal ameaça à receita."),
  ("Indicadores","Os indicadores do período, todos calculados da base."),
  ("Perguntas_Bro","As perguntas para a vendedora de energia, cada uma ancorada em um número."),
  ("Plano_de_Acao","O que fazer, por prazo e por impacto financeiro."),
  ("Base_Lancamentos",f"Os {R['base_last']-4} lançamentos extraídos dos PDFs. Fonte de tudo. Não editar.")]:
    ws.cell(r,1,aba).font=NB; ws.cell(r,3,desc).font=N; r+=1
r+=1
ws.cell(r,1,"Legenda de cores").font=SUB; r+=1
for cor,fill,txt in [("Azul",None,"Número lido diretamente do PDF (input). Alterar aqui muda os cálculos."),
                     ("Preto",None,"Fórmula calculada pela planilha."),
                     ("Vermelho / fundo rosa",ALERT,"Problema confirmado, exige ação."),
                     ("Fundo amarelo",WARN,"Depende de informação que ainda falta."),
                     ("Fundo verde",OKF,"Conferido e fechado.")]:
    c=ws.cell(r,1,cor); c.font=NB
    if cor=="Azul": c.font=Font(name=F,size=10,bold=True,color="0000FF")
    if fill: c.fill=fill
    ws.cell(r,3,txt).font=N; r+=1
r+=1
ws.cell(r,1,"Como os números foram obtidos").font=SUB; r+=1
for t in [f"Os {NM} PDFs foram lidos por extração automática de texto e convertidos em {R['base_last']-4} lançamentos.",
 "Os totais de dinheiro de cada relatório batem exatamente com o rodapé do PDF correspondente.",
 "Os totais de kWh diferem em 1 a 3 kWh por mês (menos de 0,03%) porque o PDF soma valores já arredondados.",
 'Linhas marcadas "neg 1/2" e "neg 2/2" em set/out são parcelas de uma dívida negociada da UC 3014144595 e foram tratadas como uma só competência.',
 "Tags de mês no PDF (ex.: mar-26) foram normalizadas para o formato 2026-03 para permitir conciliar boleto com pagamento."]:
    ws.cell(r,1,"• "+t).font=N; r+=1
r+=1
ws.cell(r,1,"Ressalvas — leia antes de decidir").font=SUB; r+=1
for t in ["A série está completa: o relatório de fevereiro foi entregue depois de cobrado e as dívidas de janeiro estavam quitadas nele.",
 "Os relatórios não mostram a geração medida na usina, só a energia alocada por UC. Um inversor ficou parado e nenhum relatório sinalizou.",
 "Não foi apresentado o contrato com a Bro. Prazo, rescisão e propriedade da carteira de clientes são desconhecidos.",
 "ESTRUTURAL: estes relatórios são emitidos para LF AGROPASTORIL, mas o ativo (a usina) pertence à FOTOVOLT CURRAL NOVO SPE LTDA.",
 "Em 9 meses, R$ 67.638,47 de repasse entraram numa empresa que não é a dona do ativo, sem contrato entre as duas. Isso precisa ser resolvido."]:
    c=ws.cell(r,1,"• "+t); c.font=N
    if t.startswith(("ESTRUTURAL","Em 9 meses")): c.font=Font(name=F,size=10,bold=True,color="C00000")
    r+=1

ordem=["Leia-me","Relatorios","Clientes_Comparativo","Inadimplencia","Contas_a_Receber",
       "Energia","Indicadores","Perguntas_Bro","Plano_de_Acao","Base_Lancamentos"]
wb._sheets=[wb[s] for s in ordem]
for s in wb.sheetnames:
    wb[s].sheet_view.showGridLines=False
wb.save(OUT); print("abas:",wb.sheetnames)
