import json

import requests

from payment_receipt import const
from payment_receipt.converters.map import MAP_YEARS
from payment_receipt.models.cgmodel import CGModel
from payment_receipt.utils.get_token import WsGetToken
from payment_receipt.utils.headers import headers
from payment_receipt.utils.instance_request import request_portal


class QuoteParser(CGModel):

    def __init__(self, rubrics, company, collaborators, generic_receipt):
        super().__init__(rubrics, company, collaborators, generic_receipt)

        self.id_collaborator = {}
        self.json_update_generic_receipt = {}
        self.publish_collaborators()
        self.publish_receipt()

    def publish_collaborators(self):

        for get_id_company, v in self.getter_collaborators().items():
            self.cnpj_emp = self.getter_company(get_id_company)

            headers.update({'Authorization': 'Token ' + WsGetToken().get_token()['key']})
            get_company = requests.get(f"{const.URL_API_COMPANY}?cnpj={self.cnpj_emp[0]}", headers=headers, verify=True)
            format_get_company = json.loads(get_company.text)
            headers.update({'Authorization': 'Token ' + WsGetToken().get_token()['key']})
            self.id_collaborator.update(
                {format_get_company[0]['id']: {"collaborator": []}}
            )

            for collaborator_json in v['collaborator']:
                requests.post(url=f"{const.URL_API_COLLABORATORS}",
                              data=json.dumps(collaborator_json),
                              headers=headers, verify=True)

            get_collaborators = request_portal.get_cg(const.URL_API_COLLABORATORS)

            for collaborator in get_collaborators:
                for collaborator_insert in v['collaborator']:
                    try:
                        if str(collaborator_insert['code']) in str(collaborator['code']):
                            self.id_collaborator[format_get_company[0]['id']]["collaborator"].append(collaborator['id'])
                    except Exception:
                        #TODO ADICIONA LOGS
                        pass

        for id_company, collaborator_id in self.id_collaborator.items():
            requests.patch(url=f"{const.URL_API_POST_COMPANY}{id_company}/",
                           data=json.dumps(collaborator_id),
                           headers=headers, verify=True)

    def publish_receipt(self):
        get_collaborators_portal = request_portal.get_cg(const.URL_API_COLLABORATORS)
        get_company = request_portal.get_cg(const.URL_API_COMPANY)

        for cod_collaborator, date_values in self.getter_rubrics().items():
            for date, values in date_values.items():
                try:
                    self.getter_generic_receipt()[cod_collaborator][date]['rubrics'].append(values)
                except KeyError:
                    pass

        for cd_collaborator, values_date_collaborator in self.getter_generic_receipt().items():
            for date, values_rubrics in values_date_collaborator.items():

                date_format = date.split('-')
                month = MAP_YEARS[str(date_format[1]).zfill(2)]

                for collaborator in get_collaborators_portal:
                    if str(cd_collaborator) in str(collaborator['code']):
                        for company in get_company:
                            for collaborator_company_id in company['collaborator']:
                                if str(collaborator['id']) in str(collaborator_company_id['id']):
                                    self.json_update_generic_receipt = {
                                        "company": {
                                            "company": company['id'],
                                            "cc": collaborator['cc'],
                                            "monthly": collaborator['monthly'],
                                            "payment": "Adiantamento"
                                        },
                                        "collaborator": collaborator['id'],
                                        "total": {
                                            "total_due_date": values_rubrics['total']['total_due_date'],
                                            "total_discount": values_rubrics['total']['total_discount'],
                                            "net_value": values_rubrics['total']['net_value'],
                                            "base_salary": values_rubrics['total']['base_salary'],
                                            "salary_inss": values_rubrics['total']['salary_inss'],
                                            "fgts_base_calculation": values_rubrics['total']['fgts_base_calculation'],
                                            "fgts_month": values_rubrics['total']['fgts_month'],
                                            "irrf_base_calculation": values_rubrics['total']['irrf_base_calculation'],
                                            "irrf_range": values_rubrics['total']['irrf_range']
                                        },
                                        "year": str(date_format[0]),
                                        "month": month,
                                        "payment": "Adiantamento"
                                    }
                                    headers.update({'Authorization': 'Token ' + WsGetToken().get_token()['key']})

                                    self.json_update_generic_receipt.update({"rubrics": values_rubrics['rubrics']})
                                    requests.post(url=f"{const.URL_API_PAYCHECK}",
                                                  data=json.dumps(self.json_update_generic_receipt),
                                                  headers=headers, verify=True)


