# vue学习笔记 📝

## 组合式函数

“组合式函数”(Composables) 是一个利用 Vue 的组合式 API 来封装和复用有状态逻辑的函数。  

### vue3中最重要的API——ref和reactive

* 第一部分、数据的「响应式」  
  ref和reactive是干什么用？就是把数据变成「响应式」的，ue 核心思想——数据驱动视图。你已经看到，数据和 DOM 被建立了关联，所有东西都是「响应式」的，数据（JS）counter变化，视图层（HTML）就会跟着变化。

* Vue3的响应式

1. Proxy 对象
   Proxy 对象：用于创建一个对象的代理，主要用于改变对象的默认访问行为，实际上是在访问对象之前增加一层拦截，在任何对对象的访问行为都会通过这层拦截。在这层拦截中，我们可以增加自定义的行为。基本语法如下：

   ```js
    /*
    * target: 目标对象
    * handler: 配置对象，用来定义拦截的行为
    * proxy: Proxy构造器的实例
    */
    var proxy = new Proxy(target,handler)
   ```

2. Proxy 对象基本用法  
看个简单例子：

  ```js

  var target = {
    num:1
  }
  // 自定义访问拦截器
  var handler = {
    // receiver: 操作发生的对象，通常是代理
    get:function(target,prop,receiver){
      console.log(target,prop,receiver)
      return target[prop]*2
    },
    set:function(trapTarget,key,value,receiver){
      console.log(trapTarget.hasOwnProperty(key),isNaN(value))
      if(!trapTarget.hasOwnProperty(key)){
        if(typeof value !== 'number'){
          throw new Error('入参必须为数字')
        }
        return Reflect.set(trapTarget,key,value,receiver)
      }
    }
  }
  // 创建target的代理实例dobuleTarget
  var dobuleTarget = new Proxy(target,handler)
  console.log(dobuleTarget.num) // 2
  
  dobuleTarget.count = 2
  // 代理对象新增属性，目标对象也跟着新增
  console.log(dobuleTarget) // {num: 1, count: 2}
  console.log(target)  // {num: 1, count: 2}
  // 目标对象新增属性，Proxy能监听到
  target.c = 2
  console.log(dobuleTarget.c)  // 4 能监听到target新增的属
  ```

  例子里，我们通过Proxy构造器创建了target的代理dobuleTarget，即是代理了整个target对象，此时通过对dobuleTarget属性的访问都会转发到target身上，并且针对访问的行为配置了自定义handler对象。因此任何通过dobuleTarget访问target对象的属性，都会执行handler对象自定义的拦截操作。
  Proxy 对象可以拦截对data任意属性的任意(13种)操作, 包括属性值的读写, 属性的添加, 属性的删除等..这些操作被拦截后会触发响应特定操作的「陷阱函数」。
  这13种「陷阱函数」如下图所示：  

  | 陷阱函数 | 覆写的特性 |
  |----------|:-------------:|
  | get | 读取一个值 |
  | set | 写入一个值 |
  | has | in操作符 |
  | deleteProperty | Object.getPrototypeOf() |
  | getPrototypeOf | Object.getPrototypeOf() |
  | setPrototypeOf | Object.setPrototypeOf() |
  | isExtensible | Object.isExtensible() |
  | preventExtensions | Object.preventExtensions() |
  | getOwnPropertyDescriptor | Object.getOwnPropertyDescriptor() |
  | defineProperty | Object.defineProperty |
  | ownKeys | Object.keys() Object.getOwnPropertyNames()和Object.getOwnPropertySymbols()
  | apply | 调用一个函数 |
  | construct | 用new调用一个函数 |

**Proxy 对象比Object.defineProperty更牛逼！它把vue2响应式的硬伤全部解决了！总结一下**：  

