import os
import csv

csv_iou = open('iou.csv','w')
csvwriter = csv.writer(csv_iou)

csv_data = open('check.csv', 'r')
csvreader = csv.reader(csv_data, delimiter=',', quotechar='|')
for i, row in enumerate(csvreader):
    print (row)
    if (int(row[5]) == 0 and int(row[6]) == 0 and int(row[7]) == 0 and int(row[8]) == 0):
        csvwriter.writerow([0,0,0,0,0,0,0,0,0,0,i+1])
    else:
        overlapping_coords = []
        if int(row[1]) == int(row[5]):
            if int(row[2]) == int(row[6]):
                overlapping_coords.append(int(row[1]))
                overlapping_coords.append(int(row[2]))
            elif int(row[2]) < int(row[6]) and int(row[4]) > int(row[6]):
                overlapping_coords.append(int(row[5]))
                overlapping_coords.append(int(row[6]))
            elif int(row[2]) > int(row[6]) and int(row[8]) > int(row[2]):
                overlapping_coords.append(int(row[1]))
                overlapping_coords.append(int(row[2]))
        elif int(row[1]) < int(row[5]) and int(row[3]) > int(row[5]):
            if int(row[2]) == int(row[6]):
                overlapping_coords.append(int(row[5]))
                overlapping_coords.append(int(row[6]))
            elif int(row[2]) < int(row[6]) and int(row[4]) > int(row[6]):
                overlapping_coords.append(int(row[5]))
                overlapping_coords.append(int(row[6]))
            elif int(row[2]) > int(row[6]) and int(row[8]) > int(row[2]):
                overlapping_coords.append(int(row[5]))
                overlapping_coords.append(int(row[2]))
        elif int(row[1]) > int(row[5]) and int(row[7]) > int(row[1]):
            if int(row[2]) == int(row[6]):
                overlapping_coords.append(int(row[1]))
                overlapping_coords.append(int(row[2]))
            elif int(row[2]) < int(row[6]) and int(row[4]) > int(row[6]):
                overlapping_coords.append(int(row[1]))
                overlapping_coords.append(int(row[6]))
            elif int(row[2]) > int(row[6]) and int(row[8]) > int(row[2]):
                overlapping_coords.append(int(row[1]))
                overlapping_coords.append(int(row[2]))
        if int(row[3]) == int(row[7]):
            if int(row[4]) == int(row[8]):
                overlapping_coords.append(int(row[3]))
                overlapping_coords.append(int(row[4]))
            elif int(row[4]) < int(row[8]) and int(row[4]) > int(row[6]):
                overlapping_coords.append(int(row[3]))
                overlapping_coords.append(int(row[4]))
            elif int(row[4]) > int(row[8]) and int(row[8]) > int(row[2]):
                overlapping_coords.append(int(row[7]))
                overlapping_coords.append(int(row[8]))
        elif int(row[3]) < int(row[7]) and int(row[3]) > int(row[5]):
            if int(row[4]) == int(row[8]):
                overlapping_coords.append(int(row[3]))
                overlapping_coords.append(int(row[4]))
            elif int(row[4]) < int(row[8]) and int(row[4]) > int(row[6]):
                overlapping_coords.append(int(row[3]))
                overlapping_coords.append(int(row[4]))
            elif int(row[4]) > int(row[8]) and int(row[8]) > int(row[2]):
                overlapping_coords.append(int(row[3]))
                overlapping_coords.append(int(row[8]))
        elif int(row[3]) > int(row[7]) and int(row[7]) > int(row[1]):
            if int(row[4]) == int(row[8]):
                overlapping_coords.append(int(row[7]))
                overlapping_coords.append(int(row[8]))
            elif int(row[4]) < int(row[8]) and int(row[4]) > int(row[6]):
                overlapping_coords.append(int(row[7]))
                overlapping_coords.append(int(row[4]))
            elif int(row[4]) > int(row[8]) and int(row[8]) > int(row[2]):
                overlapping_coords.append(int(row[7]))
                overlapping_coords.append(int(row[8]))
        print (overlapping_coords)
        if len(overlapping_coords) > 0:
            area_drawn = (int(row[3])-int(row[1]))*(int(row[4])-int(row[2]))
            area_pred = (int(row[7])-int(row[5]))*(int(row[8])-int(row[6]))
            area_overlap = (int(overlapping_coords[2])-int(overlapping_coords[0]))*(int(overlapping_coords[3])-int(overlapping_coords[1]))
            iou = float(area_overlap)/(area_drawn+area_pred-area_overlap)
            recall = float(area_overlap)/area_pred
            prec = float(area_overlap)/area_drawn
            overlapping_coords = overlapping_coords + [area_drawn,area_pred,area_overlap,iou,recall,prec]
            overlapping_coords.append(i+1)
            csvwriter.writerow(overlapping_coords)
        else:
            csvwriter.writerow([0,0,0,0,0,0,0,0,0,0,i+1])

csv_iou.close()
csv_data.close()

