from typing import Iterable, List
from collections import defaultdict

def binary_search(arr: List[any], x: any, low: int, high: int) -> bool:
    while low <= high:
        mid = (high + low) // 2
        if arr[mid] == x:
            return True
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return False

def create_schema(items: Iterable[dict], folders_in_db: Iterable[str]) -> List[dict]:
    awaitable = defaultdict(lambda: list())
    ans = []

    def build_schema(parent: List[dict]) -> int:
        count = 0
        for item in parent:
            item['children'] = awaitable[item['id']]
            count += build_schema(item['children']) + 1
        return count

    for i in items:
        p_id = i['parentId']

        if p_id is not None and not binary_search(folders_in_db, p_id, 0, len(folders_in_db) - 1):
            awaitable[p_id].append(i)
        else:
            ans.append(i)

    count = build_schema(ans)
        
    if count != len(items):
        raise ValueError("invalid schema")

    return ans