from .models import Orcamento
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Flowable, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
import json
from collections import Counter


def formatar_portoes(portoes_json_str: str) -> str:
    """
    Recebe uma string JSON de portões e a formata para um texto legível.
    Exemplo de entrada: '{"portao_1": "single", "portao_2": "double"}'
    Exemplo de saída: "1 Single, 1 Double"
    """
    if not portoes_json_str or portoes_json_str == '{}':
        return "Nenhum"

    try:
        portoes_dict = json.loads(portoes_json_str)
        contagem = Counter(portoes_dict.values())
        partes_formatadas = []
        if contagem['single'] > 0:
            # Adiciona "s" se for plural
            sufixo = 's' if contagem['single'] > 1 else ''
            partes_formatadas.append(
                f"{contagem['single']} Single Gate{sufixo}")

        if contagem['double'] > 0:
            sufixo = 's' if contagem['double'] > 1 else ''
            partes_formatadas.append(
                f"{contagem['double']} Double Gate{sufixo}")

        return ", ".join(partes_formatadas)

    except (json.JSONDecodeError, TypeError):
        # Retorna o dado bruto se não for um JSON válido, para debug
        return portoes_json_str


def gerar_orcamento(orcamento: Orcamento, caminho_arquivo: str):
    """Gera um PDF de orçamento a partir dos dados do orçamento."""

    orcamento_pdf = SimpleDocTemplate(caminho_arquivo)

    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(name="Titulo", parent=styles['Normal'],
                                   fontName="Helvetica-Bold",
                                   fontSize=14,
                                   leading=22,
                                   alignment=TA_CENTER
                                   )
    estilo_normal = ParagraphStyle(name="Normal", parent=styles['Normal'],
                                   fontName="Helvetica",
                                   fontSize=11,
                                   leading=14,
                                   alignment=TA_LEFT
                                   )
    estilo_endereco = ParagraphStyle(name="Endereco", parent=styles['Normal'],
                                     fontName="Helvetica",
                                     fontSize=10,
                                     leading=14,
                                     alignment=TA_LEFT
                                     )
    estilo_bold = ParagraphStyle(name="Bold", parent=styles['Normal'],
                                 fontName="Helvetica-Bold",
                                 fontSize=10,
                                 leading=22,
                                 alignment=TA_CENTER
                                 )

    dados_cliente = [
        Paragraph(orcamento.cliente.nome, estilo_endereco),
        Paragraph(orcamento.cliente.endereco, estilo_endereco),
        Paragraph(f"Phone: {orcamento.cliente.telefone}", estilo_endereco),
        Paragraph(f"Email: {orcamento.cliente.email}", estilo_endereco)
    ]

    portoes_formatados = formatar_portoes(orcamento.portoes)

    dados_tabela = [
        ['Fence Type:', orcamento.material],
        ['Color:',  orcamento.cor_material if orcamento.cor_material else 'N/A'],
        ['Length:', f"{orcamento.metragem} ft"],
        ['Gates:', portoes_formatados if orcamento.portao else 'N/A'],
        ['Estimated Cost:', f"$ {orcamento.valor_estimado:.2f}"],
        ['Removal/Disposal', 'FREE']
    ]

    tabela = Table(dados_tabela)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story = []

    image = Image("fence.logo1.png", width=200, height=100)
    story.append(image)
    story.append(
        Paragraph("Subject: Proposal for Fence Installation", estilo_titulo))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Dear Customer,", estilo_normal))
    story.append(Spacer(1, 12))
    story.append(dados_cliente[0])
    story.append(dados_cliente[1])
    story.append(dados_cliente[2])
    story.append(dados_cliente[3])
    story.append(Spacer(1, 20))
    story.append(Paragraph("Thank you for considering Nunes Fence LLC for your fencing needs. "
                           "We are pleased to provide you with the following proposal based on the specifications discussed:", estilo_normal))
    story.append(Spacer(1, 20))
    story.append(tabela)
    story.append(Spacer(1, 10))
    story.append(
        Paragraph("Please note that this estimate is valid for 7 days.", estilo_bold))
    story.append(Spacer(1, 26))
    story.append(Paragraph("All materials and labor are included in this estimate. Our fences are built with high-quality"
                           " materials and professional craftsmanship, ensuring durability and long-lasting performance.", estilo_normal))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "To move forward, just reply to this email or reach us by call/text with any questions. We look forward to working with you!", estilo_normal))
    story.append(Spacer(1, 26))
    story.append(Paragraph("Sincerely,", estilo_normal))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Nunes Fence LLC", estilo_endereco))
    story.append(Paragraph("123 Main Street", estilo_endereco))
    story.append(Paragraph("Orlando, Florida, 32801", estilo_endereco))
    story.append(Paragraph("Phone: (351) 201-4314", estilo_endereco))
    story.append(Paragraph("Email: nunesfence12@gmail.com", estilo_endereco))

    orcamento_pdf.build(story)

def criar_corpo_html_orcamento(orcamento: Orcamento) -> str:
    """Cria uma string HTML formatada para o corpo do e-mail a partir de um orçamento."""

    
    portoes_formatados = formatar_portoes(orcamento.portoes)

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #333; }}
            .container {{ max-width: 680px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
            .header {{ text-align: center; margin-bottom: 25px; }}
            .titulo {{ font-size: 16pt; font-weight: bold; color: #000; margin-top: 10px; }}
            .endereco {{ font-size: 10pt; line-height: 1.5; margin-bottom: 15px; }}
            .bold {{ font-weight: bold; text-align: center; font-size: 10pt; margin-top: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 25px 0; }}
            th, td {{ border: 1px solid #cccccc; padding: 10px; text-align: left; }}
            th {{ background-color: #f2f2f2; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="cid:fence.logo1.png" alt="Nunes Fence Logo" width="200">
                <p class="titulo">Proposal for Fence Installation</p>
            </div>
            
            <p>Dear {orcamento.cliente.nome},</p>
            
            <p>Thank you for considering Nunes Fence LLC for your fencing needs. We are pleased to provide you with the following proposal based on the specifications discussed:</p>

            <table>
                <tr><th>Fence Type:</th><td>{orcamento.material}</td></tr>
                <tr><th>Color:</th><td>{orcamento.cor_material if orcamento.cor_material else 'N/A'}</td></tr>
                <tr><th>Length:</th><td>{orcamento.metragem} ft</td></tr>
                <tr><th>Gates:</th><td>{portoes_formatados if orcamento.portao else 'N/A'}</td></tr>
                <tr><th>Estimated Cost:</th><td>$ {orcamento.valor_estimado:.2f}</td></tr>
                <tr><th>Removal/Disposal:</th><td>FREE</td></tr>
            </table>

            <p class="bold">Please note that this estimate is valid for 7 days.</p>

            <p>All materials and labor are included in this estimate. Our fences are built with high-quality materials and professional craftsmanship, ensuring durability and long-lasting performance.</p>
            
            <p>To move forward, just reply to this email or reach us by call/text with any questions. We look forward to working with you!</p>
            
            <p>Sincerely,</p>
            
            <div class="endereco">
                <b>Nunes Fence LLC</b><br>
                123 Main Street<br>
                Orlando, Florida, 32801<br>
                Phone: (351) 201-4314<br>
                Email: nunesfence12@gmail.com
            </div>
        </div>
    </body>
    </html>
    """
    return html