from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit, QDateEdit, 
                             QRadioButton, QPushButton, QTableWidget, 
                             QVBoxLayout, QHBoxLayout, QMessageBox, 
                             QTableWidgetItem, QFileDialog, QDialog, 
                             QDialogButtonBox, QFormLayout, QStyle, QComboBox)
from PyQt5.QtCore import Qt, QDate, QSize
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
import matplotlib.pyplot as plt

class SelecionarDataDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Selecionar Período")
        layout = QVBoxLayout(self)

        self.data_inicio = QDateEdit(calendarPopup=True)
        self.data_fim = QDateEdit(calendarPopup=True)
        
        data_atual = QDate.currentDate()
        self.data_inicio.setDate(data_atual.addMonths(-1))
        self.data_fim.setDate(data_atual)

        layout.addWidget(QLabel("Data de Início:"))
        layout.addWidget(self.data_inicio)
        layout.addWidget(QLabel("Data de Fim:"))
        layout.addWidget(self.data_fim)

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botoes.accepted.connect(self.accept)
        botoes.rejected.connect(self.reject)
        layout.addWidget(botoes)

class InterfaceUsuario(QMainWindow):
    def __init__(self, controle_financas, analise_dados):
        super().__init__()
        self.controle_financas = controle_financas
        self.analise_dados = analise_dados
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Controle de Finanças')
        self.setGeometry(100, 100, 800, 600)  
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        
        self.data_edit = QDateEdit(calendarPopup=True)
        self.data_edit.setDate(QDate.currentDate())
        self.data_edit.setDisplayFormat("dd/MM/yyyy")
        self.data_edit.setMinimumWidth(120)
        
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(["Uber", "99", "Combustível", "Manutenção", 
                                       "IPVA/Licenciamento", "Multa", "Seguro", "Outros"])
        
        self.descricao_edit = QLineEdit()
        self.valor_edit = QLineEdit()
        
        form_layout.addRow("Data:", self.data_edit)
        form_layout.addRow("Categoria:", self.categoria_combo)
        form_layout.addRow("Descrição (opcional):", self.descricao_edit)
        form_layout.addRow("Valor:", self.valor_edit)
        
        layout.addLayout(form_layout)

        opcoes_layout = QHBoxLayout()
        
        self.entrada_radio = QRadioButton("Entrada")
        self.saida_radio = QRadioButton("Saída")
        self.entrada_radio.setChecked(True)
        
        self.adicionar_btn = QPushButton("Adicionar")
        
        opcoes_layout.addWidget(self.entrada_radio)
        opcoes_layout.addWidget(self.saida_radio)
        opcoes_layout.addWidget(self.adicionar_btn)
        opcoes_layout.addStretch()
        
        layout.addLayout(opcoes_layout)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(['Data', 'Descrição', 'Valor', 'Tipo', 'Editar', 'Deletar'])
        layout.addWidget(self.tabela)

        self.tabela.setColumnWidth(0, 100)
        self.tabela.setColumnWidth(1, 200)
        self.tabela.setColumnWidth(2, 100)
        self.tabela.setColumnWidth(3, 80)
        self.tabela.setColumnWidth(4, 50)
        self.tabela.setColumnWidth(5, 50)

        self.total_entradas_label = QLabel("Total de Entradas: R$ 0.00")
        self.total_saidas_label = QLabel("Total de Saídas: R$ 0.00")
        self.total_liquido_label = QLabel("Valor Líquido: R$ 0.00")
        layout.addWidget(self.total_entradas_label)
        layout.addWidget(self.total_saidas_label)
        layout.addWidget(self.total_liquido_label)

        botoes_layout = QHBoxLayout()
        self.gerar_relatorio_btn = QPushButton("Gerar Relatório")
        self.gerar_analise_btn = QPushButton("Gerar Análise de Dados")
        botoes_layout.addWidget(self.gerar_relatorio_btn)
        botoes_layout.addWidget(self.gerar_analise_btn)
        layout.addLayout(botoes_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.adicionar_btn.clicked.connect(self.adicionar_transacao)
        self.gerar_relatorio_btn.clicked.connect(self.gerar_relatorio)
        self.gerar_analise_btn.clicked.connect(self.gerar_analise_dados)

        self.atualizar_tabela()
        self.atualizar_totais()

    def adicionar_transacao(self):
        data = self.data_edit.date().toPyDate()
        categoria = self.categoria_combo.currentText()
        descricao_adicional = self.descricao_edit.text()
        descricao = categoria if not descricao_adicional else f"{categoria} - {descricao_adicional}"
        try:
            valor = float(self.valor_edit.text().replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, "Erro", "Por favor, insira um valor numérico válido.")
            return
        tipo = "Entrada" if self.entrada_radio.isChecked() else "Saída"

        self.controle_financas.adicionar_transacao(data, descricao, valor, tipo)
        self.atualizar_tabela()
        self.atualizar_totais()
        self.limpar_campos()

    def atualizar_tabela(self):
        self.tabela.setRowCount(0)
        for transacao in self.controle_financas.obter_todas_transacoes():
            row_position = self.tabela.rowCount()
            self.tabela.insertRow(row_position)
            
            data = transacao[1]
            if isinstance(data, str):
                data = datetime.strptime(data, "%Y-%m-%d").date()
            self.tabela.setItem(row_position, 0, QTableWidgetItem(data.strftime("%d/%m/%Y")))
            
            self.tabela.setItem(row_position, 1, QTableWidgetItem(str(transacao[2])))
            self.tabela.setItem(row_position, 2, QTableWidgetItem(f"R$ {float(transacao[3]):.2f}"))
            self.tabela.setItem(row_position, 3, QTableWidgetItem(str(transacao[4])))
            
            editar_widget = QWidget()
            editar_layout = QHBoxLayout(editar_widget)
            editar_layout.setContentsMargins(0, 0, 0, 0)
            editar_layout.setAlignment(Qt.AlignCenter)
            
            deletar_widget = QWidget()
            deletar_layout = QHBoxLayout(deletar_widget)
            deletar_layout.setContentsMargins(0, 0, 0, 0)
            deletar_layout.setAlignment(Qt.AlignCenter)
            
            editar_btn = QPushButton()
            editar_btn.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
            editar_btn.setIconSize(QSize(16, 16))
            editar_btn.setFixedSize(24, 24)
            editar_btn.setStyleSheet("background-color: transparent; border: none;")
            
            deletar_btn = QPushButton()
            deletar_btn.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
            deletar_btn.setIconSize(QSize(16, 16))
            deletar_btn.setFixedSize(24, 24)
            deletar_btn.setStyleSheet("background-color: transparent; border: none;")
            
            editar_btn.clicked.connect(lambda _, id=transacao[0]: self.editar_transacao(id))
            deletar_btn.clicked.connect(lambda _, id=transacao[0]: self.deletar_transacao(id))
            
            editar_layout.addWidget(editar_btn)
            deletar_layout.addWidget(deletar_btn)
            
            self.tabela.setCellWidget(row_position, 4, editar_widget)
            self.tabela.setCellWidget(row_position, 5, deletar_widget)

        self.tabela.resizeRowsToContents()

    def editar_transacao(self, id_transacao):
        transacao = self.controle_financas.obter_transacao(id_transacao)
        if transacao:
            dialog = EditarTransacaoDialog(transacao, self)
            if dialog.exec_() == QDialog.Accepted:
                nova_data = dialog.data_edit.date().toPyDate()
                nova_categoria = dialog.categoria_combo.currentText()
                nova_descricao_adicional = dialog.descricao_edit.text()
                nova_descricao = nova_categoria if not nova_descricao_adicional else f"{nova_categoria} - {nova_descricao_adicional}"
                novo_valor = float(dialog.valor_edit.text().replace(',', '.'))
                novo_tipo = "Entrada" if dialog.entrada_radio.isChecked() else "Saída"
                
                self.controle_financas.atualizar_transacao(id_transacao, nova_data, nova_descricao, novo_valor, novo_tipo)
                self.atualizar_tabela()
                self.atualizar_totais()

    def deletar_transacao(self, id_transacao):
        resposta = QMessageBox.question(self, 'Confirmar Exclusão', 
                                        'Tem certeza que deseja excluir esta transação?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            self.controle_financas.deletar_transacao(id_transacao)
            self.atualizar_tabela()
            self.atualizar_totais()

    def atualizar_totais(self):
        total_entradas, total_saidas = self.controle_financas.calcular_totais()
        total_liquido = total_entradas - total_saidas
        self.total_entradas_label.setText(f"Total de Entradas: R$ {total_entradas:.2f}")
        self.total_saidas_label.setText(f"Total de Saídas: R$ {total_saidas:.2f}")
        self.total_liquido_label.setText(f"Valor Líquido: R$ {total_liquido:.2f}")

    def limpar_campos(self):
        self.data_edit.setDate(QDate.currentDate())
        self.categoria_combo.setCurrentIndex(0)
        self.descricao_edit.clear()
        self.valor_edit.clear()
        self.entrada_radio.setChecked(True)

    def gerar_relatorio(self):
        dialog = SelecionarDataDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data_inicio = dialog.data_inicio.date().toPyDate()
            data_fim = dialog.data_fim.date().toPyDate()
            
            opcoes = QFileDialog.Options()
            nome_arquivo, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório", "", "PDF Files (*.pdf)", options=opcoes)
            if nome_arquivo:
                if not nome_arquivo.endswith('.pdf'):
                    nome_arquivo += '.pdf'
                
                self.criar_relatorio_pdf(nome_arquivo, data_inicio, data_fim)
                QMessageBox.information(self, "Sucesso", f"Relatório gerado com sucesso: {nome_arquivo}")

    def criar_relatorio_pdf(self, nome_arquivo, data_inicio, data_fim):
        doc = SimpleDocTemplate(nome_arquivo, pagesize=letter)
        elementos = []

        styles = getSampleStyleSheet()
        elementos.append(Paragraph("Relatório Financeiro", styles['Title']))
        elementos.append(Paragraph(f"Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}", styles['Normal']))
        elementos.append(Spacer(1, 12))

        transacoes = self.controle_financas.obter_transacoes_periodo(data_inicio, data_fim)
        dados = [['Data', 'Descrição', 'Valor', 'Tipo']]
        for transacao in transacoes:
            data = transacao[1]
            if isinstance(data, str):
                data = datetime.strptime(data, "%Y-%m-%d").date()
            dados.append([
                data.strftime("%d/%m/%Y"),
                transacao[2],
                f"R$ {transacao[3]:.2f}",
                transacao[4]
            ])

        tabela = Table(dados)
        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        for i in range(1, len(dados)):
            if dados[i][3] == "Saída":
                estilo.add('TEXTCOLOR', (2, i), (2, i), colors.red)

        tabela.setStyle(estilo)
        elementos.append(tabela)

        total_entradas, total_saidas = self.controle_financas.calcular_totais_periodo(data_inicio, data_fim)
        total_liquido = total_entradas - total_saidas

        elementos.append(Spacer(1, 12))
        elementos.append(Paragraph(f"Total de Entradas: R$ {total_entradas:.2f}", styles['Normal']))
        
        estilo_saida = ParagraphStyle('SaidaStyle', parent=styles['Normal'], textColor=colors.red)
        elementos.append(Paragraph(f"Total de Saídas: R$ {total_saidas:.2f}", estilo_saida))
        
        cor_liquido = colors.red if total_liquido < 0 else colors.green
        estilo_liquido = ParagraphStyle('LiquidoStyle', parent=styles['Normal'], textColor=cor_liquido)
        elementos.append(Paragraph(f"Valor Líquido: R$ {total_liquido:.2f}", estilo_liquido))

        doc.build(elementos)

    def gerar_analise_dados(self):
        pdf_filename = "analise_dados.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Título principal
        story.append(Paragraph("Análise de Dados Financeiros", styles['Title']))
        story.append(Spacer(1, 0.2*inch))

        # Gastos por Categoria
        story.append(Paragraph("Gastos por Categoria", styles['Heading2']))
        story.append(self.get_image(self.analise_dados.gastos_por_categoria, width=5*inch, height=3*inch))
        story.append(Spacer(1, 0.2*inch))

        # Tendências de Receitas e Despesas
        story.append(Paragraph("Tendências de Receitas e Despesas", styles['Heading2']))
        story.append(self.get_image(self.analise_dados.tendencias_receitas_despesas, width=5*inch, height=3*inch))

        # Forçar quebra de página
        story.append(PageBreak())

        # Previsão de Gastos 
        story.append(Paragraph("Previsão de Gastos", styles['Heading2']))
        story.append(self.get_image(self.analise_dados.previsao_gastos, width=7*inch, height=5*inch))

        # Balanço mensal
        story.append(PageBreak())
        story.append(Paragraph("Balanço Mensal", styles['Heading2']))
        
        balanco = self.analise_dados.balanco_mensal()
        dados_balanco = [['Mês', 'Entrada', 'Saída', 'Saldo']]
        for _, row in balanco.iterrows():
            dados_balanco.append([
                row['mes'].strftime('%m/%y'),  # Formato mm/YY
                f"R$ {row.get('entrada', 0):.2f}",
                f"R$ {row.get('saída', 0):.2f}",
                f"R$ {row['saldo']:.2f}"
            ])
        
        tabela_balanco = Table(dados_balanco)
        tabela_balanco.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TEXTCOLOR', (2, 1), (2, -1), colors.red),  
            ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),  
        ]))
        story.append(tabela_balanco)

        doc.build(story)
        print(f"Análise de dados gerada em {pdf_filename}")
        QMessageBox.information(self, "Sucesso", f"Análise de dados gerada em {pdf_filename}")

    def get_image(self, plot_function, width, height):
        fig = plot_function()
        img_data = io.BytesIO()
        fig.savefig(img_data, format='png', dpi=300, bbox_inches='tight')
        img_data.seek(0)
        img = Image(img_data, width=width, height=height)
        plt.close(fig)
        return img

