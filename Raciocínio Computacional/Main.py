#Luis Felipe Kryzozun Correa - Análise e Desenvolvimento de sistemas - Raciocínio Computacional - Formativa 5
import json;
import os;
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

@dataclass
class Estudantes(Entity):
    ID:int=0
    nome:str=''
    cpf:str=''
    status:bool=True;

@dataclass
class Professores(Entity):
    ID:int=0
    nome:str=''
    cpf:str=''
    status:bool=True;

@dataclass
class Disciplinas(Entity):
    ID:int=0
    nome:str=''
    status:bool=True;

@dataclass
class Turmas(Entity):
    ID:int=0
    IDProfessor:int=0
    IDDisciplina:int=0
    status:bool=True;

@dataclass
class Matrículas(Entity):
    IDTurma:int=0
    IDEstudante:int=0
    status:bool=True;

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
        if Generics.ValidFunction(Entity):
            if Entity!=9:
                MenuName=Generics.GetEntityName(Entity)
                print("-"*10+' Menu de '+MenuName+'s '+'-'*10)
                for function in ListFunctions:
                    print(' '*2 + str(function) +' - '+ ListFunctions[function])
                print(' '*2 +'9 - Voltar')
                print("-"*(29+len(MenuName)))
            else:
                print("Finalizando o sistema!")
        else:
            print("!!! Selecione uma opção válida !!!")

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


@dataclass
class Generics:

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
        return Function in ListFunctions

    #Validando se a entidade informada existe
    def ValidEntity(Entity):
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

class Crud:

    #Método de inserção nas listas de cada Entidade
    def Create(Entity):
        Path=Data.GetPath(Entity)
        Name=Generics.GetEntityName(Entity)
        List=Data.GetListEntity(Entity)
        List.append(Data.SetEstr(Entity))

        with open(Path, "w") as Arquivo:
            json.dump(List, Arquivo)
            Arquivo.close()
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
        if len(List)>0:
            for item in List:
                item=json.loads(item)
                if int(item["Codigo"])==id:
                    Entity=item
                    if show:
                        UI.HeaderEntity(TypeEntity)
                        print(Entity.ToString())
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
            Crud.ReadAll(Entity)
        elif Confirma.upper()=='N':
            Crud.ReadOne(Entity, True)
        else:
            print("Digite um valor válido")

    #Método para atualizar entidades
    def Update(EntityType):
        Entity=Crud.ReadOne(EntityType)
        EntityName=Generics.GetEntityName(EntityType)
        if Entity!=None:
            Confirma=input("Deseja alterar o(a) "+EntityName+" '"+Entity["Nome"]+"'? (S/N)\n")
            if Confirma.upper()=="S":
                List=Data.GetListEntity(EntityType)
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
        List=Data.GetListEntity(EntityType)
        Entity=Crud.ReadOne(EntityType)
        EntityName=Generics.GetEntityName(EntityType)
        if Entity!=None:
            Confirma=input("Deseja remover o(a) "+EntityName+" '"+Entity["Nome"]+"'? (S/N)\n")
            if Confirma.upper()=="S":
                Entity["Status"]=False;
                print(EntityName+" '"+ Entity["Nome"]+"' foi removido, porém ainda estará visível na consulta por código.")

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
                    if OptionEntity==1:
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
                        print("Em desenvolvimento")
                        break
            else:
                print("Finalizando sistema...")
                break
        else:
            print("!!! Selecione uma opção válida !!!")

init()