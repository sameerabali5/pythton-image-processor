"""Contains solutions to Pixelmagic
CPE101
Section <05>
Project 5, Pixelmagic
Name: <Sameera> <Balijepalli>
Cal Poly User: <sbalijep>
"""
import sys
import copy


def main():
    if len(sys.argv) < 3:
        print("Usage: python pixelmagic.py <mode> <image>")
        sys.exit()
    try:
        pixels = read_file(sys.argv[2])
        header = pixels[0:3]
        pixels = pixels[3:] #skips header
        _groups = grouped(pixels)
        if sys.argv[1] == "decode":
            decoded_puzzle = find_image(_groups)
            write_file("decoded.ppm", decoded_puzzle, header)
        elif sys.argv[1] == "fade":
            _fading = True
            if len(sys.argv) != 6:
                print("Usage: python pixelmagic.py fade <image> <row> <col> <radius>")
                sys.exit()
            faded_image = fade_image(_groups, int(sys.argv[3]),int(sys.argv[4]),
                int(sys.argv[5]), header)
            write_file("faded.ppm", faded_image, header)
        elif sys.argv[1] == "denoise":
            _denoise = True
            if len(sys.argv) != 5:
                print("Usage: python pixelmagic.py denoise <image> <reach> <beta>")
                sys.exit()
            width, height = header[0], header[1]
            denoised_image = denoise(_groups, width, height, int(sys.argv[3]), 
            float(sys.argv[4]))
            write_file("denoised.ppm", denoised_image, header)
        else:
            print("Error: Invalid Mode")
    except IOError:
        print("Error: Unable to Open " + sys.argv[2])
        sys.exit()


def read_file(file_name):
    """Function reads image file
    Args:
        file_name(str): taken from command line
    Returns:
        _pixlst(list): list of all pixels from file
    """
    with open(file_name) as _r:
        _pixlst = []
        for line in _r:
            if line != "P3\n":
                _new = (line[0:len(line)-1]).split()
                for item in _new:
                    _pixlst.append(int(item)) 
    return _pixlst
    

def write_file(file_name, pixel_groups, line):
    """Function writes image into specified file name
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
        for _i in pixel_groups:
            for _j in _i:
                _o.write('{0:d}\n'.format(_j))


def grouped(pixels):
    """Function returns pixels in groups of 3
    Args:
        pixels(ppm): taken from command line
    Returns:
        list: 2d list
    """
    _n = 3 #groups it by 3
    _grouped = [pixels[_i :_i + _n] for _i in range(0,len(pixels), _n)]
    return _grouped


def find_image(grouped):
    """Function returns decoded image
    Args:
        grouped(ppm): list of list of pixels
    Returns:
        decoded(ppm): decoded image
    """
    for _i in grouped:
        _i[0] = _i[0] * 10 #increases value of red components
        if _i[0] > 225:
            _i[0] = 225
        _i[1] = _i[0] #sets green components equal to red
        _i[2] = _i[0] #sets blue components equal to red
    return grouped


def fade_image(grouped, row, col, radius, width):
    """Function returns faded image specks
    Args:
        grouped(list): list of lists in groups of 3
        row(int): taken from command line 
        col(int): taken from command line
        radius(int): taken from command line
        width(list): header info
    Returns:
        list: faded image in list of lists
    """
    _width = width[0]
    for _i, _j in enumerate(grouped):
        _pixelx = (_i / _width) - row
        _pixely = (_i % _width) - col
        distance = ((_pixelx)**2 + (_pixely)**2)**0.5
        scale_val = (radius - distance) / radius
        if scale_val < 0.2:
            scale_val = 0.2
        _j[0] = int(_j[0]*scale_val)
        _j[1] = int(_j[1]*scale_val)
        _j[2] = int(_j[2]*scale_val)
    return grouped


def insertion_sort(new_list):
    """Function sorts list using insertion sort
    Args:
        new_list: list of 1d array
    Returns:
        None
    """
    for _i in range(1, len(new_list)): 
        _point = new_list[_i]
        _j = _i-1
        while _j >=0 and _point < new_list[_j] : 
                new_list[_j+1] = new_list[_j] 
                _j -= 1
        new_list[_j+1] = _point


def locate_neighbors(grouped, row, column, width, height, reach):
    """Function finds neighboring pixels
    Args: 
        new_pixels(list): 2-d array 
        row(int): row number
        column(int): column number
        width(int): width of image
        height(int): height of image
        reach(int): window filter
    Returns: 
        neighbors(list): list of neighboring pixels
    """
    neighbors = []
    for row_val in range(2*int(reach) + 1):
        for col_val in range(2*int(reach) + 1):
            row_final = row - int(reach) + row_val
            col_final = column - int(reach) + col_val
            if col_final == column and row_final == row:
                 continue
            if col_final >= width or col_final < 0:
                continue
            if row_final >= height or row_final < 0:
                continue
            row_num = (row_final * width) + col_final
            final_int = grouped[row_num][0]
            neighbors.append(final_int)
    return neighbors


def denoise(grouped, width, height, reach, beta):
    """Function returns list of neighboring pixels
    Args:
        grouped(list): 2-d array
        width(int): width of image
        height(int): width of image
        reach(int): window of filter
        beta(int): determines if pixel needs to be replaced
    Returns:
        new_pixels(list): list of denoised pixels
    """
    new_pixels = []
    new_pixels = copy.deepcopy(grouped)
    for row in range(height):
        for column in range(width):
            neighbors = locate_neighbors(grouped, row, column, width, height, reach)
            insertion_sort(neighbors)
            med = neighbors[len(neighbors)//2]
            row_num = (row * width) + column
            original = new_pixels[row_num][0]
            if abs(original - med) / (original + 0.1) > beta:
                new_pixels[row_num][0] = int(med)
                new_pixels[row_num][1] = int(med)
                new_pixels[row_num][2] = int (med)
    return new_pixels


if __name__ == "__main__":
    main()
