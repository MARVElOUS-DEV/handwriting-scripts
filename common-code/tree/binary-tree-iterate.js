
/***
 * BFS : Broad First Search 广度优先遍历
给你二叉树的根节点 root ，返回其节点值的 层序遍历 。 （即逐层地，从左到右访问所有节点）。
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]
示例 2：

输入：root = [1]
输出：[[1]]
示例 3：

输入：root = []
输出：[]
 */


/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root
 * @return {number[][]}
 */
var levelOrder = function(root) {
  if (root === null) {
    return []
  }
  const queue = [root]
  const result = []
  while(queue.length) {
      const level = []
      const size = queue.length
      for(let i=0; i<size; i++) { // 关键点，队列中可能有多个节点，所以出队列的时候，存在不同层的节点处于一个队列里面，所以需要根据size来做同层一次性出队列---队列节点不需要全部出完
          const node = queue.shift()
          level.push(node.val)
          node.left && queue.push(node.left)
          node.right && queue.push(node.right)
      }
      result.push(level)
  }
  return result
};






/*solution explained: https://leetcode.cn/problems/binary-tree-level-order-traversal/solutions/244853/bfs-de-shi-yong-chang-jing-zong-jie-ceng-xu-bian-l/ 
BFS用队列出
DFS用递归
*/