"""Contains solutions to Pixelmagic
CPE101
Section <05>
Project 5, Pixelmagic
Name: <Sameera> <Balijepalli>
Cal Poly User: <sbalijep>
"""
import sys


def main():
    try:
        pixels = read_image(sys.argv[1])
        print(pixels)
        header = pixels[0:3]
        del pixels[0:3]
        _groups = pixel_groups(pixels)
        decoded_puzzle = find_image(_groups)
        write_image("decoded.ppm", decoded_puzzle, header)
    except IOError:
        if len(pixels) != 2:
            print("Usage: python pixelmagic.py <mode> <image>")
        elif sys.argv[1] != "decode" or "fade" or "denoise":
            print("Error: Invalid Mode")
        else:
            print("Usage: python pixelmagic.py <mode> <image>")
        sys.exit()

def read_image(file_name):
    f = open(file_name, 'r')
    file_type = f.readline() #Taking out P3
    data_list = []
    while True:
        line = f.readline()
        if line == " ":
            break
        line_list = line.split()
        for sub_comp in line_list:
            data_list.append(int(sub_comp))
    f.close()
    return data_list

def read_image2(file_name):
    with open(file_name, 'r') as f:
        file_type = f.readline()[0:]
        image_list = []
        while True: #runs until False
            pixels = f.readline()
            if pixels == '':
                break
            line_data = pixels.split()
            for i in line_data:
                image_list.append(int(i)) #creates list of lists
        return image_list

def pixel_groups(pixels):
    i = 0
    f_list = []
    s_list = []
    for num in pixels:
        i += 1
        if i <= 3:
            s_list.append(num)
        else:
            f_list.append(s_list)
            s_list = []
            s_list.append(num)
            i = 1
    return f_list + [s_list]


def find_image(pixel_groups):
    """Function outputs decoded image to a file
    Args:
        pixels(ppm): input image file
    Returns:
        decoded(ppm): decoded image
    """
    for pixels in pixel_groups:
        pixels[0] = pixels[0] * 10
        if pixels[0] > 225:
            pixels[0] = 225
        pixels[1] = pixels[0]
        pixels[2] = pixels[0]
    return pixel_groups


def write_image(file, pixel_groups, header):
    _f = open(file, "w")
    _f.write("P3\n")
    _f.write("{0}{1}\n".format(header[0], header[1]))
    _f.write("{0}\n".format(header[2]))
    for p in pixel_groups:
        for pixel in p:
            _f.write('{0:d}\n'.format(pixel))
    _f.close()

if __name__ == "__main__":
    main()