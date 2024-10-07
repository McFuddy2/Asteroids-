import csv
from datetime import datetime


def get_top_ten_scores():
    hall_of_fame = []
    try:
        with open('halloffame.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    if row[0] == "Player_Name":
                        continue
                    player_name, score, date = row

                    try:
                        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                        formatted_date = date_obj.strftime("%m-%d-%y")
                    except:
                        formatted_date = date

                    hall_of_fame.append([player_name, int(score), formatted_date])
        hall_of_fame.sort(key=lambda x: x[1], reverse=True)
    except FileNotFoundError:
        print("Hall Of Fame Not Found")
    return hall_of_fame[:10]