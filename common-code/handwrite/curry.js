/**
 * a(1,2,3)
 * a(1,2)(3)
 * a(1)(2)(3)
 **/

function curry(func) {
  if (typeof func !== 'function') {
    throw new Error("should be a function")
  }
  const len = func.length
  let finalArgs = []
  const loop =  (...args) => {
    finalArgs = finalArgs.concat(args)
    if(finalArgs.length < len){
      return (...a) => {
        return loop(...a)
      }
    } else {
      return func(...finalArgs)
    }
  }
  return loop;
}

/**
 * 参数收集器，偏函数
 */
const curry2 = (fn) => (...args) =>  fn.bind(null, ...args);



const AFunc = (a, b, c) => {
  return a + b + c
}

const curriedAFunc = curry(AFunc)
const curriedBFunc = curry(AFunc)
const curriedCFunc = curry(AFunc)

const test1 = curriedAFunc(1,2,3)
console.log("🚀 ~ test1:", test1)
const test2 = curriedBFunc(1)(2)(4)
console.log("🚀 ~ test2:", test2)
const test3 = curriedCFunc(1, 2)(5)
console.log("🚀 ~ test3:", test3)

const curriedDFunc= curry2(AFunc)
const test4 = curriedDFunc(4,2)(3)
console.log("🚀 ~ test4:", test4)
