/**
给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。
请注意 ，必须在不复制数组的情况下原地对数组进行操作。

示例 1:
输入: nums = [0,1,0,3,12]
输出: [1,3,12,0,0]
示例 2:
输入: nums = [0]
输出: [0]
https://leetcode.cn/problems/move-zeroes
 */

/**
 * @param {number[]} nums
 * @return {void} Do not return anything, modify nums in-place instead.
 */
var moveZeroes = function(nums) {
    let storeIndex = 0;
    for(let i=0; i< nums.length; i++) {
        if(nums[i]!==0) {
            nums[storeIndex++] = nums[i];
        }
    }
    while(storeIndex < nums.length) {
        nums[storeIndex++] = 0;
    }
};

// 借鉴快排寻找pivot位置的思想，因为寻找pivot位置的过程就是数组原地交换，
// pivot左侧全部大于0，右边小于等于0，就是当前问题的场景
// 不过这里并非需要全部大于0移动到左侧，只需要非0移动即可，这样，storeIndex指向的是第一个0的位置，后面的全部填上0即可。