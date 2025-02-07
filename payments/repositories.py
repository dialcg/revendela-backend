from authy.models import CustomUser
from .models import Transaction
from decimal import Decimal


class TransactionRepository:
    @staticmethod
    def create_transaction(
        wompi_id: str, reference: str, amount: Decimal, status: str, user: CustomUser
    ) -> Transaction:
        if status in [choice[0] for choice in Transaction.STATUS_CHOICES]:
            transaction, created = Transaction.objects.get_or_create(
                wompi_id=wompi_id,
                defaults={
                    "reference": reference,
                    "amount": amount,
                    "status": status,
                    "user": user,
                },
            )
            return transaction
        return None

    @staticmethod
    def get_transaction_by_wompi_id(wompi_id):
        return Transaction.objects.filter(wompi_id=wompi_id).first()

    @staticmethod
    def update_transaction_status(wompi_id, new_status):

        transaction = Transaction.objects.get(wompi_id=wompi_id)
        transaction.status = new_status
        transaction.save()
        return transaction
