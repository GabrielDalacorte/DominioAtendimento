from payment_receipt.models.enum import Rubrics, Company, Collaborator, GenericReceipt
from payment_receipt.actions.publish import QuoteParser

# Init Project
QuoteParser(Rubrics, Company, Collaborator, GenericReceipt)
