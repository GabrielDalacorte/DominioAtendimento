import datetime
import unittest

from tests.enum_teste_case import Rubrics, Company, Collaborator


def len_string(value):
    return len(value)


def if_none(value):
    if value is not None:
        return value
    else:
        return '0'


class TestRubrics(unittest.TestCase):

    def test_code(self):
        self.assertIsInstance(Rubrics().code, str)

    def test_description(self):
        self.assertIsInstance(Rubrics().description, float)

    def test_reference(self):
        self.assertIsInstance(Rubrics().reference, float)

    def test_due_date(self):
        self.assertIsInstance(Rubrics().due_date, float)

    def test_discount(self):
        self.assertIsInstance(Rubrics().discount, float)

    def test_date(self):
        self.assertIsInstance(Rubrics().date, datetime.datetime)

    def test_collaborator_id(self):
        self.assertIsInstance(Rubrics().collaborator_id, str)


class TestCompany(unittest.TestCase):

    def test_code_company(self):
        self.assertIsInstance(Company().codi_emp, str)

    def test_len_cnpj_company(self):
        self.assertEqual(len_string(Company().cnpj_emp), 14)


class TestCollaborator(unittest.TestCase):
    def test_code_collaborator(self):
        code = if_none(Collaborator().code)
        self.assertIsInstance(code, str)

    def test_name_collaborator(self):
        name = if_none(Collaborator().name)
        self.assertIsInstance(name, str)

    def test_cpf__collaborator(self):
        cpf = if_none(Collaborator().cpf)
        self.assertEqual(len_string(cpf), 11)

    def test_ctps_collaborator(self):
        ctps = if_none(Collaborator().ctps)
        self.assertIsInstance(ctps, str)

    def test_admission_date_collaborator(self):
        self.assertIsInstance(Collaborator().admission_date, datetime.datetime)

    def test_ctps_series_collaborator(self):
        ctps_series = if_none(Collaborator().ctps_series)
        self.assertIsInstance(ctps_series, str)

    def test_branch_collaborator(self):
        branch = if_none(Collaborator().branch)
        self.assertIsInstance(branch, str)

    def test_bank_collaborator(self):
        bank = if_none(Collaborator().bank)
        self.assertIsInstance(bank, str)

    def test_agency_collaborator(self):
        agency = if_none(Collaborator().agency)
        self.assertIsInstance(agency, str)

    def test_cc_collaborator(self):
        cc = if_none(Collaborator().cc)
        self.assertIsInstance(cc, str)

    def test_monthly_collaborator(self):
        monthly_list = ['Adiantamento', 'Mensalista']
        monthly = if_none(Collaborator().monthly)
        self.assertIn(monthly, monthly_list)


if __name__ == '__main__':
    unittest.main()

