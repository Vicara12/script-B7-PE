import os
import csv
import time

file_path = "./files/"


def show_time (started_time, progress):
	seconds_left = round((1-progress)*(time.time()-started_time)/progress)
	print("Estimated time left: ", end = "")
	# print hours
	if (int(seconds_left/3600) != 0):
		print(int(seconds_left/3600), "h ", end = "")
	# print minutes
	if (int(seconds_left/60) != 0):
		minutes = int(seconds_left/60)
		print(minutes%60, "m ", end = "")

	print(seconds_left%60, "s")


def get_data (file_names, iterations, progress = True, actualization_time = 2):
	# returns a dictionary with key = file_name and a list with two lists as value
	# the first one with size in RAR, the second size with ZIP, the third time with RAR
	# and the last time with ZIP

	data = {}

	for file in file_names:
		data.setdefault(file, 
			[os.path.getsize(file_path+file),[],[],[],[]])

	init_time = time.time()
	started_time = time.time()

	for i in range(iterations):
		if (progress and time.time() > actualization_time + init_time):
			print("Currently at:", str(round(i/iterations*100, 2)) + "%")
			show_time(started_time, i/iterations)
			print()
			init_time = time.time()
			
		for file in file_names:
			# for the RAR part
			initial = time.time()
			os.system("rar a file.rar " + file_path + file + " >terminal.out")
			final = time.time()
			data[file][1].append(os.path.getsize("file.rar"))
			os.system("rm file.rar")
			data[file][3].append(final - initial)

			# for the zip part
			initial = time.time()
			os.system("zip file.zip " + file_path + file + " >terminal.out")
			final = time.time()
			data[file][2].append(os.path.getsize("file.zip"))
			os.system("rm file.zip")
			data[file][4].append(final - initial)

	return data
	

def print_times (data, precission = 5):
	for file in data.keys():
		print("~~~~~~", file, "(", data[file][0], "bytes) ~~~~~~")

		print("  *RAR (s): ", end= " ")
		for item in data[file][1]:
			print(item, end = " ")
		print("\n")

		print("  *ZIP (s): ", end= " ")
		for item in data[file][2]:
			print(item, end = " ")
		print("\n")

		print("  *RAR (t): ", end= " ")
		for item in data[file][3]:
			print(round(item, precission), end = " ")
		print("\n")

		print("  *ZIP (t): ", end= " ")
		for item in data[file][4]:
			print(round(item, precission), end = " ")
		print("\n")



def WriteListToCSV(csv_file,csv_columns,data_list):
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(csv_columns)
        for data in data_list:
            writer.writerow(data) 
    return



def generate_csv (data, n_iterations):
	#generates the csv file
	os.system("touch labels.csv RAR_size.csv ZIP_size.csv RAR_time.csv ZIP_time.csv")

	labels = []
	rar_size = []
	zip_size = []
	rar_time = []
	zip_time = []

	# make the labels list
	for file in data.keys():
		labels.append([file, data[file][0]])

	# make the rar_size list
	for iteration in range(n_iterations):
		it_data = []
		for file in data.keys():
			it_data.append(data[file][1][iteration])
		rar_size.append(it_data)

	# make the zip_size list
	for iteration in range(n_iterations):
		it_data = []
		for file in data.keys():
			it_data.append(data[file][2][iteration])
		zip_size.append(it_data)

	# make the rar_time list
	for iteration in range(n_iterations):
		it_data = []
		for file in data.keys():
			it_data.append(data[file][3][iteration])
		rar_time.append(it_data)

	# make the zip_time list
	for iteration in range(n_iterations):
		it_data = []
		for file in data.keys():
			it_data.append(data[file][4][iteration])
		zip_time.append(it_data)

	# write all lists to csv

	WriteListToCSV("labels.csv", ["file_name", "original_size"], labels)
	WriteListToCSV("RAR_size.csv", list(data.keys()), rar_size)
	WriteListToCSV("ZIP_size.csv", list(data.keys()), zip_size)
	WriteListToCSV("RAR_time.csv", list(data.keys()), rar_time)
	WriteListToCSV("ZIP_time.csv", list(data.keys()), zip_time)


def main():

	iterations = int(input("Iterations: "))
	gen_csv = input("Generate csv? [y/n]: ") == "y"
	show = input("Show results at the end? [y/n]: ") == "y"
	progress = input("Show progress? [y/n]: ") == "y"

	time = 0

	if progress:
		time = int(input("Show progress each (seconds): "))

	file_names = os.listdir(file_path)

	print("\n\nStarting data collection...\n\n")

	data = get_data(file_names, iterations ,progress, time)

	if show:
		print_times(data)

	if gen_csv:
		print("\n\nGenerating csv files...")
		generate_csv(data, iterations)
		print("\nDone")


main()