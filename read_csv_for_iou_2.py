import os
import csv

csv_iou = open('iou_slab.csv','w')
csvwriter = csv.writer(csv_iou)

csv_data = open('iou.csv', 'r')
csvreader = csv.reader(csv_data, delimiter=',', quotechar='|')
counter = 0
list_iou = []
list_recall = []
list_prec = []
for row in csvreader:
	list_iou.append(float(row[7]))
	list_recall.append(float(row[8]))
	list_prec.append(float(row[9]))
	if float(row[10])//2 > counter:
		counter+=1
		csvwriter.writerow([(sum(list_iou)/2),(sum(list_recall)/2),(sum(list_prec)/2)])
		list_iou = []
		list_recall = []
		list_prec = []

csv_iou.close()
csv_data.close()

