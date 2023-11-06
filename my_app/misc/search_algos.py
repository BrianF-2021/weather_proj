import re
from collections import deque as dq


def find_substring(substring, the_string):
    if not substring or not the_string:
        return
    substring = substring.lower()
    the_string = the_string.lower()
# print(substring, the_string)
    temp_substring = ""
    index = 0
    current_char = substring[index]

    for i in range(len(the_string)):
        if the_string[i] != current_char:
            print("Chars Don't Match")
            print(
                f"current_char: {current_char}\nthe_string[i]: {the_string[i]}")
            temp_substring = ""
            current_char = substring[0]
            index = 0
        if the_string[i] == current_char:
            print("Chars Match!")
            print(
                f"current_char: {current_char}\nthe_string[i]: {the_string[i]}")
            temp_substring += the_string[i]
            if index < len(substring)-1:
                index += 1
                current_char = substring[index]
        if temp_substring == substring:
            print(f"Found substring '{substring}'")
            return i-len(temp_substring)
    print(f"Substring '{substring}' not found...")
    return False


def extract_nums_from_str(data,  return_type="int"):
    regex_num = "^[-]?\d+(\.\d+)?$"
    if not data:
        return []
    is_period_used = False
    temp = ""
    result = []
    for i, char in enumerate(data):
        # print(f"TEMP: {temp}, CHAR: {char}")
        if char == "-" and temp == "":
            temp += char
        elif char.isnumeric():
            temp += char
            if i == len(data)-1 and return_type == "float":
                result.append(float(temp))
                return result
            if i == len(data)-1 and return_type == "int":
                result.append(int(temp))
                return result

        elif char == "." and is_period_used is False:
            temp += char
            is_period_used = True
        else:
            if re.search(regex_num, temp):
                if return_type == "float":
                    result.append(float(temp))
                if return_type == "int":
                    result.append(int(temp))

            temp = ""
            is_period_used = False
# print(result)
    return result


def get_clean_string(the_string):
    cleaned_string = ""
    specials = ["\n", "\r", "\t", "\\"]
# prev_char = the_string[0]
    white_space_counter = 0
    for index, char in enumerate(the_string):
        if char != " " and char not in specials:
            white_space_counter = 0
            cleaned_string += char
        if (char == " ") and (white_space_counter == 0) and (index != len(the_string)-1) and (len(cleaned_string) != 0):
            white_space_counter += 1
            cleaned_string += char
    if cleaned_string[-1] == " ":
        cleaned_string = cleaned_string[:-1]
# print(cleaned_string)
# for i, val in enumerate(cleaned_string):
# if val == " ":
# print(i, "WHITE SPACE")
# print()
    return cleaned_string


def dfs_left_right(grid, direction, target, start, pos, result):
    if not is_pos_inbound(grid, pos) or not is_pos_inbound(grid, start):
        return dfs_result_str(result)
    row, col = pos
    char = grid[row][col]

    if grid[row][col] != target and direction == "left":
        result.appendleft(char)
        if col > 0:
            return dfs_left_right(grid, "left", target, start, (row, col-1), result)
        if col == 0:
            row, col = start
            return dfs_left_right(grid, "right", target, start, (row, col+1), result)

    if grid[row][col] == target and direction == "left":
        row, col = start
        return dfs_left_right(grid, "right", target, start, (row, col+1), result)

    if grid[row][col] != target and direction == "right":
        result.append(char)
        if col < len(grid[0])-1:
            return dfs_left_right(grid, "right", target, start, (row, col+1), result)
        if col == len(grid[0])-1:
            return dfs_result_str(result)

    if grid[row][col] == target and direction == "right":
        return dfs_result_str(result)


def dfs_up_down(grid, direction, target, start, pos, result):
    if not is_pos_inbound(grid, pos) or not is_pos_inbound(grid, start):
        return dfs_result_str(result)
    row, col = pos
# if (row < 0) or (row > len(grid)-1) or (col < 0) or (col > len(grid[0])-1):
    print("updown_pos: ", pos)
# return

    char = grid[row][col]

    if grid[row][col] != target and direction == "up":
        result.appendleft(char)
        if row > 0:
            return dfs_up_down(grid, "up", target, start, (row-1, col), result)
        if row == 0:
            row, col = start
            return dfs_up_down(grid, "down", target, start, (row+1, col), result)

    if grid[row][col] == target and direction == "up":
        row, col = start
        return dfs_up_down(grid, "down", target, start, (row+1, col), result)

    if grid[row][col] != target and direction == "down":
        result.append(char)
        if row < len(grid)-1:
            return dfs_up_down(grid, "down", target, start, (row+1, col), result)
        if row == len(grid)-1:
            return dfs_result_str(result)

    if grid[row][col] == target and direction == "down":
        return dfs_result_str(result)


def dfs_result_str(result):
    result_string = ""
    for char in result:
        result_string += char
    return result_string


def is_pos_inbound(grid, pos):
    row, col = pos
    if (row < 0) or (row > len(grid)-1) or (col < 0) or (col > len(grid[0])-1):
        # print("updown_pos: ", False, pos)
        return False
# print("updown_pos: ", True, pos)
    return True

# search ajacent chars in a grid


def dfs_adjacent_chars(grid, orientation, target, start, pos, result):
    if not is_pos_inbound(grid, pos) or not is_pos_inbound(grid, start):
        return dfs_result_str(result)
    row, col = pos
    print(pos)

    # checking vertical adjacents in a row
    if orientation == "horizontal":
        grid_char = grid[row][col]
        # search up
        while (row >= 0) and grid_char != target:
            grid_char = grid[row][col]
            if grid_char == target:
                break
            if row == 0:
                result.appendleft(grid_char)
                break
            result.appendleft(grid_char)
            row -= 1
        # search down
        row, col = start
        row += 1
        while (row <= len(grid)-1) and grid_char != target:
            grid_char = grid[row][col]
            if grid_char == target:
                break
            if row == len(grid)-1:
                result.append(grid_char)
                break
            result.append(grid_char)
            row += 1
        return dfs_result_str(result)

    # checking horizontal adjacents in a column
    if orientation == "vertical":
        grid_char = grid[row][col]
        # search left
        while (col >= 0) and grid_char != target:
            grid_char = grid[row][col]
            if grid_char == target:
                break
            if col == 0:
                result.appendleft(grid_char)
                break
            result.appendleft(grid_char)
            col -= 1
        # search right
        row, col = start
        col += 1
        while (col <= len(grid[0])-1) and grid_char != target:
            grid_char = grid[row][col]
            if grid_char == target:
                break
            if col == len(grid[0])-1:
                result.append(grid_char)
                break
            result.append(grid_char)
            col += 1
        return dfs_result_str(result)
