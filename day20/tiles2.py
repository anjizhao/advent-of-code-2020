
from collections import Counter
import math

import numpy as np

with open('input.txt', 'r') as f:
    input_text = f.read()
# with open('test_input.txt', 'r') as f:
#     input_text = f.read()


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
        tiles_dict[tile_number] = image_array
        # tiles_dict[tile_number] = (image_array == '#').astype(int)
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
        'flip_v': False,
        'rot_90': 0,
    }


def add_first_corner(border_matches, corner_id, tile_arrangement):
    corner_piece_matches = {
        k: v for k, v in border_matches.items() if k[0] == corner_id
    }

    # put first corner piece in top left of array.
    # flip/rotate it so matched edges face in (we want a right and bottom)
    inner_faces = [k[1] for k in corner_piece_matches.keys()]

    transformations = _base_transform(corner_id)

    if 'top' in inner_faces:
        transformations['flip_v'] = transformations['flip_v'] ^ True
    if 'left' in inner_faces:
        transformations['flip_v'] = transformations['flip_v'] ^ True
        transformations['rot_90'] = 2

    tile_arrangement[0, 0] = transformations
    return transformations


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
            transformations['flip_v'] = True
            transformations['rot_90'] = 1
    if tiles[index[0], index[1] + 1] is not None:
        assert tiles[index[0], index[1] + 1] == transformations
    else:
        tiles[index[0], index[1] + 1] = transformations
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
            transformations['flip_v'] = True
    elif adjacent_face == 'left':
        transformations['rot_90'] = 3
        if reverse:
            transformations['flip_v'] = True
    if tiles[index[0] + 1, index[1]] is not None:
        assert tiles[index[0] + 1, index[1]] == transformations
    else:
        tiles[index[0] + 1, index[1]] = transformations
    return transformations


def add_adjacent_tiles(border_matches, tiles, index):
    t = tiles[index]
    t_edges = {
        k: v for k, v in border_matches.items()
        if k[0] == t['tile_id']
    }
    for k, v in t_edges.items():
        transformed = apply_transformation_to_edge_tuple(k, t)

        if transformed[1] == 'right':
            next_tile_index = (index[0], index[1] + 1)
            if tiles[next_tile_index]:
                continue  # next tile already exists, we can skip it
            # add v to the right of this tile
            next_tile = add_right(tiles, index, v, transformed[2])
            # add tiles to right and bottom of the new tile we just added
            add_adjacent_tiles(border_matches, tiles, next_tile_index)

        elif transformed[1] == 'bottom':
            next_tile_index = (index[0] + 1, index[1])
            if tiles[next_tile_index]:
                continue  # next tile already exists, we can skip it
            # add v to the bottom of this tile
            next_tile = add_below(tiles, index, v, transformed[2])
            # add tiles to right and bottom of the new tile we just added
            add_adjacent_tiles(border_matches, tiles, next_tile_index)


def build_grid(border_matches, corner_id, n):
    tile_arrangement = np.empty((n, n), dtype=object)
    add_first_corner(border_matches, corner_id, tile_arrangement)
    index = (0, 0)
    add_adjacent_tiles(border_matches, tile_arrangement, index)

    return tile_arrangement


tiles_dict = read_input(input_text)
all_borders = get_borders(tiles_dict)
grid_dimension = int(math.sqrt(len(tiles_dict)))

matches = match_borders(all_borders)

corners = find_corners(matches)
print('corners', corners)
print('product', np.prod(corners))


tile_arrangement = build_grid(matches, corners[0], grid_dimension)

# print(tile_arrangement)

example_tile = tiles_dict[corners[0]]
# print(example_tile)

tile_dimension = example_tile.shape[0]


def apply_transformation_to_tile(tile, transformations):
    transformed = tile
    if transformations['flip_v']:
        transformed = np.flipud(transformed)
    for i in range(transformations['rot_90']):
        transformed = np.rot90(transformed)
    return transformed


def make_full_image(tile_arrangement, tiles_dict):
    # get size of full image
    sample_tile = next(iter(tiles_dict.values()))
    tile_dimension = sample_tile.shape[0] - 2   # remove tile borders
    grid_dimension = tile_arrangement.shape[0]
    image_dim = grid_dimension * tile_dimension
    image_arr = np.zeros((image_dim, image_dim), dtype=str)

    for i in range(tile_arrangement.shape[0]):
        i_image = i * tile_dimension
        for j in range(tile_arrangement.shape[1]):
            j_image = j * tile_dimension

            tile_info = tile_arrangement[i, j]
            tile = tiles_dict[tile_info['tile_id']]
            # apply transformations
            transformed_tile = apply_transformation_to_tile(tile, tile_info)

            image_arr[
                i_image:i_image + tile_dimension,
                j_image:j_image + tile_dimension
            ] = transformed_tile[
                1:tile_dimension + 1, 1:tile_dimension + 1
            ]

    return image_arr


image = make_full_image(tile_arrangement, tiles_dict)

def display_image(image_arr):
    for row in image_arr:
        print(''.join([str(r) for r in row]))

# display_image(image)

monster_str = '                  # \n#    ##    ##    ###\n #  #  #  #  #  #   '  # noqa
monster_arr = np.array([list(i) for i in monster_str.split('\n')])

print('monster array shape', monster_arr.shape)
# display_image(monster_arr)


def check_slices_in_image(image, monster_shape, monster_indices):
    count_monsters = 0
    for i in range(image.shape[0] - monster_shape[0]):
        for j in range(image.shape[1] - monster_shape[1]):
            img_slice = image[i:i + monster_shape[0], j:j + monster_shape[1]]
            # if i == 2:
            #     # print(i, j)
            #     display_image(img_slice)
            if all(img_slice[monster_indices] == '#'):
                count_monsters += 1
    return count_monsters


def count_monsters_in_image(image, monster_shape, monster_indices):
    # try all rotations, then flip v & try all rotations until we find a match
    # for flip in range(2):
    for flip in [1]:
        new_image = image
        if flip:
            new_image = np.flipud(new_image)
        # for rotations in range(4):  # try rotating 0, 1, 2, 3 times
        for rotations in [3]:  # try rotating 0, 1, 2, 3 times
            for i in range(rotations):
                new_image = np.rot90(new_image)
            count_monsters = check_slices_in_image(
                new_image, monster_shape, monster_indices,
            )
            if count_monsters:
                return count_monsters


def find_monsters(image, monster_arr):
    monster_shape = monster_arr.shape
    monster_indices = np.where(monster_arr == '#')
    count_monsters = count_monsters_in_image(
        image, monster_shape, monster_indices)
    return count_monsters


count_monsters = find_monsters(image, monster_arr)
print('count_monsters:', count_monsters)

filled_tiles_in_monster = (monster_arr == '#').sum()
filled_tiles_in_image = (image == '#').sum()

print('filled_tiles_in_monster', filled_tiles_in_monster)
print('filled_tiles_in_image', filled_tiles_in_image)
print(
    'non-monster tiles',
    filled_tiles_in_image - (filled_tiles_in_monster * count_monsters)
)
