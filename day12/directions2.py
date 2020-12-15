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

ship_position = np.array([0, 0])  # ship starts at origin of x/y plane
waypoint_rel = np.array([10, 1])  # waypoint location relative to ship

for action, value in directions:
    if action in ['L', 'R']:
        rotation_matrix = TURNS[action]
        assert value % 90 == 0
        turns = value // 90
        for i in range(turns):
            waypoint_rel = np.dot(rotation_matrix, waypoint_rel)
    elif action in ['N', 'S', 'W', 'E']:
        movement = MOVEMENTS[action] * value
        waypoint_rel += movement
    elif action == 'F':
        movement = waypoint_rel * value
        ship_position += movement
    # print('ship position', ship_position)
    # print('waypoint relative position to ship', waypoint_rel)

print('ship position', ship_position)
print('waypoint relative position to ship', waypoint_rel)
