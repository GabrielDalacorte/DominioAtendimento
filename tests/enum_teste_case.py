import datetime


class Rubrics:

    def __init__(self):
        self.code = "691"
        self.description = 100.0
        self.reference = 200.0
        self.due_date = 619.32
        self.discount = 333.0
        self.date = datetime.datetime.now()
        self.collaborator_id = "200"


class Company:

    def __init__(self):
        self.codi_emp = "296"
        self.cnpj_emp = "00334455667788"


class Collaborator:

    def __init__(self):

        self.code = "691"
        self.name = "Usuario Teste"
        self.cpf = "99988877732"
        self.ctps = "320"
        self.admission_date = datetime.datetime.now()
        self.ctps_series = "000324"
        self.position_company = "Gerente"
        self.cbo = "8000"
        self.department = "262600"
        self.branch = '1'
        self.bank = "BANCO BRADESCO"
        self.agency = "5670"
        self.cc = "185 - SE INGA"
        self.monthly = "Adiantamento"
