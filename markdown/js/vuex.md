# vuex笔记

vuex 是一个专为 Vue.js 应用程序开发的状态管理模式 + 库。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。

vuex 可以帮助我们管理共享状态，并附带了更多的概念和框架。这需要对短期和长期效益进行权衡。  
如果您不打算开发大型单页应用，使用 Vuex 可能是繁琐冗余的。确实是如此——如果您的应用够简单，您最好不要使用 Vuex。一个简单的 store 模式就足够您所需了。但是，如果您需要构建一个中大型单页应用，您很可能会考虑如何更好地在组件外部管理状态，Vuex 将会成为自然而然的选择

## 开始

每一个 Vuex 应用的核心就是 store（仓库）。“store”基本上就是一个容器，它包含着你的应用中大部分的状态 (state)。Vuex 和单纯的全局对象有以下两点不同：

1. Vuex 的状态存储是响应式的。当 Vue 组件从 store 中读取状态的时候，若 store 中的状态发生变化，那么相应的组件也会相应地得到高效更新。

2. 你不能直接改变 store 中的状态。改变 store 中的状态的唯一途径就是显式地提交 (commit) mutation。这样使得我们可以方便地跟踪每一个状态的变化，从而让我们能够实现一些工具帮助我们更好地了解我们的应用。

* 创建  
   创建一个 store。创建过程直截了当——仅需要提供一个初始 state 对象和一些 mutation
   可以通过 store.state 来获取状态对象，并通过 store.commit 方法触发状态变更  
**强调**，我们通过提交 mutation 的方式，而非直接改变 store.state.count，是因为我们想要更明确地追踪到状态的变化。这个简单的约定能够让你的意图更加明显，这样你在阅读代码的时候能更容易地解读应用内部的状态改变。此外，这样也让我们有机会去实现一些能记录每次状态改变，保存状态快照的调试工具。有了它，我们甚至可以实现如时间穿梭般的调试体验。
由于 store 中的状态是响应式的，在组件中调用 store 中的状态简单到仅需要在计算属性中返回即可。触发变化也仅仅是在组件的 methods 中提交 mutation。

## 核心概念

* State
  uex 使用单一状态树——是的，用一个对象就包含了全部的应用层级状态。至此它便作为一个“唯一数据源 (SSOT)”而存在。这也意味着，每个应用将仅仅包含一个 store 实例

* 在 Vue 组件中获得 Vuex 状态
  1. 从 store 实例中读取状态最简单的方法就是通过store.state.count 中返回某个状态
  2. uex 通过 Vue 的插件系统将 store 实例从根组件中“注入”到所有的子组件里。且子组件能通过 this.$store 访问到
  3. mapState 辅助函数

   ```js
    // 在单独构建的版本中辅助函数为 Vuex.mapState
    import { mapState } from 'vuex'

    export default {
    // ...
    computed: mapState({
        // 箭头函数可使代码更简练
        count: state => state.count,

        // 传字符串参数 'count' 等同于 `state => state.count`
        countAlias: 'count',

        // 为了能够使用 `this` 获取局部状态，必须使用常规函数
        countPlusLocalState (state) {
        return state.count + this.localCount
        }
    })
    }
   ```

   当映射的计算属性的名称与 state 的子节点名称相同时，我们也可以给 mapState 传一个字符串数组
  4. 对象展开运算符 javaScript 的 对象展开运算符 ... 是一种从数组、对象或任何您可以迭代到函数或变量赋值的东西传递多个值的简便方法。
  5. 组件仍然保有局部状态使用 Vuex 并不意味着你需要将所有的状态放入 Vuex。虽然将所有的状态放到 Vuex 会使状态变化更显式和易调试，但也会使代码变得冗长和不直观。如果有些状态严格属于单个组件，最好还是作为组件的局部状态。你应该根据你的应用开发需要进行权衡和确定

## Getter

Vuex 允许我们在 store 中定义“getter”（可以认为是 store 的计算属性）Getter 接受 state 作为其第一个参数

* 通过属性访问 Getter 会暴露为 store.getters 对象，你可以以属性的形式访问这些值
* 通过方法访问 通过让 getter 返回一个函数，来实现给 getter 传参。在你对 store 里的数组进行查询时非常有用。注意，getter 在通过方法访问时，每次都会去进行调用，而不会缓存结果。
* mapGetters 辅助函数  
  mapGetters 辅助函数仅仅是将 store 中的 getter 映射到局部计算属性

  ```js
    import { mapGetters } from 'vuex'

    export default {
    // ...
    computed: {
    // 使用对象展开运算符将 getter 混入 computed 对象中
        ...mapGetters([
        'doneTodosCount',
        'anotherGetter',
        // ...
        ])
    }

  ```

  如果你想将一个 getter 属性另取一个名字，使用对象形式：

  ```js
    ...mapGetters({
    // 把 `this.doneCount` 映射为 `this.$store.getters.doneTodosCount`
    doneCount: 'doneTodosCount'
    })
  ```

