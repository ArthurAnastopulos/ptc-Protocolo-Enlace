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

    """ Construtor do Quadro 

    @kwargs: argumentos de chave que formam o Quadro
    """
    def __init__(self, **kwargs): # keyword args para argumentos de chave que formam o Quadro
        self.controle = 0
        if kwargs is not None:
            if 'tipoMsgArq' in kwargs:
                self.tipoMsgArq = kwargs['tipoMsgArq']
            else:
                self.tipoMsgArq = 0
            # if 'tipoQuadro' in kwargs:
            #     self.tipoQuadro = kwargs['tipoQuadro']
            # else:
            #    self.tipoQuadro = 0
            if 'numSequencia' in kwargs:
                self.numSequencia = kwargs['numSequencia']
            else:
                self.numSequencia = 0
            if 'idProto' in kwargs:
                self.idProto = kwargs['idProto']
            else:
               self.idProto = 1
            if 'data' in kwargs:
                self.data = kwargs['data']
            else:
                self.data = ""
            if 'fcs' in kwargs:
                self.fsc = kwargs['fcs']   

    def deserialize(self, buffer: bytes):
        pass 
    
    """ Serializa o quadro em um buffer 

    @return buffer: retorna um buffer
    """
    def serialize(self):
        self.buffer = bytearray()

        # Verificar os 7 bits do Controle, colocando os valores definidos
        self.controle |= ( self.tipoMsgArq << 7 )
        self.controle |= ( self.numSequencia << 3 )

        self.buffer.append(self.controle)
        self.buffer.append(0) #Reservado
        
        if self.tipoMsgArq == 0: # Este campo existe somente em quadros do Tipo DATA
            self.buffer.append(self.idProto)
        
        self.buffer += self.inserirEsc(self.data)

        fcs = CRC16(self.buffer)
        self.buffer = fcs.gen_crc()

        return self.buffer

    """ Inseri Escapes em um Quadro 

    @params data: dados a serem modificados
    @return dados: dados formatados com os escapes
    """
    def inserirEsc(self, data):
        dados = bytearray()

        for i in range(len(data)):
            if data[i] == b'\x7E':
                dados += b'\x7D'
                dados += bytes([dados[i] ^ 0x02]) #xor
            else:
                if type(data[i]) == str:
                    dados += str.encode(data[i])
                else:
                    dados.append(data[i])
        return dados