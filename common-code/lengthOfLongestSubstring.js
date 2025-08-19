/**
  给定一个字符串 s ，请你找出其中不含有重复字符的 最长 子串 的长度。
示例 1:

输入: s = "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
示例 2:

输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
示例 3:

输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。

提示：

0 <= s.length <= 5 * 104
s 由英文字母、数字、符号和空格组成
 */

/**
 * @param {string} s
 * @return {number}
 */
var lengthOfLongestSubstring_me = function(s) {
  const arr= Array.from(s)
  let res=0
  if(arr.length > 0) {
      let m=0, n=1, res=1
      for(; m < arr.length-1 && n< arr.length; n++) {
        if(arr.slice(m, n).includes(arr[n])){
          res = Math.max(n - m, res)
          m ++ 
          n = m
        } else if (n === arr.length -1) {
          res = Math.max(n - m+1, res)
          break
        } else {
          continue
        }
      }
      return res
  } else {
    return 0
  }
};


var lengthOfLongestSubstring = function(s) {
  // 哈希集合，记录每个字符是否出现过
  const occ = new Set();
  let l = 0, ans = 0;
  /**
   * 滑动窗口,双指针都从左侧开始移动
   * 1. 右指针不断向右移动，直到出现重复字符
   * 2. 左指针不断向右移动，直到重复字符被移除
   * 3. 重复步骤1和2，直到右指针到达字符串的末尾
   */
  for (let rk =0; rk < s.length; ++rk) {
      while (rk < s.length && occ.has(s.charAt(rk))) {
          // 不断地移动左指针直到occ中没有重复字符
          occ.delete(s.charAt(l));
          ++l;
      }
      occ.add(s.charAt(rk)); // 将当前字符添加到occ中
      // 第 l 到 rk 个字符无重复字符子串, 计算当前的最大长度
      ans = Math.max(ans, rk - l + 1);
  }
  return ans;
};
console.log(lengthOfLongestSubstring('abcb'))
// 作者：力扣官方题解
// 链接：https://leetcode.cn/problems/longest-substring-without-repeating-characters/solutions/227999/wu-zhong-fu-zi-fu-de-zui-chang-zi-chuan-by-leetc-2/
// 来源：力扣（LeetCode）
// 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。