import csv

def add_safe(dictionary, file_key, user_key, value):
    if not file_key in dictionary:
        dictionary[file_key] = {}
    if not user_key in dictionary[file_key]:
        dictionary[file_key][user_key] = []

    dictionary[file_key][user_key].append(value)

def get_area(x):
    xmin, ymin, xmax, ymax = x
    return (xmax - xmin) * (ymax - ymin)   # xmax-xmin * ymax-ymin

def get_interserction(a, b):
    # a starts before b (within x-axis)
    if a[0] > b[0]:
        a, b = b, a

    # size of common part in x-axis
    x_common = a[2] - b[0] if a[2] > b[0] else 0

    # a starts before b (within y-axis)
    if a[1] > b[1]:
        a, b = b, a

    # size of common part in a-axis
    y_common = a[3] - b[1] if a[3] > b[1] else 0
    return x_common * y_common

def get_intersection_over_union(a, b):
    a_area = get_area(a)
    b_area = get_area(b)

    intersection_area = get_interserction(a, b)
    union_area = (a_area + b_area - intersection_area)

    return intersection_area / union_area

def get_smaller(a, b):
    return a if get_area(a) < get_area(b) else b

def get_intersection_over_smaller(a, b):
    '''
    Return ration between intersection and the area of the smaller. 
    I.e. if one box contains the other it's still ~1.
    '''
    a_area = get_area(a)
    b_area = get_area(b)

    intersection_area = get_interserction(a, b)
    return intersection_area / (a_area if a_area < b_area else b_area)

def get_box_from_row(box_row):
    return int(box_row[6]), int(box_row[7]), int(box_row[8]), int(box_row[9])


def is_confirmed_by_other_user(files_users_boxes, file_key, user_key, box):
    '''
    A box is confirmed by another user if another user also annoted a box that either:
    - intersection_over_union > 0.5 -> they mostly overlap each other
    - intersection_over_smaller > 0.9 -> the bigger one covers 90 % of the smaller one
    '''
    for other_user_key in files_users_boxes[file_key]:
        if other_user_key == user_key:
            continue
        
        for box_row in files_users_boxes[file_key][other_user_key]:
            other_box = get_box_from_row(box_row)
            if get_intersection_over_union(box, other_box) > 0.5 or get_intersection_over_smaller(box, other_box) > 0.9:
                return True

    return False

def is_not_added_by_previous_user(files_users_boxes, file_key, user_key, box):
    '''
    A box has been added by previous user if previous user also annoted a box that either:
    - intersection_over_union > 0.5 -> they mostly overlap each other
    - intersection_over_smaller > 0.9 -> the bigger one covers 90 % of the smaller one
    '''
    for other_user_key in files_users_boxes[file_key]:
        if other_user_key == user_key:
            return True
        
        for box_row in files_users_boxes[file_key][other_user_key]:
            other_box = get_box_from_row(box_row)
            if get_intersection_over_union(box, other_box) > 0.5 or get_intersection_over_smaller(box, other_box) > 0.90:
                return False

files_users_boxes = {}
file_name = "../pacificdrone/drone_ocean_labels_complete.csv"
file_name_output = "../pacificdrone/drone_ocean_labels_complete_cleaned.csv"

# Load data to `files_users_boxes` for processing
with open(file_name, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    _ = next(reader, None)  # skip the headers

    for row in reader:
        pic_name, user = row[1], row[2]        
        add_safe(files_users_boxes, pic_name, user, row)

MIN_AREA = 50
MAX_AREA = 180144
MIN_DIM = 7
MAX_DIM = 512
def is_acceptable_box(box):
    area = get_area(box)
    if area < MIN_AREA or area > MAX_AREA:
        return False

    xmin, ymin, xmax, ymax = box
    h = ymax - ymin
    w = xmax - xmin

    if h < MIN_DIM or h > MAX_DIM: return False
    if w < MIN_DIM or w > MAX_DIM: return False

    return True

def is_allowed_user(box_row):
    black_list = [
        "debricen",
        "dcameirinha",
        "not-logged-in-cb860046772af2394015",
        "Cedrikchavez",
        "not-logged-in-a1951b8866631729b988",
        "not-logged-in-c400ca4c1df65b4c6bbd",
        "not-logged-in-1d632c1121910f00d2d0",
        "RubyDee",
        "not-logged-in-e0261965dc5ff056279e",
        "not-logged-in-0789e1b5096fa3ca1572",
        "not-logged-in-f02a8a1ea62b3d4569aa",
        "not-logged-in-2cf6fc5957277004ac3f",
        "kawills",
        "ktquinn13",
        "not-logged-in-b396ffbeded7faba4f0e",
        "not-logged-in-bed2d75d80ce9d50d635",
        "Judy322",
        "anonymoushelper",
        "daniblar",
        "not-logged-in-2a4d02b1ec4b990ce8d7",
        "not-logged-in-160c71faa6abe948ffcb",
        "not-logged-in-f93565a5b5df88d8a633",
        "not-logged-in-35e02a593d99f4f9862f",
        "qilo",
        "not-logged-in-bc86d6c995e6377ca484",
        "not-logged-in-313cb1c6028c88d00bde",
        "not-logged-in-f72be762552cb9e204ec"
    ]
    user = box_row[2]
    return (not user in black_list)


filtered_boxes = []
filtered_out_boxes = []
for file_key in files_users_boxes:
    users_boxes = files_users_boxes[file_key]
    for user_key in users_boxes:
        for box_row in users_boxes[user_key]:
            box = get_box_from_row(box_row)

            #if is_not_added_by_previous_user(files_users_boxes, file_key, user_key, box) and is_acceptable_box(box):
            if is_acceptable_box(box) and is_allowed_user(box_row):
                filtered_boxes.append(box_row)   
            else:
                filtered_out_boxes.append(box_row)
                
print(len(filtered_boxes), len(filtered_out_boxes))

with open(file_name_output, 'w') as csvfile:
    for row in filtered_boxes:
        print(", ".join(row), file=csvfile)