* Proxy是对整个对象的代理，而Object.defineProperty只能代理某个属性。
* 对象上新增属性，Proxy可以监听到，Object.defineProperty不能。
* 数组新增修改，Proxy可以监听到，Object.defineProperty不能。
* 若对象内部属性要全部递归代理，Proxy可以只在调用的时候递归，而Object.definePropery需要一次完成所有递归，性能比Proxy差。
* Proxy不兼容IE，Object.defineProperty不兼容IE8及以下
* Proxy使用上比Object.defineProperty方便多。
* Vue3的响应式具体实现  
  Vue3的响应式实现，正是使用了这个强大的Proxy代理对象，Vue 会将该数据包裹在一个带有 get 和 set 处理程序的 Proxy 中。当Proxy 对象监听到了的数据变更时，通过 Reflect(反射): 动态对被代理对象的相应属性进行特定的操作，具体代码如下：  

  ```js
  new Proxy(data, {
  // 拦截读取属性值
    get (target, prop) {
     return Reflect.get(target, prop)
    },
    // 拦截设置属性值或添加新属性
    set (target, prop, value) {
     return Reflect.set(target, prop, value)
    },
    // 拦截删除属性
    deleteProperty (target, prop) {
     return Reflect.deleteProperty(target, prop)
    }
  })
  proxy.name = 'tom'
  ```

  例子：

  ```js
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proxy 与 Reflect</title>
  </head>
  <body>
    <script>
      
      const user = {
        name: "John",
        age: 12
      };
  
      /* 
      proxyUser是代理对象, user是被代理对象
      后面所有的操作都是通过代理对象来操作被代理对象内部属性
      */
      const proxyUser = new Proxy(user, {
  
        get(target, prop) {
          console.log('劫持get()', prop)
          return Reflect.get(target, prop)
        },
  
        set(target, prop, val) {
          console.log('劫持set()', prop, val)
          return Reflect.set(target, prop, val); // (2)
        },
  
        deleteProperty (target, prop) {
          console.log('劫持delete属性', prop)
          return Reflect.deleteProperty(target, prop)
        }
      });
      // 读取属性值
      console.log(proxyUser===user)
      console.log(proxyUser.name, proxyUser.age)
      // 设置属性值
      proxyUser.name = 'bob'
      proxyUser.age = 13
      console.log(user)
      // 添加属性
      proxyUser.sex = '男'
      console.log(user)
      // 删除属性
      delete proxyUser.sex
      console.log(user)
    </script>
  </body>
  </html>
  ```

3. Proxy递归代理  
   Proxy只代理对象的外层属性。例子如下：  
   那么针对内层属性的变更，如何实现代理呢？答案是递归设置代理：

    ```js
    var target = {
      a:1,
      b:{
        c:2,
        d:{e:3}
      }
    }
    var handler = {
      get:function(trapTarget,prop,receiver){
        var val = Reflect.get(trapTarget,prop)
        console.log('get',prop)
        if(val !== null && typeof val==='object'){
          return new Proxy(val,handler) // 代理内层
        }
        return Reflect.get(trapTarget,prop)
      },
      set:function(trapTarget,key,value,receiver){
        console.log('触发set:',key,value)
        return Reflect.set(trapTarget,key,value,receiver)
      }
    }
    var proxy = new Proxy(target,handler)
    proxy.b.d.e
    // 输出： 均被代理
    // get b
    // get d
    // get e

    ```

从递归代理可以看出，如果对象内部要全部递归代理，Proxy可以只在调用时递归设置代理。

* vue3的reative和ref  
  1.reative
  含义：将「引用类型」数据转换为「响应式」数据，即，把值类型的数据包装编程响应式的引用类型的数据  
  类型：函数  
  参数：reactive参数必须是对象(json/arr)  
  本质: 将传入的数据包装成一个Proxy对象  
  手写reative函数实现：

  ```js
    const reactiveHandler = {
    get (target, key) {
  
      if (key==='_is_reactive') return true
  
      return Reflect.get(target, key)
    },
  
    set (target, key, value) {
      const result = Reflect.set(target, key, value)
      console.log('数据已更新, 去更新界面')
      return result
    },
  
    deleteProperty (target, key) {
      const result = Reflect.deleteProperty(target, key)
      console.log('数据已删除, 去更新界面')
      return result
    },
  }
  
  
  /* 
  自定义reactive
  */
  function reactive (target) {
    if (target && typeof target==='object') {
      if (target instanceof Array) { // 数组
        target.forEach((item, index) => {
          target[index] = reactive(item)
        })
      } else { // 对象
        Object.keys(target).forEach(key => {
          target[key] = reactive(target[key])
        })
      }
  
      const proxy = new Proxy(target, reactiveHandler)
      return proxy
    }
  
    return target
  }
  /* 测试自定义reactive */
  const obj = {
    a: 'abc',
    b: [{x: 1}],
    c: {x: [11]},
  }
  
  const proxy = reactive(obj)
  console.log(proxy)
  proxy.b[0].x += 1
  proxy.c.x[0] += 1
  ```

看到这里，你可能会想：既然reative函数已经实现了数据的「响应式」，那为什么还会有另一个实现「响应式」的函数——ref？
现在我来解答这个问题，你需要注意一下，在reative函数定义中，有这么一句：将「引用类型」数据转换为「响应式」数据。这个「引用类型」是什么？
这个就要从JS的数据类型讲起了

