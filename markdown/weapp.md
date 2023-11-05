# 小程序代码构成

## 小程序代码构成

​在上一章中，我们通过开发者工具快速创建了一个 QuickStart 项目。你可以留意到这个项目里边生成了不同类型的文件:  

* .json 后缀的 JSON 配置文件  
* .wxml 后缀的 WXML 模板文件  
* .wxss 后缀的 WXSS 样式文件  
* .js 后缀的 JS 脚本逻辑文件  
  
接下来我们分别看看这4种文件的作用。

### JSON 配置

JSON 是一种数据格式，并不是编程语言，在小程序中，JSON扮演的静态配置的角色。

我们可以看到在项目的根目录有一个 app.json 和 project.config.json，此外在 pages/logs 目录下还有一个 logs.json，我们依次来说明一下它们的用途。

* 小程序配置 app.json  
app.json 是当前小程序的全局配置，包括了小程序的所有页面路径、界面表现、网络超时时间、底部 tab 等。QuickStart 项目里边的 app.json 配置内容:

1. pages字段 —— 用于描述当前小程序所有页面路径，这是为了让微信客户端知道当前你的小程序页面定义在哪个目录。  
2. window字段 —— 定义小程序所有页面的顶部背景颜色，文字颜色定义等

* 工具配置 project.config.json  
通常大家在使用一个工具的时候，都会针对各自喜好做一些个性化配置，例如界面颜色、编译配置等等，当你换了另外一台电脑重新安装工具的时候，你还要重新配置。  
考虑到这点，小程序开发者工具在每个项目的根目录都会生成一个 project.config.json，你在工具上做的任何配置都会写入到这个文件，当你重新安装工具或者换电脑工作时，你只要载入同一个项目的代码包，开发者工具就自动会帮你恢复到当时你开发项目时的个性化配置，其中会包括编辑器的颜色、代码上传时自动压缩等等一系列选项

* 页面配置 page.json  
这里的 page.json 其实用来表示 pages/logs 目录下的 logs.json 这类和小程序页面相关的配置。  
如果你整个小程序的风格是蓝色调，那么你可以在 app.json 里边声明顶部颜色是蓝色即可。实际情况可能不是这样，可能你小程序里边的每个页面都有不一样的色调来区分不同功能模块，因此我们提供了 page.json，让开发者可以独立定义每个页面的一些属性，例如刚刚说的顶部颜色、是否允许下拉刷新等等

### WXML 模板

WXML（WeiXin Markup Language）是框架设计的一套标签语言，结合基础组件、事件系统，可以构建出页面的结构。

1. 数据绑定
2. 列表渲染
3. 条件渲染
4. 模板

### WXSS 样式

WXSS (WeiXin Style Sheets)是一套样式语言，用于描述 WXML 的组件样式。  
WXSS 用来决定 WXML 的组件应该怎么显示。  
为了适应广大的前端开发者，WXSS 具有 CSS 大部分特性。同时为了更适合开发微信小程序，WXSS 对 CSS 进行了扩充以及修改。
与 CSS 相比，WXSS 扩展的特性有：  

1. 尺寸单位  
   rpx（responsive pixel）: 可以根据屏幕宽度进行自适应。规定屏幕宽为750rpx。如在 iPhone6 上，屏幕宽度为375px，共有750个物理像素，则750rpx = 375px = 750物理像素，1rpx = 0.5px = 1物理像素。
2. 样式导入  
   使用@import语句可以导入外联样式表，@import后跟需要导入的外联样式表的相对路径，用;表示语句结束。

### JS 逻辑交互

一个服务仅仅只有界面展示是不够的，还需要和用户做交互：响应用户的点击、获取用户的位置等等。在小程序里边，我们就通过编写 JS 脚本文件来处理用户的操作。

## 小程序宿主环境

我们称微信客户端给小程序所提供的环境为宿主环境。小程序借助宿主环境提供的能力，可以完成许多普通网页无法完成的功能。

上一章中我们把小程序涉及到的文件类型阐述了一遍，我们结合 QuickStart 这个项目来讲一下这些文件是怎么配合工作的。

### 渲染层和逻辑层

首先，我们来简单了解下小程序的运行环境。小程序的运行环境分成渲染层和逻辑层，其中 WXML 模板和 WXSS 样式工作在渲染层，JS 脚本工作在逻辑层。

小程序的渲染层和逻辑层分别由2个线程管理：渲染层的界面使用了WebView 进行渲染；逻辑层采用JsCore线程运行JS脚本。一个小程序存在多个界面，所以渲染层存在多个WebView线程，这两个线程的通信会经由微信客户端（下文中也会采用Native来代指微信客户端）做中转，逻辑层发送网络请求也经由Native转发，小程序的通信模型下图所示。

有关渲染层和逻辑层的详细文档参考 小程序框架 。

### 程序与页面

微信客户端在打开小程序之前，会把整个小程序的代码包下载到本地。

紧接着通过 app.json 的 pages 字段就可以知道你当前小程序的所有页面路径:

```js
{
  "pages":[
    "pages/index/index",
    "pages/logs/logs"
  ]
}
```

这个配置说明在 QuickStart 项目定义了两个页面，分别位于 pages/index/index 和 pages/logs/logs。而写在 pages 字段的第一个页面就是这个小程序的首页（打开小程序看到的第一个页面）。

于是微信客户端就把首页的代码装载进来，通过小程序底层的一些机制，就可以渲染出这个首页。

小程序启动之后，在 app.js 定义的 App 实例的 onLaunch 回调会被执行:

```js
App({
  onLaunch: function () {
    // 小程序启动之后 触发
  }
})
```

整个小程序只有一个 App 实例，是全部页面共享的，更多的事件回调参考文档 注册程序 App 。

接下来我们简单看看小程序的一个页面是怎么写的。

你可以观察到 pages/logs/logs 下其实是包括了4种文件的，微信客户端会先根据 logs.json 配置生成一个界面，顶部的颜色和文字你都可以在这个 json 文件里边定义好。紧接着客户端就会装载这个页面的 WXML 结构和 WXSS 样式。最后客户端会装载 logs.js，你可以看到 logs.js 的大体内容就是:

```js
Page({
  data: { // 参与页面渲染的数据
    logs: []
  },
  onLoad: function () {
    // 页面渲染后 执行
  }
})
```

Page 是一个页面构造器，这个构造器就生成了一个页面。在生成页面的时候，小程序框架会把 data 数据和 index.wxml 一起渲染出最终的结构，于是就得到了你看到的小程序的样子。

在渲染完界面之后，页面实例就会收到一个 onLoad 的回调，你可以在这个回调处理你的逻辑。

有关于 Page 构造器更多详细的文档参考 注册页面 Page 。

### 组件

小程序提供了丰富的基础组件给开发者，开发者可以像搭积木一样，组合各种组件拼合成自己的小程序。

就像 HTML 的 div, p 等标签一样，在小程序里边，你只需要在 WXML 写上对应的组件标签名字就可以把该组件显示在界面上，例如，你需要在界面上显示地图，你只需要这样写即可：

```html
<map></map>
```

使用组件的时候，还可以通过属性传递值给组件，让组件可以以不同的状态去展现，例如，我们希望地图一开始的中心的经纬度是广州，那么你需要声明地图的 longitude（中心经度） 和 latitude（中心纬度）两个属性:

```html
<map longitude="广州经度" latitude="广州纬度"></map>
```

组件的内部行为也会通过事件的形式让开发者可以感知，例如用户点击了地图上的某个标记，你可以在 js 编写 markertap 函数来处理：

```js
<map bindmarkertap="markertap" longitude="广州经度" latitude="广州纬度"></map>
```

当然你也可以通过 style 或者 class 来控制组件的外层样式，以便适应你的界面宽度高度等等。

更多的组件可以参考 小程序的组件。

### API

为了让开发者可以很方便的调起微信提供的能力，例如获取用户信息、微信支付等等，小程序提供了很多 API 给开发者去使用。

要获取用户的地理位置时，只需要：

```js
wx.getLocation({
  type: 'wgs84',
  success: (res) => {
    var latitude = res.latitude // 纬度
    var longitude = res.longitude // 经度
  }
})
```

调用微信扫一扫能力，只需要：

```js
wx.scanCode({
  success: (res) => {
    console.log(res)
  }
})
```

需要注意的是：多数 API 的回调都是异步，你需要处理好代码逻辑的异步问题。

## 框架

小程序开发框架的目标是通过尽可能简单、高效的方式让开发者可以在微信中开发具有原生 APP 体验的服务。

整个小程序框架系统分为两部分：逻辑层（App Service）和 视图层（View）。小程序提供了自己的视图层描述语言 WXML 和 WXSS，以及基于 JavaScript 的逻辑层框架，并在视图层与逻辑层间提供了数据传输和事件系统，让开发者能够专注于数据与逻辑

1. 响应的数据绑定
  框架的核心是一个响应的数据绑定系统，可以让数据与视图非常简单地保持同步。当做数据修改的时候，只需要在逻辑层修改数据，视图层就会做相应的更新。

2. 页面管理  
框架 管理了整个小程序的页面路由，可以做到页面间的无缝切换，并给以页面完整的生命周期。开发者需要做的只是将页面的数据、方法、生命周期函数注册到 框架 中，其他的一切复杂的操作都交由 框架 处理。

3. 基础组件  
框架 提供了一套基础的组件，这些组件自带微信风格的样式以及特殊的逻辑，开发者可以通过组合基础组件，创建出强大的微信小程序 。

4. 丰富的 API  
框架 提供丰富的微信原生 API，可以方便的调起微信提供的能力，如获取用户信息，本地存储，支付功能等。

### 逻辑层 App Service

小程序开发框架的逻辑层使用 JavaScript 引擎为小程序提供开发 JavaScript 代码的运行环境以及微信小程序的特有功能。

逻辑层将数据进行处理后发送给视图层，同时接受视图层的事件反馈。

开发者写的所有代码最终将会打包成一份 JavaScript 文件，并在小程序启动的时候运行，直到小程序销毁。这一行为类似 ServiceWorker，所以逻辑层也称之为 App Service。

在 JavaScript 的基础上，我们增加了一些功能，以方便小程序的开发：

1. 增加 App 和 Page 方法，进行程序注册和页面注册。
2. 增加 getApp 和 getCurrentPages 方法，分别用来获取 App 实例和当前页面栈。
3. 提供丰富的 API，如微信用户数据，扫一扫，支付等微信特有能力。
4. 提供模块化能力，每个页面有独立的作用域。  

**注意**：小程序框架的逻辑层并非运行在浏览器中，因此 JavaScript 在 web 中一些能力都无法使用，如 window，document 等。

#### 注册小程序

每个小程序都需要在 app.js 中调用 App 方法注册小程序实例，绑定生命周期回调函数、错误监听和页面不存在监听函数等

```js
// app.js
App({
  onLaunch (options) {
    // Do something initial when launch.
  },
  onShow (options) {
    // Do something when show.
  },
  onHide () {
    // Do something when hide.
  },
  onError (msg) {
    console.log(msg)
  },
  globalData: 'I am global data'
})
```

整个小程序只有一个 App 实例，是全部页面共享的。开发者可以通过 getApp 方法获取到全局唯一的 App 实例，获取App上的数据或调用开发者注册在 App 上的函数。

