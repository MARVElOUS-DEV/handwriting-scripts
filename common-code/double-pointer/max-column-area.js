/**
给定一个长度为 n 的整数数组 height 。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i]) 。

找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

返回容器可以储存的最大水量。
https://leetcode.cn/problems/container-with-most-water
 */

/**
 * @param {number[]} height
 * @return {number}
 */
var maxArea = function(height) {
    let mSize = 0;
    let l =0, r= height.length-1;
    while (l < r) {
        const size = Math.min(height[l], height[r]) * (r-l);
        mSize = Math.max(mSize, size);
        // 关键题解： 保持长边不动，短边向矩形内移动，若此时新的短边增高了，则有可能面积增大；如果长边向内移动，则面积必然减小。
        // 所以只要每次移动短边直到左右指针相遇即可找到最大面积
        height[l] > height[r] ? r--: l++; 
    }
    return mSize;
};