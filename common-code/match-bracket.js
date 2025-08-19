/***
 * input: a{sdsd[sdfdsf(123123[]dsd)ads]asdas}ds
 * 判断字符串里的扩号是否匹配
 */

/**
 * 需要用数组模拟栈，左括号入栈，有括号要匹配后出栈
 * 栈是逻辑结构，可以用数组的API模拟出栈入栈
 * */
function testBracketMatch(s) {
  const stack = [];
  const leftSymbols= '{[(';
  const rightSymbols= '}])';

  function isMatch (a, b) {
    if (a==='{' && b ==='}') return true;
    if (a==='[' && b ===']') return true;
    if (a==='(' && b ===')') return true;
    return false;
  }

  for (let i = 0; i < s.length; i++) {
    const e = s[i];
    if (leftSymbols.includes(e)) {
      stack.push(e);
    }
    if (rightSymbols.includes(e)) {
      if (isMatch(stack[stack.length - 1], e)) {
        stack.pop();
      } else {
        return false;
      }
    }
  }
  return stack.length === 0;
}

console.log(testBracketMatch('{a{sdsd[sdfdsf(123123[]dsd)ads]asdas}ds}'))
