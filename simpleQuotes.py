import re
import addressUpdate

def format_phone(phone_number):
    # removing all non-digit characters
    phone_number = re.sub(r'\D', '', phone_number)
    # formatting the phone number
    formatted_phone_number = f'({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}'
    return formatted_phone_number

fixthis = """Nicole Ann
De La Torre
The DLT Group, LLC
thedltgroup@gmail.com
818-309-5847
6603 Maplegrove St, Oak Park, CA 91377
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
    output_string = '\n'.join([line1, business_name, email, phone_number, complete_address])
    
    return output_string

print(process_string(fixthis))