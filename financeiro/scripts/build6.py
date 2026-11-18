# -*- coding: utf-8 -*-
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
OUT="/home/user/GuiFIzz/financeiro/LF_Agropastoril_Analise_Relatorios_2026.xlsx"
wb=load_workbook(OUT)
F="Arial"
N=Font(name=F,size=10); NB=Font(name=F,size=10,bold=True); SM=Font(name=F,size=9,color="404040")
VM=Font(name=F,size=10,bold=True,color="C00000")
ALERT=PatternFill("solid",fgColor="FCE4E4"); WARN=PatternFill("solid",fgColor="FFF2CC")

wb["Contrato_Bro"]["E14"]="A Bro aplica esta leitura. Confere com os 9 relatórios (diferença de 2 centavos = arredondamento mensal)."
wb["Contrato_Bro"]["E14"].font=SM

# ---- novas perguntas vindas do contrato
ws=wb["Perguntas_Bro"]
r=max(x for x in range(5,60) if ws.cell(x,1).value is not None)+1
novas=[("SUSPENSA","O contrato GD074 está no nome de AGRO PASTORIL DOS POCOES. A usina é da FOTOVOLT CURRAL NOVO SPE e o repasse vai para LF AGROPASTORIL. Como corrigir a titularidade?",
        "Preâmbulo e considerandos do GD-074-02-24 contra o QSA da SPE e os relatórios mensais.",
        "São três CNPJs em três papéis. Enquanto não bater, a receita está sendo declarada por quem não é dono do ativo."),
 ("SUSPENSA","Cadê o contrato de locação da usina com o consórcio, que define a Parcela Fixa de R$ 1.000,00/mês?",
  "Cláusula 2.2 do GD074 cita esse contrato; ele nunca foi apresentado e não aparece em nenhum relatório.",
  "É o documento que dá base legal ao enquadramento como locação de equipamento."),
 ("SUSPENSA","A titularidade da UC geradora foi transferida para o consórcio? Em nome de quem ela está hoje na CEMIG?",
  "Cláusulas 1.1.3 e 1.1.4 autorizam sublocação da UFV e troca de titularidade da UC geradora.",
  "Se a UC geradora saiu do nome da SPE, o controle do ativo mudou sem que isso apareça em lugar nenhum."),
 ("SUSPENSA","A Taxa de Administração é 10% do RECEBIDO (cl. 2.1 B) ou sobre a energia compensada independentemente do pagamento (cl. 2.2)?",
  "O próprio contrato traz as duas definições. A Bro aplica a primeira.",
  "Exposição de R$ 3.146,12 em 9 meses se a Bro passar a aplicar a segunda leitura."),
 ("SUSPENSA",'A cláusula 4.2 diz que "todo o trabalho desenvolvido será de exclusiva propriedade da CONTRATADA". Isso inclui a carteira de clientes?',
  "Cláusula 4.2 do GD074.",
  "Se a carteira é da Bro, a SPE não tem ativo comercial — tem um fluxo que pode ser desligado."),
 ("SUSPENSA","O contrato declara usina de 37 kWp, mas a geração observada e os dois inversores indicam potência muito maior. Qual a potência registrada na CEMIG para esta UC geradora?",
  "Cláusula 2.1 contra a média dos relatórios e a configuração real da usina.",
  "Um contrato que descreve metade do ativo não serve de base para nada — nem para seguro, nem para venda."),
 ("SUSPENSA","Qual foi a Taxa Inicial efetivamente paga desde 2024?",
  "Cláusula 2.1(A): 50% do primeiro faturamento de cada consumidor captado.",
  "A multa rescisória é múltiplo desse valor. Sem ele não se sabe se sair do contrato é caro ou barato."),
]
i=r-4
for pr,q,ev,dec in novas:
    ws.cell(r,1,i).font=N; i+=1
    c=ws.cell(r,2,pr); c.font=VM if pr=="CRÍTICA" else NB
    c.fill=ALERT if pr=="CRÍTICA" else (WARN if pr=="ALTA" else PatternFill("solid",fgColor="D9D9D9") if pr=="SUSPENSA" else PatternFill())
    if pr=="SUSPENSA": q="[SUSPENSA — nasceu do GD-074, contrato de outra empresa] "+q
    c.alignment=Alignment(horizontal="center")
    for ci,t in [(3,q),(4,ev),(5,dec)]:
        x=ws.cell(r,ci,t); x.font=N if ci==3 else SM
        x.alignment=Alignment(wrap_text=True,vertical="top")
    ws.row_dimensions[r].height=42
    r+=1

# ---- novas acoes
ws=wb["Plano_de_Acao"]
r=max(x for x in range(5,60) if ws.cell(x,1).value is not None)+1
i=r-4
for pz,ac,pq,imp in [
 ("Até 30 dias","Corrigir a titularidade do contrato GD074 — hoje assinado por Agro Pastoril dos Poções.",
  "A SPE é dona do ativo, Poções assinou o contrato e LF recebe o dinheiro. Três CNPJs, três papéis.","Regulariza toda a receita"),
 ("Até 30 dias","Obter o contrato de locação com o consórcio e passar a faturar a Parcela Fixa de R$ 1.000,00/mês.",
  "É a base legal do enquadramento como locação; previsto na cl. 2.2 e nunca executado.","R$ 12.000/ano documentados"),
 ("Até 30 dias","Levar ao contador a base tributável correta: R$ 75.261,28 e não R$ 67.638,47.",
  "A taxa de administração é despesa, não redução de receita. A base do contrato é maior que o repasse.","~R$ 864 em 9 meses"),
 ("Até 60 dias","Leitura jurídica da cláusula 4.2 antes de qualquer renegociação com a Bro.",
  "A redação sugere que a carteira de clientes é propriedade da Bro.","Define o valor do negócio"),
 ("Até 60 dias","Levantar a Taxa Inicial paga desde 2024 e calcular o custo real de sair do contrato.",
  "Estamos no mês 32: multa de 2x a Taxa Inicial, mais 90 dias de aviso prévio.","Define o poder de barganha"),
]:
    ws.cell(r,1,i).font=N; i+=1
    c=ws.cell(r,2,pz); c.font=NB; c.alignment=Alignment(horizontal="center")
    for ci,t in [(3,ac),(4,pq),(5,imp)]:
        x=ws.cell(r,ci,t); x.font=N if ci==3 else SM
        x.alignment=Alignment(wrap_text=True,vertical="top")
    ws.row_dimensions[r].height=30
    r+=1

# ---- Leia-me: apontar a nova aba
lm=wb["Leia-me"]
rr=max(x for x in range(10,40) if lm.cell(x,1).value=="Base_Lancamentos")
lm.insert_rows(rr)
lm.cell(rr,1,"Contrato_Bro").font=NB
lm.cell(rr,3,"O contrato GD074 contra o que foi praticado: remuneração da Bro, parcela fixa, base tributável, garantia de geração e custo de saída.").font=N
wb.save(OUT); print("ok")
