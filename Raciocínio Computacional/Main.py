#Luis Felipe Kryzozun Correa - Análise e Desenvolvimento de sistemas - Raciocínio Computacional - Somativa Final
import json
import os
import uuid
from dataclasses import dataclass

#Dicionário de opções do menu principal
ListEntitys = {
    1: "Estudantes",
    2: "Professores",
    3: "Disciplinas",
    4: "Turmas",
    5: "Matrículas",
}

#Dicionário de opções do menu secundário
ListFunctions = {
    1: "Incluir",
    2: "Listar",
    3: "Atualizar",
    4: "Excluir",
}

#Classe genérica para herança de funções comuns a todas as entidades
@dataclass
class Entity():
    def toString(self, header=False):
        result='';
        if (not header):
            for attribute in self.__dict__:
                value=self.__getattribute__(attribute)
                result=result+str(value)+ " | "
        else:
            for attribute in self.__dict__:
                result = result+str(attribute).upper()+" | "

        return result


    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    def fromJSON(self,Entity):
        for attribute in self.__dict__:
            self.__setattr__(attribute,Entity[attribute])

#Classe de estudates
@dataclass
class Estudantes(Entity):
    ID:int=0
    nome:str=''
    cpf:str=''
    status:bool=True;

#Classe de professores
@dataclass
class Professores(Entity):
    ID:int=0
    nome:str=''
    cpf:str=''
    status:bool=True;

#Classe de disciplinas
@dataclass
class Disciplinas(Entity):
    ID:int=0
    nome:str=''
    status:bool=True;

#Classe de turmas
@dataclass
class Turmas(Entity):
    ID:int=0
    IDProfessor:int=0
    IDDisciplina:int=0
    status:bool=True;

#Classe de matriculas
@dataclass
class Matriculas(Entity):
    IDTurma:int=0
    IDEstudante:int=0
    status:bool=True;

#Classe genérica para interface de apresentação
@dataclass
class UI:
    #Método para exibir menu principal
    def PrintMenuPrincipal():
        print("-"*10+' Menu Principal '+'-'*10)
        for entity in ListEntitys:
            print(' '*2 + str(entity) +' - '+ ListEntitys[entity])
        print(' '*2 +'9 - Sair')
        print("-"*36)

    #Método para exibir menu secundário
    def PrintMenuSecundario(Entity):
        if Entity!=9:
            MenuName=Generics.GetEntityName(Entity)
            print("-"*10+' Menu de '+MenuName+'s '+'-'*10)
            for function in ListFunctions:
                print(' '*2 + str(function) +' - '+ ListFunctions[function])
            print(' '*2 +'9 - Voltar')
            print("-"*(29+len(MenuName)))
        else:
            print("Finalizando o sistema!")

    #Método para mostrar o cabeçalho da listagem
    def HeaderEntity(Entity):
        List=Data.GetListEntity(Entity)
        Cabecalho = "-" * 10 + " Lista de " + Generics.GetEntityName(Entity) + "s " + "-" * 10
        print(Cabecalho)
        i = 0
        Infos="";
        object=Generics.GetObject(Entity)
        print(object.toString(True))
        print(Infos)
        return Cabecalho


#Classe genérica para funções gerais
@dataclass
class Generics:

    #Método para retorno do objeto correto em relação ao númmero da entidade
    def GetObject(Entity):
        if Entity==1: object=Estudantes()
        elif Entity==2: object=Professores()
        elif Entity==3: object=Disciplinas()
        elif Entity==4: object=Turmas()
        elif Entity==5: object=Matriculas()
        return object

    #Método para pegar o nome da entidade sem o S no final
    def GetEntityName(number):
        Name=ListEntitys.get(number)
        return Generics.LeftStr(Name,len(Name)-1)

    #Método para pega o nome da função do menu
    def GetFunctionName(number):
        return ListFunctions.get(number)

    #Validando se a função informada existe
    def ValidFunction(Function):
        if Function==9:
            return True
        else:
            return Function in ListFunctions

    #Validando se a entidade informada existe
    def ValidEntity(Entity):
        if Entity==9:
            return True
        else:
            return Entity in ListEntitys

    #Método para pegar input do usuário
    def GetOption(Text=''):
        if Text=="":Text="Seleciona uma opção e pressione 'Enter' para confirmar\n"
        try:
            return int(input(Text))
        except:
            return "";
            print("Digite um valor válido")


    #Método para pegar string até definido índice
    def LeftStr(str, index):
        if index<=len(str):
            return str[0:index]

#Classe relacionada ao acesso dos dados
@dataclass
class Data:

    #Retornar informações da entidade
    def SetEstr(Entity):
        object=Generics.GetObject(Entity)
        entityName=Generics.GetEntityName(Entity)
        for attribute in object.__dict__:
            if attribute=='ID':
                object.__setattr__(attribute,int(uuid.uuid4()))
            elif attribute!='status':
                info=input("Digite o "+attribute+" do(a) "+entityName+"\n")
                object.__setattr__(attribute,info)
        return object.toJSON()

    #Método para achar o caminho do arquivo de dados
    def GetPath(Entity):
        EntityName=Generics.GetEntityName(Entity)
        Path="Data/"+EntityName.lower()+"s.json"
        return Path

    #Método para achar a lista certa para CRUD
    def GetListEntity(Entity):
        Path=Data.GetPath(Entity)
        if not os.path.exists(Path):
            with open(Path, "w") as arquivo:
                json.dump([], arquivo)
                arquivo.close()
        with open(Path, "r") as arquivo:
            List=json.load(arquivo)
            arquivo.close()
        return List

