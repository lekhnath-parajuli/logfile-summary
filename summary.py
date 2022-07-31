import re
import csv

sample_error = {
    "The ticket was modified while updating",
    "Permission denied while closing ticket",
    "Tried to add information to closed ticket",
    "Timeout while retrieving information",
    "Ticket doesn't exist",
    "Connection to DB failed",
    "Timeout while retrieving information",
}

def error_messages(file: str) -> dict:
    error_stat = {}
    with open(file, 'r') as log_file:
        logs = log_file.read()
        for err in sample_error:
            found = re.findall(err, logs)
            error_stat[err] = len(found)
    return error_stat


def user_stats(file: str) -> dict:
    user_stats = {}
    with open(file, 'r') as log_file:
        logs = log_file.read()
        users = [user[1:-1] for user in re.findall(r'\([a-zA-Z.-]*\)', logs)]
        error_type = re.findall('(ERROR|INFO)', logs)

        for user, err in zip(users, error_type):
            if user in user_stats.keys():
                user_stats[user][err] += 1
                continue
            user_stats[user] = {}
            user_stats[user]['ERROR'] = 0
            user_stats[user]['INFO'] = 0
    return user_stats

def csv_writer(file: str, header: list, data: dict):
    with open(file, 'w') as opened:
        writer = csv.DictWriter(opened, header)
        writer.writeheader()
        writer.writerows(data)


file = './syslog.log'


errors_header = ["Error", "Count"]
errors_dict = sorted(error_messages(file).items(), key=lambda x: x[1], reverse=True)
errors = [{"Error": err, "Count": count} for err, count in errors_dict]
csv_writer('./error_message.csv', errors_header, errors)

users_header = ["Username", "INFO", "ERROR"]
users_dict = sorted(user_stats(file).items(), key=lambda x: x[0])
users = [{"Username": user[0], "INFO": user[1]["INFO"], "ERROR": user[1]["ERROR"]} for user in users_dict]
csv_writer('./user_statistics.csv', users_header, users)