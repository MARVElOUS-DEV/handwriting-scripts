/**
 * 1. Fn = fn.myBind(owner, a, b) 考察bind和this指向
 * 2. const instance = new Fn() 考察 new.target
 */
Function.prototype.myBind= function() {
  const owner = arguments[0]
  const outerArgs = Array.prototype.slice.call(arguments, 1)
  owner.fn= this;
  return function() {
    const innerArgs = Array.prototype.slice.call(arguments, 0)
    if (new.target !== 'undefined') {
      const uniFn = owner.fn;
      return uniFn.apply(this, ...outerArgs.concat(innerArgs))
    } else {
      return owner.fn(...outerArgs.concat(innerArgs))
    }
  }
}

globalThis.a = 1
globalThis.b = 2
function test() {
  return this.a + this.b
}
// console.log("🚀 ~ test ~ test:", test())

const test2 = test.myBind({a: 3, b: 4 })
console.log("🚀 ~ test2:", test2())

const test3 = new test2()
console.log("🚀 ~ test3:", test3 instanceof test2)