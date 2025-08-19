/**
给你单链表的头指针 head 和两个整数 left 和 right ，其中 left <= right 。请你反转从位置 left 到位置 right 的链表节点，返回 反转后的链表 。

示例 1：
输入：head = [1,2,3,4,5], left = 2, right = 4
输出：[1,4,3,2,5]

示例 2：
输入：head = [5], left = 1, right = 1
输出：[5]
提示：

链表中节点数目为 n
1 <= n <= 500
-500 <= Node.val <= 500
1 <= left <= right <= n

进阶： 你可以使用一趟扫描完成反转吗？
 */

/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} head
 * @param {number} left
 * @param {number} right
 * @return {ListNode}
 */
var reverseBetween = function(head, left, right) {
    let cur = head
    let leftCnt = 0
    let prev = cur;
    let subPrev= null; // 翻转后头部的前一个节点需要额外记录
    if (left>1) {
      while (leftCnt < left) {
          prev=cur
          cur = cur.next;
          leftCnt++;
          if (leftCnt===left-1) {
            subPrev = prev;
          } 
      }
    } else {
      cur=cur.next;
      leftCnt++;
    }
    let rightCnt = leftCnt;
    let subTail = prev; // 反转后的尾部节点，实际是反转前的第一个节点
    while (rightCnt < right && cur !==null ) {
        const tmp = cur.next;
        cur.next = prev;
        prev=cur;
        cur= tmp;
        rightCnt++;
    }
    // 此时prev是反转后的头部, 与前面连接起来
    if(subPrev) { subPrev.next = prev;}
    subTail.next = cur; // 上一个循环结束后，此时cur已经指向right+1节点了，把它连接起来
    return subPrev ? head: prev; // 这里处理极端情况，left=1时，左侧其实没有了原来的节点，头部就要变成反转后的头节点
};