from random import randrange


def xword_args(size=None, max_word_len=None, max_black_len=None):
    '''Handles default argument assignment.'''
    if size is None:
        num_sqr = 15
    else:
        if size.lower() == "s":
            num_sqr = 15
        elif size.lower() == "l":
            num_sqr = 21
        else:
            raise ValueError('size argument must be either "S" or "L".')
    if max_word_len is None:
        max_word_len = 5
    elif max_word_len > num_sqr:
        raise ValueError('"max_word_len" must be <= ' + num_sqr + ', the number\
                of squares in all rows and columns.')
    if max_black_len is None:
        max_black_len = 4
    elif max_black_len > num_sqr:
        raise ValueError('"max_blanks" must be <= ' + num_sqr + ', the number\
                of squares in all rows and columns.')
    return num_sqr, max_word_len, max_black_len


def xword_random_row(size=None, max_word_len=None, max_black_len=None):
    '''Generates a 'valid' crossword row.
    Valid crossword row specifications:
        - 15x15 or 21x21 grid (size="s" or "l")
        - minimum word length = 3 letters
    '''
    # Handle default argument assignments.
    variables = xword_args(size, max_word_len, max_black_len)
    num_sqr = variables[0]
    max_word_len = variables[1]
    max_black_len = variables[2]
    # min_word_len is dictated by typical crossword structure.
    min_word_len = 3
    # Generate psuedo-random row.
    row = []
    word_start_ind = randrange(0, max_black_len + 1)
    row.extend([0] * word_start_ind)
    while (len(row) <= num_sqr - min_word_len):
        word_len = randrange(min_word_len, max_word_len + 1)
        row.extend([1] * word_len)
        black_len = randrange(1, max_black_len + 1)
        row.extend([0] * black_len)
    ref_ind = num_sqr - min_word_len
    ref_sqr_1 = row[ref_ind - 1]
    ref_sqr_2 = row[ref_ind - 2]
    ref_sqr_3 = row[ref_ind - 3]
    if len(row) > ref_ind:
        row = row[:ref_ind]
    if ref_sqr_1 == 0:
        row.extend([randrange(0, 2)] * min_word_len)
    else:  # ref_sqr_1 == 1
        if ref_sqr_2 == 0:
            num_on = randrange(2, min_word_len + 1)
            row.extend([1] * num_on)
            row.extend([0] * (min_word_len - num_on))
        else:  # ref_sqr_2 == 1
            if ref_sqr_3 == 0:
                start_num = 1
            else:  # ref_sqr_3 == 1
                start_num = 0
            num_on = randrange(start_num, min_word_len + 1)
            row.extend([1] * num_on)
            row.extend([0] * (min_word_len - num_on))
    return row


def look_left(row, index):
    '''Returns a value that indicates what may or must go in a square (index)
    in a crossword row (list) based on its left previous (up to three) squares.
    Returned values may be:
        0: Current square must be 'off'/black, and thus the list must have
           a zero integer at this index.
        1: Current square must be 'on'/white, and thus the list must have
           a one integer at this index.
        2: Current square may be 'on' or 'off', and thus the list must have
           either a one or zero integer at this index.
    '''
    min_word_len = 3
    num_sqr = len(row)
    val_1 = row[index - 1]
    val_2 = row[index - 2]
    val_3 = row[index - 3]
    if index < min_word_len:
        if val_1 == 0:
            on_or_off = 2
        else:  # val_1 == 1
            on_or_off = 1
    elif index >= min_word_len and index <= num_sqr - min_word_len:
        if val_1 == 0:
            if val_2 == 0:
                on_or_off = 2
            else:  # val_2 == 1
                on_or_off = 2
        else:  # val_1 == 1
            if val_2 == 0:
                on_or_off = 1
            else:  # val_2 == 1
                if val_3 == 1:
                    on_or_off = 2
                else:  # val_3 == 0
                    on_or_off = 1
    else:  # index > num_sqr - min_word_len
        if val_1 == 0:
            on_or_off = 0
        else:  # val_1 == 1
            if val_2 == 0:
                on_or_off = 1
            else:  # val_2 == 1
                if val_3 == 1:
                    on_or_off = 2
                else:  # val_3 == 0
                    on_or_off = 1
    return on_or_off


