/**
 * 给你一个二叉树的根节点 root ， 检查它是否轴对称
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
 * @return {boolean}
 */
var isSymmetric = function(root) {
    
    const symmetricJudge = (p, q)  => {
        if(p ===null && q === null) return true;
        if(p ===null && q !== null) return false;
        if(p !==null && q === null) return false;
        if(p.val !== q.val) return false;
        const outSame = symmetricJudge(p.left, q.right);
        const innerSame = symmetricJudge(p.right, q.left);
        return outSame && innerSame;
    }
    return symmetricJudge(root.left, root.right);
};