from PIL import Image

shredded_image = Image.open('TokyoPanoramaShredded.png')
shredded_data = shredded_image.getdata()
NUMBER_OF_COLUMNS = 20
shred_width = shredded_image.size[0]//NUMBER_OF_COLUMNS
shred_height = shredded_image.size[1]


def get_pixel_value(x, y):
    width, height = shredded_image.size
    pixel = shredded_data[y * width + x]
    return pixel


def get_diff(i, j):
    diff = 0
    for k in range(shred_height):
        pixela = get_pixel_value((shred_width)*(i+1)-1, k)
        pixelb = get_pixel_value((shred_width)*(j), k)
        r = abs(pixela[0] - pixelb[0])
        g = abs(pixela[1] - pixelb[1])
        b = abs(pixela[2] - pixelb[2])
        diff += r + g + b
    return diff/3


def get_diff_at_zero(i, j):
    pixela = get_pixel_value((shred_width)*(i+1)-1, 0)
    pixelb = get_pixel_value((shred_width)*(j), 0)
    r = abs(pixela[0] - pixelb[0])
    g = abs(pixela[1] - pixelb[1])
    b = abs(pixela[2] - pixelb[2])
    diff = r + g + b
    return diff/3


# Currently unused
def circular(l, i, j):
    i_maps_j = False
    j_maps_i = False
    for tup in l:
        if tup[0] == i and tup[1] == j:
            i_maps_j = True
        if tup[0] == j and tup[1] == i:
            j_maps_i = True
    return i_maps_j or j_maps_i


def main():
    unshredded = Image.new('RGBA', shredded_image.size)

    # Get initial shred mapping
    shreds = []
    for i in range(NUMBER_OF_COLUMNS):
        shreds.append((0, 0, 9999999))
        for j in range(NUMBER_OF_COLUMNS):
            # Shreds cannot map to themselves
            if i != j:
                temp = i, j, get_diff(i, j)
                if temp[2] < shreds[i][2]:
                    shreds[i] = temp

    # Follow a path through the initial mapping to get the sorted version
    sorted_shreds = [shreds[0]]
    next_shred = shreds[0][1]
    for i in range(1, len(shreds)):
        sorted_shreds.append(shreds[next_shred])
        next_shred = shreds[next_shred][1]

    # Need to find place where there is a jump (image is not contiguous)
    jump = (0, 0)
    for i in range(1, len(sorted_shreds)):
        # Use get_diff_at_zero to get the diff at a particular y value
        temp = i, get_diff_at_zero(sorted_shreds[i-1][0], sorted_shreds[i-1][1])
        if temp[1] > jump[1]:
            jump = temp
    # Rotate the sorted shreds until we no longer have a jump
    for i in range(jump[0]):
        temp = sorted_shreds.pop(0)
        sorted_shreds.append(temp)

    for i in range(NUMBER_OF_COLUMNS):
        shred_num = sorted_shreds[i][0]
        x1, y1, = (shred_width)*(shred_num), 0
        x2, y2 = x1+shred_width, shred_height
        source_region = shredded_image.crop((x1, y1, x2, y2))
        destination_point = (shred_width*i, 0)
        unshredded.paste(source_region, destination_point)
    unshredded.save('unshredded.png', 'PNG')


if __name__ == '__main__':
    main()
