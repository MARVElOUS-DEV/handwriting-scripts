class OClass {
  name = null
  constructor(name) {
    this.name = name;
  }
  call() {
    console.log(this.name);
  }
}

/**
 * 使用闭包和IIFE
 */

OClass.getInstance = (() => {
  let instance;
  return () => {
    if (instance) {
      return instance;
    }else {
      return instance = new OClass('singleton');
    }
  }
})()

const a = OClass.getInstance();
const b = OClass.getInstance();
console.log('a === b ? ',a==b)
