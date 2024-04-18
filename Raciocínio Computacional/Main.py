#Luis Felipe Kryzozun Correa - Análise e Desenvolvimento de sistemas - Raciocínio Computacional - Formativa 5
import json;
import os;
import pickle;
import uuid
from dataclasses import dataclass

@dataclass
class Estudantes:
    codigo:int
    nome:str
    cpf:str

#Dicionário de opções do menu principal
ListEntitys = {
    1: "Estudantes",
    2: "Professores",
    3: "Disciplinas",
    4: "Turmas",
    5: "Matrículas",
    9: "Sair"
}

#Dicionário de opções do menu secundário
ListFunctions = {
    1: "Incluir",
    2: "Listar",
    3: "Atualizar",
    4: "Excluir",
    9: "Voltar"
}

#Método para pegar input do usuário
def GetOption(Text=''):
    if Text=='':Text="Seleciona uma opção e pressione 'Enter' para confirmar\n"
    num=input(Text)
    if num!="": return int(num)

#Método para pegar string até definido índice
def LeftStr(str, index):
    if index<=len(str):
        return str[0:index]

#Método para pegar o nome da entidade sem o S no final
def GetEntityName(number):
    Name=ListEntitys.get(number)
    return LeftStr(Name,len(Name)-1)

#Método de definição da estrutura da entidade
def DefEstrEntity(Entity):
    match Entity:
        case 1:
            Name = input("Digite o nome do(a) aluno e pressione 'Enter' para confirmar\n")
            CPF = input("Digite o cpf do(a) aluno e pressione 'Enter' para confirmar\n")
            Estr= {"Codigo":int(uuid.uuid1()),"Nome":Name, "Cpf":CPF,"Status":True}
        case 2:
            Estr
        case 3:
            Estr
        case 4:
            Estr
    return json.dumps(Estr)


#Método para pega o nome da função do menu
def GetFunctionName(number):
    return ListFunctions.get(number)

#Método para exibir menu principal
def PrintMenuPrincipal():
    print("-"*10+' Menu Principal '+'-'*10)
    for entity in ListEntitys:
        print(' '*2 + str(entity) +' - '+ ListEntitys[entity])
    print("-"*36)

#Método para exibir menu secundário
def PrintMenuSecundario(Entity):
    if ValidFunction(Entity):
        if Entity!=9:
            MenuName=GetEntityName(Entity)
            print("-"*10+' Menu de '+MenuName+'s '+'-'*10)
            for function in ListFunctions:
                print(' '*2 + str(function) +' - '+ ListFunctions[function])
            print("-"*(29+len(MenuName)))
        else:
            print("Finalizando o sistema!")
    else:
        print("!!! Selecione uma opção válida !!!")

#Validando se a função informada existe
def ValidFunction(Function):
    return Function in ListFunctions

#Validando se a entidade informada existe
def ValidEntity(Entity):
    return Entity in ListEntitys

#Método de inserção nas listas de cada Entidade
def Insert(Entity):
    Path=GetPath(Entity)
    Name=GetEntityName(Entity)
    List=GetListEntity(Entity)
    List.append(DefEstrEntity(Entity))

    with open(Path, "w") as Arquivo:
        json.dump(List, Arquivo)
        Arquivo.close()
    print(Name +" inserido com sucesso!")

def GetPath(Entity):
    EntityName=GetEntityName(Entity)
    Path="Data/"+EntityName.lower()+"s.json"
    return Path


#Método para achar a lista certa para CRUD
def GetListEntity(Entity):
    Path=GetPath(Entity)
    if not os.path.exists(Path):
        with open(Path, "w") as arquivo:
            json.dump([], arquivo)
            arquivo.close()
    with open(Path, "r") as arquivo:
        List=json.load(arquivo)
        arquivo.close()
    return List

#Método para retornar a estrutura cadastral das entidades
def GetEstrEntity(EntityType, E):
    match EntityType:
        case 1:
            StrEntity=str(E["Codigo"]) + " | " + E["Nome"] + " | " + E["Cpf"]+ " | " + str(E["Status"])
        case 2:
            StrEntity=str(E["Codigo"]) + " | " + E["Nome"] + " | " + E["Cpf"]+ " | " + str(E["Status"])
        case 3:
            StrEntity=str(E["Codigo"]) + " | " + E["Nome"] + " | " + E["Cpf"]+ " | " + str(E["Status"])
        case 4:
            StrEntity=str(E["Codigo"]) + " | " + E["Nome"] + " | " + E["Cpf"]+ " | " + str(E["Status"])
        case _:
            print("Entidade não encontrada!")
            exit()
    return StrEntity


