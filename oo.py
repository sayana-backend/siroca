from transliterate import translit
import random
from apps.company.models import Company

def generate_codes(company_name):
    company_name = translit(company_name.replace(' ', ''), 'ru', reversed=True).upper()
    middle_chars = [char for char in company_name[1:-1]]

    codes = set() 
    for _ in range(10):
        middle_char = random.choice(middle_chars)
        code = company_name[0] + middle_char + company_name[-1]
        if not Company.objects.filter(company_code=code).exists():
            codes.add(code)
    return list(codes)


print(generate_codes('mbank'))

