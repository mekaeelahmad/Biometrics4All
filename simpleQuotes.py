import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import addressUpdate

def format_phone(phone_number):
    # removing all non-digit characters
    phone_number = re.sub(r'\D', '', phone_number)
    # formatting the phone number
    formatted_phone_number = f'({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}'
    return formatted_phone_number

#fix this in the format:
"""FirstName
LastName
BusinessName
Email
Number (can be any format, just needs 10 digits)
Incomplete Address (needs to at least include address line 1 and city) Make sure there is no # 
"""
fixthis = """Luz
Acosta
Luz Acosta
luzacostahomes@gmail.com
805-587-0403
2655 First St 259 Simi Valley 
"""
#Ctrl + L below to copy line and send client after sending initial quote 
#Thank you for reaching out to us regarding your Live Scan needs.  I just sent you a separate email with information and quotes.  Please do not hesitate to reach out with additional questions.
def omit_country(address):
    # Split the string into parts, using ', ' as the separator
    parts = address.rsplit(', ', 1)

    # If the string was split into at least 2 parts, omit the last part
    if len(parts) >= 2:
        return parts[0]

    # If the string wasn't split, return it as is
    return address

def split_address(fulladdress):
    if (fulladdress == None):
        return Exception
    split = fulladdress.split(', ')
    address1 = split[0]
    address2 = ', '.join(split[1:-1]) + ', ' + split[-1]
    return address1, address2

def process_string(input_string):
    # Splitting the string into lines
    lines = input_string.strip().split('\n')
    
    # Separating the First and Last Name
    first_name = lines[0]
    last_name = lines[1]
    
    # Line 1: LastName | FirstName
    line1 = f"{last_name} | {first_name}"
    
    # Getting the other information from the string
    business_name = lines[2]
    email = lines[3]
    phone_number = format_phone(lines[4]) # Here we call a function to format the phone number
    incomplete_address = lines[5]
    complete_address = addressUpdate.correct_address(addressUpdate.api_key, incomplete_address)
    complete_address = omit_country(complete_address)
    address1, address2 = split_address(complete_address)
    output_string = '\n'.join([line1, business_name, email, phone_number, address1, address2])
    
    return output_string

print(process_string(fixthis))

#this is for the commit