def look_up(matrix, row_num, index):
    '''Returns a value that indicates what may or must go in a square (index)
    in the crossword row (list) based on its adjacent squares in the up or down
    direction. Not applicable for the first row. All other rows 'check' upward,
    up to three sqaures, except for the center row; the center row must check
    up three and down three to ensure symmetry and validity in the crossword.
    If there is conflict in the center row, the squares in the upward direction
    take presendence over the downward direction.
    Returned values may be:
        0: Current square must be 'off'/black, and thus the list must have
           a zero integer at this index.
        1: Current square must be 'on'/white, and thus the list must have
           a one integer at this index.
        2: Current square may be 'on' or 'off', and thus the list must have
           either a one or zero integer at this index.
        3: Current square must be 'off'/black, the list must have a zero at
           this index, and the value directly below this value must be
           changed from a one to a zero.
        4: Current square must be 'on'/white, the list must have a one at this
           index, and the value directly below this value must be changed from
           a zero to a one.
    '''
    min_word_len = 3
    num_rows = len(matrix)
    val_1 = matrix[row_num - 1][index]
    val_2 = matrix[row_num - 2][index]
    val_3 = matrix[row_num - 3][index]
    if row_num < min_word_len:
        if val_1 == 0:
            on_or_off = 2
        else:  # val_1 == 1
            on_or_off = 1
    elif row_num >= min_word_len and row_num < num_rows // 2:
        if val_1 == 0:
            on_or_off = 2
        else:  # val_1 == 1
            if val_2 == 0:
                on_or_off = 1
            else:  # val_2 == 1
                if val_3 == 0:
                    on_or_off = 1
                else:  # val_3 == 1
                    on_or_off = 2
    else:  # center row
        vald_1 = matrix[row_num + 1][index]
        vald_2 = matrix[row_num + 2][index]
        vald_3 = matrix[row_num + 3][index]
        # Must check adjacent mirror values
        if val_1 == 0:
            if val_2 == 0:
                if vald_1 == 0:
                    on_or_off = 0
                else:  # vald_1 == 1:
                    if vald_2 == 0:
                        on_or_off = 3
                    else:  # vald_2 == 1
                        if vald_3 == 0:
                            on_or_off = 1
                        else:  # vald_3 == 1
                            on_or_off = 2
            else:  # val_1 == 0, val_2 == 1
                if val_3 == 1:
                    if vald_1 == 0:
                        on_or_off = 0
                    else:  # vald_1 == 1:
                        if vald_2 == 0:
                            on_or_off = 3
                        else:  # vald_2 == 1
                            if vald_3 == 0:
                                on_or_off = 1
                            else:  # vald_3 == 1
                                on_or_off = 2
        else:  # val_1 == 1
            if val_2 == 0:
                if val_3 == 0:
                    if vald_1 == 0:
                        on_or_off = 4
                    else:  # vald_1 == 1:
                        on_or_off = 1
                else:  # val_1 == 1, val_2 == 0, val_3 == 1
                    if vald_1 == 0:
                        on_or_off = 4
                    else:  # vald_1 == 1:
                        on_or_off = 1
            else:  # val_1 == 1, val_2 == 1
                if val_3 == 0:
                    on_or_off = 1
                else:  # val_1 == 1, val_2 == 1, val_3 == 1
                    if vald_1 == 0:
                        on_or_off = 2
                    else:  # vald_1 == 1
                        if vald_2 == 0:
                            on_or_off = 1
                        else:  # vald_2 == 1
                            if vald_3 == 0:
                                on_or_off = 1
                            else:  # vald_3 == 1
                                on_or_off = 2
    return on_or_off