```js
// xxx.js
const appInstance = getApp()
console.log(appInstance.globalData) // I am global data
```

#### 注册页面

对于小程序中的每个页面，都需要在页面对应的 js 文件中进行注册，指定页面的初始数据、生命周期回调、事件处理函数等。

* 使用 Page 构造器注册页面  
简单的页面可以使用 Page() 进行构造。

代码示例：

```js
//index.js
Page({
  data: {
    text: "This is page data."
  },
  onLoad: function(options) {
    // 页面创建时执行
  },
  onShow: function() {
    // 页面出现在前台时执行
  },
  onReady: function() {
    // 页面首次渲染完毕时执行
  },
  onHide: function() {
    // 页面从前台变为后台时执行
  },
  onUnload: function() {
    // 页面销毁时执行
  },
  onPullDownRefresh: function() {
    // 触发下拉刷新时执行
  },
  onReachBottom: function() {
    // 页面触底时执行
  },
  onShareAppMessage: function () {
    // 页面被用户分享时执行
  },
  onPageScroll: function() {
    // 页面滚动时执行
  },
  onResize: function() {
    // 页面尺寸变化时执行
  },
  onTabItemTap(item) {
    // tab 点击时执行
    console.log(item.index)
    console.log(item.pagePath)
    console.log(item.text)
  },
  // 事件响应函数
  viewTap: function() {
    this.setData({
      text: 'Set some data for updating view.'
    }, function() {
      // this is setData callback
    })
  },
  // 自由数据
  customData: {
    hi: 'MINA'
  }
})
```

详细的参数含义和使用请参考 Page 参考文档 。

* 在页面中使用 behaviors  
基础库 2.9.2 开始支持，低版本需做兼容处理。  
页面可以引用 behaviors 。 behaviors 可以用来让多个页面有相同的数据字段和方法。

```js
// my-behavior.js
module.exports = Behavior({
  data: {
    sharedText: 'This is a piece of data shared between pages.'
  },
  methods: {
    sharedMethod: function() {
      this.data.sharedText === 'This is a piece of data shared between pages.'
    }
  }
})
// page-a.js
var myBehavior = require('./my-behavior.js')
Page({
  behaviors: [myBehavior],
  onLoad: function() {
    this.data.sharedText === 'This is a piece of data shared between pages.'
  }
})
```

具体用法参见 behaviors 。

* 使用 Component 构造器构造页面  
基础库 1.6.3 开始支持，低版本需做兼容处理。  
Page 构造器适用于简单的页面。但对于复杂的页面， Page 构造器可能并不好用。  
此时，可以使用 Component 构造器来构造页面。 Component 构造器的主要区别是：方法需要放在 methods: { } 里面。  
代码示例：

```js
Component({
  data: {
    text: "This is page data."
  },
  methods: {
    onLoad: function(options) {
      // 页面创建时执行
    },
    onPullDownRefresh: function() {
      // 下拉刷新时执行
    },
    // 事件响应函数
    viewTap: function() {
      // ...
    }
  }
})
```

这种创建方式非常类似于 自定义组件 ，可以像自定义组件一样使用 behaviors 等高级特性。

#### 生命周期

下图说明了页面 Page 实例的生命周期。
![生命周期](./image/page-lifecycle.png "page lifecycle")

#### 页面路由

在小程序中所有页面的路由全部由框架进行管理。

* 页面栈
框架以栈的形式维护了当前的所有页面。 当发生路由切换的时候，页面栈的表现如下：
路由方式 页面栈表现
初始化 新页面入栈
打开新页面 新页面入栈
页面重定向 当前页面出栈，新页面入栈
页面返回 页面不断出栈，直到目标返回页
Tab 切换 页面全部出栈，只留下新的 Tab 页面
重加载 页面全部出栈，只留下新的页面
开发者可以使用 getCurrentPages() 函数获取当前页面栈。

路由方式
对于路由的触发方式以及页面生命周期函数如下：

| 路由方式 | 触发时机 | 路由前页面 | 路由后页面 |
|----------|:-------------:|-------|-------|
| 初始化 | 小程序打开的第一个页面 | | onLoad, onShow
| 打开新页面 | 调用 API wx.navigateTo  使用组件 \<navigator open-type="navigateTo"/\> | onHide | onLoad, onShow |
| 页面重定向 | 调用 API wx.redirectTo | 使用组件 \<navigator open-type="redirectTo"/\> |  onUnload | onLoad, onShow
| 页面返回 | 调用 API wx.navigateBack 使用组件\<navigator open-type="navigateBack"\> 用户按左上角返回按钮 |  onUnload | onShow
| Tab 切换 | 调用 API wx.switchTab 使用组件 \<navigator open-type="switchTab"/\> 用户切换 Tab  | | 各种情况请参考下表
| 重启动 |调用 API wx.reLaunch 使用组件 \<navigator open-type="reLaunch"/\> | onUnload | onLoad, onShow |

Tab 切换对应的生命周期（以 A、B 页面为 Tabbar 页面，C 是从 A 页面打开的页面，D 页面是从 C 页面打开的页面为例）：

| 当前页面 | 路由后页面 | 触发的生命周期（按顺序）
|----------|-----------|------------|
| A | A | Nothing happend
| A | B | A.onHide(), B.onLoad(), B.onShow()
| A | B | （再次打开） A.onHide(), B.onShow()
| C | A | C.onUnload(), A.onShow()
| C | B | C.onUnload(), B.onLoad(), B.onShow()
| D | B | D.onUnload(), C.onUnload(), B.onLoad(), B.onShow()
| D（从转发进入）| A| D.onUnload(), A.onLoad(), A.onShow()
| D（从转发进入）| B| D.onUnload(), B.onLoad(), B.onShow()

注意事项
navigateTo, redirectTo 只能打开非 tabBar 页面。
switchTab 只能打开 tabBar 页面。
reLaunch 可以打开任意页面。
页面底部的 tabBar 由页面决定，即只要是定义为 tabBar 的页面，底部都有 tabBar。
调用页面路由带的参数可以在目标页面的onLoad中获取。

#### 模块化

可以将一些公共的代码抽离成为一个单独的 js 文件，作为一个模块。模块只有通过 module.exports 或者 exports 才能对外暴露接口。  
**注意**：

* exports 是 module.exports 的一个引用，因此在模块里边随意更改 exports 的指向会造成未知的错误。所以更推荐开发者采用 module.exports 来暴露模块接口，除非你已经清晰知道这两者的关系。
* 小程序目前不支持直接引入 node_modules , 开发者需要使用到 node_modules 时候建议拷贝出相关的代码到小程序的目录中，或者使用小程序支持的 npm 功能。

```js
// common.js
function sayHello(name) {
  console.log(`Hello ${name} !`)
}
function sayGoodbye(name) {
  console.log(`Goodbye ${name} !`)
}

module.exports.sayHello = sayHello
exports.sayGoodbye = sayGoodbye
```

​在需要使用这些模块的文件中，使用 require 将公共代码引入

```js
var common = require('common.js')
Page({
  helloMINA: function() {
    common.sayHello('MINA')
  },
  goodbyeMINA: function() {
    common.sayGoodbye('MINA')
  }
})
```

#### 文件作用域  

在 JavaScript 文件中声明的变量和函数只在该文件中有效；不同的文件中可以声明相同名字的变量和函数，不会互相影响。

通过全局函数 getApp 可以获取全局的应用实例，如果需要全局的数据可以在 App() 中设置，如：

```js
// app.js
App({
  globalData: 1
})
// a.js
// The localValue can only be used in file a.js.
var localValue = 'a'
// Get the app instance.
var app = getApp()
// Get the global data and change it.
app.globalData++
// b.js
// You can redefine localValue in file b.js, without interference with the localValue in a.js.
var localValue = 'b'
// If a.js it run before b.js, now the globalData shoule be 2.
console.log(getApp().globalData)
```

#### API  

小程序开发框架提供丰富的微信原生 API，可以方便的调起微信提供的能力，如获取用户信息，本地存储，支付功能等。详细介绍请参考 API 文档。

通常，在小程序 API 有以下几种类型：

事件监听 API  
我们约定，以 on 开头的 API 用来监听某个事件是否触发，如：wx.onSocketOpen，wx.onCompassChange 等。

这类 API 接受一个回调函数作为参数，当事件触发时会调用这个回调函数，并将相关数据以参数形式传入。

代码示例

```js
wx.onCompassChange(function (res) {
  console.log(res.direction)
})
```

同步 API  
我们约定，以 Sync 结尾的 API 都是同步 API， 如 wx.setStorageSync，wx.getSystemInfoSync 等。此外，也有一些其他的同步 API，如 wx.createWorker，wx.getBackgroundAudioManager 等，详情参见 API 文档中的说明。

同步 API 的执行结果可以通过函数返回值直接获取，如果执行出错会抛出异常。

代码示例

```js
try {
  wx.setStorageSync('key', 'value')
} catch (e) {
  console.error(e)
}
```

异步 API  
大多数 API 都是异步 API，如 wx.request，wx.login 等。这类 API 接口通常都接受一个 Object 类型的参数，这个参数都支持按需指定以下字段来接收接口调用结果：

Object 参数说明

| 参数名 | 类型  | 必填 | 说明 |
|--------|-------|-------|-----|
| success | function | 否 | 接口调用成功的回调函数
| fail | function | 否 | 接口调用失败的回调函数
| complete | function | 否 | 接口调用结束的回调函数（调用成功、失败都会执行）
| 其他 | Any | - | 接口定义的其他参数

回调函数的参数  
success，fail，complete 函数调用时会传入一个 Object 类型参数，包含以下字段：

|属性 | 类型 | 说明 |
|-----|-------|-----|
|errMsg | string | 错误信息，如果调用成功返回 ${apiName}:ok
|errCode | number | 错误码，仅部分 API 支持，具体含义请参考对应 API 文档，成功时为 0。
|其他 | Any | 接口返回的其他数据

异步 API 的执行结果需要通过 Object 类型的参数中传入的对应回调函数获取。部分异步 API 也会有返回值，可以用来实现更丰富的功能，如 wx.request，wx.connectSocket 等。

代码示例

```js
wx.login({
  success(res) {
    console.log(res.code)
  }
})
```

异步 API 返回 Promise  
基础库 2.10.2 版本起，异步 API 支持 callback & promise 两种调用方式。当接口参数 Object 对象中不包含 success/fail/complete 时将默认返回 promise，否则仍按回调方式执行，无返回值。

注意事项
部分接口如 downloadFile, request, uploadFile, connectSocket, createCamera（小游戏）本身就有返回值， 它们的 promisify 需要开发者自行封装。
当没有回调参数时，异步接口返回 promise。此时若函数调用失败进入 fail 逻辑， 会报错提示 Uncaught (in promise)，开发者可通过 catch 来进行捕获。
wx.onUnhandledRejection 可以监听未处理的 Promise 拒绝事件。
代码示例

```js
// callback 形式调用
wx.chooseImage({
  success(res) {
    console.log('res:', res)
  }
})

// promise 形式调用
wx.chooseImage().then(res => console.log('res: ', res))
```

云开发 API  
开通并使用微信云开发，即可使用云开发API，在小程序端直接调用服务端的云函数。

代码示例

```js
wx.cloud.callFunction({
  // 云函数名称
  name: 'cloudFunc',
  // 传给云函数的参数
  data: {
    a: 1,
    b: 2,
  },
  success: function(res) {
    console.log(res.result) // 示例
  },
  fail: console.error
})
// 此外，云函数同样支持promise形式调用
```