## Mutation

  更改 Vuex 的 store 中的状态的唯一方法是提交 mutation。Vuex 中的 mutation 非常类似于事件：每个 mutation 都有一个字符串的事件类型 (type)和一个回调函数 (handler)。这个回调函数就是我们实际进行状态更改的地方，并且它会接受 state 作为第一个参数。你不能直接调用一个 mutation 处理函数。这个选项更像是事件注册：“当触发一个类型为 increment 的 mutation 时，调用此函数。”要唤醒一个 mutation 处理函数，你需要以相应的 type 调用 store.commit 方法

  * Mutation 必须是同步函数  
     一条重要的原则就是要记住 mutation 必须是同步函数
  * 在组件中提交 Mutation  
    可以在组件中使用 this.$store.commit('xxx') 提交 mutation，或者使用 mapMutations 辅助函数将组件中的 methods 映射为 store.commit 调用

    ```js
        import { mapMutations } from 'vuex'

    export default {
    // ...
    methods: {
        ...mapMutations([
        'increment', // 将 `this.increment()` 映射为 `this.$store.commit('increment')`

        // `mapMutations` 也支持载荷：
        'incrementBy' // 将 `this.incrementBy(amount)` 映射为 `this.$store.commit('incrementBy', amount)`
        ]),
        ...mapMutations({
        add: 'increment' // 将 `this.add()` 映射为 `this.$store.commit('increment')`
        })
    }
    }
    ```

## Action

Action 类似于 mutation，不同在于：

1. Action 提交的是 mutation，而不是直接变更状态。  
2. Action 可以包含任意异步操作。

Action 函数接受一个与 store 实例具有相同方法和属性的 context 对象，因此你可以调用 context.commit 提交一个 mutation，或者通过 context.state 和 context.getters 来获取 state 和 getters。

* 分发 Action  
Action 通过 store.dispatch 方法触发：

```js
store.dispatch('increment')
```

乍一眼看上去感觉多此一举，我们直接分发 mutation 岂不更方便？实际上并非如此，还记得 mutation 必须同步执行这个限制么？Action 就不受约束！我们可以在 action 内部执行异步操作：

```js
actions: {
  incrementAsync ({ commit }) {
    setTimeout(() => {
      commit('increment')
    }, 1000)
  }
}
```

* 在组件中分发 Action  
 你在组件中使用 this.$store.dispatch('xxx') 分发 action，或者使用 mapActions 辅助函数将组件的 methods 映射为 store.dispatch 调用（需要先在根节点注入 store）  

 ```js
 import { mapActions } from 'vuex'

export default {
  // ...
  methods: {
    ...mapActions([
      'increment', // 将 `this.increment()` 映射为 `this.$store.dispatch('increment')`

      // `mapActions` 也支持载荷：
      'incrementBy' // 将 `this.incrementBy(amount)` 映射为 `this.$store.dispatch('incrementBy', amount)`
    ]),
    ...mapActions({
      add: 'increment' // 将 `this.add()` 映射为 `this.$store.dispatch('increment')`
    })
  }
}
 ```

* 组合 Action  
  ction 通常是异步的，那么如何知道 action 什么时候结束呢？更重要的是，我们如何才能组合多个 action，以处理更加复杂的异步流程？
  首先，你需要明白 store.dispatch 可以处理被触发的 action 的处理函数返回的 Promise，并且 store.dispatch 仍旧返回 Promise

  ```js
  actions: {
  actionA ({ commit }) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        commit('someMutation')
        resolve()
      }, 1000)
    })
  }
}
  ```

  现在你可以：  

  ```js
    store.dispatch('actionA').then(() => {
    // ...
    })
  ```

  在另外一个 action 中也可以：

  ```js
  actions: {
  // ...
  actionB ({ dispatch, commit }) {
    return dispatch('actionA').then(() => {
      commit('someOtherMutation')
    })
  }
}
  ```

  最后，如果我们利用 async / await，我们可以如下组合 action：

```js
// 假设 getData() 和 getOtherData() 返回的是 Promise

actions: {
  async actionA ({ commit }) {
    commit('gotData', await getData())
  },
  async actionB ({ dispatch, commit }) {
    await dispatch('actionA') // 等待 actionA 完成
    commit('gotOtherData', await getOtherData())
  }
}
```