def look_compare(xword, i, j, up, left):
    '''Compares the 'look_left' and 'look_up' to output appropriate square value.
    Returns a list with current square value, and may contain additional values
    that need to be changed in special cases (center row, mirroring).
    '''
    num_rows = len(xword)
    num_sqr = len(xword[0])
    min_word_len = 3
    return_vals = []
    # First rows up to center row.
    if i < num_rows // 2:
        if j != 0:  # First column (j == 0)  was already created as base.
            if up == 2:
                if left == 2:
                    if j == num_sqr - min_word_len:
                        diag_look_1 = look_up(xword, i - 1, j + 1)
                        diag_look_2 = look_up(xword, i - 1, j + 2)
                        right_look = look_up(xword, i, j + 1)
                        if diag_look_1 or diag_look_2 == 1 or\
                                right_look == 1:
                            val = 1
                        else:
                            val = randrange(0, 2)
                    elif j == num_sqr - min_word_len + 1:
                        diag_look = look_up(xword, i - 1, j + 1)
                        right_look = look_up(xword, i, j + 1)
                        if diag_look == 1 or right_look == 1:
                            val = 1
                        else:
                            val = randrange(0, 2)
                    else:
                        val = randrange(0, 2)
                elif left == 1:
                    val = 1
                else:  # left == 0
                    val = 0
            else:  # up == 1
                if left == 2:
                    val = 1
                elif left == 1:
                    val = 1
    # Center row.
    elif i == num_rows // 2:
        # Get first half of center row.
        if j < num_sqr // 2:
            if j == 0:
                if up == 4:
                    val = 1
                    vald_1 = 1
                elif up == 3:
                    val = 0
                    vald_1 = 0
                elif up == 2:
                    val = randrange(0, 2)
                elif up == 1:
                    val = 1
                else:  # up == 0
                    val = 0
            else:  # j > 0:
                down_left = look_left(xword[i + 1], j)
                if down_left != 2:
                    vald_1 = down_left
                if left == 2:
                    if up == 4:
                        val = 1
                        vald_1 = 1
                    elif up == 3:
                        val = 0
                        vald_1 = 0
                    elif up == 2:
                        val = randrange(0, 2)
                    elif up == 1:
                        val = 1
                    else:  # up == 0
                        val = 0
                elif left == 1:
                    if up == 4:
                        val = 1
                        vald_1 = 1
                    elif up == 3:
                        val = 0
                        val_l = 5
                    elif up == 2:
                        val = 1
                    elif up == 1:
                        val = 1
                    else:  # up == 0
                        val = 1
                        vald_1 = 1
                else:  # left == 0
                    if up == 3:
                        val = 0
                        vald_1 = 0
                    elif up == 2:
                        val = 0
                    else:  # up == 0
                        val = 0
        # Very center square of puzzle.
        elif j == num_sqr // 2:
            if xword[i][j - 1] == 0:
                val = 0
                if up == 1:
                    val_1 = 1
                    val_2 = 1
                    vald_1 = 1
                    vald_2 = 1
            else:
                if left == 2:
                    if up == 2:
                        if xword[i - 1][j] == 0:
                            val = 0
                        else:
                            val = randrange(0, 2)
                    elif up == 0:
                        val = 0
                    else:  # up == 1
                        val = 1
                else:
                    val = 1
    try:
        return_vals.append(val)
        return_vals.append(vald_1)
        return_vals.append(vald_2)
        return_vals.append(val_1)
        return_vals.append(val_2)
    except NameError:
        try:
            return_vals.append(val_l)
        except NameError:
            return return_vals


