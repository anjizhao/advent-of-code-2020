
from collections import Counter
import math

import numpy as np

# with open('input.txt', 'r') as f:
#     input_text = f.read()
with open('test_input.txt', 'r') as f:
    input_text = f.read()


# '#' = 1
# '.' = 0

def read_input(input_text):
    tiles_str_list = input_text.strip().split('\n\n')
    tiles_dict = {}
    for tile_str in tiles_str_list:
        label_str, image_str = tile_str.strip().split(':\n')
        tile_number = label_str.replace('Tile ', '')
        assert tile_number.isdigit()
        tile_number = int(tile_number)
        image_rows = image_str.split('\n')
        image_array = np.array([list(s) for s in image_rows])
        tiles_dict[tile_number] = (image_array == '#').astype(int)
    return tiles_dict


def get_borders(tiles_dict):
    all_borders = {}
    for number, arr in tiles_dict.items():
        left = arr[::-1, 0]
        right = arr[:, -1]
        top = arr[0, :]
        bottom = arr[-1, ::-1]
        all_borders[(number, 'left')] = left
        all_borders[(number, 'right')] = right
        all_borders[(number, 'top')] = top
        all_borders[(number, 'bottom')] = bottom
    return all_borders


def match_borders(all_borders):
    # returns a DICT of edge: (adjacent edge, reversed status)
    # example: {
    #     (1427, 'left'): ((2729, 'right'), False))
    #     (2729, 'right'): ((1427, 'left'), False))
    # }
    matches = {}
    for key_1, arr_1 in all_borders.items():
        for key_2, arr_2 in all_borders.items():
            if key_1 == key_2:
                continue
            if (arr_1 == arr_2).all():
                matches[key_1] = (key_2, False)
            elif (arr_1 == np.flip(arr_2)).all():
                matches[key_1] = (key_2, True)
    return matches


def find_corners(border_matches):
    # border_matches is a dict
    tile_ids = [t[0] for t in border_matches.keys()]
    c = Counter(tile_ids)
    # corners only have two matched edges each
    corners = [tile_id for tile_id, count in c.items() if count == 2]
    return corners


def _base_transform(corner_id):
    return {
        'tile_id': corner_id,
        # 'flip_h': False,
        'flip_v': False,
        'rot_90': 0,
    }


def add_first_corner(border_matches, corner_id, tile_arrangement):
    corner_piece_matches = {
        k: v for k, v in border_matches.items()
        if k[0] == corner_id
    }
    # print(corner_piece_matches)
    # {(1951, 'right'): ((2311, 'left'), False), (1951, 'top'): ((2729, 'bottom'), False)}  # noqa

    # put first corner piece in top left of array.
    # flip/rotate it so matched edges face in
    # want a right and bottom
    inner_faces = [k[1] for k in corner_piece_matches.keys()]
    # print(inner_faces)

    transformations = _base_transform(corner_id)

    if 'top' in inner_faces:
        transformations['flip_v'] = transformations['flip_v'] ^ True
    if 'left' in inner_faces:
        transformations['flip_v'] = transformations['flip_v'] ^ True
        transformations['rot_90'] = 2

    tile_arrangement[0, 0] = transformations
    return transformations


# FLIP_H = {
#     'left': 'right',
#     'right': 'left',
# }
# WE ARE GETTING RID OF FLIP_H!!!
# flip_h is the same as flip_v + 180deg rotation

FLIP_V = {
    'top': 'bottom',
    'bottom': 'top',
}

ROT_90 = {
    'left': 'bottom',
    'bottom': 'right',
    'right': 'top',
    'top': 'left',
}



def apply_transformation_to_edge_tuple(edge_tuple, t_dict):
    tile_id, face = edge_tuple
    rev = False
    if t_dict['flip_v']:
        face = FLIP_V.get(face, face)
        rev = rev ^ True
    for i in range(t_dict['rot_90']):
        face = ROT_90.get(face, face)
    return (tile_id, face, rev)