* Module
  vuex 允许我们将 store 分割成模块（module）。每个模块拥有自己的 state、mutation、action、getter、甚至是嵌套子模块——从上至下进行同样方式的分割  
  1. 模块的局部状态  
  对于模块内部的 mutation 和 getter，接收的第一个参数是模块的局部状态对象
  2. 命名空间
      通过添加 namespaced: true 的方式使其成为带命名空间的模块。当模块被注册后，它的所有 getter、action 及 mutation 都会自动根据模块注册的路径调整命名。例如：

    ```js
    const store = createStore({
    modules: {
        account: {
        namespaced: true,

        // 模块内容（module assets）
        state: () => ({ ... }), // 模块内的状态已经是嵌套的了，使用 `namespaced` 属性不会对其产生影响
        getters: {
            isAdmin () { ... } // -> getters['account/isAdmin']
        },
        actions: {
            login () { ... } // -> dispatch('account/login')
        },
        mutations: {
            login () { ... } // -> commit('account/login')
        },

        // 嵌套模块
        modules: {
            // 继承父模块的命名空间
            myPage: {
            state: () => ({ ... }),
            getters: {
                profile () { ... } // -> getters['account/profile']
            }
            },

            // 进一步嵌套命名空间
            posts: {
            namespaced: true,

            state: () => ({ ... }),
            getters: {
                popular () { ... } // -> getters['account/posts/popular']
            }
            }
        }
        }
    }
    })
    ```

  3. 在带命名空间的模块内访问全局内容  
   rootState 和 rootGetters 会作为第三和第四参数传入 getter，也会通过 context 对象的属性传入 action.需要在全局命名空间内分发 action 或提交 mutation，将 { root: true } 作为第三参数传给 dispatch 或 commit 即可。
  4. 带命名空间的绑定函数
   可以将模块的空间名称字符串作为第一个参数传递给上述函数，这样所有绑定都会自动将该模块作为上下文。于是上面的例子可以简化为：

   ```js
    computed: {
    ...mapState('some/nested/module', {
        a: state => state.a,
        b: state => state.b
    }),
    ...mapGetters('some/nested/module', [
        'someGetter', // -> this.someGetter
        'someOtherGetter', // -> this.someOtherGetter
    ])
    },
    methods: {
    ...mapActions('some/nested/module', [
        'foo', // -> this.foo()
        'bar' // -> this.bar()
    ])
    }
   ```

    还可以通过使用 createNamespacedHelpers 创建基于某个命名空间辅助函数。它返回一个对象，对象里有新的绑定在给定命名空间值上的组件绑定辅助函数：

    ```js
        import { createNamespacedHelpers } from 'vuex'

    const { mapState, mapActions } = createNamespacedHelpers('some/nested/module')

    export default {
    computed: {
        // 在 `some/nested/module` 中查找
        ...mapState({
        a: state => state.a,
        b: state => state.b
        })
    },
    methods: {
        // 在 `some/nested/module` 中查找
        ...mapActions([
        'foo',
        'bar'
        ])
    }
    }
    ```

    5. 模块动态注册
   在 store 创建之后，你可以使用 store.registerModule 方法注册模块：

    ```js
        import { createStore } from 'vuex'

        const store = createStore({ /* 选项 */ })

        // 注册模块 `myModule`
        store.registerModule('myModule', {
        // ...
        })

        // 注册嵌套模块 `nested/myModule`
        store.registerModule(['nested', 'myModule'], {
        // ...
        })
    ```

    模块动态注册功能使得其他 Vue 插件可以通过在 store 中附加新模块的方式来使用 Vuex 管理状态。例如，vuex-router-sync 插件就是通过动态注册模块将 Vue Router 和 Vuex 结合在一起，实现应用的路由状态管理。

    你也可以使用 store.unregisterModule(moduleName) 来动态卸载模块。注意，你不能使用此方法卸载静态模块（即创建 store 时声明的模块）。

    注意，你可以通过 store.hasModule(moduleName) 方法检查该模块是否已经被注册到 store。需要记住的是，嵌套模块应该以数组形式传递给 registerModule 和 hasModule，而不是以路径字符串的形式传递给 module。

    6. 保留 state 可以通过 preserveState 选项将其归档：store.registerModule('a', module, { preserveState: true })。

    当你设置 preserveState: true 时，该模块会被注册，action、mutation 和 getter 会被添加到 store 中，但是 state 不会

    7. 模块重用