* JS的数据类型  
  1）栈(stack)和堆（heap）
  stack为自动分配的内存空间，它由系统自动释放；而heap则是动态分配的内存，大小也不一定会自动释放

  2）数据类型
  JS分两种数据类型：  
  基本数据类型：Number、String、Boolean、Null、 Undefined、Symbol（ES6），这些类型可以直接操作保存在变量中的实际值。  
  引用数据类型：Object（在JS中除了基本数据类型以外的都是对象，数据是对象，函数是对象，正则表达式是对象）

  3）基本数据类型（存放在栈中）
  基本数据类型是指存放在栈中的简单数据段，数据大小确定，内存空间大小可以分配，它们是直接按值存放的，所以可以直接按值访问  
  4）引用数据类型（存放在堆内存中的对象，每个空间大小不一样，要根据情况进行特定的配置）
  Proxy对象只能代理引用类型的对象，面对基本数据类型你如何实现响应式呢？

vue的解决方法是把基本数据类型变成一个对象：这个对象只有一个value属性，value属性的值就等于这个基本数据类型的值。然后，就可以用reative方法将这个对象，变成响应式的Proxy对象。

这个带有value属性的ref对象，整个过程的方法vue3封装在了ref函数里，即，ref的本质是  
ref(0) --> reactive( { value:0 })  
理解了这点，你再看ref就很简单了很多~

*ref
作用：1.把基本类型的数据包装编程响应式的引用类型的数据。
2.获取DOM元素： 在Vue3.x中我们也可以通过ref函数来获取元素  
类型：函数  
参数：1.基本数据类型
2.引用类型类型（最好别传，传了也是内部调用reative）
3.DOM的ref属性值  
本质: 将传入的数据包装成一个Proxy对象  
使用：1.把基本类型数据转换响应式：通过返回值的 value 属性获取响应式的值 ，修改也需要对 .value进行修改。注意，在js中要.value, 在模板中则不需要(内部解析模板时会自动添加.value)。

* ref和reactive的区别  
  ref是把值类型添加一层包装，使其变成响应式的引用类型的值。  
  reactive 则是引用类型的值变成响应式的值。  
  所以两者的区别只是在于是否需要添加一层引用包装  
  再次声明：本质上，ref(0)  等于 reactive( { value:0 })
* ref和reative的使用心得  
  1）写法1：reative声明所有变量，最后return的时候一起toRefs

  ```js
  <template>
    <h2>name: {{state.name}}</h2>
    <h2>age: {{state.age}}</h2>
    <h2>wife: {{state.wife}}</h2>
    <hr>
    <button @click="update">更新</button>
  </template>
  
  <script>
  /* 
  reactive: 
      作用: 定义多个数据的响应式
      const proxy = reactive(obj): 接收一个普通对象然后返回该普通对象的响应式代理器对象
      响应式转换是“深层的”：会影响对象内部所有嵌套的属性
      内部基于 ES6 的 Proxy 实现，通过代理对象操作源对象内部数据都是响应式的
  */
  import {
    reactive,toRefs
  } from 'vue'
  export default {
    setup () {
      /* 
      定义响应式数据对象
      */
      const state = reactive({
        name: 'tom',
        age: 25,
        wife: {
          name: 'marry',
          age: 22
        },
      })
      console.log(state, state.wife)
  
      const update = () => {
        state.name += '--'
        state.age += 1
        state.wife.name += '++'
        state.wife.age += 2
      }
  
      return {
        ...toRefs(state)
      }
    }
  }
  </script>
  ```

  2）写法2：从头到尾都用ref声明变量，赋值的时候要注意加.value

## 状态管理

每一个 Vue 组件实例都已经在“管理”它自己的响应式状态了
当我们有多个组件共享一个共同的状态时，就没有这么简单了：  

1. 多个视图可能都依赖于同一份状态。  
2. 来自不同视图的交互也可能需要更改同一份状态。  
对于情景 1，一个可行的办法是将共享状态“提升”到共同的祖先组件上去，再通过 props 传递下来。然而在深层次的组件树结构中这么做的话，很快就会使得代码变得繁琐冗长。这会导致另一个问题：Prop 逐级透传问题。  
对于情景 2，我们经常发现自己会直接通过模板引用获取父/子实例，或者通过触发的事件尝试改变和同步多个状态的副本。但这些模式的健壮性都不甚理想，很容易就会导致代码难以维护。

* 用响应式 API 做简单状态管理
  在选项式 API 中，响应式数据是用 data() 选项声明的。在内部，data() 的返回值对象会通过 reactive() 这个公开的 API 函数转为响应式。如果你有一部分状态需要在多个组件实例间共享，你可以使用 reactive() 来创建一个响应式对象，并将它导入到多个组件中