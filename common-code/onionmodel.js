/**
 * 洋葱模型，有的地方也叫中间件模型，它有非常好的扩展性，在很多框架中有使用过，如koa，express, axios等
 * 关键点: 1.收集中间件 2. 串联起收集的中间件执行，通常也叫compose
 * refer: https://segmentfault.com/a/1190000037780772
 */


class MyOnionModel {
  middlewares = []
  async process(inStr) {
    const context = { param: inStr }
    const fn = this.compose(this.middlewares) // compose 需要返回一个方法
    await fn(context, async() => console.log('process core logic done'))
    console.log('done')
  }
  compose(mids) {
    return function(ctx, next) {
      let i = -1; // 记录最后执行的middleware 序号

      function dispatch(index) {
        if (index <= i) {
          throw new Error(`${index} 重复执行了`)
        }
        i = index
        let fn = mids[index]
        if (index === mids.length) fn = next
        if(!fn) return Promise.resolve()
        try {
          // 精髓之处，通过序号递归的将下一个middleware逻辑传递到给上一个中间件的next方法里
          // dispatch.bind 返回函数，区别使用箭头函数，因为会绑定this到当前实例
          return Promise.resolve(fn(ctx, dispatch.bind(null, index + 1))) 
        } catch (error) {
          return Promise.reject('error', index)
        }
      }
      return dispatch(0)
    }
  }
  use(m) {
    this.middlewares.push(m)
  }
}


const myApp = new MyOnionModel()

myApp.use(async(ctx, next) => {
  console.log('m1', ctx)
  await next()
  console.log('m1 after')
})

myApp.use(async(ctx, next) => {
  console.log('m2', ctx)
  await next()
  console.log('m2 after')
})


myApp.process('abc');