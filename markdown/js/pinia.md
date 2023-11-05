# pinia 笔记 📝

## store

* 什么是store

一个 Store （如 Pinia）是一个实体，它持有未绑定到您的组件树的状态和业务逻辑。换句话说，它托管全局状态。它有点像一个始终存在并且每个人都可以读取和写入的组件。它有三个概念，state、getters 和 actions 并且可以安全地假设这些概念等同于组件中的“数据”、“计算”和“方法”。

* 定义一个 Store

Store 是使用 defineStore() 定义的，并且它需要一个唯一名称，作为第一个参数传递：  

```js
import { defineStore } from 'pinia'

// useStore 可以是 useUser、useCart 之类的任何东西
// 第一个参数是应用程序中 store 的唯一 id
export const useStore = defineStore('main', {
  // other options...
})
```

* 使用store
  
1. 直接拿 store 进行渲染
store 是一个用reactive 包裹的对象，这意味着不需要在getter 之后写.value，但是，就像setup 中的props 一样，我们不能对其进行解构, 解构会破坏响应式

```js
export default defineComponent({
  setup() {
    const store = useStore()
    // ❌ 这不起作用，因为它会破坏响应式
    // 这和从 props 解构是一样的
    const { name, doubleCount } = store //解构

    name // "eduardo"
    doubleCount // 2

    return {
      // 一直会是 "eduardo"
      name,
      // 一直会是 2
      doubleCount,
      // 这将是响应式的
      doubleValue: computed(() => store.doubleCount),
      }
  },
})
```
1. 使用storeToRefs解构
为了从 Store 中提取属性同时保持其响应式，您需要使用storeToRefs()。 它将为任何响应式属性创建 refs。 当您仅使用 store 中的状态但不调用任何操作时，这很有用

```js
import { storeToRefs } from 'pinia'

export default defineComponent({
  setup() {
    const store = useStore()
    // `name` 和 `doubleCount` 是响应式引用
    // 这也会为插件添加的属性创建引用
    // 但跳过任何 action 或 非响应式（不是 ref/reactive）的属性
    const { name, doubleCount } = storeToRefs(store)

    return {
      name,
      doubleCount
    }
  },
})
```


## State

在 Pinia 中，状态被定义为返回初始状态的函数。 Pinia 在服务器端和客户端都可以工作

```js
import { defineStore } from 'pinia'

const useStore = defineStore('storeId', {
  // 推荐使用 完整类型推断的箭头函数
  state: () => {
    return {
      // 所有这些属性都将自动推断其类型
      counter: 0,
      name: 'Eduardo',
      isAdmin: true,
    }
  },
})
```

* 访问 “state”

通过 store 实例访问状态来直接读取和写入状态：

```js
const store = useStore()

store.counter++

```

* 重置状态

过调用 store 上的 $reset() 方法将状态 重置 到其初始值

* 用 Composition API  
使用的是 computed、methods、...，则可以使用 mapState() 帮助器将状态属性映射为只读计算属性：

```js
import { mapState } from 'pinia'
import { useCounterStore } from '../stores/counterStore'

export default {
computed: {
  // 允许访问组件内部的 this.counter
  // 与从 store.counter 读取相同
  ...mapState(useCounterStore, {
    myOwnName: 'counter',
    // 您还可以编写一个访问 store 的函数
    double: store => store.counter * 2,
    // 它可以正常读取“this”，但无法正常写入...
    magicValue(store) {
      return store.someGetter + this.counter + this.double
    },
  }),
},
}
```

* 使用map helper   
  使用 computed、methods、...，则可以使用 mapState() 帮助器将状态属性映射为只读计算属性

```js
import { mapState } from 'pinia'
import { useCounterStore } from '../stores/counterStore'

export default {
  computed: {
    // 允许访问组件内部的 this.counter
    // 与从 store.counter 读取相同
    ...mapState(useCounterStore, {
      myOwnName: 'counter',
      // 您还可以编写一个访问 store 的函数
      double: store => store.counter * 2,
      // 它可以正常读取“this”，但无法正常写入...
      magicValue(store) {
        return store.someGetter + this.counter + this.double
      },
    }),
  },
}
```

* 可修改状态  
希望能够写入这些状态属性（例如，如果您有一个表单），您可以使用 mapWritableState() 代替。 请注意，您不能传递类似于 mapState() 的函数

## Getters

Getter 完全等同于 Store 状态的 计算值

* 访问其他 getter  
  可以组合多个 getter。 通过 this 访问任何其他 getter
* 将参数传递给 getter  
  可以从 getter 返回一个函数以接受任何参数

```js
import { useOtherStore } from './other-store'

export const useStore = defineStore('main', {
  state: () => ({
    // ...
  }),
  getters: {
    otherGetter(state) {
      const otherStore = useOtherStore()
      return state.localData + otherStore.data
    },
  },
})
```

* 与 setup() 一起使用 直接访问任何 getter 作为 store 的属性

## actions

Actions 相当于组件中的 methods。 它们可以使用 defineStore() 中的 actions 属性定义，并且它们非常适合定义业务逻辑

actions 可以是异步的，您可以在其中await 任何 API 调用甚至其他操作