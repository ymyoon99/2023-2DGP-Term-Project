objects = [[] for _ in range(4)]  # 시각적인 관점에서의 월드.

# fill here
# 충돌 관점의 월드
collision_pairs = {}  # { 'boy:ball' : { [ball], [ball1, ball2, ...] } 딕셔너리


def add_object(o, depth=0):
    objects[depth].append(o)


def add_objects(ol, depth=0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


# 충돌을 체크하는 함수
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True  # 충돌 했을 때


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:  # a 그룹
            pairs[0].remove(o)
        if o in pairs[1]:  # b 그룹
            pairs[1].remove(o)


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)  # 시각적 월드(레이어)에서 삭제 완료.
            remove_collision_object(o)  # 충돌 그룹에서 삭제 완료.
            del o  # 객체 자체를 완전히 메모리에서 삭제.
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'New group {group} added.')
        collision_pairs[group] = [[], []]  # 초기화
    if a:  # a가 있을 때 == a가 None이 아니면..
        collision_pairs[group][0].append(a)
    if b:  # b가 있을 때 ...
        collision_pairs[group][1].append(b)


def handle_collisions():
    collided_pairs = []
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    collided_pairs.append((group, a, b))
    for group, a, b in collided_pairs:
        a.handle_collision(group, b)
        b.handle_collision(group, a)


def all_objects():
    for layer in objects:
        for o in layer:
            yield o
def clear_collision_pairs():
    collision_pairs.clear()