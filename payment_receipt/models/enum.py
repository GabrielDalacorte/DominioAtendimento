from typing import Optional


class Rubrics:

    def __init__(self, code: str = Optional, description: str = Optional, reference: float = Optional,
                 due_date: float = Optional, discount: float = Optional, date: str = Optional,
                 collaborator_id: str = Optional):
        self.code = code
        self.description = description
        self.reference = reference
        self.due_date = due_date
        self.discount = discount
        self.date = date
        self.collaborator_id = collaborator_id
        self.json_rubrics_collaborator = {}


class Company:

    def __int__(self, codi_emp: str = Optional, cnpj_emp: str = Optional):
        self.codi_emp = codi_emp
        self.cnpj_emp = cnpj_emp


class Collaborator:

    def __int__(self, code: str = Optional, name: str = Optional, cpf: str = Optional, ctps: str = Optional,
                admission_date: str = Optional, ctps_series: str = Optional, position_company: str = Optional,
                cbo: str = Optional, department: str = Optional, branch: str = Optional, bank: str = Optional,
                agency: str = Optional, cc: str = Optional, monthly: str = Optional):

        self.code = code
        self.name = name
        self.cpf = cpf
        self.ctps = ctps
        self.admission_date = admission_date
        self.ctps_series = ctps_series
        self.position_company = position_company
        self.cbo = cbo
        self.department = department
        self.branch = branch
        self.bank = bank
        self.agency = agency
        self.cc = cc
        self.monthly = monthly


class GenericReceipt:
    def __init__(self, total_due_date: float = Optional, total_discount: float = Optional, net_value: float = Optional,
                 base_salary: float = Optional, salary_inss: float = Optional, fgts_base_calculation: float = Optional,
                 fgts_month: float = Optional, irrf_base_calculation: float = Optional, irrf_range: float = Optional):

        self.total_due_date = total_due_date
        self.total_discount = total_discount
        self.net_value = net_value
        self.base_salary = base_salary
        self.salary_inss = salary_inss
        self.fgts_base_calculation = fgts_base_calculation
        self.fgts_month = fgts_month
        self.irrf_base_calculation = irrf_base_calculation
        self.irrf_range = irrf_range



