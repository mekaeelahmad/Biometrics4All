import re
import sys
import os
import pandas as pd
import xlwings as xw
import tkinter as tk
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

#Ctrl + L below to copy line and send client after sending initial quote 
#Thank you for reaching out to us regarding your Live Scan needs.  I just sent you a separate email with information and quotes.  Please do not hesitate to reach out with additional questions.
def omit_country(address):
    parts = address.rsplit(', ', 1)

    if len(parts) >= 2:
        return parts[0]

    return address

def split_address(fulladdress):
    if (fulladdress == None):
        return Exception
    split = fulladdress.split(', ')
    address1 = split[0]
    address2 = ', '.join(split[1:-1]) + ', ' + split[-1]
    return address1, address2

def edit_and_save_as_pdf(business_name, phone_number, client_name, email, address1, address2):
    app = xw.App(visible=False)
    wb = app.books.open('Unprotected CA Template.xlsx')

    sheet = wb.sheets['Using Sales Activity Sheet']

    sheet.range('B2').value = business_name
    sheet.range('E2').value = business_name
    sheet.range('G2').value = phone_number
    sheet.range('H2').value = client_name
    sheet.range('I2').value = email
    sheet.range('L2').value = address1
    sheet.range('M2').value = address2

    if not os.path.exists('Quotes'):
        os.makedirs('Quotes')
    wb.save(f'Quotes/{business_name}.xlsx')

    wb.sheets['CA Multi Tenprint'].api.ExportAsFixedFormat(0, f'{os.getcwd()}\\Quotes\\{business_name}.pdf')
    wb.close()



def process_string(input_string):
    lines = input_string.strip().split('\n')
    
    first_name = lines[0]
    last_name = lines[1]
    
    line1 = f"{last_name} | {first_name}"
    
    business_name = lines[2]
    email = lines[3]
    phone_number = format_phone(lines[4]) 
    incomplete_address = lines[5]
    complete_address = addressUpdate.correct_address(addressUpdate.api_key, incomplete_address)
    complete_address = omit_country(complete_address)
    address1, address2 = split_address(complete_address)
    output_string = '\n'.join([line1, business_name, email, phone_number, address1, address2])
    edit_and_save_as_pdf(business_name, phone_number, line1, email, address1, address2)
    return output_string


def process_input():
    input_string = text_widget.get("1.0", tk.END).strip()  # Get content from Text widget
    text_widget.delete("1.0", tk.END)  # Clear the text widget
    result_label.config(text="Processing...")

    # Continue with your existing code here to process the input_string
    print("Value of fixthis:", input_string)
    # ... rest of your code
    fixthis = input_string
    print(process_string(fixthis))
    result_label.config(text="Input processed! Ready for next input.")

# Create a GUI window
root = tk.Tk()
root.title('Enter Client Details')
root.geometry('400x300') # Window size

# Create a Frame for padding
frame = tk.Frame(root, padx=15, pady=15)
frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

# Create a Label
label = tk.Label(frame, text="Please enter the details in the following format:\nFirstName, LastName, BusinessName, Email, Number, Incomplete Address", wraplength=350, justify=tk.LEFT)
label.pack()

# Create a Text widget
text_widget = tk.Text(frame, wrap=tk.WORD, height=8, padx=10, pady=10)
text_widget.pack(expand=True, fill=tk.BOTH)

# Create a Button widget
button = tk.Button(frame, text="Submit", command=process_input, width=15, bg='#4CAF50', fg='white')
button.pack(pady=5)

# Label to show processing result
result_label = tk.Label(frame, text="")
result_label.pack()

# Run the main loop
root.mainloop()



#this is for the commit