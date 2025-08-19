
/**
 * 给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。

注意：答案中不可以包含重复的三元组。

示例 1：

输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]
解释：
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0 。
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0 。
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0 。
不同的三元组是 [-1,0,1] 和 [-1,-1,2] 。
注意，输出的顺序和三元组的顺序并不重要。
示例 2：

输入：nums = [0,1,1]
输出：[]
解释：唯一可能的三元组和不为 0 。
示例 3：

输入：nums = [0,0,0]
输出：[[0,0,0]]
解释：唯一可能的三元组和为 0 。

提示：

3 <= nums.length <= 3000
-105 <= nums[i] <= 105
 */


/**
 * @param {number[]} nums
 * @return {number[][]}
 */
var threeSum = function(nums) {
  const list = nums.sort((a,b) =>  a-b)
  if(list.length<3) {
      return []
  }
  if(list[0] > 0) { // 数字全部大于0，直接退出循环
    return []
  }
  let res = []
  for(let l = 0; l < list.length; l++) {
    if(l > 0 && list[l-1] === list[l]) { // 对第一个数字去重
      continue
    }
    if(list[l] > 0) { // 第一个数字大于0，后面的数字都大于0，直接退出循环
      break
    }
    let m = l+1 ,r=list.length -1
    if(m > r-1) {
        break
    }

    while(m < r) {
      while(list[l] + list[m] + list[r]>0 && m<r){
          r--
      }
      while(list[l] + list[m] + list[r]<0 && m<r){
          m++
      }
      if(m===r) {
        break
      }
      if(list[l] + list[m] + list[r]===0) { // 找到一组后开始去重，此时对第二个数字list[m]和第三个数字list[r]去重
        
        res.push([list[l], list[m], list[r]])
        while(list[m] === list[m+1]) {
          m++
        }
        while(list[r] === list[r-1]) {
          r--
        }
        m++
        r--
      }
    }
      
  }
  console.log(res.toString())
  return res
};

// threeSum([-1,0,1,2,-1,-4])
// threeSum([0,0,0,0])

// [-4,-1,-1,0,1,2]

var threeSum_Test = function(nums) {
    const list = nums.sort()
    if(list[0]>0) return [];
    const len = nums.length;
    if(len<3) return [];
    let res=[]
    for(let left=0; left < len-2; left++) {
        if(left > 0 && nums[left] === nums[left-1]) continue; // ⚠️注意，不能写成nums[left]===nums[left+1]
        let mid = left+1, right=len-1;
        while(mid < right) { // 第一个数固定，第2、3 个数变化
            let t = list[left]+ list[mid] + list[right];
            while(t>0 && right>mid) {
                right--
                t = list[left]+ list[mid] + list[right];
            }
            while(t<0 && mid< right) {
                mid++
                t = list[left]+ list[mid] + list[right];
            }
            if(mid>=right) break;
            if(t===0) {
                res.push([list[left], list[mid] , list[right]]);
                // 去重
                while(list[mid+1]===list[mid] && mid < right) mid++;
                while(list[right-1]===list[right] && mid < right) right--;
                mid++;
                right--;
            }
        }
    }
    console.log("🚀 ~ res:", res)
    return res;
};
threeSum_Test([2,-3,0,-2,-5,-5,-4,1,2,-2,2,0,2,-4,5,5,-10])
