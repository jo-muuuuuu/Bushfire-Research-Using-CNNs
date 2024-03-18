import os


def delete_images(base_path):
    files_in_folder = os.listdir(base_path)

    for filename in files_in_folder:
        full_file_path = os.path.join(base_path, filename)

        if (filename.endswith('-4.png') or
                filename.endswith('-11.png') or
                filename.endswith('-12.png') or
                filename.endswith('-14.png') or
                filename.endswith('-16.png')):
            os.remove(full_file_path)


if __name__ == '__main__':
    image_type_lst = ["NDMI", "NDVI", "NBRRAW"]

    for image_type in image_type_lst:
        base_path = "../images" + image_type
        delete_images(base_path)