### 视图层 View

框架的视图层由 WXML 与 WXSS 编写，由组件来进行展示。  
将逻辑层的数据反映成视图，同时将视图层的事件发送给逻辑层。  
WXML(WeiXin Markup language) 用于描述页面的结构。  
WXS(WeiXin Script) 是小程序的一套脚本语言，结合 WXML，可以构建出页面的结构。  
WXSS(WeiXin Style Sheet) 用于描述页面的样式。  
组件(Component)是视图的基本组成单元。

#### WXS

WXS（WeiXin Script）是小程序的一套脚本语言，结合 WXML，可以构建出页面的结构。

**注意事项**  

WXS 不依赖于运行时的基础库版本，可以在所有版本的小程序中运行。  
WXS 与 JavaScript 是不同的语言，有自己的语法，并不和 JavaScript 一致。  
WXS 的运行环境和其他 JavaScript 代码是隔离的，WXS 中不能调用其他 JavaScript 文件中定义的函数，也不能调用小程序提供的API。  
由于运行环境的差异，在 iOS 设备上小程序内的 WXS 会比 JavaScript 代码快 2 ~ 20 倍。在 android 设备上二者运行效率无差异。  

以下是一些使用 WXS 的简单示例，要完整了解 WXS 语法，请参考WXS 语法参考。

页面渲染

```js
<!--wxml-->
<wxs module="m1">
var msg = "hello world";

module.exports.message = msg;
</wxs>

<view> {{m1.message}} </view>
```

页面输出：

```text
hello world
```

数据处理

```js
// page.js
Page({
  data: {
    array: [1, 2, 3, 4, 5, 1, 2, 3, 4]
  }
})
<!--wxml-->
<!-- 下面的 getMax 函数，接受一个数组，且返回数组中最大的元素的值 -->
<wxs module="m1">
var getMax = function(array) {
  var max = undefined;
  for (var i = 0; i < array.length; ++i) {
    max = max === undefined ?
      array[i] :
      (max >= array[i] ? max : array[i]);
  }
  return max;
}

module.exports.getMax = getMax;
</wxs>

<!-- 调用 wxs 里面的 getMax 函数，参数为 page.js 里面的 array -->
<view> {{m1.getMax(array)}} </view>
```

页面输出：

```text
5
```

#### 事件

1. 什么是事件  
事件是视图层到逻辑层的通讯方式。  
事件可以将用户的行为反馈到逻辑层进行处理。  
事件可以绑定在组件上，当达到触发事件，就会执行逻辑层中对应的事件处理函数。  
事件对象可以携带额外信息，如 id, dataset, touches。

2. 事件的使用方式

* 在组件中绑定一个事件处理函数。
  如bindtap，当用户点击该组件的时候会在该页面对应的Page中找到相应的事件处理函数。
* 在相应的page定义中写上相应的事件处理函数，参数是event
* log出来的信息大致如下:
  
```js
{
  "type":"tap",
  "timeStamp":895,
  "target": {
    "id": "tapTest",
    "dataset":  {
      "hi":"Weixin"
    }
  },
  "currentTarget":  {
    "id": "tapTest",
    "dataset": {
      "hi":"Weixin"
    }
  },
  "detail": {
    "x":53,
    "y":14
  },
  "touches":[{
    "identifier":0,
    "pageX":53,
    "pageY":14,
    "clientX":53,
    "clientY":14
  }],
  "changedTouches":[{
    "identifier":0,
    "pageX":53,
    "pageY":14,
    "clientX":53,
    "clientY":14
  }]
}
```

#### 使用WXS函数响应事件

#### 事件详解

1. 事件分类  
事件分为冒泡事件和非冒泡事件：  
冒泡事件：当一个组件上的事件被触发后，该事件会向父节点传递。  
非冒泡事件：当一个组件上的事件被触发后，该事件不会向父节点传递。

2. 普通事件绑定  
  事件绑定的写法类似于组件的属性，如：

    ```js
    <view bindtap="handleTap">
        Click here!
    </view>
    ```

    事件绑定函数可以是一个数据绑定，如：

    ```js
    <view bindtap="{{ handlerName }}">
        Click here!
    </view>
    ```

    此时，页面的 this.data.handlerName 必须是一个字符串，指定事件处理函数名；如果它是个空字符串，则这个绑定会失效（可以利用这个特性来暂时禁用一些事件）。

    自基础库版本 1.5.0 起，在大多数组件和自定义组件中， bind 后可以紧跟一个冒号，其含义不变，如 bind:tap 。基础库版本 2.8.1 起，在所有组件中开始提供这个支持。

3. 绑定并阻止事件冒泡  
除 bind 外，也可以用 catch 来绑定事件。与 bind 不同， catch 会阻止事件向上冒泡。  
例如在下边这个例子中，点击 inner view 会先后调用handleTap3和handleTap2(因为tap事件会冒泡到 middle view，而 middle view 阻止了 tap 事件冒泡，不再向父节点传递)，点击 middle view 会触发handleTap2，点击 outer view 会触发handleTap1。

    ```js
    <view id="outer" bindtap="handleTap1">
      outer view
      <view id="middle" catchtap="handleTap2">
        middle view
        <view id="inner" bindtap="handleTap3">
          inner view
        </view>
      </view>
    </view>
    ```

4. 互斥事件绑定
自基础库版本 2.8.2 起，除 bind 和 catch 外，还可以使用 mut-bind 来绑定事件。一个 mut-bind 触发后，如果事件冒泡到其他节点上，其他节点上的 mut-bind 绑定函数不会被触发，但 bind 绑定函数和 catch 绑定函数依旧会被触发。  
换而言之，所有 mut-bind 是“互斥”的，只会有其中一个绑定函数被触发。同时，它完全不影响 bind 和 catch 的绑定效果。  
例如在下边这个例子中，点击 inner view 会先后调用 handleTap3 和 handleTap2 ，点击 middle view 会调用 handleTap2 和 handleTap1 。

    ```js
    <view id="outer" mut-bind:tap="handleTap1">
      outer view
      <view id="middle" bindtap="handleTap2">
        middle view
        <view id="inner" mut-bind:tap="handleTap3">
          inner view
        </view>
      </view>
    </view>
    ```

5. 事件的捕获阶段  
自基础库版本 1.5.0 起，触摸类事件支持捕获阶段。捕获阶段位于冒泡阶段之前，且在捕获阶段中，事件到达节点的顺序与冒泡阶段恰好相反。需要在捕获阶段监听事件时，可以采用capture-bind、capture-catch关键字，后者将中断捕获阶段和取消冒泡阶段。  
在下面的代码中，点击 inner view 会先后调用handleTap2、handleTap4、handleTap3、handleTap1。

    ```js
    <view id="outer" bind:touchstart="handleTap1" capture-bind:touchstart="handleTap2">
      outer view
      <view id="inner" bind:touchstart="handleTap3" capture-bind:touchstart="handleTap4">
        inner view
      </view>
    </view>
    ```

    如果将上面代码中的第一个capture-bind改为capture-catch，将只触发handleTap2。

    ```js
    <view id="outer" bind:touchstart="handleTap1" capture-catch:touchstart="handleTap2">
      outer view
      <view id="inner" bind:touchstart="handleTap3" capture-bind:touchstart="handleTap4">
        inner view
      </view>
    </view>
    ```

6. 事件对象  
如无特殊说明，当组件触发事件时，逻辑层绑定该事件的处理函数会收到一个事件对象。  
BaseEvent 基础事件对象属性列表：  

    | 属性 | 类型 | 说明 | 基础库版本 |
    |-------|-------|------|----------|
    | type | String | 事件类型 | |
    | timeStamp | Integer | 事件生成时的时间戳 | |
    | target | Object | 触发事件的组件的一些属性值集合 | |
    | currentTarget | Object | 当前组件的一些属性值集合 | |
    | mark | Object | 事件标记数据 | 2.7.1 |

CustomEvent 自定义事件对象属性列表（继承 BaseEvent）：

| 属性 | 类型 | 说明
|-------|------|-----|
| detail | Object | 额外的信息

 TouchEvent  触摸事件对象属性列表（继承 BaseEvent）：

| 属性 | 类型 | 说明
|-------|------|-----
| touches | Array | 触摸事件，当前停留在屏幕中的触摸点信息的数组
| changedTouches | Array | 触摸事件，当前变化的触摸点信息的数组

type  
代表事件的类型。

timeStamp  
页面打开到触发事件所经过的毫秒数。

target  
触发事件的源组件。

|属性 | 类型 | 说明
|----|-------|-----
id | String | 事件源组件的id
dataset|  Object | 事件源组件上由data-开头的自定义属性组成的集合

currentTarget  
事件绑定的当前组件。

| 属性 | 类型 | 说明
|-------|------|------
| id | String | 当前组件的id
| dataset | Object | 当前组件上由data-开头的自定义属性组成的集合

**说明： target 和 currentTarget 可以参考上例中，点击 inner view 时，handleTap3 收到的事件对象 target 和 currentTarget 都是 inner，而 handleTap2 收到的事件对象 target 就是 inner，currentTarget 就是 middle。**

dataset  
在组件节点中可以附加一些自定义数据。这样，在事件中可以获取这些自定义的节点数据，用于事件的逻辑处理。

在 WXML 中，这些自定义数据以 data- 开头，多个单词由连字符 - 连接。这种写法中，连字符写法会转换成驼峰写法，而大写字符会自动转成小写字符。如：  
data-element-type ，最终会呈现为 event.currentTarget.dataset.elementType ；
data-elementType ，最终会呈现为 event.currentTarget.dataset.elementtype 。
示例：

```js
<view data-alpha-beta="1" data-alphaBeta="2" bindtap="bindViewTap"> DataSet Test </view>
Page({
  bindViewTap:function(event){
    event.currentTarget.dataset.alphaBeta === 1 // - 会转为驼峰写法
    event.currentTarget.dataset.alphabeta === 2 // 大写会转为小写
  }
})
```

mark  
在基础库版本 2.7.1 以上，可以使用 mark 来识别具体触发事件的 target 节点。此外， mark 还可以用于承载一些自定义数据（类似于 dataset ）。

当事件触发时，事件冒泡路径上所有的 mark 会被合并，并返回给事件回调函数。（即使事件不是冒泡事件，也会 mark 。）

代码示例：

在开发者工具中预览效果

```js
<view mark:myMark="last" bindtap="bindViewTap">
  <button mark:anotherMark="leaf" bindtap="bindButtonTap">按钮</button>
</view>
```

在上述 WXML 中，如果按钮被点击，将触发 bindViewTap 和 bindButtonTap 两个事件，事件携带的 event.mark 将包含 myMark 和 anotherMark 两项。

```js
Page({
  bindViewTap: function(e) {
    e.mark.myMark === "last" // true
    e.mark.anotherMark === "leaf" // true
  }
})
```

mark 和 dataset 很相似，主要区别在于： mark 会包含从触发事件的节点到根节点上所有的 mark: 属性值；而 dataset 仅包含一个节点的 data- 属性值。

**细节注意事项：  
如果存在同名的 mark ，父节点的 mark 会被子节点覆盖。
在自定义组件中接收事件时， mark 不包含自定义组件外的节点的 mark 。
不同于 dataset ，节点的 mark 不会做连字符和大小写转换。**  

