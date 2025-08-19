/**
给你一个整数数组 nums ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
子数组是数组中的一个连续部分。

示例 1：
输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。
示例 2：
输入：nums = [1]
输出：1
示例 3：
输入：nums = [5,4,-1,7,8]
输出：23

提示：
1 <= nums.length <= 105
-104 <= nums[i] <= 104
 */

/**
 * @param {number[]} nums
 * @return {number}
 */
var maxSubArray = function(nums) {
  let max = Number.NEGATIVE_INFINITY
  let count = 0
  for(let i=0; i< nums.length; i++) {
      const sum = count+nums[i]
      if(sum<0) {
        count = 0
      } else {
        count = sum
      }
      max = max > sum? max: sum
  }
  console.log(max)
  return max
};

// maxSubArray([-2,1,-3,4,-1,2,1,-5,4])
maxSubArray([-1,0,-2])