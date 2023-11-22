import json 
from datetime import datetime, timedelta
with open('trainings.txt') as f:
    file_contents = json.load(f)

def training_completion_count(training_data):
    completion_count = {}
    for contents in training_data:
        for completion in contents['completions']:
            training_name = completion['name']
            completion_count[training_name] = completion_count.get(training_name, 0) + 1
    with open('completed_trainings.json', 'w') as file:
        json.dump(completion_count, file)


def completed_in_fiscal_year(trainings_data, trainings, fiscal_year):
    fiscal_year_start = datetime(fiscal_year - 1, 7, 1)
    fiscal_year_end = datetime(fiscal_year, 6, 30)

    completed_in_fiscal_year = {}

    for training_name in trainings:
        completed_in_fiscal_year[training_name] = []

        for person in trainings_data:
            latest_completion_date = None

            for completion in person['completions']:
                if completion['name'] == training_name:
                    completion_date = datetime.strptime(completion['timestamp'], "%m/%d/%Y")

                    if not latest_completion_date or completion_date > latest_completion_date:
                        latest_completion_date = completion_date

            if latest_completion_date and fiscal_year_start <= latest_completion_date <= fiscal_year_end:
                completed_in_fiscal_year[training_name].append(person['name'])

    with open('completed_trainings_by_fiscal_year.json', 'w') as file:
        json.dump(completed_in_fiscal_year, file)

def find_expiring_trainings(trainings_data, reference_date):
    reference_date = datetime.strptime(reference_date, "%m/%d/%Y")
    expiring_trainings = []

    for person in trainings_data:
        for completion in person['completions']:
            if completion['expires']:
                expiration_date = datetime.strptime(completion['expires'], "%m/%d/%Y")
                days_until_expiration = (expiration_date - reference_date).days

                if days_until_expiration <= 30:
                    expiring_trainings.append({
                        'name': person['name'],
                        'training_name': completion['name'],
                        'expires_soon': days_until_expiration >= 0
                    })

    with open('expiring_trainings.json', 'w') as file:  
        json.dump(expiring_trainings, file)

training_completion_count(file_contents)

trainings_list = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
fiscal_year = 2024
completed_in_fiscal_year(file_contents, trainings_list, fiscal_year)

reference_date = "10/01/2023"
find_expiring_trainings(file_contents, reference_date)