touches  
touches 是一个数组，每个元素为一个 Touch 对象（canvas 触摸事件中携带的 touches 是 CanvasTouch 数组）。 表示当前停留在屏幕上的触摸点。

Touch 对象
| 属性 | 类型 | 说明
|------|-------|-----
| identifier | Number | 触摸点的标识符
| pageX, pageY | Number | 距离文档左上角的距离，文档的左上角为原点 ，横向为X轴，纵向为Y轴
| clientX, clientY | Number | 距离页面可显示区域（屏幕除去导航条）左上角距离，横向为X轴，纵向为Y轴

CanvasTouch 对象
| 属性 | 类型 | 说明 | 特殊说明
|-------|------|-------|--------
| identifier | Number | 触摸点的标识符
| x, y | Number | 距离 Canvas 左上角的距离，Canvas 的左上角为原点 ，横向为X轴，纵向为Y轴

changedTouches  
changedTouches 数据格式同 touches。 表示有变化的触摸点，如从无变有（touchstart），位置变化（touchmove），从有变无（touchend、touchcancel）。

detail  
自定义事件所携带的数据，如表单组件的提交事件会携带用户的输入，媒体的错误事件会携带错误信息，详见组件定义中各个事件的定义。

点击事件的detail 带有的 x, y 同 pageX, pageY 代表距离文档左上角的距离。

#### 简易双向绑定

1. 双向绑定语法  
    在 WXML 中，普通的属性的绑定是单向的。例如：

    ```js
    <input value="{{value}}" />
    ```

    如果使用 this.setData({ value: 'leaf' }) 来更新 value ，this.data.value 和输入框的中显示的值都会被更新为 leaf ；但如果用户修改了输入框里的值，却不会同时改变 this.data.value 。

    如果需要在用户输入的同时改变 this.data.value ，需要借助简易双向绑定机制。此时，可以在对应项目之前加入 model: 前缀：

    ```js
    <input model:value="{{value}}" />
    ```

    这样，如果输入框的值被改变了， this.data.value 也会同时改变。同时， WXML 中所有绑定了 value 的位置也会被一同更新， 数据监听器 也会被正常触发。

    在开发者工具中预览效果

    用于双向绑定的表达式有如下限制：

    只能是一个单一字段的绑定，如

    ```js
    <input model:value="值为 {{value}}" />
    <input model:value="{{ a + b }}" />
    ```

    都是非法的；

    目前，尚不能 data 路径，如

    ```js
    <input model:value="{{ a.b }}" />
    ```

    这样的表达式目前暂不支持。

2. 在自定义组件中传递双向绑定  
    双向绑定同样可以使用在自定义组件上。如下的自定义组件：

    ```js
    // custom-component.js
    Component({
      properties: {
        myValue: String
      }
    })
    <!-- custom-component.wxml -->
    <input model:value="{{myValue}}" />
    ```

    这个自定义组件将自身的 myValue 属性双向绑定到了组件内输入框的 value 属性上。这样，如果页面这样使用这个组件：

    ```js
    <custom-component model:my-value="{{pageValue}}" />
    ```

    当输入框的值变更时，自定义组件的 myValue 属性会同时变更，这样，页面的 this.data.pageValue 也会同时变更，页面 WXML 中所有绑定了 pageValue 的位置也会被一同更新
3. 在自定义组件中触发双向绑定更新
   自定义组件还可以自己触发双向绑定更新，做法就是：使用 setData 设置自身的属性。例如：

    ```js
    // custom-component.js
    Component({
      properties: {
        myValue: String
      },
      methods: {
        update: function() {
          // 更新 myValue
          this.setData({
            myValue: 'leaf'
          })
        }
      }
    })
    ```

    如果页面这样使用这个组件：

    ```js
    <custom-component model:my-value="{{pageValue}}" />
    ```

    当组件使用 setData 更新 myValue 时，页面的 this.data.pageValue 也会同时变更，页面 WXML 中所有绑定了 pageValue 的位置也会被一同更新。

#### 获取界面上的节点信息

1. WXML节点信息
    节点信息查询 API 可以用于获取节点属性、样式、在界面上的位置等信息。

    最常见的用法是使用这个接口来查询某个节点的当前位置，以及界面的滚动位置。

    示例代码：

    ```js
    const query = wx.createSelectorQuery()
    query.select('#the-id').boundingClientRect(function(res){
      res.top // #the-id 节点的上边界坐标（相对于显示区域）
    })
    query.selectViewport().scrollOffset(function(res){
      res.scrollTop // 显示区域的竖直滚动位置
    })
    query.exec()
    ```

    上述示例中， #the-id 是一个节点选择器，与 CSS 的选择器相近但略有区别，请参见 SelectorQuery.select 的相关说明。  

    在自定义组件或包含自定义组件的页面中，推荐使用 this.createSelectorQuery 来代替 wx.createSelectorQuery ，这样可以确保在正确的范围内选择节点。
2. WXML节点布局相交状态
   可用于监听两个或多个组件节点在布局位置上的相交状态。这一组API常常可以用于推断某些节点是否可以被用户看见、有多大比例可以被用户看见。

    这一组API涉及的主要概念如下。

    参照节点：监听的参照节点，取它的布局区域作为参照区域。如果有多个参照节点，则会取它们布局区域的 交集 作为参照区域。页面显示区域也可作为参照区域之一。
    目标节点：监听的目标，默认只能是一个节点（使用 selectAll 选项时，可以同时监听多个节点）。
    相交区域：目标节点的布局区域与参照区域的相交区域。
    相交比例：相交区域占参照区域的比例。
    阈值：相交比例如果达到阈值，则会触发监听器的回调函数。阈值可以有多个。
    以下示例代码可以在目标节点（用选择器 .target-class 指定）每次进入或离开页面显示区域时，触发回调函数。

    示例代码：

    ```js
    Page({
      onLoad: function(){
        wx.createIntersectionObserver().relativeToViewport().observe('.target-class', (res) => {
          res.id // 目标节点 id
          res.dataset // 目标节点 dataset
          res.intersectionRatio // 相交区域占目标节点的布局区域的比例
          res.intersectionRect // 相交区域
          res.intersectionRect.left // 相交区域的左边界坐标
          res.intersectionRect.top // 相交区域的上边界坐标
          res.intersectionRect.width // 相交区域的宽度
          res.intersectionRect.height // 相交区域的高度
        })
      }
    })
    ```

    以下示例代码可以在目标节点（用选择器 .target-class 指定）与参照节点（用选择器 .relative-class 指定）在页面显示区域内相交或相离，且相交或相离程度达到目标节点布局区域的20%和50%时，触发回调函数。

    示例代码：

    ```js
    Page({
      onLoad: function(){
        wx.createIntersectionObserver(this, {
          thresholds: [0.2, 0.5]
        }).relativeTo('.relative-class').relativeToViewport().observe('.target-class', (res) => {
          res.intersectionRatio // 相交区域占目标节点的布局区域的比例
          res.intersectionRect // 相交区域
          res.intersectionRect.left // 相交区域的左边界坐标
          res.intersectionRect.top // 相交区域的上边界坐标
          res.intersectionRect.width // 相交区域的宽度
          res.intersectionRect.height // 相交区域的高度
        })
      }
    })
    ```

    注意：与页面显示区域的相交区域并不准确代表用户可见的区域，因为参与计算的区域是“布局区域”，布局区域可能会在绘制时被其他节点裁剪隐藏（如遇祖先节点中 overflow 样式为 hidden 的节点）或遮盖（如遇 fixed 定位的节点）。

    在自定义组件或包含自定义组件的页面中，推荐使用 this.createIntersectionObserver 来代替 wx.createIntersectionObserver ，这样可以确保在正确的范围内选择节点。

#### 分栏模式

在 PC 等能够以较大屏幕显示小程序的环境下，小程序支持以分栏模式展示。分栏模式可以将微信窗口分为左右两半，各展示一个页面

目前， Windows 微信 3.3 以上版本支持分栏模式。对于其他版本微信，分栏模式不会生效。

启用分栏模式
在 app.json 中同时添加 "resizable": true 和 "frameset": true 两个配置项就可以启用分栏模式。

代码示例：

```js
{
  "resizable": true,
  "frameset": true
}
```

启用分栏模式后，可以使用开发者工具的自动预览功能来预览分栏效果。

分栏占位图片
当某一栏没有展示任何页面时，会展示一张图片在此栏正中央。

如果代码包中的 frameset/placeholder.png 文件存在，这张图片将作为此时展示的图片。

分栏适配要点
启用分栏模式后，一些已有代码逻辑可能出现问题。可能需要更改代码来使其能够在分栏模式下正确运行。

避免使用更改页面展示效果的接口
更改当前页面展示效果的接口，总是对最新打开的页面生效。

例如，在右栏打开一个新页面后，更改页面标题的接口 wx.setNavigationBarTitle 即使是在左栏的页面中调用，也将更改右栏内页面的标题！

因此，应当尽量避免使用这样的接口，而是改用 page-meta 和 navigation-bar 组件代替。

变更路由接口调用
如果在路由接口中使用相对路径，总是相对于最新打开的页面路径。

例如，在右栏打开一个新页面后，路由接口 wx.navigateTo 即使是在左栏的页面中调用，跳转路径也将相对于右栏内页面的路径！

因此，应当将这样的路由接口改成 Router 接口调用，如 this.pageRouter.navigateTo 。

页面大小不是固定值
启用分栏模式的同时，页面大小也是可能动态变化的了。请使用 响应显示区域变化 的方法来处理页面大小变化时的响应方式。

#### 动画

在小程序中，通常可以使用 CSS 渐变 和 CSS 动画 来创建简易的界面动画。

在开发者工具中预览效果

动画过程中，可以使用 bindtransitionend bindanimationstart bindanimationiteration bindanimationend 来监听动画事件。

**注意：这几个事件都不是冒泡事件，需要绑定在真正发生了动画的节点上才会生效。**

同时，还可以使用 wx.createAnimation 接口来动态创建简易的动画效果。（新版小程序基础库中推荐使用下述的关键帧动画接口代替。

1. 关键帧动画
    基础库 2.9.0 开始支持，低版本需做兼容处理。

    从小程序基础库 2.9.0 开始支持一种更友好的动画创建方式，用于代替旧的 wx.createAnimation 。它具有更好的性能和更可控的接口。

    在页面或自定义组件中，当需要进行关键帧动画时，可以使用 this.animate 接口：

    ```js
    this.animate(selector, keyframes, duration, callback)
    ```

    调用 animate API 后会在节点上新增一些样式属性覆盖掉原有的对应样式。如果需要清除这些样式，可在该节点上的动画全部执行完毕后使用 this.clearAnimation 清除这些属性。

    ```js
    this.clearAnimation(selector, options, callback)
    ```

2. 滚动驱动的动画
   我们发现，根据滚动位置而不断改变动画的进度是一种比较常见的场景，这类动画可以让人感觉到界面交互很连贯自然，体验更好。因此，从小程序基础库 2.9.0 开始支持一种由滚动驱动的动画机制。

    基于上述的关键帧动画接口，新增一个 ScrollTimeline 的参数，用来绑定滚动元素（目前只支持 scroll-view）。接口定义如下：

    ```js
    this.animate(selector, keyframes, duration, ScrollTimeline)
    ```

