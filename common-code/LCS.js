/***
 * 求两个字符串的最长公共子串
 * 输入: 
 * abcadf
 * acbad
 * 输出:
 * 2
 * 
 * solution explain refer: https://blog.csdn.net/weixin_44572229/article/details/121816153
 */

function print2DArray(a) {
  for (let i = 0; i < a.length; i++) {
    console.log(a[i]);
  }
}


function lcs(aStr, bStr) {
  // 从1开始，因为状态转移方程是dp[i][j]=dp[i-1][j-1]+1
  const aArr = aStr.split('');
  const bArr = bStr.split('');
  // 注意，如果是new Array(aArr.length+1).fill(对象), 改动其中一个对象，其余的都会变化，应该是指向了同一个对象
  let dp = new Array(aArr.length+1).fill(undefined).map(() => new Array(bArr.length+1).fill(0)); // 初始化base状态
  let max=0; 
  for (let index = 1; index < aStr.length + 1; index++) {
    const ae = aArr[index-1];
    for (let i = 1; i < bStr.length + 1; i++) {
      const be = bArr[i-1];
      if (ae == be) {
        dp[index][i] = dp[index-1][i-1] + 1; // 状态转移方程
      } else {
        dp[index][i] = 0;
      }
      if (dp[index][i] >= max) {
        max = dp[index][i];
      }
    }
  }
  print2DArray(dp);
  console.log(`max: ${max}`);
  return max;
}

lcs('aaccab', 'abaccb');







0,0,1,0,0,0,1
0,0,1,0,0,0,1
0,0,1,0,0,0,1