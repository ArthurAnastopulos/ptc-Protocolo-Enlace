from crc import CRC16

'''
ACK  = 0
DATA = 1

1 - Controle
1 - Reservado
1 - ID
    Dados
2 - FCS    
'''
class Quadro():

    def __init__(self, **kwargs): # keyword args para argumentos ce chave que formam o Quadro
        self.__controle = 0
        if kwargs is not None:
            if 'tipoQuadro' in kwargs:
                self.__tipoQuadro = kwargs['tipoQuadro']
            else: #Se não Controle gerar Exceção !!Este caso nunca é para acontecer
               raise Exception("Está faltando o bit do tipo de Quadro(ACK ou DATA)")
            if 'numSequencia' in kwargs:
                self.__numSequencia = kwargs['numSequencia']
            else:
                raise Exception("Está faltando o bit do número de Sequencia")
            if 'idProto' in kwargs:
                self.__idProto = kwargs['idProto']
            else:
                raise Exception("Está faltando idProto") #Vem da Adaptação
            if 'data' in kwargs:
                self.__data = kwargs['data']
            else:
                self.__data = ""
            if 'FCS' in kwargs:
                self.__fsc = kwargs['fcs']   

    @staticmethod
    def deserialize(self, buffer: bytes):
        pass 
    
    def serialize(self):
        self.__buffer = bytearray()

        # Verificar os 7 bits do Controle, colocando os valores definidos
        self.__controle |= ( self.__tipoQuadro << 7 )
        self.__controle |= ( self.__numSequencia << 3 )


        self.__buffer.append(self.__controle)
        self.__buffer.append(0) #Reservado
        
        if self.__tipoQuadro == 0: # Este campo existe somente em quadros do Tipo DATA
            self.__buffer.append(self.__idProto)
        
        self.__buffer += self.__data

        fcs = CRC16(self.__buffer)
        self.__buffer = fcs.gen_crc()

        return self.__buffer

    def getData(self):
        return self.__data