def add_right(tiles, index, adjacent_tile_info, already_reversed):
    tile_info, adjacent_reversed = adjacent_tile_info
    reverse = already_reversed == adjacent_reversed
    adjacent_tile_id, adjacent_face = tile_info
    # print('adjacent_tile_id', adjacent_tile_id)
    # print('already_reversed', already_reversed)
    # print('adjacent_reversed', adjacent_reversed)
    # print('reverse', reverse)
    transformations = _base_transform(adjacent_tile_id)
    # want to transform so the face becomes left
    if adjacent_face == 'right':
        transformations['rot_90'] = 2
        if reverse:
            transformations['flip_v'] = True
    elif adjacent_face == 'left':
        if reverse:
            transformations['flip_v'] = True
    elif adjacent_face == 'top':
        transformations['rot_90'] = 1
        if reverse:
            transformations['flip_v'] = True
            transformations['rot_90'] = 3
    elif adjacent_face == 'bottom':
        transformations['rot_90'] = 3
        if reverse:
            # we flip before rotation, so 'bottom' should be flipped first
            transformations['flip_v'] = True
            transformations['rot_90'] = 1
    if tiles[index[0], index[1] + 1] is not None:
        assert tiles[index[0], index[1] + 1] == transformations
    else:
        tiles[index[0], index[1] + 1] = transformations
        # print('added', transformations, 'at', index[0], index[1] + 1)
    return transformations


def add_below(tiles, index, adjacent_tile_info, already_reversed):
    tile_info, adjacent_reversed = adjacent_tile_info
    reverse = already_reversed == adjacent_reversed
    adjacent_tile_id, adjacent_face = tile_info
    transformations = _base_transform(adjacent_tile_id)
    # want to transform so the face becomes top
    if adjacent_face == 'bottom':
        if not reverse:
            transformations['rot_90'] = 2
        else:
            transformations['flip_v'] = True
    elif adjacent_face == 'top':
        if reverse:
            transformations['flip_v'] = True
            transformations['rot_90'] = 2
    elif adjacent_face == 'right':
        transformations['rot_90'] = 1
        if reverse:
            # we flip before rotation, so 'right' should be flipped first
            transformations['flip_v'] = True
    elif adjacent_face == 'left':
        transformations['rot_90'] = 3
        if reverse:
            transformations['flip_v'] = True
    if tiles[index[0] + 1, index[1]] is not None:
        assert tiles[index[0] + 1, index[1]] == transformations
    else:
        tiles[index[0] + 1, index[1]] = transformations
        # print('added', transformations, 'at', index[0] + 1, index[1])
    return transformations


def add_adjacent_tiles(border_matches, tiles, index):
    t = tiles[index]
    # print('index', index)
    # print('t', t)
    t_edges = {
        k: v for k, v in border_matches.items()
        if k[0] == t['tile_id']
    }
    # {(1951, 'right'): ((2311, 'left'), False), (1951, 'top'): ((2729, 'bottom'), False)}  # noqa
    for k, v in t_edges.items():
        # print(k, ':', v)
        # example (1951, 'right') : ((2311, 'left'), False)
        transformed = apply_transformation_to_edge_tuple(k, t)
        # print('transformed', transformed)
        # if index == (2, 2):
        #     print(tiles)
        #     return
        if transformed[1] == 'right':
            # add v to the right of this tile
            next_tile = add_right(tiles, index, v, transformed[2])
            add_adjacent_tiles(border_matches, tiles, (index[0], index[1] + 1))
        elif transformed[1] == 'bottom':
            # add v to the bottom of this tile
            next_tile = add_below(tiles, index, v, transformed[2])
            add_adjacent_tiles(border_matches, tiles, (index[0] + 1, index[1]))


def build_picture(border_matches, corner_id, n):
    tile_arrangement = np.empty((n, n), dtype=object)
    add_first_corner(border_matches, corner_id, tile_arrangement)
    index = (0, 0)
    add_adjacent_tiles(border_matches, tile_arrangement, index)

    return tile_arrangement


tiles_dict = read_input(input_text)
# print(tiles_dict)
all_borders = get_borders(tiles_dict)
# for k in list(all_borders.keys())[:3]:
#     print(k, all_borders[k])

matches = match_borders(all_borders)
print(len(matches))
# print(matches)

corners = find_corners(matches)
print(corners)
print(np.prod(corners))


r = build_picture(matches, corners[0], int(math.sqrt(len(tiles_dict))))
# print(r)
