# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None
#
# class Solution(object):
#     def addTwoNumbers(self, l1, l2):
#         """
#         :type l1: ListNode
#         :type l2: ListNode
#         :rtype: ListNode
#         """
#
import re
line = 'asdf fjdk; afed, fjek,asdf, foo"5555"'
print(re.split(r'[; ,"]\s*',line))
#删除一个节点之后记得要把链表长度减一
def delete(self, index):
    if self.isEmpty():
        print "this chain table is empty."
        return

    if index < 0 or index >= self.length:
        print 'error: out of index'
        return
    #要注意删除第一个节点的情况
    #如果有空的头节点就不用这样
    #但是我不喜欢弄头节点
    if index == 0:
        self.head = self.head._next
        self.length -= 1
        return

    #prev为保存前导节点
    #node为保存当前节点
    #当j与index相等时就
    #相当于找到要删除的节点
    j = 0
    node = self.head
    prev = self.head
    while node._next and j < index:
        prev = node
        node = node._next
        j += 1

    if j == index:
        prev._next = node._next
        self.length -= 1
