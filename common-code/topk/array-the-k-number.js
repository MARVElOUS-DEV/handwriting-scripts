
/** 
给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。
请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。
你必须设计并实现时间复杂度为 O(n) 的算法解决此问题。
示例 1:

输入: [3,2,1,5,6,4], k = 2
输出: 5
示例 2:

输入: [3,2,3,1,2,4,5,5,6], k = 4
输出: 4

提示：

1 <= k <= nums.length <= 105
-104 <= nums[i] <= 104
*/

/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
var findKthLargest = function(nums, k) {
    
  // 使用快速选择算法，平均时间复杂度为 O(n)
  const quickSelect = (left, right, kSmallest) => {
    if (left === right) return nums[left];
  
    // 随机选择枢轴
    const pivotIndex = Math.floor(Math.random() * (right - left + 1)) + left;
    const pivotIndexAfterPartition = partition(left, right, pivotIndex);
  
    if (kSmallest === pivotIndexAfterPartition) {
      return nums[kSmallest];
    } else if (kSmallest < pivotIndexAfterPartition) {
      return quickSelect(left, pivotIndexAfterPartition - 1, kSmallest);
    } else {
      return quickSelect(pivotIndexAfterPartition + 1, right, kSmallest);
    }
  };
  
  // 分区函数，返回枢轴的最终位置
  const partition = (left, right, pivotIndex) => {
    const pivotValue = nums[pivotIndex];
    // 将枢轴交换到最右边
    [nums[pivotIndex], nums[right]] = [nums[right], nums[pivotIndex]];
    let storeIndex = left;
  
    for (let i = left; i < right; i++) {
      if (nums[i] > pivotValue) { // 降序排列，找第k大
        [nums[storeIndex], nums[i]] = [nums[i], nums[storeIndex]];
        storeIndex++;
      }
    }
    // 将枢轴交换到正确位置
    [nums[right], nums[storeIndex]] = [nums[storeIndex], nums[right]];
    return storeIndex;
  };
  
  // 调用快速选择，寻找第k大的元素（索引为k-1）
  const kthLargest = quickSelect(0, nums.length - 1, k - 1);
  console.log("🚀 ~ findKthLargest ~ kthLargest:", kthLargest)
  return kthLargest;
};


/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
var aFindKthLargest = function(nums, k) {
    const partition = (l,r,pivot) => {
        const pivotValue = nums[pivot]
        let storeIndex = l; // 注意此处的分号很重要
        [nums[pivot], nums[r]] = [nums[r], nums[pivot]]
        for(let i = l; i < r ; i++) {
            if(nums[i] > pivotValue) { // 降序排列，大的往前交换
                if(i !== storeIndex && nums[storeIndex]!==nums[i] ) { // 优化一下，相同的下标就不交换
                    [nums[storeIndex], nums[i]] = [nums[i], nums[storeIndex]]
                }
                storeIndex++
            }
        }
        [nums[storeIndex],nums[r]] = [nums[r],nums[storeIndex]]
        return storeIndex
    }

    const quickSelect =(l, r, theK) => {
        // 初始pivot 优化一下，随机取
        const initPivot = Math.floor( Math.random() * (r-l+1))+ l
        const p = partition(l, r, initPivot)
        if(p === theK-1) {
            return nums[p]
        } else if(p > theK-1) {
            return quickSelect(l, p-1, theK)
        } else {
            return quickSelect(p+1, r, theK)
        }
    }
    return quickSelect(0, nums.length-1, k)
};



// aFindKthLargest([3,2,3,1,2,4,5,5,6], 2)


//分三路，前面的比pivot大，中间的等于pivot，后面的比pivot小
const partition = (arr, left, right) => {
  if (left >= right) return [left, right]
  const pivotIndex = Math.floor(Math.random() * (right - left + 1)) + left
  const pivotValue = arr[pivotIndex];
  [arr[pivotIndex], arr[right]] = [arr[right], arr[pivotIndex]]
  let begin = left, i = left, end=right-1;
  while(i<=end && end >=begin){
    if(arr[i] > pivotValue) { // 降序排列，大的往前交换
      i!==begin && ([arr[i], arr[begin]] = [arr[begin], arr[i]]);
      begin++
      i++
    } else if(arr[i] < pivotValue) {
      i!==end && ([arr[i], arr[end]] = [arr[end], arr[i]]);
      end--
    }else {
      i++
    }
  }
  begin!== right && ([arr[begin], arr[right]] = [arr[right], arr[begin]])
  return [begin, end]
}

const quickSelect3 = (arr, left, right, k) => {
  if (left >= right) return arr[left]
  const [begin, end] = partition(arr, left, right)
  if (begin === k) return arr[begin]
  if (begin > k) { // begin 与 k 的比较优先级高于 end 与 k 的比较，否则会遗漏分支
    return quickSelect3(arr, left, begin-1, k)
  } else { // begin < k
  if (end === k) return arr[end];
    return  end > k ? quickSelect3(arr, begin+1, end-1, k): quickSelect3(arr, end+1, right, k)
  }
}

function aFindKthLargest3(nums, k) {
  const res =  quickSelect3(nums, 0, nums.length-1, k-1)
  console.log(res)
  return res
}
aFindKthLargest3([-1,2,0], 2)