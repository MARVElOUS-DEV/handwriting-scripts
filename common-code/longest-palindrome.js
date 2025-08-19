/**
给你一个字符串 s，找到 s 中最长的 回文 子串。
示例 1：
输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。
示例 2：
输入：s = "cbbd"
输出："bb"
提示：
1 <= s.length <= 1000
s 仅由数字和英文字母组成
 */

/**
 * @param {string} s
 * @return {string}
 */
var longestPalindrome = function(s) {
  if (s.length=== 1) {
    return s
  }
  if (s.length=== 2) {
    return s[0]===s[1] ? s : s[0]
  }
  let max = 0, pos=[0,0]
  for (let i = 1; i < s.length; i++) {
    let left = i-1
    let right = i+1
    while (left >= 0 && right < s.length && s[left] === s[i]) { //1. 向左扩散，此时有可能left变为-1
      left--
    }
    while (right < s.length && s[right] === s[i]) { // 2. 向右扩散时，需要去掉左侧left>=0；如果是先右侧扩散，那么需要补充left>=0,同时上方1处需要去除right<s.length 的条件
      right++
    }
    while (left >= 0 && right < s.length && s[left] === s[right]) {
      left--
      right++
    }
    max = max > right-left-1 ? max : right-left-1 // 正确位置是left+1, right-1，长度为right-1 -(left+1) -1= right-left-1
    pos = max > right-left-1 ? pos: [left+1, right-1]
  const res = s.slice(pos[0], pos[1]+1);
  console.log("🚀 ~ longestPalindrome ~ res:", res)
  
  return res
};

longestPalindrome("babad")