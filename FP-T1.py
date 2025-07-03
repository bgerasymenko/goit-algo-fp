#!/usr/bin/env python3
from typing import Optional, Tuple

class ListNode:
    """
    Вузол однозв'язного списку.
    """
    def __init__(self, val: int, next: 'ListNode' = None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"{self.val} → {self.next}"


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Реверсує однозв'язний список, змінюючи посилання між вузлами.
    Повертає нову голову списку.
    """
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def merge_two_sorted(l1: Optional[ListNode],
                     l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Об'єднує два відсортовані однозв'язні списки в один відсортований.
    Повертає голову нового списку.
    """
    dummy = ListNode(0)
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next


def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Сортує однозв'язний список методом злиття (Merge Sort).
    Повертає голову відсортованого списку.
    """
    if not head or not head.next:
        return head

    # Знаходимо середину списку
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    mid = slow.next
    slow.next = None  # Розриваємо список на дві частини

    # Рекурсивно сортуємо обидві половини
    left = sort_list(head)
    right = sort_list(mid)

    # Зливаємо відсортовані половини
    return merge_two_sorted(left, right)


# -------------------
# Допоміжні функції для тестування
# -------------------

def build_list(values: list[int]) -> Optional[ListNode]:
    """
    Створює однозв'язний список з Python-списку значень і повертає його голову.
    """
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head

def list_to_py(head: Optional[ListNode]) -> list[int]:
    """
    Перетворює однозв'язний список в Python-список значень.
    """
    out = []
    curr = head
    while curr:
        out.append(curr.val)
        curr = curr.next
    return out

if __name__ == "__main__":
    # Приклад 1: реверсування списку
    vals = [1, 2, 3, 4, 5]
    head = build_list(vals)
    print("Оригінал:", list_to_py(head))
    rev = reverse_list(head)
    print("Реверс:",  list_to_py(rev))

    # Приклад 2: сортування списку
    import random
    random_vals = random.sample(range(1, 20), 10)
    head2 = build_list(random_vals)
    print("\nНесортований:", list_to_py(head2))
    sorted_head = sort_list(head2)
    print("Сортований: ", list_to_py(sorted_head))

    # Приклад 3: об’єднання двох відсортованих списків
    a = build_list([1, 4, 6, 8])
    b = build_list([2, 3, 5, 7, 9])
    merged = merge_two_sorted(a, b)
    print("\nЗлиття [1,4,6,8] та [2,3,5,7,9]:", list_to_py(merged))
