import xlrd 
from writeonimage import WriteOnImage
from mailer import sendemail

# Give the location of the file 
loc = ("./tickets/names.xlsx") 
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 
details=[]
for k in range(1,91):
    name=sheet.cell_value(k, 1)
    email=sheet.cell_value(k,3)
    price=int(sheet.cell_value(k,5))
    details.append([name,email,price])

print(len(details))
sendemail(details)
# WriteOnImage(details)