#Método para mostrar o Header da listagem
def HeaderEntity(Entity):
    List=GetListEntity(Entity)
    print(" ")
    Cabecalho = "-" * 10 + " Lista de " + GetEntityName(Entity) + "s " + "-" * 10
    print(Cabecalho)
    i = 0
    Infos="";
    for key in json.loads(List[0]).keys():
        Infos=Infos+key+5*" "+" | "
    print(Infos)
    print(" ")
    return Cabecalho

#Método para listar todas as entidades
def ReadAll(TypeEntity):
    List=GetListEntity(TypeEntity)
    if len(List)>0:
        Cabecalho=HeaderEntity(TypeEntity)
        for Entity in List:
            Entity=json.loads(Entity)
            if Entity["Status"]:
                print(GetEstrEntity(TypeEntity,Entity))
        print(" ")
        print("-" * len(Cabecalho));
        print(" ")
    else:
        print("Nenhum(a) " + GetEntityName(Entity) + " cadastrado(a)!")

#Método para listar a Entidade selecionada
def ReadOne(TypeEntity,show=False):
    List=GetListEntity(TypeEntity)
    EntityName=GetEntityName(TypeEntity)
    id=int(input("Digite o código do(a) "+EntityName+":\n"))
    if len(List)>0:
        for item in List:
            item=json.loads(item)
            if int(item["Codigo"])==id:
                Entity=item
                if show:
                    HeaderEntity(TypeEntity)
                    print(GetEstrEntity(TypeEntity,Entity))
                    print(" ")
                break
        if Entity=="":
            print("Codigo '"+str(id)+"' não encontrado(a) na lista de "+EntityName+"s")
        return Entity
    else:
        print("Nenhum(a) " + EntityName + " cadastrado(a)!")

#Método para verificar se o usuário deseja listar todos ou uma entidade específica
def RedirectRead(Entity):
    Confirma=input("Deseja listar todos? (S/N)\n")
    if Confirma.upper()=="S":
        ReadAll(Entity)
    else:
        ReadOne(Entity, True)

#Método para atualizar entidades
def Update(EntityType):
    Entity=ReadOne(EntityType)
    EntityName=GetEntityName(EntityType)
    if Entity!=None:
        Confirma=input("Deseja alterar o(a) "+EntityName+" '"+Entity["Nome"]+"'? (S/N)\n")
        if Confirma.upper()=="S":
            List=GetListEntity(EntityType)
            for key in List[0].keys():
                if key!="Codigo":
                    Confirma=input("Deseja alterar o "+key+"? (S/N/X)\n")
                    if Confirma.upper()=="S":
                        NewValue=input("Digite o novo valor para o "+key+"\n")
                        Entity[key]=NewValue
                    elif Confirma.upper()=="X":
                        print("O processo foi encerrado e as informações alteradas foram salvas")
                        break
            print(EntityName+" alterado(a) com sucesso!")
            print(" ")
        else:
            print("Saindo da edição...")

#Método para "excluir" entidades
def Delete(EntityType):
    List=GetListEntity(EntityType)
    Entity=ReadOne(EntityType)
    EntityName=GetEntityName(EntityType)
    if Entity!=None:
        Confirma=input("Deseja remover o(a) "+EntityName+" '"+Entity["Nome"]+"'? (S/N)\n")
        if Confirma.upper()=="S":
            Entity["Status"]=False;
            print(EntityName+" '"+ Entity["Nome"]+"' foi removido, porém ainda estará visível na consulta por código.")

#Método de redirecionamento de CRUD
def Crud(Entity, Function):
    if Function==1:Insert(Entity)
    elif Function==2:RedirectRead(Entity)
    elif Function==3:Update(Entity)
    elif Function==4:Delete(Entity)

#Método para inicialização do sistema
def init():
    teste= Teste()
    teste.SetTeste(input("teste"))
    print(teste.GetTeste())
    while True:
        PrintMenuPrincipal()
        OptionEntity=GetOption();
        if ValidEntity(OptionEntity):
            if OptionEntity!=9:
                while True:
                    if OptionEntity==1:
                        PrintMenuSecundario(OptionEntity)
                        OptionFunction=GetOption();
                        if ValidFunction(OptionFunction):
                            if OptionFunction!=9:
                                Crud(OptionEntity, OptionFunction)
                            else:
                                break
                        else:
                            print("!!! Selecione uma opção válida !!!")
                    else:
                        print("Em desenvolvimento")
                        break
            else:
                print("Finalizando sistema...")
                break
        else:
            print("!!! Selecione uma opção válida !!!")

init()