import csv
import json
import os
import random

#  receives a JSON file name containing recipes and creates a CSV file with the ingredients
def recJSONtoIngCSV(path):
    fn=os.path.basename(path)
    print(fn)
    recipes = []
    for line in open(fn, 'r'):
        d = json.dumps(line)
        c = json.loads(d)
        recipes.append(c)
    ingredients = []

    for i in recipes:
        d = json.loads(i)
        for ing in d['ingredients']:
            ingredients.append(ing['ingredient'])
        ingredients = set(ingredients)
        ingredients = list(ingredients)
    rec_columns = ['id'] + ingredients
    rec_i=1
    with open(fn+".csv", mode='w') as csv_file:
        rec_rows = dict.fromkeys(rec_columns, 0)
        ing_dict_writer = csv.DictWriter(csv_file, fieldnames=rec_columns, lineterminator='\n')
        ing_dict_writer.writeheader()
        for j in recipes:
            d = json.loads(j)
            rec_rows['id'] = d['id']
            for i in ingredients:
                # print(rec_rows)
                for ing in d['ingredients']:
                    if ing['ingredient'] == i:
                        rec_rows[i] = 1
                        break
                    else:
                        rec_rows[i] = 0
            # print(rec_rows)
            # print(rec_columns)
            print("({rec_i}/{rec_size}) Working on recipe id: {ingId}".format(rec_i=rec_i, rec_size=len(recipes),ingId=d['id']))
            ing_dict_writer.writerow(rec_rows)
            rec_i += 1

recJSONtoIngCSV("every5.json")


# def what2ask(path):
#     fn = os.path.basename(path)
#     gi = []
#     # count the number of rows
#     with open(fn, 'r') as csvfile:
#         nrows = sum(1 for row in csvfile) - 1
#     with open(fn, 'r') as csvfile:
#         reader = csv.reader(csvfile)
#         ncols = len(next(reader))  # count the amount of columns and jump to the next line
#         for i in range(1, ncols):
#             yes = 0
#             no = 0
#             for row in reader:
#                 # print(row[i])
#                 if int(row[i]) == 1:
#                     yes += 1
#                 else:
#                     no += 1
#             gi.append(1 - (yes / nrows) ** 2 - (no / nrows) ** 2)
#             # print("yes={yes},no={no}".format(yes=yes, no=no))
#             csvfile.seek(0)
#             next(reader)
#     print(gi)
#     m = max(gi)
#     maxs = [i for i, j in enumerate(gi) if j == m]
#     with open(fn, 'r') as csvfile:
#         reader = csv.reader(csvfile)
#         return next(reader)[maxs[random.randint(0,len(maxs)-1)]]


# print(what2ask("ingredients_table1.csv")+" Y/N? ")
# yn = input()
# if(yn=='y'):
#     print("yessss")

# m = max(gi)
# maxs=[i for i, j in enumerate(gi) if j == m]
# # print(maxs)
# with open('CSV-recipes-cut.json', 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     what2ask=next(reader)[maxs[1]]
#
# print(what2ask)
# count the amount of rows
# with open(ing_csv, 'r') as csvfile:
#     nrows = sum(1 for row in csvfile) - 1
#
# with open(ing_csv, 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     ncols = len(next(reader))  # count the amount of columns and jump to the next line
#     for i in range(1, ncols):
#         yes = 0
#         no = 0
#         for row in reader:
#             # print(row[i])
#             if int(row[i]) == 1:
#                 yes += 1
#             else:
#                 no += 1
#         gi.append(1 - (yes / nrows) ** 2 - (no / nrows) ** 2)
#         # print("yes={yes},no={no}".format(yes=yes, no=no))
#         csvfile.seek(0)
#         next(reader)
# # print(gi)
# m = max(gi)
# maxs=[i for i, j in enumerate(gi) if j == m]
# # print(maxs)
# with open(ing_csv, 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     what2ask=next(reader)[maxs[2]]
#     print(what2ask+"? Y/N")



        # for i in range(1,filelen):
# recipes = []
# ing_csv = 'ingredients_table1.csv'
# for line in open('recipes-cut.json', 'r'):
#     d = json.dumps(line)
#     c = json.loads(d)
#     recipes.append(c)
#
# ingredients = []
# recIds = []
# for i in recipes:
#     d = json.loads(i)
#     recIds.append(d['id'])
#     for ing in d['ingredients']:
#         ingredients.append(ing['ingredient'])
# # print(recIds)
# ingredients = set(ingredients)
# ingredients = list(ingredients)
# rec_columns = ['id'] + ingredients
#
# ing_columns = []
# rec_i = 1
# with open(ing_csv, mode='w') as csv_file:
#     rec_rows = dict.fromkeys(rec_columns, 0)
#     ing_dict_writer = csv.DictWriter(csv_file, fieldnames=rec_columns, lineterminator='\n')
#     ing_dict_writer.writeheader()
#     for j in recipes:
#         d = json.loads(j)
#         rec_rows['id'] = d['id']
#         for i in ingredients:
#             # print(rec_rows)
#             for ing in d['ingredients']:
#                 if ing['ingredient'] == i:
#                     rec_rows[i] = 1
#         # print(rec_rows)
#         # print(rec_columns)
#         print("({rec_i}/{rec_size}) Working on recipe id: {ingId}".format(rec_i=rec_i, rec_size=len(recipes),
#                                                                           ingId=d['id']))
#         ing_dict_writer.writerow(rec_rows)
#         rec_i = rec_i + 1