#### 初始渲染缓存

1. 初始渲染缓存工作原理  
小程序页面的初始化分为两个部分。  
逻辑层初始化：载入必需的小程序代码、初始化页面 this 对象（也包括它涉及到的所有自定义组件的 this 对象）、将相关数据发送给视图层。  
视图层初始化：载入必需的小程序代码，然后等待逻辑层初始化完毕并接收逻辑层发送的数据，最后渲染页面。  
在启动页面时，尤其是小程序冷启动、进入第一个页面时，逻辑层初始化的时间较长。在页面初始化过程中，用户将看到小程序的标准载入画面（冷启动时）或可能看到轻微的白屏现象（页面跳转过程中）。  
启用初始渲染缓存，可以使视图层不需要等待逻辑层初始化完毕，而直接提前将页面初始 data 的渲染结果展示给用户，这可以使得页面对用户可见的时间大大提前。它的工作原理如下：  
在小程序页面第一次被打开后，将页面初始数据渲染结果记录下来，写入一个持久化的缓存区域（缓存可长时间保留，但可能因为小程序更新、基础库更新、储存空间回收等原因被清除）；  
在这个页面被第二次打开时，检查缓存中是否还存有这个页面上一次初始数据的渲染结果，如果有，就直接将渲染结果展示出来；  
如果展示了缓存中的渲染结果，这个页面暂时还不能响应用户事件，等到逻辑层初始化完毕后才能响应用户事件。  
利用初始渲染缓存，可以：  
快速展示出页面中永远不会变的部分，如导航栏；  
预先展示一个骨架页，提升用户体验；  
展示自定义的加载提示；  
提前展示广告，等等。

2. 支持的组件
    在初始渲染缓存阶段中，复杂组件不能被展示或不能响应交互。

    目前支持的内置组件：

    ```html
    <view />
    <text />
    <button />
    <image />
    <scroll-view />
    <rich-text />
    ```

    自定义组件本身可以被展示（但它们里面用到的内置组件也遵循上述限制）。

3. 静态初始渲染缓存  
    若想启用初始渲染缓存，最简单的方法是在页面的 json 文件中添加配置项 "initialRenderingCache": "static" ：

    ```js
    {
      "initialRenderingCache": "static"
    }
    ```

    如果想要对所有页面启用，可以在 app.json 的 window 配置段中添加这个配置：

    ```js
    {
      "window": {
        "initialRenderingCache": "static"
      }
    }
    ```

    添加这个配置项之后，在手机中预览小程序首页，然后杀死小程序再次进入，就会通过初始渲染缓存来渲染首页。

    注意：这种情况下，初始渲染缓存记录的是页面 data 应用在页面 WXML 上的结果，不包含任何 setData 的结果。

    例如，如果想要在页面中展示出“正在加载”几个字，这几个字受到 loading 数据字段控制：

    ```js
    <view wx:if="{{loading}}">正在加载</view>
    ```

    这种情况下， loading 应当在 data 中指定为 true ，如：

    ```js
    // 正确的做法
    Page({
      data: {
        loading: true
      }
    })
    ```

    而不能通过 setData 将 loading 置为 true ：

    // 错误的做法！不要这么做！
    Page({
      data: {},
      onLoad: function() {
        this.setData({
          loading: true
        })
      }
    })
    换而言之，这种做法只包含页面 data 的渲染结果，即页面的纯静态成分。

    在初始渲染缓存中添加动态内容
    有些场景中，只是页面 data 的渲染结果会比较局限。有时会想要额外展示一些可变的内容，如展示的广告图片 URL 等。

    这种情况下可以使用“动态”初始渲染缓存的方式。首先，配置 "initialRenderingCache": "dynamic" ：

    ```js
    {
      "initialRenderingCache": "dynamic"
    }
    ```

    此时，初始渲染缓存不会被自动启用，还需要在页面中调用 this.setInitialRenderingCache(dynamicData) 才能启用。其中， dynamicData 是一组数据，与 data 一起参与页面 WXML 渲染。

    ```js
    Page({
      data: {
        loading: true
      },
      onReady: function() {
        this.setInitialRenderingCache({
          loadingHint: '正在加载' // 这一部分数据将被应用于界面上，相当于在初始 data 基础上额外进行一次 setData
        })
      }
    })
    <view wx:if="{{loading}}">{{loadingHint}}</view>
    ```

    从原理上说，在动态生成初始渲染缓存的方式下，页面会在后台使用动态数据重新渲染一次，因而开销相对较大。因而要尽量避免频繁调用 this.setInitialRenderingCache ，如果在一个页面内多次调用，仅最后一次调用生效。

    **注意：
    this.setInitialRenderingCache 调用时机不能早于 Page 的 onReady 或 Component 的 ready 生命周期，否则可能对性能有负面影响。
    如果想禁用初始渲染缓存，调用 this.setInitialRenderingCache(null) 。**

## 自定义组件

开发者可以将页面内的功能模块抽象成自定义组件，以便在不同的页面中重复使用；也可以将复杂的页面拆分成多个低耦合的模块，有助于代码维护。自定义组件在使用时与基础组件非常相似

1. 创建自定义组件

    类似于页面，一个自定义组件由 json wxml wxss js 4个文件组成。要编写一个自定义组件，首先需要在 json 文件中进行自定义组件声明（将 component 字段设为 true 可将这一组文件设为自定义组件）：

    ```js
    {
      "component": true
    }
    ```

    同时，还要在 wxml 文件中编写组件模板，在 wxss 文件中加入组件样式，它们的写法与页面的写法类似。具体细节和注意事项参见 组件模板和样式 。

    代码示例：

    ```js
    <!-- 这是自定义组件的内部WXML结构 -->
    <view class="inner">
      {{innerText}}
    </view>
    <slot></slot>
    /* 这里的样式只应用于这个自定义组件 */
    .inner {
      color: red;
    }
    ```

    **注意：在组件wxss中不应使用ID选择器、属性选择器和标签名选择器。**

    在自定义组件的 js 文件中，需要使用 Component() 来注册组件，并提供组件的属性定义、内部数据和自定义方法。

    组件的属性值和内部数据将被用于组件 wxml 的渲染，其中，属性值是可由组件外部传入的。更多细节参见 Component构造器 。

    代码示例：

    ```js
    Component({
      properties: {
        // 这里定义了innerText属性，属性值可以在组件使用时指定
        innerText: {
          type: String,
          value: 'default value',
        }
      },
      data: {
        // 这里是一些组件内部数据
        someData: {}
      },
      methods: {
        // 这里是一个自定义方法
        customMethod: function(){}
      }
    }
    ```

2. 使用自定义组件
   使用已注册的自定义组件前，首先要在页面的 json 文件中进行引用声明。此时需要提供每个自定义组件的标签名和对应的自定义组件文件路径：

    ```js
    {
      "usingComponents": {
        "component-tag-name": "path/to/the/custom/component"
      }
    }
    ```

    这样，在页面的 wxml 中就可以像使用基础组件一样使用自定义组件。节点名即自定义组件的标签名，节点属性即传递给组件的属性值。

    开发者工具 1.02.1810190 及以上版本支持在 app.json 中声明 usingComponents 字段，在此处声明的自定义组件视为全局自定义组件，在小程序内的页面或自定义组件中可以直接使用而无需再声明。

    代码示例：

    在开发者工具中预览效果

    ```js
    <view>
      <!-- 以下是对一个自定义组件的引用 -->
      <component-tag-name inner-text="Some text"></component-tag-name>
    </view>
    ```

    自定义组件的 wxml 节点结构在与数据结合之后，将被插入到引用位置内。

3. 注意事项  
   一些需要注意的细节：

    因为 WXML 节点标签名只能是小写字母、中划线和下划线的组合，所以自定义组件的标签名也只能包含这些字符。  
    自定义组件也是可以引用自定义组件的，引用方法类似于页面引用自定义组件的方式（使用 usingComponents 字段）。  
    自定义组件和页面所在项目根目录名不能以“wx-”为前缀，否则会报错。  

    注意，是否在页面文件中使用 usingComponents 会使得页面的 this 对象的原型稍有差异，包括：  
    使用 usingComponents 页面的原型与不使用时不一致，即 Object.getPrototypeOf(this) 结果不同。  
    使用 usingComponents 时会多一些方法，如 selectComponent 。  
    出于性能考虑，使用 usingComponents 时， setData 内容不会被直接深复制，即 this.setData({ field: obj }) 后 this.data.field === obj 。（深复制会在这个值被组件间传递时发生。）  
    如果页面比较复杂，新增或删除 usingComponents 定义段时建议重新测试一下。  

### 组件模版和样式

#### 组件模板

组件模板的写法与页面模板相同。组件模板与组件数据结合后生成的节点树，将被插入到组件的引用位置上。  
在组件模板中可以提供一个 \<slot\> 节点，用于承载组件引用时提供的子节点。

```js
<!-- 组件模板 -->
<view class="wrapper">
  <view>这里是组件的内部节点</view>
  <slot></slot>
</view>
<!-- 引用组件的页面模板 -->
<view>
  <component-tag-name>
    <!-- 这部分内容将被放置在组件 <slot> 的位置上 -->
    <view>这里是插入到组件slot中的内容</view>
  </component-tag-name>
</view>
```

**注意，在模板中引用到的自定义组件及其对应的节点名需要在 json 文件中显式定义，否则会被当作一个无意义的节点。除此以外，节点名也可以被声明为抽象节点。**

#### 模板数据绑定

与普通的 WXML 模板类似，可以使用数据绑定，这样就可以向子组件的属性传递动态数据。

代码示例：

```js
<!-- 引用组件的页面模板 -->
<view>
  <component-tag-name prop-a="{{dataFieldA}}" prop-b="{{dataFieldB}}">
    <!-- 这部分内容将被放置在组件 <slot> 的位置上 -->
    <view>这里是插入到组件slot中的内容</view>
  </component-tag-name>
</view>
```

在以上例子中，组件的属性 propA 和 propB 将收到页面传递的数据。页面可以通过 setData 来改变绑定的数据字段。

注意：这样的数据绑定只能传递 JSON 兼容数据。自基础库版本 2.0.9 开始，还可以在数据中包含函数（但这些函数不能在 WXML 中直接调用，只能传递给子组件）。

#### 组件 wxml 的 slot

在组件的 wxml 中可以包含 slot 节点，用于承载组件使用者提供的 wxml 结构。

默认情况下，一个组件的 wxml 中只能有一个 slot 。需要使用多 slot 时，可以在组件 js 中声明启用。

```js
Component({
  options: {
    multipleSlots: true // 在组件定义时的选项中启用多slot支持
  },
  properties: { /* ... */ },
  methods: { /* ... */ }
})
```

此时，可以在这个组件的 wxml 中使用多个 slot ，以不同的 name 来区分。

```js
<!-- 组件模板 -->
<view class="wrapper">
  <slot name="before"></slot>
  <view>这里是组件的内部细节</view>
  <slot name="after"></slot>
</view>
```

使用时，用 slot 属性来将节点插入到不同的 slot 上。

```js
<!-- 引用组件的页面模板 -->
<view>
  <component-tag-name>
    <!-- 这部分内容将被放置在组件 <slot name="before"> 的位置上 -->
    <view slot="before">这里是插入到组件slot name="before"中的内容</view>
    <!-- 这部分内容将被放置在组件 <slot name="after"> 的位置上 -->
    <view slot="after">这里是插入到组件slot name="after"中的内容</view>
  </component-tag-name>
</view>
```

