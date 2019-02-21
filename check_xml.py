import os
import xml.etree.ElementTree as et
import xlsxwriter

workbook = xlsxwriter.Workbook('check.xlsx')
worksheet = workbook.add_worksheet()

for i, xml_file in enumerate(os.scandir('annotations')):
    file = et.parse(xml_file).getroot()
    row = i
    col = 0 
    worksheet.write(row, col, file[1].text)
    worksheet.write(row, col+1, len(file)-4)
    worksheet.write(row, col + 2, file[3][0].text)
    worksheet.write(row, col + 3, file[3][1].text)
    col = 4
    for j in range(4,len(file)):
        worksheet.write(row, col, file[j][4][0].text)
        worksheet.write(row, col + 1, file[j][4][1].text)
        worksheet.write(row, col + 2, file[j][4][2].text)
        worksheet.write(row, col + 3, file[j][4][3].text)
        col += 4

    
