#para pegar a data de hoje
from datetime import date
import time

#Necessário para realizar import em python
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

#importando os módulos de model
from model.pedido import Pedido

#importando os módulos de controle
from controler.pedidoControler import PedidoControler
from controler.itemControler import ItemControler

#criação da classe janela
class Janela1:
    
    @staticmethod
    def mostrar_janela1(database_name: str) -> None:
        """
        View para o usuário utilizar o software
        
        return None
        """
        
        menu = ItemControler.mostrar_itens_menu(database_name)
        
        print('----------Menu----------\n')
        
        # 1. Ajustando a exbição do menu de cadastro.
        # print(f'{menu} \n') -> antigo
        
        for item_id, nome, preco, tipo, descricao in menu: 
            print(f"{item_id} -> {nome.capitalize()} - R$ {preco:.2f} <-> Tipo: {tipo.capitalize()} - Descrição: {descricao.title()}")
        print('\n')
        
        # 2. Ajustando a lógica do "y" e "n" e padronizando para (sim/nao)
        # a = 'y'
        # while a=='y': -> Basta utilizar um while True

        while True: # -> esse laço while garante uma resposta efetiva do usuário e previne possíveis erros de digitação
            a = str(input('Cadastrar pedido (sim/nao): ')).lower().strip()
            if a in ['sim', 'nao', 'não']:
                break
            else:
                print('Entrada inválida. Por favor, digite "sim" para cadastrar ou "nao" para voltar ao menu.')
        
        if a=='sim':
            print('----------Cadastrar pedido----------\n')
            lista_itens = []
            valor_total=0
            pedidos = PedidoControler.search_in_pedidos_all(database_name)
            numero_pedido = len(pedidos)+1
            
            while True:
                try:
                    item = int(input('Numero do item: '))
                    quantidade = int(input('Quantidade: '))
                except ValueError:
                    print('Entrada inválida. Por favor, digite um número INTEIRO para o item e a quantidade.')
                    continue
                
                #calculando em tempo de execução o valor do pedido
                valor_item_data = ItemControler.valor_item(database_name, item)
                if valor_item_data and len(valor_item_data) > 0: # -> verificação para garantir a existência do item
                    valor_unitario = valor_item_data[0][0]
                    custo_item_atual = valor_unitario * quantidade
                    print(f"Custo do item adicionado: R$ {custo_item_atual:.2f}") # -> retorno do valor do item
                    valor_total += custo_item_atual
                else:
                    print("Item não encontrado. Por favor, digite o número de um item válido.")
                    continue
                
                for x in range(0,quantidade): #acrescentado o mesmo item várias vezes, de acordo com a quantidade
                    lista_itens.append((numero_pedido,item))
                
                # 3 -> Ajustando a lógica do "y" e "n" e padronizando para (sim/nao) novamente
                
                while True: # -> laço para validar respostas sobre adição de novos itens
                    adicionar = str(input('Adicionar novo item? (sim/nao): ')).lower().strip()
                    if adicionar in ['sim', 'nao', 'não']:
                        break
                    else:
                        print('Entrada inválida. Por favor, digite "sim" para adicionar outro item ou "nao" para o contrário.')
                if adicionar in ['nao', 'não']:
                    break
            
            print('\n----------Finalizar pedido----------\n')
            print(f'Numero do pedido: {numero_pedido}')
            
            while True: # -> laço que valida respostas sobre a necessidade do delivery
                delivery_aux = str(input('Delivery (sim/nao): ')).lower().strip()
                if delivery_aux=='sim':
                    delivery = True
                    break
                elif delivery_aux in ['nao', 'não']:
                    delivery = False
                    break
                else:
                    print('Entrada inválida. Por favor, digite "sim" caso queira delivery ou "nao" caso contrário.')
            
            endereco = '' 
            if delivery: 
                endereco = str(input('Endereco:'))
            else:
                endereco = "Nao informado" 
            
            # 4 -> ajustando lógica para salvar status do pedido, agora com validação efetiva
            # Problema recaía sobre a lógica antiga -> if-(if-else), que se mostrava errada e inconsistente

            while True: # -> laço para validar as respostas sobre o status do pedido
                try:
                    status_aux = int(input('Status: 1-Preparo, 2-Pronto, 3-Entregue: '))
                    if status_aux in [1, 2, 3]:
                        break
                    else:
                        print('Status inválido. Por favor, digite 1, 2 ou 3.')
                except ValueError:
                    print('Entrada inválida. Por favor, digite um número para o status.')

            if status_aux == 1:
                status = 'Preparo'
            elif status_aux == 2:
                status = 'Pronto'
            elif status_aux == 3:
                status = 'Entregue'

            # 5 -> campos tratados com mensagens que auxiliam o usuário em casos de digitações erradas

            print(f'Valor Final: R${valor_total}')
            data_hoje = date.today()
            data_formatada = data_hoje.strftime('%d/%m/%Y')
            print(data_formatada)
            print(endereco)
            pedido = Pedido(status, str(delivery), endereco,data_formatada,float(valor_total))
            PedidoControler.insert_into_pedidos(database_name,pedido)
            for elem in lista_itens:
                ItemControler.insert_into_itens_pedidos(database_name,elem)
            
        elif a in ['nao', 'não']:
            print('Voltando ao Menu inicial')
            time.sleep(2)