class EditarTransacaoDialog(QDialog):
    def __init__(self, transacao, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Transação")
        self.transacao = transacao
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        self.data_edit = QDateEdit(calendarPopup=True)
        self.data_edit.setDate(QDate.fromString(self.transacao[1], "yyyy-MM-dd"))
        
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(["Uber", "99", "Combustível", "Manutenção", 
                                       "IPVA/Licenciamento", "Multa", "Seguro", "Outros"])
        
        descricao_partes = self.transacao[2].split(" - ", 1)
        categoria = descricao_partes[0]
        descricao_adicional = descricao_partes[1] if len(descricao_partes) > 1 else ""
        
        self.categoria_combo.setCurrentText(categoria)
        self.descricao_edit = QLineEdit(descricao_adicional)
        self.valor_edit = QLineEdit(str(self.transacao[3]))
        
        self.entrada_radio = QRadioButton("Entrada")
        self.saida_radio = QRadioButton("Saída")
        if self.transacao[4] == "Entrada":
            self.entrada_radio.setChecked(True)
        else:
            self.saida_radio.setChecked(True)

        layout.addRow("Data:", self.data_edit)
        layout.addRow("Categoria:", self.categoria_combo)
        layout.addRow("Descrição (opcional):", self.descricao_edit)
        layout.addRow("Valor:", self.valor_edit)
        layout.addRow("Tipo:", self.entrada_radio)
        layout.addRow("", self.saida_radio)

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botoes.accepted.connect(self.accept)
        botoes.rejected.connect(self.reject)
        layout.addRow(botoes)
