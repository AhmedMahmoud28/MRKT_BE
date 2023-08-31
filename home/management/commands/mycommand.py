from django.core.management.base import BaseCommand
from faker import Faker
from home import models

fake = Faker()

class Command(BaseCommand):
    # fake = Faker()
    help = 'Create Fake Data for Models'

    # def add_arguments(self, parser):
    #     parser.add_argument('arg_name', type=str, help='Description of the argument')

    def handle(self, *args, **options):
        # arg_value = options['arg_name']
        for i in range(1000):
            StoreCategory = models.StoreCategory.objects.create(name=fake.company_suffix())
            Store = models.Store.objects.create(name=fake.company(),category=StoreCategory)
            ProductCategory = models.ProductCategory.objects.create(name=fake.prefix())
            Brand = models.Brand.objects.create(name=fake.prefix())
            product = models.Product.objects.create(name=fake.word(),
                                                    price=fake.random_int(min=20, step=7),
                                                    inventory=fake.random_int(min=20, step=7),
                                                    category=ProductCategory,
                                                    brand=Brand,)
            product.store.set([Store])
            self.stdout.write(self.style.SUCCESS(f'Custom command executed'))
        


# # Person
# name = fake.name()
# first_name = fake.first_name()
# last_name = fake.last_name()
# prefix = fake.prefix()
# suffix = fake.suffix()
# job_title = fake.job()

# # Address
# address = fake.address()
# street_address = fake.street_address()
# city = fake.city()
# state = fake.state()
# country = fake.country()
# zipcode = fake.zipcode()

# # Contact
# phone_number = fake.phone_number()
# email = fake.email()

# # Text
# sentence = fake.sentence()
# paragraph = fake.paragraph()
# text = fake.text()

# # Date and Time
# date_of_birth = fake.date_of_birth()
# date_this_century = fake.date_this_century()
# time = fake.time()
# date_time_this_decade = fake.date_time_this_decade()

# # Numbers
# random_int = fake.random_int(min=0, max=100, step=1)
# random_float = fake.random_float()

# # Misc
# color_name = fake.color_name()
# file_extension = fake.file_extension()
# user_agent = fake.user_agent()

# # Credit Card
# credit_card_number = fake.credit_card_number()
# credit_card_expire = fake.credit_card_expire()
# credit_card_security_code = fake.credit_card_security_code()
# credit_card_full = fake.credit_card_full()

# # Company
# company_name = fake.company()
# company_suffix = fake.company_suffix()
# catch_phrase = fake.catch_phrase()

# # Internet
# username = fake.user_name()
# domain_name = fake.domain_name()
# url = fake.url()
# ipv4 = fake.ipv4()

# # Lorem
# word = fake.word()
# words = fake.words()
# sentence = fake.sentence()
# paragraph = fake.paragraph()

# # Images
# image_url = fake.image_url(width=None, height=None)

# # UUID
# uuid4 = fake.uuid4()

# # Custom Formats
# custom_format = fake.format('###-##-####')

# # Localized Data (Some locales may require additional data packages)
# localized_name = fake.first_name_female()  # For locales that have gender-specific names

