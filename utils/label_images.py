import png
import os


base_path = "../images/NBRRAW"
label_file = open('OUTPUT_TEXT_FILE', 'w')

for filename in sorted(os.listdir(base_path)):
    if filename.endswith('.png'):
        png_dir = os.path.join(base_path, filename)

        reader = png.Reader(png_dir)
        width, height, pixels, metadata = reader.read_flat()

        bit_depth = metadata['bitdepth']
        planes = metadata['planes']
        bytes_per_pixel = bit_depth // 8 * planes

        burned = 0
        unburned = 0

        for y in range(height):
            for x in range(width):
                offset = (y * width + x) * bytes_per_pixel
                pixel = pixels[offset:offset + bytes_per_pixel]

                if bit_depth == 8:
                    if planes == 3:  # RGB
                        red, green, blue = pixel

                    if red < 96:
                        burned += 1
                    else:
                        unburned += 1

        if burned / (burned + unburned) >= 0.25:  # Set a threshold
            label_file.write("1 ")
        else:
            label_file.write("0 ")

label_file.close()
