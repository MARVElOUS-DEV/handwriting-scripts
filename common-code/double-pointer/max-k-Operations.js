/**
给你一个整数数组 nums 和一个整数 k 。
每一步操作中，你需要从数组中选出和为 k 的两个整数，并将它们移出数组。
返回你可以对数组执行的最大操作数。
输入：nums = [1,2,3,4], k = 5
输出：2
解释：开始时 nums = [1,2,3,4]：
- 移出 1 和 4 ，之后 nums = [2,3]
- 移出 2 和 3 ，之后 nums = []
不再有和为 5 的数对，因此最多执行 2 次操作。
https://leetcode.cn/problems/max-number-of-k-sum-pairs
 */

/**
 * @param {number[]} nums
 * @param {number} k
 * @return {number}
 */
var maxOperations = function(nums, k) {
    const list = nums.sort((a,b) => a-b).filter(x => x<k);
    let res = 0;
    let l = 0, r = list.length-1;
    while(l < r) {
        const sum =list[l]+ list[r];
        if(sum===k) {
            res++;
            l++;
            r--;
        } else if(sum> k) {
            r--;
        } else {
            l++;
        }
    }
    return res;
};

// 解法2，O(N), 使用一个字典记录每个数据个数，在循环的时候，查询字典另一半是否存在，如果存在，则另一半个数减一；否则记录当前的数字个数。

var maxOperationsDict = function(nums, k) {
    const dict = new Map();
    let res = 0;
    for(const n of nums) {
        let cnt = dict.get(k-n);
        if(cnt !==undefined && cnt > 0) {
            res++;
            dict.set(k-n, --cnt)
        } else {
            dict.set(n, 1 + (dict.get(n)??0));
        }
    }
    return res;
};
maxOperationsDict([1,2,3,4], 5)


