import csv

file_name = "../pacificdrone/drone_ocean_labels_complete_cleaned.csv"
file_name_output = "../pacificdrone/drone_ocean_labels_complete_cleaned_converted.csv"

def safe_append(dictionary, key, value):
    if not key in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)

# Load data to `files_boxes` for processing
files_boxes = {}
categories = {}
with open(file_name, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    _ = next(reader, None)  # skip the headers

    for row in reader:
        pic_name, user = row[1], row[2]   
        category = row[5]     
        safe_append(files_boxes, pic_name, row)

        if not category in categories:
            categories[category] = len(categories)

print(len(categories))
print(len(files_boxes))

index = 0
with open(file_name_output, "w") as csvfile:
    for file_key in files_boxes:
        first_box_of_file = files_boxes[file_key][0]     
        size_x, size_y = first_box_of_file[3], first_box_of_file[4]
        
        line_prefix = f"{index} {file_key.strip()} {size_x.strip()} {size_y.strip()}"
        current_line = [line_prefix]
        for box_row in files_boxes[file_key]:
            xmin, ymin, xmax, ymax = int(box_row[6]), int(box_row[7]), int(box_row[8]), int(box_row[9])
            category = categories[box_row[5]]
            current_line.append(f"{category} {xmin} {ymin} {xmax} {ymax}")
        print(" ".join(current_line), file=csvfile) 
        index += 1