import copy
import statistics

def main():
    pixels = read_file('barbara.ppm')
    header = pixels[0:3]
    pixels = pixels[3:] #skips header
    _groups = grouped(pixels)

    # width, height = header[0:1], header[1:2]
    width, height = header[0], header[1]

    denoised_image = denoise(_groups, width, height, 2, 0.2)
    write_file("denoised-new.ppm", denoised_image, header)


def locate_neighbors(grouped, row, column, width, height, reach):
    """Function finds neighboring pixels
    Args: 
        grouped(list): 2-d array 
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
            
            # row_final = row - int(reach) + col_val
            # col_final = col_val - int(reach) + row_val
            row_final = row - int(reach) + row_val
            col_final = column - int(reach) + col_val
           
            # uncomment this if the center pixel is included in the reach
            if col_final == column and row_final == row:
                 continue
            if col_final >= width or col_final < 0:
                continue
            if row_final >= height or row_final < 0:
                continue

            # final_list = grouped[row_final][col_final]
            # neighbors.append(final_list)
            row_num = (row_final * width) + col_final
            final_int = grouped[row_num][0]
            neighbors.append(final_int)
    return neighbors


# def denoise(grouped, width, height, reach, beta, header): # no need to pass in the header
def denoise(grouped, width, height, reach, beta):
    """Function returns list of neighboring pixels
    Args:
        grouped(list): 2-d array
        width(int): width of image
        height(int): width of image
        reach(int): window of filter
        beta(int): determines if pixel needs to be replaced
        header(int): info about header
    Returns:
        new_pixels(list): list of denoised pixels
    """
    new_pixels = []
    new_pixels = copy.deepcopy(grouped)

    # width = len(new_pixels[0])
    # height = len(new_pixels)
    
    for row in range(height):
        for column in range(width):

            # neighbors = locate_neighbors(new_pixels, row, column, width, height, reach)
            neighbors = locate_neighbors(grouped, row, column, width, height, reach)

            # uncomment this once you fix insertion_sort
            # insertion_sort(neighbors)
            # med = neighbors[len(neighbors)//2]

            med = statistics.median(neighbors) # delete this once you fix insertion sort

            row_num = (row * width) + column

            # original = new_pixels[row][column]
            original = new_pixels[row_num][0]

            # if abs(original - med) / (original + 0.1) > float(beta):
            if abs(original - med) / (original + 0.1) > beta:
                # pixel = new_pixels[row][column]
                new_pixels[row_num][0] = int(med)
                new_pixels[row_num][1] = int(med)
                new_pixels[row_num][2] = int (med)
            # grouped[0] = int(med)
            # grouped[1] = int(med)
            # grouped[2] = int(med)
    return new_pixels


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
    n = 3 #groups it by 3
    grouped = [pixels[i:i+n] for i in range(0,len(pixels), n)]
    return grouped


def insertion_sort(new_list):
    """Function sorts list using insertion sort
    Args:
        new_list: list of 1d array
    Returns:
        None
    """
    size = len(new_list)
    for i in range(1, size):
        j = 1
        while j > 0 and new_list[j - 1] > new_list[j]:
            new_list[j - 1], new_list[j] = new_list[j], new_list[j - 1]
            j -= 1


if __name__ == "__main__":
    main()
