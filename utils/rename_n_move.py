import os
import json
import shutil


def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
        print(f"'{directory_name}' created")
    else:
        print(f"'{directory_name}' already exists")


def rename_n_move(base_path, image_type):
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)

        if os.path.isdir(folder_path):

            files_in_folder = os.listdir(folder_path)

            for filename in files_in_folder:
                if filename.endswith('.json'):
                    with open(os.path.join(folder_path, filename), 'r') as file:
                        json_data = json.load(file)

                        bbox = json_data["request"]["payload"]["input"]["bounds"]["bbox"]

                        if bbox == bbox_ref[0]:
                            suffix = 0
                        elif bbox == bbox_ref[1]:
                            suffix = 1
                        elif bbox == bbox_ref[2]:
                            suffix = 2
                        elif bbox == bbox_ref[3]:
                            suffix = 3
                        elif bbox == bbox_ref[4]:
                            suffix = 4
                        elif bbox == bbox_ref[5]:
                            suffix = 5
                        elif bbox == bbox_ref[6]:
                            suffix = 6
                        elif bbox == bbox_ref[7]:
                            suffix = 7
                        elif bbox == bbox_ref[8]:
                            suffix = 8
                        elif bbox == bbox_ref[9]:
                            suffix = 9
                        elif bbox == bbox_ref[10]:
                            suffix = 10
                        elif bbox == bbox_ref[11]:
                            suffix = 11
                        elif bbox == bbox_ref[12]:
                            suffix = 12
                        elif bbox == bbox_ref[13]:
                            suffix = 13
                        elif bbox == bbox_ref[14]:
                            suffix = 14
                        elif bbox == bbox_ref[15]:
                            suffix = 15
                        elif bbox == bbox_ref[16]:
                            suffix = 16
                        elif bbox == bbox_ref[17]:
                            suffix = 17
                        elif bbox == bbox_ref[18]:
                            suffix = 18
                        elif bbox == bbox_ref[19]:
                            suffix = 19
                        elif bbox == bbox_ref[20]:
                            suffix = 20
                        elif bbox == bbox_ref[21]:
                            suffix = 21
                        elif bbox == bbox_ref[22]:
                            suffix = 22
                        elif bbox == bbox_ref[23]:
                            suffix = 23
                        elif bbox == bbox_ref[24]:
                            suffix = 24
                        elif bbox == bbox_ref[25]:
                            suffix = 25

                        time = json_data["request"]["payload"]["input"]["data"][0]["dataFilter"]["timeRange"]["from"][:10]

                elif filename.endswith('.png'):
                    png_file = filename

            new_png_name = f"{time}_Area-{suffix}.png"
            os.rename(os.path.join(folder_path, png_file),
                      os.path.join(folder_path, new_png_name))

            shutil.move(new_png_name, "../../images/" + image_type)


if __name__ == '__main__':
    image_type_lst = ["NDMI", "NDVI", "NBRRAW"]

    bbox_ref = [[146.8856778125, -37.682759375, 147.7338835, -36.9382090625],
                [146.8856778125, -36.9382090625, 147.7338835, -36.193658750000004],
                [147.7338835, -37.682759375, 148.5820891875, -36.9382090625],
                [147.7338835, -36.9382090625, 148.5820891875, -36.193658750000004],
                [148.5820891875, -37.682759375, 149.43029487500002, -36.9382090625],
                [148.5820891875, -36.193658750000004,
                    149.43029487500002, -35.4491084375],
                [149.43029487500002, -37.682759375,
                    150.2785005625, -36.9382090625],
                [149.43029487500002, -36.9382090625,
                    150.2785005625, -36.193658750000004],
                [149.43029487500002, -36.193658750000004,
                    150.2785005625, -35.4491084375],
                [150.2785005625, -35.4491084375, 151.12670625, -34.704558125000005],
                [150.2785005625, -33.9600078125, 151.12670625, -33.2154575],
                [150.2785005625, -33.2154575, 151.12670625, -32.4709071875],
                [150.2785005625, -32.4709071875, 151.12670625, -31.726356875],
                [151.12670625, -33.2154575, 151.9749119375, -32.4709071875],
                [151.12670625, -31.726356875, 151.9749119375, -30.9818065625],
                [151.12670625, -30.23725625, 151.9749119375, -29.4927059375],
                [151.9749119375, -32.4709071875, 152.823117625, -31.726356875],
                [151.9749119375, -31.726356875, 152.823117625, -30.9818065625],
                [151.9749119375, -30.9818065625, 152.823117625, -30.23725625],
                [151.9749119375, -30.23725625, 152.823117625, -29.4927059375],
                [151.9749119375, -29.4927059375, 152.823117625, -28.748155625000003],
                [152.823117625, -31.726356875, 153.6713233125, -30.9818065625],
                [152.823117625, -30.9818065625, 153.6713233125, -30.23725625],
                [152.823117625, -30.23725625, 153.6713233125, -29.4927059375],
                [152.823117625, -29.4927059375, 153.6713233125, -28.748155625000003],
                [152.823117625, -28.748155625000003, 153.6713233125, -28.0036053125]]

    for image_type in image_type_lst:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        temp_path = os.path.join(current_directory, "../images")
        create_directory(os.path.join(temp_path, image_type))

        base_path = "../download/" + image_type
        rename_n_move(base_path, image_type)
