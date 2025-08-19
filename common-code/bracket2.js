/***
 * 有效的括号字符串

给你一个只包含三种字符的字符串，支持的字符类型分别是 '(' 、')' 和 '*'。请你检验这个字符串是否为有效字符串，如果是有效字符串返回true.
有效字符串符合如下规则:
- 任何左括号 '(' 必须有相应的右括号 ')' 
- 任何右括号 ')' 必须有相应的左括号 '('
- 左括号(必须在对应的右括号之前 
- '*'可以被视为单个右括号 ')'，或单个左括号 '('，或一个空字符串。
- 一个空字符串也被视为有效字符串。
示例 1:输入: s="()"输出: true
示例 2:
输入: s="(*)"
输出: true
示例 3:
输入: s="(*))"输出: true
 */


// ！！下面放的方法不行

function bracketExpressionValidate(s) {
  if (s) {
    let stack = [], flag = true
    const chars = s.split('').reverse()
    for (let i = 0; i < chars.length; i++) {
      const c = chars[i];
        
      if (stack.length === 0 ) {
        if (['*', ')'].includes(c)) {
          stack.push(c)
        } else {
          flag= false
          break
        }
      } else {
        if (isMatch(stack[stack.length -1], c)) {
          stack = stack.slice(0, stack.length -1)
        } else {
          stack.push(c)
        }
      }
    }
    const ret = flag && stack.filter(x => x !=='*').length === 0
    console.log(ret)
    return ret
  }
  function isMatch(target, incoming) {
    if (target === '(') {
      return false
    }
    if (target === ')') {
      return ['('].includes(incoming)
    }
    if (target === '*') {
      return ['(', '*'].includes(incoming)
    }
    return false;
  }

  throw new Error('输入不能为空')
}


// bracketExpressionValidate('*((*)')


// 计数法
/**
 * 算法思路
计数器：使用两个计数器，left_min 和 left_max，分别表示当前有效括号的最小和最大数量。
遍历字符串：
遇到 ( 时，left_min 和 left_max 都加 1。
遇到 ) 时，left_min 和 left_max 都减 1。
遇到 * 时，left_min 减 1（将 * 视为 )）和 left_max 加 1（将 * 视为 (）。
调整计数器：确保 left_min 不小于 0（如果小于 0，可以将其重置为 0），因为负数表示不可能有对应的左括号。
最终检查：在遍历结束后，left_min 应为 0，表示所有的左括号都有对应的右括号 } 
 */

function bracketExpressionValidate2(s) {
  let left_min = 0, left_max = 0, flag = true
  for (const c of s) {
    if (c === '(') {
      left_min += 1
      left_max += 1
    }
    if (c === '*') {
      left_min -= 1
      left_max += 1
    }
    if (c === ')') {
      left_min -= 1
      left_max -= 1
    }
    if (left_min < 0) {
      left_min = 0
    }
    if (left_max < 0) {
      flag = false
      break
    }
  }
  console.log(flag, left_min===0)
  if (flag === false) {
    return false
  }
  return left_min===0
}

bracketExpressionValidate2('*((*)')