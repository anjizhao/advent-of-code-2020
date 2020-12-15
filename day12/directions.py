import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

def read_direction(l):
    action = l[0]
    value = int(l[1:])
    return action, value

directions = [read_direction(l) for l in lines]

test_directions = [('F', 10), ('N', 3), ('F', 7), ('R', 90), ('F', 11)]  # noqa

MOVEMENTS = {  # these are unit vectors :sob:
    'N': np.array([0, 1]),
    'S': np.array([0, -1]),
    'W': np.array([-1, 0]),
    'E': np.array([1, 0]),
}

TURNS = {  # these are rotation matrices :SOB:
    'L': np.array([[0, -1], [1, 0]]),  # 90 deg rotation
    'R': np.array([[0, 1], [-1, 0]]),  # -90 deg rotation
}


current_position = np.array([0, 0])  # start at origin of x/y plane
current_face = np.array([1, 0])  # vector pointing in direction ship is facing!

for action, value in directions:
    if action in ['L', 'R']:
        rotation_matrix = TURNS[action]
        assert value % 90 == 0
        turns = value // 90
        for i in range(turns):
            current_face = np.dot(rotation_matrix, current_face)
    elif action in ['N', 'S', 'W', 'E']:
        movement = MOVEMENTS[action] * value
        current_position += movement
    elif action == 'F':
        movement = current_face * value
        current_position += movement
    # print('current position', current_position)
    # print('current face', current_face)

print('current position', current_position)
print('current face', current_face)