#### 组件样式

组件对应 wxss 文件的样式，只对组件wxml内的节点生效。编写组件样式时，需要注意以下几点：

* 组件和引用组件的页面不能使用id选择器（#a）、属性选择器（[a]）和标签名选择器，请改用class选择器。
* 组件和引用组件的页面中使用后代选择器（.a .b）在一些极端情况下会有非预期的表现，如遇，请避免使用。
* 子元素选择器（.a>.b）只能用于 view 组件与其子节点之间，用于其他组件可能导致非预期的情况。
* 继承样式，如 font 、 color ，会从组件外继承到组件内。
* 除继承样式外， app.wxss 中的样式、组件所在页面的的样式对自定义组件无效（除非更改组件样式隔离选项）。
  
```js
#a { } /* 在组件中不能使用 */
[a] { } /* 在组件中不能使用 */
button { } /* 在组件中不能使用 */
.a > .b { } /* 除非 .a 是 view 组件节点，否则不一定会生效 */
```

除此以外，组件可以指定它所在节点的默认样式，使用 :host 选择器（需要包含基础库 1.7.2 或更高版本的开发者工具支持）。

#### 组件样式隔离

默认情况下，自定义组件的样式只受到自定义组件 wxss 的影响。除非以下两种情况：

* app.wxss 或页面的 wxss 中使用了标签名选择器（或一些其他特殊选择器）来直接指定样式，这些选择器会影响到页面和全部组件。通常情况下这是不推荐的做法。
* 指定特殊的样式隔离选项 styleIsolation 。
  
```js
  Component({
  options: {
    styleIsolation: 'isolated'
  }
})
```

  styleIsolation 选项从基础库版本 2.6.5 开始支持。它支持以下取值：

* isolated 表示启用样式隔离，在自定义组件内外，使用 class 指定的样式将不会相互影响（一般情况下的默认值）；
* apply-shared 表示页面 wxss 样式将影响到自定义组件，但自定义组件 wxss 中指定的样式不会影响页面；
* shared 表示页面 wxss 样式将影响到自定义组件，自定义组件 wxss 中指定的样式也会影响页面和其他设置了 apply-shared 或 shared 的自定义组件。（这个选项在插件中不可用。）
从小程序基础库版本 2.10.1 开始，也可以在页面或自定义组件的 json 文件中配置 styleIsolation （这样就不需在 js 文件的 options 中再配置）。例如：

```json
{
  "styleIsolation": "isolated"
}
```

#### 外部样式类

有时，组件希望接受外部传入的样式类。此时可以在 Component 中用 externalClasses 定义段定义若干个外部样式类。

这个特性可以用于实现类似于 view 组件的 hover-class 属性：页面可以提供一个样式类，赋予 view 的 hover-class ，这个样式类本身写在页面中而非 view 组件的实现中。

注意：在同一个节点上使用普通样式类和外部样式类时，两个类的优先级是未定义的，因此最好避免这种情况。

代码示例：

```js
/* 组件 custom-component.js */
Component({
  externalClasses: ['my-class']
})
<!-- 组件 custom-component.wxml -->
<custom-component class="my-class">这段文本的颜色由组件外的 class 决定</custom-component>
```

这样，组件的使用者可以指定这个样式类对应的 class ，就像使用普通属性一样。在 2.7.1 之后，可以指定多个对应的 class 。

#### 引用页面或父组件的样式

即使启用了样式隔离 isolated ，组件仍然可以在局部引用组件所在页面的样式或父组件的样式。

例如，如果在页面 wxss 中定义了：

```css
.blue-text {
  color: blue;
}
```

在这个组件中可以使用 ~ 来引用这个类的样式：

```js
<view class="~blue-text"> 这段文本是蓝色的 </view>
```

如果在一个组件的父组件 wxss 中定义了：

```css
.red-text {
  color: red;
}
```

在这个组件中可以使用 ^ 来引用这个类的样式：

```js
<view class="^red-text"> 这段文本是红色的 </view>
```

也可以连续使用多个 ^ 来引用祖先组件中的样式。

注意：如果组件是比较独立、通用的组件，请优先使用外部样式类的方式，而非直接引用父组件或页面的样式。

#### 虚拟化组件节点

默认情况下，自定义组件本身的那个节点是一个“普通”的节点，使用时可以在这个节点上设置 class style 、动画、 flex 布局等，就如同普通的 view 组件节点一样。

```js
<!-- 页面的 WXML -->
<view style="display: flex">
  <!-- 默认情况下，这是一个普通的节点 -->
  <custom-component style="color: blue; flex: 1">蓝色、满宽的</custom-component>
</view>
```

但有些时候，自定义组件并不希望这个节点本身可以设置样式、响应 flex 布局等，而是希望自定义组件内部的第一层节点能够响应 flex 布局或者样式由自定义组件本身完全决定。

这种情况下，可以将这个自定义组件设置为“虚拟的”：

```js
Component({
  options: {
    virtualHost: true
  },
  properties: {
    style: { // 定义 style 属性可以拿到 style 属性上设置的值
      type: String,
    }
  },
  externalClasses: ['class'], // 可以将 class 设为 externalClasses
})
```

这样，可以将 flex 放入自定义组件内：

```js
<!-- 页面的 WXML -->
<view style="display: flex">
  <!-- 如果设置了 virtualHost ，节点上的样式将失效 -->
  <custom-component style="color: blue">不是蓝色的</custom-component>
</view>
<!-- custom-component.wxml -->
<view style="flex: 1">
  满宽的
  <slot></slot>
</view>
```

需要注意的是，自定义组件节点上的 class style 和动画将不再生效，但仍可以：

将 style 定义成 properties 属性来获取 style 上设置的值；
将 class 定义成 externalClasses 外部样式类使得自定义组件 wxml 可以使用 class 值。

### Component 构造器

omponent 构造器可用于定义组件，调用 Component 构造器时可以指定组件的属性、数据、方法等。

详细的参数含义和使用请参考 Component 参考文档。

```js
Component({

  behaviors: [],

  properties: {
    myProperty: { // 属性名
      type: String,
      value: ''
    },
    myProperty2: String // 简化的定义方式
  },
  
  data: {}, // 私有数据，可用于模板渲染

  lifetimes: {
    // 生命周期函数，可以为函数，或一个在methods段中定义的方法名
    attached: function () { },
    moved: function () { },
    detached: function () { },
  },

  // 生命周期函数，可以为函数，或一个在methods段中定义的方法名
  attached: function () { }, // 此处attached的声明会被lifetimes字段中的声明覆盖
  ready: function() { },

  pageLifetimes: {
    // 组件所在页面的生命周期函数
    show: function () { },
    hide: function () { },
    resize: function () { },
  },

  methods: {
    onMyButtonTap: function(){
      this.setData({
        // 更新属性和数据的方法与更新页面数据的方法类似
      })
    },
    // 内部方法建议以下划线开头
    _myPrivateMethod: function(){
      // 这里将 data.A[0].B 设为 'myPrivateData'
      this.setData({
        'A[0].B': 'myPrivateData'
      })
    },
    _propertyChange: function(newVal, oldVal) {

    }
  }

})
```

#### 使用 Component 构造器构造页面  

事实上，小程序的页面也可以视为自定义组件。因而，页面也可以使用 Component 构造器构造，拥有与普通组件一样的定义段与实例方法。但此时要求对应 json 文件中包含 usingComponents 定义段。

此时，组件的属性可以用于接收页面的参数，如访问页面 /pages/index/index?paramA=123&paramB=xyz ，如果声明有属性 paramA 或 paramB ，则它们会被赋值为 123 或 xyz 。

页面的生命周期方法（即 on 开头的方法），应写在 methods 定义段中。

代码示例：

```json
{
  "usingComponents": {}
}
```

```js
Component({

  properties: {
    paramA: Number,
    paramB: String,
  },

  methods: {
    onLoad: function() {
      this.data.paramA // 页面参数 paramA 的值
      this.data.paramB // 页面参数 paramB 的值
    }
  }

})
```

使用 Component 构造器来构造页面的一个好处是可以使用 behaviors 来提取所有页面中公用的代码段。

例如，在所有页面被创建和销毁时都要执行同一段代码，就可以把这段代码提取到 behaviors 中。

代码示例：

```js
// page-common-behavior.js
module.exports = Behavior({
  attached: function() {
    // 页面创建时执行
    console.info('Page loaded!')
  },
  detached: function() {
    // 页面销毁时执行
    console.info('Page unloaded!')
  }
})
// 页面 A
var pageCommonBehavior = require('./page-common-behavior')
Component({
  behaviors: [pageCommonBehavior],
  data: { /* ... */ },
  methods: { /* ... */ },
})
// 页面 B
var pageCommonBehavior = require('./page-common-behavior')
Component({
  behaviors: [pageCommonBehavior],
  data: { /* ... */ },
  methods: { /* ... */ },
})
```

### 组件间通信与事件

组件间的基本通信方式有以下几种。

* WXML 数据绑定：用于父组件向子组件的指定属性设置数据，仅能设置 JSON 兼容数据（自基础库版本 2.0.9 开始，还可以在数据中包含函数）。具体在 组件模板和样式 章节中介绍。
* 事件：用于子组件向父组件传递数据，可以传递任意数据。
* 如果以上两种方式不足以满足需要，父组件还可以通过 this.selectComponent 方法获取子组件实例对象，这样就可以直接访问组件的任意数据和方法

#### 监听事件

事件系统是组件间通信的主要方式之一。自定义组件可以触发任意的事件，引用组件的页面可以监听这些事件。关于事件的基本概念和用法，参见 事件 。

监听自定义组件事件的方法与监听基础组件事件的方法完全一致：

```js
<!-- 当自定义组件触发“myevent”事件时，调用“onMyEvent”方法 -->
<component-tag-name bindmyevent="onMyEvent" />
<!-- 或者可以写成 -->
<component-tag-name bind:myevent="onMyEvent" />
Page({
  onMyEvent: function(e){
    e.detail // 自定义组件触发事件时提供的detail对象
  }
})
```

触发事件  
自定义组件触发事件时，需要使用 triggerEvent 方法，指定事件名、detail对象和事件选项：

代码示例：

```js
<!-- 在自定义组件中 -->
<button bindtap="onTap">点击这个按钮将触发“myevent”事件</button>
Component({
  properties: {},
  methods: {
    onTap: function(){
      var myEventDetail = {} // detail对象，提供给事件监听函数
      var myEventOption = {} // 触发事件的选项
      this.triggerEvent('myevent', myEventDetail, myEventOption)
    }
  }
})
```

触发事件的选项包括：

|选项名 | 类型 | 是否必填 | 默认值 | 描述
|-------|------|---------|---------|-----
|bubbles | Boolean | 否 | false | 事件是否冒泡
|composed | Boolean | 否 | false | 事件是否可以穿越组件边界，为false时，事件将只能在引用组件的节点树上触发，不进入其他任何组件内部
|capturePhase | Boolean | 否 | false | 事件是否拥有捕获阶段
关于冒泡和捕获阶段的概念，请阅读 事件 章节中的相关说明。

代码示例：