def xword_matrix_gen(size=None, max_word_len=None, max_black_len=None):
    '''Generates a 'vald' crossword grid.
    Valid crossword specifications:
        - 15x15 or 21x21 grid (size="s" or "l")
        - minimum word length = 3 letters
        - symmetric about the origin
    '''
    # Handle default argument assignments.
    variables = xword_args(size, max_word_len, max_black_len)
    num_sqr = variables[0]
    max_word_len = variables[1]
    max_black_len = variables[2]
    num_rows = num_sqr
    # 0 indicates a square is 'off', black. 1 indicates a square is 'on', white
    # Get first row, row0.
    row0 = xword_random_row(size, max_word_len, max_black_len)
    # Get first column, col0. row0[0] must equal col0[0].
    col0 = xword_random_row(size, max_word_len, max_black_len)
    while col0[0] != row0[0]:
        col0 = xword_random_row(size, max_word_len, max_black_len)
    # Build crossword frame.
    # Add row0 and 'None' values as placeholders.
    xword = [row0]
    xword.extend([[None] * num_sqr for sqr in range(1, num_rows - 1)])
    # Mirror reverse of zero-th row to last row.
    xword.append(row0[::-1])
    # Add col0.
    for i in range(0, num_rows // 2 + 1):
        row = xword[i]
        row[0] = col0[i]
    # Generate valid squares based on row0 and col0.
    for i in range(1, num_rows // 2 + 2):
        for j in range(0, num_sqr):
            if i <= num_rows // 2:
                up = look_up(xword, i, j)
                left = look_left(xword[i], j)
                compare = look_compare(xword, i, j, up, left)
                compare_len = len(compare)
                if compare_len >= 1:
                    xword[i][j] = compare[0]
                    if compare_len >= 2:
                        xword[i - 1][-1 * j - 1] = compare[1]
                        if compare_len >= 3:
                            xword[i - 2][j] = compare[2]
                            xword[i + 1][j] = compare[3]
                            xword[i + 2][j] = compare[4]
                    if 5 in compare:
                        xword[i][j - 1] = 0
                elif i < num_rows // 2 and j == 0:
                    continue
                else:  # return list is empty for center row, j > num_sqr // 2
                    xword[i][j] = xword[i][num_sqr - j - 1]
                # Mirror reverse of row to opposite side of crossword.
                if j == num_sqr - 1:
                    xword[-1 * i - 1] = xword[i][::-1]
            else:  # i > num_rows // 2
                # Copy row before center to ensure any changes are included.
                xword[i] = xword[i - 2][::-1]
    # Check center squares.
    if xword[num_rows // 2 - 1][num_sqr // 2 - 1:num_sqr // 2 + 2] \
            == [0, 1, 0]:
        if look_up(xword, num_rows // 2 - 1, num_sqr // 2 - 1) == 2:
            xword[num_rows // 2 - 1][num_sqr // 2 - 1] = 0
            xword[num_rows // 2 + 1][num_sqr // 2 + 1] = 0
        else:
            if look_left(xword[num_rows // 2 - 1], num_sqr // 2 - 1) == 0:
                xword[num_rows // 2 - 1][num_sqr // 2 + 1] = 1
                xword[num_rows // 2 + 1][num_sqr // 2 - 1] = 1
            else:
                xword[num_rows // 2 - 1][num_sqr // 2 - 1] = 1
                xword[num_rows // 2 + 1][num_sqr // 2 + 1] = 1
    return xword


def xword_image_gen(size=None, max_word_len=None, max_black_len=None):
    from PIL import Image, ImageDraw, ImageFont
    # Handle default argument assignments.
    variables = xword_args(size, max_word_len, max_black_len)
    num_sqr = variables[0]
    max_word_len = variables[1]
    max_black_len = variables[2]
    # Generate crossword based on arguments given.
    xword_temp = xword_matrix_gen(size=size, max_word_len=max_word_len,
                                  max_black_len=max_black_len)
    # Set square size based on NYT guidelines.
    sqr_size = 35
    # Get height and width of grid variables.
    h_and_w = num_sqr * sqr_size + (num_sqr + 1)
    # Make new image as a template to draw grid upon, using PIL (Pillow).
    image = Image.new(mode='L', size=(h_and_w, h_and_w), color=255)
    # Draw rectangles on image to make grid of 'on' and 'off' squares.
    draw = ImageDraw.Draw(image)
    # Load font.
    text_font = ImageFont.truetype("Arial Bold.ttf", 10)
    # Make a blank image for the text, initialized to transparent color.
    y_start = 0
    xy_step_size = int(image.height / num_sqr)
    # Starting number for clues.
    clue_num = 1
    # Move through xword rows.
    for i in range(0, num_sqr):
        x_start = 0
        # Move through xword columns.
        for j in range(0, num_sqr):
            # Store xy coordinate for squares.
            start = (x_start, y_start)
            end = (x_start + xy_step_size, y_start + xy_step_size)
            xy = [start, end]
            # Store xy coordinates for text.
            start_text = x_start + 2
            xy_text = [start_text, y_start]
            # Check square state.
            sqr_state = xword_temp[i][j]
            # Square is 'on'.
            if sqr_state == 1:
                draw.rectangle(xy, fill=None, outline=0)
                if i == 0:
                    draw.text(xy_text, str(clue_num), fill=0, font=text_font)
                    clue_num += 1
                else:  # All other rows after the zero-th
                    if j == 0:
                        draw.text(xy_text, str(clue_num), fill=0,
                                  font=text_font)
                        clue_num += 1
                    elif j + 1 == num_sqr:
                        if xword_temp[i - 1][j] == 0:
                            draw.text(xy_text, str(clue_num), fill=0,
                                      font=text_font)
                            clue_num += 1
                    elif xword_temp[i - 1][j] == 0 or \
                            xword_temp[i][j - 1] == 0:
                        draw.text(xy_text, str(clue_num), fill=0,
                                  font=text_font)
                        clue_num += 1
            # Square is 'off'
            else:
                draw.rectangle(xy, fill=0, outline=0)
            x_start = end[0]
        y_start += xy_step_size
    del draw
    image.show()
    image.save('xword_out.png')
