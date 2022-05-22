import random


def email_gen(email_prefix='test'):
    return f'{random.randint(0, 9999)}@{email_prefix}.com'
