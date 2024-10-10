from collections import defaultdict

# 트리 구조를 저장할 변수
tree = defaultdict(list)  # 부모 -> 자식들의 리스트
color = {}  # 각 노드의 색깔을 저장
max_depth = {}  # 각 노드의 최대 깊이를 저장

# 서브트리 내의 색상을 계산하는 함수
def calculate_subtree_value(node):
    unique_colors = set()
    stack = [node]
    
    while stack:
        curr = stack.pop()
        unique_colors.add(color[curr])
        for child in tree[curr]:
            stack.append(child)
    
    return len(unique_colors)

# DFS로 트리의 깊이를 계산하는 함수
def get_depth(node, curr_depth):
    if not tree[node]:  # 리프 노드일 때
        return curr_depth
    max_child_depth = 0
    for child in tree[node]:
        max_child_depth = max(max_child_depth, get_depth(child, curr_depth + 1))
    return max_child_depth

# 명령을 처리
q = int(input())
for _ in range(q):
    command = list(map(int, input().split()))
    
    if command[0] == 100:
        # 노드 추가: 100 m_id p_id color max_depth
        m_id, p_id, color_value, max_d = command[1], command[2], command[3], command[4]
        
        if p_id == -1:
            # 새로운 트리의 루트 노드
            tree[m_id] = []
            color[m_id] = color_value
            max_depth[m_id] = max_d
        else:
            # 부모가 있는 경우
            if p_id in tree and get_depth(p_id, 1) < max_depth[p_id]:
                # 부모의 최대 깊이를 넘지 않으면 추가
                tree[p_id].append(m_id)
                tree[m_id] = []
                color[m_id] = color_value
                max_depth[m_id] = max_d
    
    elif command[0] == 200:
        # 색깔 변경: 200 m_id color
        m_id, new_color = command[1], command[2]
        
        # 서브트리의 모든 노드의 색상을 변경
        stack = [m_id]
        while stack:
            curr = stack.pop()
            color[curr] = new_color
            for child in tree[curr]:
                stack.append(child)
    
    elif command[0] == 300:
        # 색깔 조회: 300 m_id
        m_id = command[1]
        print(color[m_id])  # 해당 노드의 색깔 출력
    
    elif command[0] == 400:
        # 점수 조회: 400
        total_score = 0
        for node in tree:
            if node in color:
                value = calculate_subtree_value(node)  # 서브트리 내 고유한 색상의 수 계산
                total_score += value ** 2  # 각 노드의 가치 제곱 합산
        print(total_score)