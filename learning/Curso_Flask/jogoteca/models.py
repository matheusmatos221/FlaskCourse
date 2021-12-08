class Jogo:
    def __init__(self, nome, categoria, console, id=None):
        self.__id = id
        self.__nome = nome
        self.__categoria = categoria
        self.__console = console

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def nome(self):
        return self.__nome

    @property
    def categoria(self):
        return self.__categoria

    @property
    def console(self):
        return self.__console


class Usuario:
    def __init__(self, user_id, nome, senha):
        self.__id = user_id
        self.__nome = nome
        self.__senha = senha

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def senha(self):
        return self.__senha
