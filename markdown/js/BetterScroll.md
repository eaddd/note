# BetterScroll

## 介绍

一款重点解决移动端（已支持 PC）各种滚动场景需求的插件。它的核心是借鉴的 iscroll (opens new window)的实现，它的 API 设计基本兼容 iscroll，在 iscroll 的基础上又扩展了一些 feature 以及做了一些性能优化。BetterScroll 是使用纯 JavaScript 实现的，这意味着它是无依赖的。

简单的初始化代码如下：

```js
import BScroll from '@better-scroll/core'
let wrapper = document.querySelector('.wrapper')
let scroll = new BScroll(wrapper)
```

这里要注意的是，BetterScroll 默认处理容器（wrapper）的第一个子元素（content）的滚动，其它的元素都会被忽略。
版本 2.0.4 的 BetterScroll 可以通过 specifiedIndexAsContent 来指定 wrapper 的某个子元素作为 content

## 使用

* 安装core基础包和具备所有插件功能的完全包

安装core基础包

```sh
npm install @better-scroll/core --save

// or

yarn add @better-scroll/core
```

安装完全包

```js
npm install better-scroll --save

// or

yarn add better-scroll
```


在代码中引入

```js
import BScroll from '@better-scroll/core'
```

```js
import BetterScroll from 'better-scroll'
let bs = new BetterScroll('.wrapper', {})
```

* 基础滚动
如果你只需要一个拥有基础滚动能力的列表，只需要引入 core。

```js
import BScroll from '@better-scroll/core'
let bs = new BScroll('.wrapper', {
  // ...... 详见配置项
})
```

* 增强型滚动  
如果你需要一些额外的 feature。比如 pull-up，你需要引入额外的插件，详情查看插件。

```js
import BScroll from '@better-scroll/core'
import Pullup from '@better-scroll/pull-up'

// 注册插件
BScroll.use(Pullup)

let bs = new BScroll('.wrapper', {
  probeType: 3,
  pullUpLoad: true
})
```

* 全能力的滚动  
如果你觉得一个个引入插件很费事，我们提供了一个拥有全部插件能力的 BetterScroll 包。它的使用方式与 1.0 版本一模一样，但是体积会相对大很多，推荐按需引入。

```js
import BScroll from 'better-scroll'

let bs = new BScroll('.wrapper', {
  // ...
  pullUpLoad: true,
  wheel: true,
  scrollbar: true,
  // and so on
})
```

* BetterScroll 有多种滚动模式。  
  
1. 垂直滚动  
   默认模式 scrollY
2. 水平滚动  
   scrollX
类型：boolean
默认值： false
作用：当设置为 true 的时候，可以开启横向滚动。
备注：当设置 eventPassthrough 为 'horizontal' 的时候，该配置无效
3. freeScroll（水平与垂直同时滚动）  
freeScroll
类型：boolean
默认值：false
作用：在默认情况下，由于人的手指无法做到绝对垂直或者水平的运动，因此在一次手指操作的过程中，都会存在横向以及纵向的偏移量，内部默认会摒弃偏移量较小的一个方向，保留另一个方向的滚动。但是在某些场景我们需要同时计算横向以及纵向的手指偏移距离，而不是只计算偏移量较大的一个方向，这个时候我们只要设置 freeScroll 为 true 即可。
备注：当设置 eventPassthrough 不为空的时候，该配置无效

* 如果 BetterScroll 的 wrapper DOM 的父元素或者祖先元素发生旋转，可以通过 quadrant 选项来修正用户的交互行为。

1. 竖向滚动强制变换成横向滚动 quadrant: 2 
2. 横向滚动强制翻转 quadrant: 3 
