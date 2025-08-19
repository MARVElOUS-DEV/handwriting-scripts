/**
 * on(type, callback)
 * off(type, callback)
 * fire(type)
 * once(type,callback)
 */

class EventEmitter {
  _listenerDic= new Map()

  on(type, callback) {
    if (typeof callback !== 'function') {
      throw new Error("callback should be a function")
    }
    if (typeof type !== 'string') {
      throw new Error("type should be string")
    }
    const typeList = this._listenerDic.get(type)
    this._listenerDic.set(type, typeList? typeList.push(callback) : [callback])
  }
  off(type,callback){
    if (typeof callback !== 'function') {
      throw new Error("callback should be a function")
    }
    if (typeof type !== 'string') {
      throw new Error("type should be string")
    }
    const typeList = this._listenerDic.get(type)
    if (typeList && typeList.length) {
      this._listenerDic.set(type, typeList.filter !== callback)
    }
  }
  once(type, callback) {
    if (typeof callback !== 'function') {
      throw new Error("callback should be a function")
    }
    if (typeof type !== 'string') {
      throw new Error("type should be string")
    }
    const newCallback = (...args) => {
      callback(...args)
      this.off(type, newCallback)
    }
    this.on(type, newCallback)
  }
  fire(type, ...args) {
    if (typeof type !== 'string') {
      throw new Error("type should be string")
    }
    const typeList = this._listenerDic.get(type)
    if (typeList && typeList.length) {
      for (const func of typeList) {
        func(...args)
      }
    }else {
      console.warn(`no ${type} registered`);
    }
  }
}

const bus = new EventEmitter();
const ACallback = () => {
  console.log("🚀 ~ bus.on ~ a")
}
const BCallback = () => {
  console.log("🚀 ~ bus.on ~ b")
}
bus.on('a', ACallback)

bus.on('b', BCallback)

bus.fire('a');
bus.fire('b');
bus.fire('c');
bus.off('b', BCallback);
bus.fire('b');
const DCallback = (...args) => {
  console.log(`d func called with ${args}`);
}
bus.once('d', DCallback);
bus.fire('d',1)
bus.fire('d',2)