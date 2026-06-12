import PySimpleGUI as sg
from App.Model.Banco import Banco
from App.Functions.formtcnpj import format_cnpj as CNP

class CadEstabController:
    def __init__(self, banco):
        self.banco = banco
        
    def cadastrar_estabelecimento(self):
        sg.theme('DarkAmber') ##temas: Material1, Reddit, DarkBlue3, DarkGrey13
        layout_cadEstab = [
            [   sg.Push(),
                sg.Text("Nome:"),
                sg.Input(key="nome")
             ],
            [
                sg.Push(),
                sg.Text("CNPJ:"),
                sg.Input(key="CNPJ")
            ],
            [
                sg.Push(),
                sg.Text("Telefone:"),
                sg.Input(key="telefone")
            ],
            [
                sg.Push(),
                sg.Text("IE:"),
                sg.Input(key="IE")
            ],
            [
                sg.Push(),
                sg.Text("Endereço:"),
                sg.Input(key="endereco")
            ],
            [
                sg.Push(),
                sg.Button("Salvar", size=(12, 2)),
                sg.Button("Cancelar", size=(12, 2)),
                sg.Push()
            ]             
             
        ]
        
        janela = sg.Window("Cadastro de Estabelecimento", layout_cadEstab, modal=True, icon="./Icones/nota.ico")
        
        while True:
            event, values = janela.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                break
            
            if event == "Salvar":
                nome = values["nome"]
                CNPJ = values["CNPJ"]
                CNPJ = CNP(CNPJ)
                telefone = values["telefone"]
                IE = values["IE"]
                endereco = values["endereco"]
                self.banco.cad_estabelecimento(nome, CNPJ, telefone, IE, endereco)
                sg.popup("Atualizado cadastrado com sucesso!", title="Sucesso", keep_on_top=True, icon="./Icones/nota.ico")

        janela.close()

    def listar_estabelecimento(self):
        return self.banco.listar_estabelecimento()