```js
// 页面 page.wxml
<another-component bindcustomevent="pageEventListener1">
  <my-component bindcustomevent="pageEventListener2"></my-component>
</another-component>
// 组件 another-component.wxml
<view bindcustomevent="anotherEventListener">
  <slot />
</view>
// 组件 my-component.wxml
<view bindcustomevent="myEventListener">
  <slot />
</view>
// 组件 my-component.js
Component({
  methods: {
    onTap: function(){
      this.triggerEvent('customevent', {}) // 只会触发 pageEventListener2
      this.triggerEvent('customevent', {}, { bubbles: true }) // 会依次触发 pageEventListener2 、 pageEventListener1
      this.triggerEvent('customevent', {}, { bubbles: true, composed: true }) // 会依次触发 pageEventListener2 、 anotherEventListener 、 pageEventListener1
    }
  }
})
```

#### 获取组件实例

可在父组件里调用 this.selectComponent ，获取子组件的实例对象。

调用时需要传入一个匹配选择器 selector，如：this.selectComponent(".my-component")。

selector 详细语法可查看 selector 语法参考文档。

代码示例：

```js

// 父组件
Page({
  data: {},
  getChildComponent: function () {
    const child = this.selectComponent('.my-component');
    console.log(child)
  }
})
```

在上例中，父组件将会获取 class 为 my-component 的子组件实例对象，即子组件的 this 。

**注意 ：默认情况下，小程序与插件之间、不同插件之间的组件将无法通过 selectComponent 得到组件实例（将返回 null）。如果想让一个组件在上述条件下依然能被 selectComponent 返回，可以自定义其返回结果（见下）。**

自定义的组件实例获取结果
若需要自定义 selectComponent 返回的数据，可使用内置 behavior: wx://component-export

从基础库版本 2.2.3 开始提供支持。

使用该 behavior 时，自定义组件中的 export 定义段将用于指定组件被 selectComponent 调用时的返回值。

代码示例：

在开发者工具中预览效果

```js
// 自定义组件 my-component 内部
Component({
  behaviors: ['wx://component-export'],
  export() {
    return { myField: 'myValue' }
  }
})
<!-- 使用自定义组件时 -->
<my-component id="the-id" />
// 父组件调用
const child = this.selectComponent('#the-id') // 等于 { myField: 'myValue' }
```

在上例中，父组件获取 id 为 the-id 的子组件实例的时候，得到的是对象 { myField: 'myValue' } 。

### 组件生命周期

组件的生命周期，指的是组件自身的一些函数，这些函数在特殊的时间点或遇到一些特殊的框架事件时被自动触发。  
其中，最重要的生命周期是 created attached detached ，包含一个组件实例生命流程的最主要时间点。  

* 组件实例刚刚被创建好时， created 生命周期被触发。此时，组件数据 this.data 就是在 Component 构造器中定义的数据 data 。 此时还不能调用 setData 。 通常情况下，这个生命周期只应该用于给组件 this 添加一些自定义属性字段。
* 在组件完全初始化完毕、进入页面节点树后， attached 生命周期被触发。此时， this.data 已被初始化为组件的当前值。这个生命周期很有用，绝大多数初始化工作可以在这个时机进行。  
* 在组件离开页面节点树后， detached 生命周期被触发。退出一个页面时，如果组件还在页面节点树中，则 detached 会被触发

#### 定义生命周期方法

生命周期方法可以直接定义在 Component 构造器的第一级参数中。

自小程序基础库版本 2.2.3 起，组件的的生命周期也可以在 lifetimes 字段内进行声明（这是推荐的方式，其优先级最高）。

代码示例

```js
Component({
  lifetimes: {
    attached: function() {
      // 在组件实例进入页面节点树时执行
    },
    detached: function() {
      // 在组件实例被从页面节点树移除时执行
    },
  },
  // 以下是旧式的定义方式，可以保持对 <2.2.3 版本基础库的兼容
  attached: function() {
    // 在组件实例进入页面节点树时执行
  },
  detached: function() {
    // 在组件实例被从页面节点树移除时执行
  },
  // ...
})
```

在 behaviors 中也可以编写生命周期方法，同时不会与其他 behaviors 中的同名生命周期相互覆盖。但要注意，如果一个组件多次直接或间接引用同一个 behavior ，这个 behavior 中的生命周期函数在一个执行时机内只会执行一次。

可用的全部生命周期如下表所示。

| 生命周期 | 参数 | 描述 | 最低版本
|----------|-------|-------|-------
| created | 无 | 在组件实例刚刚被创建时执行 | 1.6.3
| attached | 无 | 在组件实例进入页面节点树时执行 | 1.6.3
| ready | 无 | 在组件在视图层布局完成后执行 | 1.6.3
| moved | 无 | 在组件实例被移动到节点树另一个位置时执行 | 1.6.3
| detached | 无 | 在组件实例被从页面节点树移除时执行 | 1.6.3
| error | Object Error | 每当组件方法抛出错误时执行 | 2.4.1

#### 组件所在页面的生命周期

还有一些特殊的生命周期，它们并非与组件有很强的关联，但有时组件需要获知，以便组件内部处理。这样的生命周期称为“组件所在页面的生命周期”，在 pageLifetimes 定义段中定义。其中可用的生命周期包括：

| 生命周期 | 参数 | 描述 | 最低版本
|-----|-----|-----|----
| show | 无 | 组件所在的页面被展示时执行 | 2.2.3
| hide | 无 | 组件所在的页面被隐藏时执行 | 2.2.3
| resize | Object Size | 组件所在的页面尺寸变化时执行 | 2.4.0
| routeDone | 无 | 组件所在页面路由动画完成时执行 |2.31.2

```js
Component({
  pageLifetimes: {
    show: function() {
      // 页面被展示
    },
    hide: function() {
      // 页面被隐藏
    },
    resize: function(size) {
      // 页面尺寸变化
    }
  }
})
```

### behaviors

behaviors 是用于组件间代码共享的特性，类似于一些编程语言中的 “mixins” 或 “traits”。

每个 behavior 可以包含一组属性、数据、生命周期函数和方法。组件引用它时，它的属性、数据和方法会被合并到组件中，生命周期函数也会在对应时机被调用。 每个组件可以引用多个 behavior ，behavior 也可以引用其它 behavior 。
在上例中， my-component 组件定义中加入了 my-behavior，

而 my-behavior 结构为：

属性：myBehaviorProperty  
数据字段：myBehaviorData  
方法：myBehaviorMethod  
生命周期函数：attached、created、ready  
这将使 my-component 最终结构为：

属性：myBehaviorProperty、myProperty  
数据字段：myBehaviorData、myData  
方法：myBehaviorMethod、myMethod  
生命周期函数：attached、created、ready  
当组件触发生命周期时，上例生命周期函数执行顺序为：  

1. [my-behavior] created
2. [my-component] created
3. [my-behavior] attached
4. [my-component] attached
5. [my-behavior] ready
6. [my-component] ready

#### 内置 behaviors

自定义组件可以通过引用内置的 behavior 来获得内置组件的一些行为。

### 组件间关系

#### 定义和使用组件间关系

有时需要实现这样的组件：

```js
<custom-ul>
  <custom-li> item 1 </custom-li>
  <custom-li> item 2 </custom-li>
</custom-ul>
```

这个例子中， custom-ul 和 custom-li 都是自定义组件，它们有相互间的关系，相互间的通信往往比较复杂。此时在组件定义时加入 relations 定义段，可以解决这样的问题。示例：

```js
// path/to/custom-ul.js
Component({
  relations: {
    './custom-li': {
      type: 'child', // 关联的目标节点应为子节点
      linked: function(target) {
        // 每次有custom-li被插入时执行，target是该节点实例对象，触发在该节点attached生命周期之后
      },
      linkChanged: function(target) {
        // 每次有custom-li被移动后执行，target是该节点实例对象，触发在该节点moved生命周期之后
      },
      unlinked: function(target) {
        // 每次有custom-li被移除时执行，target是该节点实例对象，触发在该节点detached生命周期之后
      }
    }
  },
  methods: {
    _getAllLi: function(){
      // 使用getRelationNodes可以获得nodes数组，包含所有已关联的custom-li，且是有序的
      var nodes = this.getRelationNodes('path/to/custom-li')
    }
  },
  ready: function(){
    this._getAllLi()
  }
})
// path/to/custom-li.js
Component({
  relations: {
    './custom-ul': {
      type: 'parent', // 关联的目标节点应为父节点
      linked: function(target) {
        // 每次被插入到custom-ul时执行，target是custom-ul节点实例对象，触发在attached生命周期之后
      },
      linkChanged: function(target) {
        // 每次被移动后执行，target是custom-ul节点实例对象，触发在moved生命周期之后
      },
      unlinked: function(target) {
        // 每次被移除时执行，target是custom-ul节点实例对象，触发在detached生命周期之后
      }
    }
  }
})
```

注意：必须在两个组件定义中都加入relations定义，否则不会生效。

关联一类组件
在开发者工具中预览效果

有时，需要关联的是一类组件，如：

```js
<custom-form>
  <view>
    input
    <custom-input></custom-input>
  </view>
  <custom-submit> submit </custom-submit>
</custom-form>
```

custom-form 组件想要关联 custom-input 和 custom-submit 两个组件。此时，如果这两个组件都有同一个behavior：

```js
// path/to/custom-form-controls.js
module.exports = Behavior({
  // ...
})
// path/to/custom-input.js
var customFormControls = require('./custom-form-controls')
Component({
  behaviors: [customFormControls],
  relations: {
    './custom-form': {
      type: 'ancestor', // 关联的目标节点应为祖先节点
    }
  }
})
// path/to/custom-submit.js
var customFormControls = require('./custom-form-controls')
Component({
  behaviors: [customFormControls],
  relations: {
    './custom-form': {
      type: 'ancestor', // 关联的目标节点应为祖先节点
    }
  }
})
```

则在 relations 关系定义中，可使用这个behavior来代替组件路径作为关联的目标节点：

```js
// path/to/custom-form.js
var customFormControls = require('./custom-form-controls')
Component({
  relations: {
    'customFormControls': {
      type: 'descendant', // 关联的目标节点应为子孙节点
      target: customFormControls
    }
  }
})
```

relations 定义段
relations 定义段包含目标组件路径及其对应选项，可包含的选项见下表。

|选项	类型	是否必填	描述
|type	String	是	目标组件的相对关系，可选的值为 parent 、 child 、 ancestor 、 descendant
|linked	Function	否	关系生命周期函数，当关系被建立在页面节点树中时触发，触发时机|在组件attached生命周期之后
|linkChanged	Function	否	关系生命周期函数，当关系在页面节点树中发生改变时触发，触|发时机在组件moved生命周期之后
|unlinked	Function	否	关系生命周期函数，当关系脱离页面节点树时触发，触发时机在组|件detached生命周期之后
|target	String	否	如果这一项被设置，则它表示关联的目标节点所应具有的behavior，所有拥有这一behavior的组件节点都会被关联

### 数据监听器
数据监听器可以用于监听和响应任何属性和数据字段的变化。从小程序基础库版本 2.6.1 开始支持。

#### 使用数据监听器

有时，在一些数据字段被 setData 设置时，需要执行一些操作。

例如， this.data.sum 永远是 this.data.numberA 与 this.data.numberB 的和。此时，可以使用数据监听器进行如下实现。

