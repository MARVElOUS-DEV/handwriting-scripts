/**
 * 反转单链表,返回头部节点
 * 
 * 1->2->3->4->5->null
 */

/**
* 已知信息: 单链表默认有head指向头部节点，节点内部next属性指向下一个节点
* refer: https://blog.csdn.net/zhybiancheng/article/details/113665176
*/
// type LinkNode = {
//   value: Number
//   next: LinkNode
// }


/**
 * 必须要有两个指针，其中一个指向当前节点的前向节点(prevNode)
 * 
 */
function reverseLinkNode(head) {
  let prevNode = null;
  let curNode = head;
  while(curNode) {
    // 下一步要断开当前节点与下一个节点的联系，必须先暂存下一个节点
    const nextNode = curNode.next;
    curNode.next = prevNode;
    // 一次只调整currentNode节点的指向，然后整体向后平移
    prevNode = curNode;
    curNode = nextNode;
  }
  return prevNode;
}


const testNodes = {
  value: 1,
  next: {
    value:2,
    next: {
      value: 3,
      next: {
        value:4,
        next: {
          value: 5,
          next: null
        }
      }
    }
  }
}

const result = reverseLinkNode(testNodes);

console.log(JSON.stringify(result));
