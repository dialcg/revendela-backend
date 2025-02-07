import pytest
from decimal import Decimal
from authy.models import CustomUser
from payments.models import Transaction
from payments.repositories import TransactionRepository


@pytest.mark.django_db
def test_create_transaction_sucess():
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="password123"
    )

    wompi_id = "wompi_12345"
    amount = Decimal("100.50")
    status = Transaction.WOMPI_APPROVED

    transaction = TransactionRepository.create_transaction(
        wompi_id=wompi_id,
        amount=amount,
        status=status,
        user=user,
    )

    assert Transaction.objects.filter(uuid=transaction.uuid).exists()


@pytest.mark.django_db
def test_create_transaction_wrong_status():
    user = CustomUser.objects.create_user(
        username="testuser", email="test@example.com", password="password123"
    )

    wompi_id = "wompi_12345"
    amount = Decimal("100.50")
    status = "seaprobo"

    transaction = TransactionRepository.create_transaction(
        wompi_id=wompi_id,
        amount=amount,
        status=status,
        user=user,
    )

    assert transaction == None
