/**
给你一个长度为 n 的整数数组 nums 和 一个目标值 target。请你从 nums 中选出三个整数，使它们的和与 target 最接近。
返回这三个数的和。

假定每组输入只存在恰好一个解。
示例 1：
输入：nums = [-1,2,1,-4], target = 1
输出：2
解释：与 target 最接近的和是 2 (-1 + 2 + 1 = 2)。
示例 2：

输入：nums = [0,0,0], target = 1
输出：0
解释：与 target 最接近的和是 0（0 + 0 + 0 = 0）。

提示：
3 <= nums.length <= 1000
-1000 <= nums[i] <= 1000
-104 <= target <= 104
 */
/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number}
 */
var threeSumClosest = function(nums, target) {
    const list = nums.sort((a,b)=> a-b);
    let left = 0, right = nums.length -1;
    let res = null;
    let resFind = false;
    for(let mid=left+1; mid < right && !resFind; mid++) { // 外层循环确定中间数mid位置
      while(left< mid && mid < right) { // 内层双指针left，right分别移动收缩，更新每一次的最近值
        let sum = list[left] + list[mid]+ list[right];
        res = res === null? sum: getClosest(target, res, sum);
        if(sum > target) {
          right--;
        }
        if(sum < target) {
          left++;
        }
        if(sum === target) {
          resFind = true;
          break;
        }
      }
      left = 0; right = nums.length -1; // reset
    }
    return res;
};

function getClosest(target, a, b) {
    return Math.abs(a-target) > Math.abs(b-target) ? b: a;
}
threeSumClosest([1,3,4,7,8,9], 15)
// threeSumClosest([-84,92,26,19,-7,9,42,-51,8,30,-100,-13,-38], 78)