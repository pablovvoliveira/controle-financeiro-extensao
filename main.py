import sys
from PyQt5.QtWidgets import QApplication
from interface_usuario import InterfaceUsuario
from controle_financas import ControleFinancas
from database import DatabaseManager
from analise_dados import AnaliseDados

def main():
    app = QApplication(sys.argv)
    
    db_manager = DatabaseManager('financas.db')
    controle = ControleFinancas(db_manager)
    analise_dados = AnaliseDados(db_manager)  
    
    window = InterfaceUsuario(controle, analise_dados)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()