import os
import json
changed_images_json = 'C:\\Users\\asdpa\\Downloads\\Levir-CC-dataset\\LevirCCcaptions.json'
directory = 'D:\\Python\\robustChanges\\RobustChangeCaptioning\\data\\nsc_images'
new_directory = 'C:\\Users\\asdpa\\Downloads\\Levir-CC-dataset\\images\\nsc_images'
split_json = 'C:\\Users\\asdpa\\Downloads\\Levir-CC-dataset\\images\\splits.json'

def get_file_number(filename) -> int:
    return int(filename.split('_')[1].split('.')[0])

def change_dir():
    #1 - 6815 -> train
    #6816 - 8148 -> val
    #8149 - 10077 -> test
    #open the json file
    for filename in os.listdir(directory):
        number = 8148
        number += get_file_number(filename)
        new_name = "CLEVR_semantic_" + str(number).zfill(6) + ".png"
        os.rename(os.path.join(directory, filename), os.path.join(new_directory, new_name))

#change_dir()

def default_to_nonsemantic():

    for filename in os.listdir(directory):
        number = filename.split('_')[2].split('.')[0]
        new_name = "CLEVR_nonsemantic_" + number + ".png"
        os.rename(os.path.join(directory, filename), os.path.join(new_directory, new_name))

#default_to_nonsemantic()

def get_train_val_test():
    
    data = json.load(open(changed_images_json))
    
    i = 0
    train = []
    while data["images"][i]["filepath"] == "train":
        train.append(data["images"][i]["filename"])
        i += 1
    
    val = []
    while data["images"][i]["filepath"] == "val":
        val.append(data["images"][i]["filename"])
        i += 1
    
    test = []
    for image in data["images"][i:]:
        test.append(image["filename"])
    
    return train, val, test
        
def delete_if_not_used(type):
    current_directory = 'C:\\Users\\asdpa\\Downloads\\Levir-CC-dataset\\images\\' + type + '\\B'
    train, val, test = get_train_val_test()
    allTypes = {
        "train": train,
        "val": val,
        "test": test
    }

    for filename in os.listdir(current_directory):
        if filename not in allTypes[type]:
            os.remove(os.path.join(current_directory, filename))

    #enumerate rest of the files
    i = 1
    for filename in os.listdir(current_directory):
        new_name = type + "_" + str(i).zfill(6) + ".png"
        os.rename(os.path.join(current_directory, filename), os.path.join(current_directory, new_name))
        i += 1

#delete_if_not_used("test")

def create_split_json():
    train = list(range(1, 6816))
    val = list(range(6816, 8149))
    test = list(range(8149, 10078))

    data = {
        "train": train,
        "val": val,
        "test": test
    }

    with open(split_json, "w") as outfile:
        json.dump(data, outfile)

#create_split_json()

def change_filename_to_json():
    data = json.load(open(changed_images_json))
    i = 0
    for filename in os.listdir(directory):
        data["images"][i]["filename"] = filename
        i += 1

    with open(changed_images_json, "w") as outfile:
        json.dump(data, outfile)

#change_filename_to_json()

def delete_no_changes():
    no_change_json_directory = 'D:\\Python\\robustChanges\\RobustChangeCaptioning\\data\\no_change_captions.json'
    data = json.load(open(no_change_json_directory))

    for filename in data:
        number = filename.split('_')[2].split('.')[0]
        name = "CLEVR_nonsemantic_" + str(number).zfill(6) + ".png"
        os.remove(os.path.join(directory, name))

#delete_no_changes()

def renumarate_files():
    i = 0
    for filename in os.listdir(directory):
        new_name = "CLEVR_nonsemantic_" + str(i).zfill(6) + ".png"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
        i += 1

renumarate_files()