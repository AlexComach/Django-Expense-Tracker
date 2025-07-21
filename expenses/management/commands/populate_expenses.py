from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.contrib.auth.models import User
from expenses.models import Transactions, Category

class Command(BaseCommand):
    help = 'Populate the database with fake transactions'

    def handle(self, *args, **kwargs):
        fake = Faker()

        users = list(User.objects.all())
        categories = list(Category.objects.all())
        if not users or not categories:
            self.stdout.write(self.style.ERROR('No users or categories found. Please add some first.'))
            return

        for _ in range(50):
            Transactions.objects.create(
                user=random.choice(users),
                type=random.choice(['Income', 'Expense']),
                amount=round(random.uniform(10, 500), 2),
                description=fake.sentence(nb_words=6),
                category=random.choice(categories),
                date=fake.date_between(start_date='-3y', end_date='today')
            )

        self.stdout.write(self.style.SUCCESS('Successfully added 200 fake transactions'))