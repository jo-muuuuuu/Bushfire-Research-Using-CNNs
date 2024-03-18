import shutil
import os


def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
        print(f"'{directory_name}' created")
    else:
        print(f"'{directory_name}' already exists")


def sort_images(base_path):
    with open("OUTPUT_TEXT_FILE", "r") as label_file:
        line = label_file.readline()
        labels = line.strip().split(" ")

    for folder in os.listdir(base_path):
        if folder == "NBRRAW":
            continue
        else:
            folder_path = os.path.join(base_path, folder)

            # print(folder_path)
            if folder == "NDMI":
                dest_dir = "../data/NDMI"
            elif folder == "NDVI":
                dest_dir = "../data/NDVI"

            if os.path.isdir(folder_path):

                files_in_folder = sorted(os.listdir(folder_path))
                index = 0

                for filename in files_in_folder:
                    if filename.endswith('.png'):
                        png_dir = os.path.join(folder_path, filename)

                        if labels[index] == "1":
                            shutil.move(png_dir, dest_dir+"/Burned")
                        else:
                            shutil.move(png_dir, dest_dir + "/Unburned")

                        index += 1


if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.abspath(__file__))

    create_directory(os.path.join(current_directory, "../data/NDMI"))
    create_directory(os.path.join(current_directory, "../data/NDVI"))
    create_directory(os.path.join(current_directory, "../data/NDMI/Burned"))
    create_directory(os.path.join(current_directory, "../data/NDVI/Burned"))
    create_directory(os.path.join(current_directory, "../data/NDMI/Unburned"))
    create_directory(os.path.join(current_directory, "../data/NDVI/Unburned"))

    base_path = "../images"
    sort_images(base_path)
