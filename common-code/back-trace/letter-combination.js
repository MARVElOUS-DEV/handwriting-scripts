/**
给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。答案可以按 任意顺序 返回。
给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。
示例 1：

输入：digits = "23"
输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]
示例 2：

输入：digits = ""
输出：[]
示例 3：

输入：digits = "2"
输出：["a","b","c"]

提示：
数字和字母的映射关系如下（与电话按键相同）。注意 1 不对应任何字母。
{
    2: 'abc',
    3: "def", 
    4: "ghi", 
    5: "jkl", 
    6: "mno", 
    7: "pqrs",
    8: "tuv", 
    9: "wxyz",
}
0 <= digits.length <= 4
digits[i] 是范围 ['2', '9'] 的一个数字。
https://leetcode.cn/problems/letter-combinations-of-a-phone-number/description/
 */

const digitMap = {
    2: 'abc',
    3: "def", 
    4: "ghi", 
    5: "jkl", 
    6: "mno", 
    7: "pqrs",
    8: "tuv", 
    9: "wxyz",
}
/**
 * @param {string} digits
 * @return {string[]}
 */
var letterCombinations = function(digits) {
    const result = [];
    let str = ''
    if(!digits) return result;
    const size = digits.length;
    function backTracing(curStr,index) {
        if(str.length===size) {
            result.push(str);
            return
        }
        const t = digits.charAt(index);
        const mapStr = digitMap[t]; 
        for(const s of mapStr) {
            str = curStr + s;
            backTracing(str, index + 1); // 注意这里不要使用 ++index, 会导致外部的index+1，造成访问数组越界
            str= '';
        }
    }
    backTracing('',0);
    return result;
};

letterCombinations('23')