```js
Component({
  attached: function() {
    this.setData({
      numberA: 1,
      numberB: 2,
    })
  },
  observers: {
    'numberA, numberB': function(numberA, numberB) {
      // 在 numberA 或者 numberB 被设置时，执行这个函数
      this.setData({
        sum: numberA + numberB
      })
    }
  }
})
```

#### 监听字段语法

数据监听器支持监听属性或内部数据的变化，可以同时监听多个。一次 setData 最多触发每个监听器一次。

同时，监听器可以监听子数据字段，如下例所示。

```js
Component({
  observers: {
    'some.subfield': function(subfield) {
      // 使用 setData 设置 this.data.some.subfield 时触发
      // （除此以外，使用 setData 设置 this.data.some 也会触发）
      subfield === this.data.some.subfield
    },
    'arr[12]': function(arr12) {
      // 使用 setData 设置 this.data.arr[12] 时触发
      // （除此以外，使用 setData 设置 this.data.arr 也会触发）
      arr12 === this.data.arr[12]
    },
  }
})
```

### 纯数据字段

纯数据字段是一些不用于界面渲染的 data 字段，可以用于提升页面更新性能。从小程序基础库版本 2.8.2 开始支持。

组件数据中的纯数据字段
有些情况下，某些 data 中的字段（包括 setData 设置的字段）既不会展示在界面上，也不会传递给其他组件，仅仅在当前组件内部使用。

此时，可以指定这样的数据字段为“纯数据字段”，它们将仅仅被记录在 this.data 中，而不参与任何界面渲染过程，这样有助于提升页面更新性能。

指定“纯数据字段”的方法是在 Component 构造器的 options 定义段中指定 pureDataPattern 为一个正则表达式，字段名符合这个正则表达式的字段将成为纯数据字段。
代码示例：

```js
Component({
  options: {
    pureDataPattern: /^_/ // 指定所有 _ 开头的数据字段为纯数据字段
  },
  data: {
    a: true, // 普通数据字段
    _b: true, // 纯数据字段
  },
  methods: {
    myMethod() {
      this.data._b // 纯数据字段可以在 this.data 中获取
      this.setData({
        c: true, // 普通数据字段
        _d: true, // 纯数据字段
      })
    }
  }
})
```

上述组件中的纯数据字段不会被应用到 WXML 上：

```js
<view wx:if="{{a}}"> 这行会被展示 </view>
<view wx:if="{{_b}}"> 这行不会被展示 </view>
```

组件属性中的纯数据字段
属性也可以被指定为纯数据字段（遵循 pureDataPattern 的正则表达式）。

属性中的纯数据字段可以像普通属性一样接收外部传入的属性值，但不能将它直接用于组件自身的 WXML 中。

代码示例：

```js
Component({
  options: {
    pureDataPattern: /^_/
  },
  properties: {
    a: Boolean,
    _b: {
      type: Boolean,
      observer() {
        // 不要这样做！这个 observer 永远不会被触发
      }
    },
  }
})
```

注意：属性中的纯数据字段的属性 observer 永远不会触发！如果想要监听属性值变化，使用 数据监听器 代替。

从小程序基础库版本 2.10.1 开始，也可以在页面或自定义组件的 json 文件中配置 pureDataPattern （这样就不需在 js 文件的 options 中再配置）。此时，其值应当写成字符串形式：

```json
{
  "pureDataPattern": "^_"
}
```

使用数据监听器监听纯数据字段
数据监听器 可以用于监听纯数据字段（与普通数据字段一样）。这样，可以通过监听、响应纯数据字段的变化来改变界面。

下面的示例是一个将 JavaScript 时间戳转换为可读时间的自定义组件。

在开发者工具中预览效果

代码示例：

```js
Component({
  options: {
    pureDataPattern: /^timestamp$/ // 将 timestamp 属性指定为纯数据字段
  },
  properties: {
    timestamp: Number,
  },
  observers: {
    timestamp: function () {
      // timestamp 被设置时，将它展示为可读时间字符串
      var timeString = new Date(this.data.timestamp).toLocaleString()
      this.setData({
        timeString: timeString
      })
    }
  }
})
```

### 抽象节点

有时，自定义组件模板中的一些节点，其对应的自定义组件不是由自定义组件本身确定的，而是自定义组件的调用者确定的。这时可以把这个节点声明为“抽象节点”。

例如，我们现在来实现一个“选框组”（selectable-group）组件，它其中可以放置单选框（custom-radio）或者复选框（custom-checkbox）。这个组件的 wxml 可以这样编写：

代码示例：

```js
<!-- selectable-group.wxml -->
<view wx:for="{{labels}}">
  <label>
    <selectable disabled="{{false}}"></selectable>
    {{item}}
  </label>
</view>
```

其中，“selectable”不是任何在 json 文件的 usingComponents 字段中声明的组件，而是一个抽象节点。它需要在 componentGenerics 字段中声明：

```js
{
  "componentGenerics": {
    "selectable": true
  }
}
```

使用包含抽象节点的组件
在使用 selectable-group 组件时，必须指定“selectable”具体是哪个组件：

```js
<selectable-group generic:selectable="custom-radio" />
```

这样，在生成这个 selectable-group 组件的实例时，“selectable”节点会生成“custom-radio”组件实例。类似地，如果这样使用：

```js
<selectable-group generic:selectable="custom-checkbox" />
```

“selectable”节点则会生成“custom-checkbox”组件实例。

注意：上述的 custom-radio 和 custom-checkbox 需要包含在这个 wxml 对应 json 文件的 usingComponents 定义段中。

```js
{
  "usingComponents": {
    "custom-radio": "path/to/custom/radio",
    "custom-checkbox": "path/to/custom/checkbox"
  }
}
```

抽象节点的默认组件
抽象节点可以指定一个默认组件，当具体组件未被指定时，将创建默认组件的实例。默认组件可以在 componentGenerics 字段中指定：

```js
{
  "componentGenerics": {
    "selectable": {
      "default": "path/to/default/component"
    }
  }
}
```

注意事项
节点的 generic 引用 generic:xxx="yyy" 中，值 yyy 只能是静态值，不能包含数据绑定。因而抽象节点特性并不适用于动态决定节点名的场景。

### 自定义组件扩展

为了更好定制自定义组件的功能，可以使用自定义组件扩展机制。从小程序基础库版本 2.2.3 开始支持。

扩展后的效果
为了更好的理解扩展后的效果，先举一个例子：

在开发者工具中预览效果

```js
// behavior.js
module.exports = Behavior({
  definitionFilter(defFields) {
    defFields.data.from = 'behavior'
  },
})

// component.js
Component({
  data: {
    from: 'component'
  },
  behaviors: [require('behavior.js')],
  ready() {
    console.log(this.data.from) // 此处会发现输出 behavior 而不是 component
  }
})
```

通过例子可以发现，自定义组件的扩展其实就是提供了修改自定义组件定义段的能力，上述例子就是修改了自定义组件中的 data 定义段里的内容。

使用扩展
Behavior() 构造器提供了新的定义段 definitionFilter ，用于支持自定义组件扩展。 definitionFilter 是一个函数，在被调用时会注入两个参数，第一个参数是使用该 behavior 的 component/behavior 的定义对象，第二个参数是该 behavior 所使用的 behavior 的 definitionFilter 函数列表。

以下举个例子来说明：

```js
// behavior3.js
module.exports = Behavior({
    definitionFilter(defFields, definitionFilterArr) {},
})

// behavior2.js
module.exports = Behavior({
  behaviors: [require('behavior3.js')],
  definitionFilter(defFields, definitionFilterArr) {
    // definitionFilterArr[0](defFields)
  },
})

// behavior1.js
module.exports = Behavior({
  behaviors: [require('behavior2.js')],
  definitionFilter(defFields, definitionFilterArr) {},
})

// component.js
Component({
  behaviors: [require('behavior1.js')],
})
```

上述代码中声明了1个自定义组件和3个 behavior，每个 behavior 都使用了 definitionFilter 定义段。那么按照声明的顺序会有如下事情发生：

1. 当进行 behavior2 的声明时就会调用 behavior3 的 definitionFilter 函数，其中 defFields 参数是 behavior2 的定义段， definitionFilterArr 参数即为空数组，因为 behavior3 没有使用其他的 behavior 。
2. 当进行 behavior1 的声明时就会调用 behavior2 的 definitionFilter 函数，其中 defFields 参数是 behavior1 的定义段， definitionFilterArr 参数是一个长度为1的数组，definitionFilterArr[0] 即为 behavior3 的 definitionFilter 函数，因为 behavior2 使用了 behavior3。用户在此处可以自行决定在进行 behavior1 的声明时要不要调用 behavior3 的 definitionFilter 函数，如果需要调用，在此处补充代码 definitionFilterArr[0](defFields) 即可，definitionFilterArr 参数会由基础库补充传入。
3. 同理，在进行 component 的声明时就会调用 behavior1 的 definitionFilter 函数。  
   
简单概括，definitionFilter 函数可以理解为当 A 使用了 B 时，A 声明就会调用 B 的 definitionFilter 函数并传入 A 的定义对象让 B 去过滤。此时如果 B 还使用了 C 和 D ，那么 B 可以自行决定要不要调用 C 和 D 的 definitionFilter 函数去过滤 A 的定义对象。

代码示例：

在开发者工具中预览效果

真实案例
下面利用扩展简单实现自定义组件的计算属性功能:

```js
// behavior.js
module.exports = Behavior({
  lifetimes: {
    created() {
      this._originalSetData = this.setData // 原始 setData
      this.setData = this._setData // 封装后的 setData
    }
  },
  definitionFilter(defFields) {
    const computed = defFields.computed || {}
    const computedKeys = Object.keys(computed)
    const computedCache = {}

    // 计算 computed
    const calcComputed = (scope, insertToData) => {
      const needUpdate = {}
      const data = defFields.data = defFields.data || {}

      for (let key of computedKeys) {
        const value = computed[key].call(scope) // 计算新值
        if (computedCache[key] !== value) needUpdate[key] = computedCache[key] = value
        if (insertToData) data[key] = needUpdate[key] // 直接插入到 data 中，初始化时才需要的操作
      }

      return needUpdate
    }

    // 重写 setData 方法
    defFields.methods = defFields.methods || {}
    defFields.methods._setData = function (data, callback) {
      const originalSetData = this._originalSetData // 原始 setData
      originalSetData.call(this, data, callback) // 做 data 的 setData
      const needUpdate = calcComputed(this) // 计算 computed
      originalSetData.call(this, needUpdate) // 做 computed 的 setData
    }

    // 初始化 computed
    calcComputed(defFields, true) // 计算 computed
  }
})
```

在组件中使用：

```js
const beh = require('./behavior.js')
Component({
  behaviors: [beh],
  data: {
    a: 0,
  },
  computed: {
    b() {
      return this.data.a + 100
    },
  },
  methods: {
    onTap() {
      this.setData({
        a: ++this.data.a,
      })
    }
  }
})
<view>data: {{a}}</view>
<view>computed: {{b}}</view>
<button bindtap="onTap">click</button>
```

实现原理很简单，对已有的 setData 进行二次封装，在每次 setData 的时候计算出 computed 里各字段的值，然后设到 data 中，以达到计算属性的效果。

此实现只是作为一个简单案例来展示，请勿直接在生产环境中使用。




## 小程序配置
