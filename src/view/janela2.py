#Necessário para realizar import em python
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from controler.pedidoControler import PedidoControler
from controler.itemControler import ItemControler

class Janela2:
    @staticmethod
    def mostrar_janela2(database_name:str):
        faturamento = 0
        print('------Pesquisar Pedido--------')

        while True: # -> garante uma validação efetiva 
            try:
                q = int(input('1-Buscar Pedido Unico\n2-Listar Todos os Pedidos\n3-Atualizar Estado de um Pedido\nDigite sua escolha: '))
                if q in [1, 2, 3]:
                    break
                else:
                    print('Opção inválida. Por favor, digite 1, 2 ou 3.')
            except ValueError:
                print('Entrada inválida. Por favor, digite um número que corresponde a uma opção.')

        if q==1:

            try:
                indice = int(input('Digite o número do pedido: '))
            except ValueError:
                print('Entrada inválida. Digite um número INTEIRO para acessar o pedido. Retornando ao menu.')
                return 

            # -> verificando se o pedido existe
            informacoes_pedido = PedidoControler.search_in_pedidos_id(database_name, indice)
            
            if not informacoes_pedido:
                print(f'Pedido com número {indice} não encontrado.')
                return

            informacoes_pedido = informacoes_pedido[0]
            resume = ItemControler.search_into_itens_pedidos_id(database_name, indice)
            quantidade_itens = len(resume)
            exibir_tela = ''
            
            for elem in resume:
                exibir_tela+=f'Tipo: {elem[2]}| Sabor: {elem[0]}| Descricao: {elem[3]}| R$ {elem[1]}|\n'
            
            print(f'\nResumo do pedido {indice}: \n{exibir_tela}\nItens: {quantidade_itens}\n')
            print(f'Status: {informacoes_pedido[1]}\nDelivery: {informacoes_pedido[2]}\nEndereco: {informacoes_pedido[3]}\nData: {informacoes_pedido[4]}\nR$ {informacoes_pedido[5]}')
            print('\nVoltando ao menu inicial...\n')

        elif q==2:

            row = PedidoControler.search_in_pedidos_all(database_name)
            faturamento = 0
            exibir_tela = ''
            i=1
            
            for elem in row:
                endereco_raw = elem.endereco
                if isinstance(endereco_raw, (tuple, list)):
                    endereco_raw = endereco_raw[0]
                faturamento+=elem.valor_total
                endereco = endereco_raw or 'Nao informado'
                exibir_tela+= f'Nº: {i}| Status: {elem.status}| Delivery: {elem.delivery}| Endereco: {endereco}| Valor: R$ {elem.valor_total} \n'
                i+=1
            print(f'\nPedidos \n\n{exibir_tela}')
            print(f'Faturamento Total: R$ {faturamento:.2f}')

        elif q==3:

            try:
                indice = int(input('Digite o número do pedido que deseja atualizar: '))
            except ValueError:
                print('Entrada inválida. Digite um número inteiro para se referir ao pedido. Retornando ao menu.')
                return

            # -> verifica a existência do pedido
            if not PedidoControler.search_in_pedidos_id(database_name, indice):
                 print(f'Pedido com número {indice} não encontrado.')
                 return
            
            while True:
                try:
                    novo_status_aux = int(input('Novo status: 1-Preparo, 2-Pronto, 3-Entregue: '))
                    if novo_status_aux in [1, 2, 3]:
                        break
                    else:
                        print('Status inválido. Por favor, digite 1, 2 ou 3.')
                except ValueError:
                    print('Entrada inválida. Por favor, digite um número para o status.')
            
            # -> atualizando pedido no BD
            result = PedidoControler.update_pedido_status_id(database_name, indice, novo_status_aux)
            if result:
                print(f'Status do Pedido {indice} atualizado com sucesso!')
            else:
                print('Erro ao atualizar o status do pedido.')