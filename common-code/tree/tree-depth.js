/**
 * 给定一个二叉树 root ，返回其最大深度。

二叉树的 最大深度 是指从根节点到最远叶子节点的最长路径上的节点数。
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
 * @return {number}
 */
// 精简版
var maxDepthSimple = function(root) {
    if(root===null) return 0;
    return Math.max(maxDepth(root.left) + 1, maxDepth(root.right) + 1);
};
// 思路版
var maxDepth = function(root) {
    if(root===null) return 0;
    let height = 1;
    const recursive = (node, h) => {
        if(node===null) return h;
        return Math.max(recursive(node.left, h+1), recursive(node.right, h+1));
    }
    const l = recursive(root.left, 1)
    const r = recursive(root.right, 1)
    return Math.max(l,r);
};