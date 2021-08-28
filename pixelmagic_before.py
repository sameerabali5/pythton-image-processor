"""Contains solutions to Pixelmagic
CPE101
Section <05>
Project 5, Pixelmagic
Name: <Sameera> <Balijepalli>
Cal Poly User: <sbalijep>
"""
import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: python pixelmagic.py <mode> <image>")
        sys.exit()
    try:
        pixels = read_file2(sys.argv[2])
        header = pixels[0:3]
        pixels = pixels[3:] #do not count header
        _groups = grouped2(pixels)
        if sys.argv[1] == "decode":
            decoded_puzzle = find_image(_groups)
            write_file("decoded.ppm", decoded_puzzle, header)
        elif sys.argv[1] == "fade":
            _fading = True
            if len(sys.argv) != 6:
                print("Usage: python pixelmagic.py fade <image> <row> <col> <radius>")
                sys.exit()
            faded_image = fade_image(_groups, int(sys.argv[2]),int(sys.argv[3]),\
                int(sys.argv[4]),header)
            write_file("faded.ppm", faded_image, header)
        else:
            print("Error: Invalid Mode")
    except IOError:
        print("Error: Unable to Open ", pixels)
        sys.exit()


def read_file(file_name):
    """Function reads image file
    Args:
        file_name(str): taken from command line
    Returns:
        image_list(list): list of all pixels from file
    """
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


def read_file2(file_name):
    with open(file_name, 'r') as f:
        file = f.readline()
        image_data = file[0:]
        image_list = [(i.strip()).split() for i in image_data]
    return image_list

def read_file(file_name):
    with open(file_name) as _r:
        _pixs = _r.readlines()
    _data = _pixs[0:]
    _datalst = [(space.strip()).split() for space in _data]
    return _datalst


def write_file(file_name, pixel_groups, line):
    """Writes image into specified file name
    Args:
        file(str): written in main
        pixel_groups(list): pixels in groups of 3
        line(list): header of file
    Returns:
        _f(ppm): ppm file
    """
    with open(file_name, 'w') as _o:
        _o.write("P3\n") #writes file type
        _o.write("{0}\t{1}\n".format(line[0], line[1]))
        _o.write("{0}\n".format(line[2]))
        for item, pixel in enumerate(pixel_groups):
            _o.write('{0:d}\n'.format(pixel))


def grouped(pixels):
    """Function returns pixels in groups of 3
    Args:
        pixels(ppm): taken from command line
    Returns:
        list: culmination of both lists
    """
    j = 0
    list_1 = []
    list_2 = []
    for i in pixels:
        j += 1
        if j <= 3:
            list_2.append(i)
        else:
            list_1.append(list_2)
            list_2 = []
            list_2.append(i)
            j = 1
    return list_1 + [list_2]

def grouped2(pixels):
    grouped = []
    for i in pixels:
        val = [int(data) for data in i]
        grouped.append(val)
    return grouped

def find_image(grouped):
    """Function returns decoded image
    Args:
        grouped(ppm): list of list of pixels
    Returns:
        decoded(ppm): decoded image
    """
    for i in grouped:
        i[0] = i[0] * 10 #increases value of red components
        if i[0] > 225:
            i[0] = 225
        i[1] = i[0] #sets green components equal to red
        i[2] = i[0] #sets blue components equal to red
    return grouped


def fade_image(grouped, row, col, radius, line):
    """Function returns faded image specks
    Args:
        grouped(list): list of lists in groups of 3
        row(int): taken from command line 
        col(int): taken from command line
        radius(int): taken from command line
        line(list): header info
    Returns:
        list: faded image's list of lists
    """
    _width = line[0]
    for i, _j in enumerate(grouped):
        #calculations for x
        pixelx = i / _width
        _x = pixelx - row
        #calculations for y
        pixely = i % _width
        _y = pixely - col
        distance = ((_x)**2 + (_y)**2)**0.5 #calculates distance
        scale_val = (radius - distance) / radius #distance from pixel to point
        if scale_val < 0.2:
            scale_val = 0.2
        #performs calculation for each element within list of lists
        _j[0] = int(_j[0]*scale_val)
        _j[1] = int(_j[1]*scale_val)
        _j[2] = int(_j[2]*scale_val)
    return grouped


if __name__ == "__main__":
    main()

"""
def read_file(file_name):
    #"""#Function reads image file
    #Args:
        #file_name(str): taken from command line
    #Returns:
        #image_list(list): list of all pixels from file
    """
    # with open(file_name, 'r') as f:
    #     pixels = f.readline()[0:]
    #     image_list = []
    #     while True: #runs until False
    #         pixels = f.readline()
    #         if pixels == '':
    #             break
    #         line_data = pixels.split()
    #         for i in line_data:
    #             image_list.append(int(i)) #creates list
    #     return image_list
"""

def read_file(file_name):
    with open(file_name) as _r:
        _skip = _r.readline()[0:]
        _pixlst = []
        while not False:
            pixels = _r.readline()
            if pixels == '':
                break
            _data = pixels.split()
            for _i in _data:
                _pixlst.append(int(_i))
        return _pixlst