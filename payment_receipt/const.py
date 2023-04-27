DOMAIN_ = None
STATUS = ''
if STATUS == '':
    DOMAIN = ''
    DOMAIN_ = DOMAIN
    USERNAME_LOGIN = ""
    PASSWORD_LOGIN = ''
elif STATUS == '':
    USERNAME_LOGIN = ""
    PASSWORD_LOGIN = ""
    DOMAIN = ''
    DOMAIN_ = DOMAIN

URL_LOGIN = f"{DOMAIN_}rest-auth/login/"
URL_API_COLLABORATORS = f"{DOMAIN_}api/v1/collaborator/"
URL_API_COMPANY = f"{DOMAIN_}api/v1/empresas/"
URL_API_POST_COMPANY = f"{DOMAIN_}api/v1/post/empresas/"
URL_API_PAYCHECK = f"{DOMAIN_}api/v1/post/valores-paycheck/"

DATABASE = ""
USER = ""
PWD = ""
HOST = ""
PORT = ""

URL_API_PAYMENTS = f"{DOMAIN_}api/v1/payment/"
