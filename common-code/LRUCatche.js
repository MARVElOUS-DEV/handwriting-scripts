/**
请你设计并实现一个满足  LRU (最近最少使用) 缓存 约束的数据结构。
实现 LRUCache 类：
LRUCache(int capacity) 以 正整数 作为容量 capacity 初始化 LRU 缓存
int get(int key) 如果关键字 key 存在于缓存中，则返回关键字的值，否则返回 -1 。
void put(int key, int value) 如果关键字 key 已经存在，则变更其数据值 value ；如果不存在，则向缓存中插入该组 key-value 。如果插入操作导致关键字数量超过 capacity ，则应该 逐出 最久未使用的关键字。
函数 get 和 put 必须以 O(1) 的平均时间复杂度运行。
示例：

输入
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
输出
[null, null, null, 1, null, -1, null, -1, 3, 4]

解释
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // 缓存是 {1=1}
lRUCache.put(2, 2); // 缓存是 {1=1, 2=2}
lRUCache.get(1);    // 返回 1
lRUCache.put(3, 3); // 该操作会使得关键字 2 作废，缓存是 {1=1, 3=3}
lRUCache.get(2);    // 返回 -1 (未找到)
lRUCache.put(4, 4); // 该操作会使得关键字 1 作废，缓存是 {4=4, 3=3}
lRUCache.get(1);    // 返回 -1 (未找到)
lRUCache.get(3);    // 返回 3
lRUCache.get(4);    // 返回 4

提示：

1 <= capacity <= 3000
0 <= key <= 10000
0 <= value <= 105
最多调用 2 * 105 次 get 和 put
 */

// 解法1，map + 双向链表
/**
 * @param {number} capacity
 */
var LRUCache = function(capacity) {
    this.size=0;
    this.max_size=capacity;
    this.map = new Map();
    this.dLinkHead = new DLinkNode(0,0);
    this.dLinkTail = new DLinkNode(0,0);
    this.dLinkHead.next = this.dLinkTail;
    this.dLinkTail.prev = this.dLinkHead;
};

/** 
 * @param {number} key
 * @return {number}
 */
LRUCache.prototype.get = function(key) {
    const t = this.map.get(key)
    if(t) {
        this.moveToTail(t)
        return t.value
    }
    return -1
};

/** 
 * @param {number} key 
 * @param {number} value
 * @return {void}
 */
LRUCache.prototype.put = function(key, value) {
    const t = this.map.get(key)
    if(t) {
        t.value = value
        this.moveToTail(t)
    } else {
        const newNode = new DLinkNode(key, value)
        this.map.set(key, newNode)
        this.addToTail(newNode)
        if(this.size > this.max_size) {
            const first = this.dLinkHead.next
            this.remove(first)
            this.map.delete(first.key)
            
        }
    }
};
LRUCache.prototype.moveToTail = function(node) {
  this.remove(node);
  this.addToTail(node);
}
LRUCache.prototype.addToTail = function(node) {
  const tail = this.dLinkTail.prev;
  node.next = this.dLinkTail;
  node.prev = tail;
  tail.next = node;
  this.dLinkTail.prev = node;
  this.size++
}
LRUCache.prototype.remove = function(node) {
  const prev = node.prev;
  const next = node.next;
  prev.next = next;
  next.prev = prev;
  node.prev = null;
  node.next = null;
  this.size--
}

class DLinkNode {
    constructor(key, value) {
        this.key = key
        this.value = value
        this.prev = null
        this.next = null
    }
}


// 解法2 orderdMap
/**
 * @param {number} capacity
 */
var LRUCache2 = function(capacity) {
    this.max_size=capacity;
    this.map = new Map(); // map 本身是有序的
};

/** 
 * @param {number} key
 * @return {number}
 */
LRUCache2.prototype.get = function(key) {
    const t = this.map.get(key)
    if(t!==undefined) {
        this.map.delete(key)
        this.map.set(key, t)
        return t
    }
    return -1
};

/** 
 * @param {number} key 
 * @param {number} value
 * @return {void}
 */
LRUCache2.prototype.put = function(key, value) {
  const t = this.map.get(key)
  if(t) {
      this.map.delete(key)
      this.map.set(key, value)
  } else {
      this.map.set(key, value)
      if(this.map.size > this.max_size) {
          const first = this.map.keys().next().value;
          this.map.delete(first)
      }
  }
};