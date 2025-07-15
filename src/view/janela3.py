# Necessário para realizar import em python
import sys
import time
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# importando os módulos de controle
from controler.itemControler import ItemControler

# importando o modelo de dados do item
from model.item import Item 

class Janela3:
    """
    View para o usuário efetuar o cadastro dos itens
    """
    
    @staticmethod
    def mostrar_janela3(database_name: str) -> None:
        """
        Coleta os dados dos itens, faz a validação e o insere no BD
        """
        print('---------- Cadastrar Novo Item no Cardápio ----------\n')

        while True:
            nome = input("Nome do item: ").strip().capitalize()
            if nome: 
                break
            else:
                print("Entrada inválida. O nome do item não pode ser vazio.")

        # -> como é uma pizzaria, não deve fugir muito do escopo padrão de categoria de itens
        categorias = {1: 'Pizza', 2: 'Bebida', 3: 'Sobremesa', 4: 'Outro'}
        print("\nSelecione a categoria:")
        for num, cat_nome in categorias.items():
            print(f"{num} - {cat_nome}")
        
        while True:
            try:
                escolha_cat = int(input("Escolha o número da categoria: "))
                if escolha_cat in categorias:
                    tipo = categorias[escolha_cat]
                    break
                else:
                    print("Opção inválida. Por favor, escolha um número da lista.")
            except ValueError:
                print("Entrada inválida. Por favor, digite apenas o número da categoria.")

        while True:
            try:
                # -> o replace garante uma flexibilidade maior na escrita do preço
                preco = float(input("Preço do item (ex: 25.50): ").replace(',', '.').strip())
                if preco > 0:
                    break
                else:
                    print("Entrada inválida. O preço deve ser um número maior que zero.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um valor numérico para o preço.")

        while True:
            descricao = input("Descrição do item: ").strip().capitalize()
            if descricao: 
                break
            else:
                print("Entrada inválida. A descrição não pode ser vazia.")

        try:
            # -> criando uma instância de Item
            novo_item = Item(nome=nome, preco=preco, tipo=tipo, descricao=descricao)
            
            # -> inserindo o item novo no BD
            sucesso = ItemControler.insert_into_item(database_name, novo_item)
            
            if sucesso:
                print(f'\nSUCESSO! O item "{nome}" foi cadastrado no cardápio.')
            else:
                print(f'\nERRO! Não foi possível cadastrar o item "{nome}". Verifique se o item já existe.')

        except Exception as e:
            print(f"\nOcorreu um erro inesperado durante o cadastro: {e}")
            
        print("\nRetornando ao menu principal...")
        time.sleep(2)