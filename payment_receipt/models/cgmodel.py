from payment_receipt import const
from payment_receipt.converters.map import consult_rubrics, consult_empregados, consult_recibo_calculo_base
from payment_receipt.models.enum import Rubrics, Company, Collaborator, GenericReceipt
from payment_receipt.utils.connect_database import DatabaseConnect
from payment_receipt.utils.instance_request import request_portal

init_database = DatabaseConnect()
connection = init_database.connection()


class CGModel(Rubrics, Company, Collaborator, GenericReceipt):

    def __init__(self, rubrics, company, collaborators, generic_receipt):
        super().__init__(rubrics, company, collaborators, generic_receipt)

        self.json_values_collaborator = {}
        self.json_values_generic_receipt = {}

        self.setter_rubrics()
        self.setter_collaborators()
        self.setter_generic_receipt()

    def setter_rubrics(self):
        for value in init_database.return_consult(consult_rubrics):
            self.code = str(value[4])
            self.description = str(value[9])
            self.reference = float(value[5])
            self.due_date = float(value[6])
            self.discount = float(value[7])
            self.date = value[2].strftime('%Y-%m-%d')
            self.collaborator_id = float(value[1])

            self.json_rubrics_collaborator.update({
                value[1]: {
                    self.date: {
                        "code": self.code,
                        "description": self.description,
                        "reference": self.reference,
                        "due_date": self.due_date,
                        "discount": self.discount
                    }
                }
            })

    def getter_rubrics(self):
        return self.json_rubrics_collaborator

    def setter_company(self):
        cursor = DatabaseConnect().connect_rds()
        cursor.execute(f"SELECT cgce_emp from geempre where codi_emp = '{self.codi_emp}'")
        result = cursor.fetchone()

        return result

    def getter_company(self, codi_emp):
        self.codi_emp = codi_emp
        return self.setter_company()

    def setter_collaborators(self):
        for value in init_database.return_consult(consult_empregados):
            self.json_values_collaborator.update(
                {value[0]: {
                    "collaborator": []
                }}
            )
        new_consult = init_database.return_consult(consult_empregados)

        for value_i in new_consult:
            self.code = value_i[1]
            self.name = value_i[2]
            self.cpf = value_i[3]
            self.ctps = value_i[4]
            self.admission_date = value_i[5].strftime('%Y-%m-%d')
            self.ctps_series = value_i[6]
            self.position_company = value_i[11]
            self.cbo = value_i[12]
            self.department = value_i[7]
            self.branch = value_i[8]
            self.bank = value_i[24]
            self.agency = value_i[25]
            self.cc = value_i[16]
            self.monthly = value_i[17]

            self.json_values_collaborator[value_i[0]]['collaborator'].append({
                "code": self.code,
                "name": self.name,
                "cpf": self.cpf,
                "ctps": self.ctps,
                "admission_date": self.admission_date,
                "ctps_series": self.ctps_series,
                "position_company": self.position_company,
                "cbo": self.cbo,
                "department": self.department,
                "branch": self.branch,
                "bank": self.bank,
                "agency": self.agency,
                "cc": self.cc,
                "monthly": self.monthly,
            })

            if value_i[27] is not None:
                self.json_values_collaborator[value_i[0]]['collaborator'].append(
                    {"account_bank": f"{value_i[26]}{value_i[27]}"})
            else:
                self.json_values_collaborator[value_i[0]]['collaborator'].append({"account_bank": value_i[26]})

    def getter_collaborators(self):
        return self.json_values_collaborator

    def setter_generic_receipt(self):
        collaborator_values = init_database.return_consult(consult_recibo_calculo_base)

        for value in collaborator_values:
            self.total_due_date = float(value[7])
            self.total_discount = float(value[8])
            self.net_value = float(value[6])
            self.base_salary = float(value[3])
            self.salary_inss = float(value[11])
            self.fgts_base_calculation = float(value[12])
            self.fgts_month = float(value[13])
            self.irrf_base_calculation = float(value[4])
            self.irrf_range = float(value[5])

            date = value[2].strftime('%Y-%m-%d')
            self.json_values_generic_receipt.update({
                value[1]: {
                    date: {
                        "rubrics": [],
                        "total": {
                            "total_due_date": self.total_due_date,
                            "total_discount": self.total_discount,
                            "net_value": self.net_value,
                            "base_salary": self.base_salary,
                            "salary_inss": self.salary_inss,
                            "fgts_base_calculation": self.fgts_base_calculation,
                            "fgts_month": self.fgts_month,
                            "irrf_base_calculation": self.irrf_base_calculation,
                            "irrf_range": self.irrf_range
                        },
                    }
                }
            })

    def getter_generic_receipt(self):
        return self.json_values_generic_receipt
