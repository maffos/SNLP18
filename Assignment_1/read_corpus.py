import json

with open("/home/matthias/Schreibtisch/Uni/6.Semester/SNLP/Assignments/Assignment_1/hin.json", 'r') as data_file:
	data = json.load(data_file)
	for key in data:
		with open("/home/matthias/Schreibtisch/Uni/6.Semester/SNLP/Assignments/Assignment_1/hin.id", 'a') as id_file:
			id_file.write(key["id_str"])
			id_file.write("\n")