#Classe relacionada a operações de CRUD com os dados
class Crud:

    #Método para salvar os dados
    def Save(Path, List):
        with open(Path, "w") as Arquivo:
            json.dump(List, Arquivo)
            Arquivo.close()

    #Método de inserção nas listas de cada Entidade
    def Create(Entity):
        Path=Data.GetPath(Entity)
        Name=Generics.GetEntityName(Entity)
        List=Data.GetListEntity(Entity)
        List.append(Data.SetEstr(Entity))
        Crud.Save(Path, List);
        print(Name +" inserido com sucesso!")

    #Método para listar todas as entidades
    def ReadAll(TypeEntity):
        List=Data.GetListEntity(TypeEntity)
        if len(List)>0:
            Cabecalho=UI.HeaderEntity(TypeEntity)
            for Entity in List:
                Entity=json.loads(Entity)
                if Entity["status"]==True:
                    object=Generics.GetObject(TypeEntity);
                    object.fromJSON(Entity);
                    print(object.toString())
            print(" ")
            print("-" * len(Cabecalho));
            print(" ")
        else:
            print("Nenhum(a) " + Generics.GetEntityName(TypeEntity) + " cadastrado(a)!")

    #Método para listar a Entidade selecionada
    def ReadOne(TypeEntity,show=False):
        List=Data.GetListEntity(TypeEntity)
        EntityName=Generics.GetEntityName(TypeEntity)
        try:
            id=int(input("Digite o código do(a) "+EntityName+":\n"))
        except:
            print("Digite um valor válido")
            exit()
        object=''
        Entity=''
        if len(List)>0:
            for item in List:
                Entity=json.loads(item)
                if int(Entity["ID"])==id:
                    object = Generics.GetObject(TypeEntity)
                    object.fromJSON(Entity)
                    if show:
                        UI.HeaderEntity(TypeEntity)
                        print(object.toString())
                        print(" ")
                    break
            if Entity=="":
                print("Codigo '"+str(id)+"' não encontrado(a) na lista de "+EntityName+"s")
            return object
        else:
            print("Nenhum(a) " + EntityName + " cadastrado(a)!")

    #Método para verificar se o usuário deseja listar todos ou uma entidade específica
    def RedirectRead(Entity):
        entityName=Generics.GetEntityName(Entity)
        print("---------- Listar "+entityName+"s ----------")
        print("  1 - Listar todos")
        print("  2 - Listar um")
        print("  3 - Voltar")
        print("--------------------")
        Confirma=int(input("Selecione uma das opções acima:\n").strip())
        if Confirma==1:
            Crud.ReadAll(Entity)
        elif Confirma==2:
            Crud.ReadOne(Entity, True)
        elif Confirma==3:
            print("Retornando ao menu principal...")
        else:
            print("Digite um valor válido")

    #Método para atualizar entidades
    def Update(EntityType):
        Entity=Crud.ReadOne(EntityType)
        EntityName=Generics.GetEntityName(EntityType)
        if Entity!=None:
            Confirma=input("Deseja alterar o(a) "+EntityName+" '"+Entity.nome+"'? (S/N)\n")
            if Confirma.upper()=="S":
                List=Data.GetListEntity(EntityType)
                List.remove(Entity.toJSON())
                for attribute in Entity.__dict__:
                    if attribute!="ID" and attribute!="status":
                        Confirma=input("Deseja alterar o "+attribute+"? (S/N/X)\n")
                        if Confirma.upper()=="S":
                            NewValue=input("Digite o novo valor para o "+attribute+"\n")
                            Entity.__setattr__(attribute, NewValue)
                        elif Confirma.upper()=="X":
                            print("O processo foi encerrado e as informações alteradas foram salvas")
                            break
                List.append(Entity.toJSON())
                Path = Data.GetPath(EntityType)
                Crud.Save(Path, List)
                print(EntityName+" alterado(a) com sucesso!")
                print(" ")
            else:
                print("Saindo da edição...")

    #Método para "excluir" entidades
    def Delete(EntityType):
        Entity=Crud.ReadOne(EntityType)
        if Entity!=None:
            EntityName=Generics.GetEntityName(EntityType)
            List=Data.GetListEntity(EntityType)
            Confirma=input("Confirma a exclusão? (S/N)\n")
            if Confirma.upper().strip()=="S":
                List.remove(Entity.toJSON())
                Entity.status=False;
                List.append(Entity.toJSON())
                Path=Data.GetPath(EntityType)
                Crud.Save(Path, List)
                print(EntityName+" removido(a), porém ainda estará visível na consulta por código.")

    #Método de redirecionamento de CRUD
    def Set(Entity, Function):
        if Function==1:Crud.Create(Entity)
        elif Function==2:Crud.RedirectRead(Entity)
        elif Function==3:Crud.Update(Entity)
        elif Function==4:Crud.Delete(Entity)


#Método para inicialização do sistema
def init():
    while True:
        UI.PrintMenuPrincipal()
        OptionEntity=Generics.GetOption();
        if Generics.ValidEntity(OptionEntity):
            if OptionEntity!=9:
                while True:
                    UI.PrintMenuSecundario(OptionEntity)
                    OptionFunction=Generics.GetOption();
                    if Generics.ValidFunction(OptionFunction):
                        if OptionFunction!=9:
                            Crud.Set(OptionEntity, OptionFunction)
                        else:
                            break
                    else:
                        print("!!! Selecione uma opção válida !!!")
            else:
                print("Finalizando sistema...")
                break
        else:
            print("!!! Selecione uma opção válida !!!")
    exit()

init()