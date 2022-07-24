from flask import Flask, request, json, session
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

USUARIOS = {
    'jose':'jose',
    'william':'william',
}

lista_tarefas = [
    {   'id':0, 
        'responsavel':'José', 
        'tarefa':'Construir app API', 
        'status':'em processo'
    },
    {   'id':1, 
        'responsavel':'William', 
        'tarefa':'Construir front-end', 
        'status':'pausado'
    }
]

@auth.verify_password
def verificacao(login, senha):
    print('Validando usuario:')
    print(USUARIOS.get(login) == senha)
    if not (login, senha):
        return false 
    return USUARIOS.get(login) == senha


class ListaTarefas(Resource):
    def get(self):
        return lista_tarefas
    
    
    @auth.login_required
    def post(self):    
        dados = json.loads(request.data)
        posicao = len(lista_tarefas)
        dados['id'] = posicao
        lista_tarefas.append(dados)
        return lista_tarefas[posicao]



class Tarefa(Resource):
    def get(self, id):
        try:
            response = lista_tarefas[id]
        except IndexError:
            mensagem = "Tarefa com ID {} não existe!".format(id)
            response = {"status": "erro", "mensagem": mensagem }
        except Exception:
            mensagem = "Erro desconhecido. Procure o administrador da API!"
            response = {"status": "erro", "mensagem": mensagem }
        return response

    @auth.login_required
    def put(self, id):
        dados = json.loads(request.data)
        lista_tarefas[id] = dados
        return dados
    
    @auth.login_required
    def delete(self, id):
        lista_tarefas.pop(id)
        return {'status':'Sucesso', 'mensagem':'Registro excluído'}


api.add_resource(ListaTarefas, "/tarefas")
api.add_resource(Tarefa,"/tarefas/<int:id>")


if __name__=='__main__':
    app.run()
