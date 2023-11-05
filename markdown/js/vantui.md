# vantUI

Vant 是一个轻量、可定制的移动端组件库，于 2017 年开源

## 特性
🚀 性能极佳，组件平均体积小于 1KB（min+gzip）  
🚀 70+ 个高质量组件，覆盖移动端主流场景  
🚀 零外部依赖，不依赖三方 npm 包  
💪 使用 TypeScript 编写，提供完整的类型定义  
💪 单元测试覆盖率超过 90%，提供稳定性保障  
📖 提供丰富的中英文文档和组件示例  
📖 提供 Sketch 和 Axure 设计资源  
🍭 支持 Vue 2、Vue 3 和微信小程序  
🍭 支持 Nuxt 2、Nuxt 3，提供 Nuxt 的 Vant Module  
🍭 支持主题定制，内置 700+ 个主题变量  
🍭 支持按需引入和 Tree Shaking  
🍭 支持无障碍访问（持续改进中）  
🍭 支持深色模式  
🍭 支持服务器端渲染  
🌍 支持国际化，内置 30+ 种语言包

## 安装

在现有项目中使用 Vant 时，可以通过 npm 进行安装：
```sh
# Vue 3 项目，安装最新版 Vant
npm i vant

# Vue 2 项目，安装 Vant 2
npm i vant@latest-v2
```

## 引入组件

```js
import { createApp } from 'vue';
// 1. 引入你需要的组件
import { Button } from 'vant';
// 2. 引入组件样式
import 'vant/lib/index.css';

const app = createApp();

// 3. 注册你需要的组件
app.use(Button);
```

## 按需引入组件样式

1. 使用 unplugin-vue-components 插件，它可以自动引入组件，并按需引入组件的样式

    ```sh
    1. 安装插件
    # 通过 npm 安装
    npm i unplugin-vue-components -D

    # 通过 yarn 安装
    yarn add unplugin-vue-components -D

    # 通过 pnpm 安装
    pnpm add unplugin-vue-components -D
    ```

2. 配置插件
如果是基于 vite 的项目，在 vite.config.js 文件中配置插件：

    ```js
    import vue from '@vitejs/plugin-vue';
    import Components from 'unplugin-vue-components/vite';
    import { VantResolver } from 'unplugin-vue-components/resolvers';

    export default {
    plugins: [
        vue(),
        Components({
        resolvers: [VantResolver()],
        }),
    ],
    };
    ```

3. 使用组件
   完成以上两步，就可以直接在模板中使用 Vant 组件了，unplugin-vue-components 会解析模板并自动注册对应的组件。
4. 引入函数组件的样式
   Vant 中有个别组件是以函数的形式提供的，包括 Toast，Dialog，Notify 和 ImagePreview 组件。在使用函数组件时，unplugin-vue-components 无法自动引入对应的样式，因此需要手动引入样式。

## 基础组件

1. 按钮

   ```js
    <van-button type="primary">主要按钮</van-button>
    <van-button type="success">成功按钮</van-button>
    <van-button type="default">默认按钮</van-button>
    <van-button type="warning">警告按钮</van-button>
    <van-button type="danger">危险按钮</van-button>
    <van-button plain type="primary">朴素按钮</van-button>
    <van-button plain type="success">朴素按钮</van-button>
    <van-button plain hairline type="primary">细边框按钮</van-button>
    <van-button plain hairline type="success">细边框按钮</van-button>
    <van-button disabled type="primary">禁用状态</van-button>
    <van-button disabled type="success">禁用状态</van-button>
    <van-button loading type="primary" />
    <van-button loading type="primary" loading-type="spinner" />
    <van-button loading type="success" loading-text="加载中..." />
   ```
2. Cell 单元格

3. ConfigProvider 全局配置
用于全局配置 Vant 组件，提供深色模式、主题定制等能力。  
**深色模式**  
将 ConfigProvider 组件的 theme 属性设置为 dark，可以开启深色模式。  
**定制主题**  
Vant 组件通过丰富的 CSS 变量 来组织样式，通过覆盖这些 CSS 变量，可以实现定制主题、动态切换主题等效果。
以 Button 组件为例，查看组件的样式，可以看到 .van-button--primary 类名上存在以下变量：

   ```css
    .van-button--primary {
    color: var(--van-button-primary-color);
    background-color: var(--van-button-primary-background);
    }
   ```

这些变量的默认值被定义在 :root 节点上，HTML 里的所有子节点都可以访问到这些变量

**自定义 CSS 变量**   
可以直接在代码中覆盖这些 CSS 变量，Button 组件的样式会随之发生改变：

```js
/* 添加这段样式后，Primary Button 会变成红色 */
:root:root {
  --van-button-primary-background: red;
}
```

注意：为什么要写两个重复的 :root？

由于 vant 中的主题变量也是在 :root 下声明的，所以在有些情况下会由于优先级的问题无法成功覆盖。通过 :root:root 可以显式地让你所写内容的优先级更高一些，从而确保主题变量的成功覆盖。

**通过 ConfigProvider 覆盖**  
ConfigProvider 组件提供了覆盖 CSS 变量的能力，你需要在根节点包裹一个 ConfigProvider 组件，并通过 theme-vars 属性来配置一些主题变量。

```js
<van-config-provider :theme-vars="themeVars">
  <van-form>
    <van-field name="rate" label="评分">
      <template #input>
        <van-rate v-model="rate" />
      </template>
    </van-field>
    <van-field name="slider" label="滑块">
      <template #input>
        <van-slider v-model="slider" />
      </template>
    </van-field>
    <div style="margin: 16px">
      <van-button round block type="primary" native-type="submit">
        提交
      </van-button>
    </div>
  </van-form>
</van-config-provider>
```

```js
import { ref, reactive } from 'vue';

export default {
  setup() {
    const rate = ref(4);
    const slider = ref(50);

    // themeVars 内的值会被转换成对应 CSS 变量
    // 比如 sliderBarHeight 会转换成 `--van-slider-bar-height`
    const themeVars = reactive({
      rateIconFullColor: '#07c160',
      sliderBarHeight: '4px',
      sliderButtonWidth: '20px',
      sliderButtonHeight: '20px',
      sliderActiveBackground: '#07c160',
      buttonPrimaryBackground: '#07c160',
      buttonPrimaryBorderColor: '#07c160',
    });

    return {
      rate,
      slider,
      themeVars,
    };
  },
};
```

**主题变量**  
基础变量  
Vant 中的 CSS 变量分为 基础变量 和 组件变量。组件变量会继承基础变量，因此在修改基础变量后，会影响所有相关的组件。

修改变量  
由于 CSS 变量继承机制的原因，两者的修改方式有一定差异：

基础变量只能通过 :root 选择器 修改，不能通过 ConfigProvider 组件 修改。
组件变量可以通过 :root 选择器 和 ConfigProvider 组件 修改。
你也可以使用 .van-theme-light 和 .van-theme-dark 这两个类名选择器来单独修改浅色或深色模式下的基础变量和组件变量。

## Icon 图标
基础用法  
通过 name 属性来指定需要使用的图标，Vant 内置了一套图标库（见右侧示例），可以直接传入对应的名称来使用。

```js
<van-icon name="chat-o" />
```

使用图片 URL  
你也可以直接在 name 属性中传入一个图片 URL 来作为图标。

```js
<van-icon name="https://fastly.jsdelivr.net/npm/@vant/assets/icon-demo.png" />
```

徽标提示  
设置 dot 属性后，会在图标右上角展示一个小红点；设置 badge 属性后，会在图标右上角展示相应的徽标。

```js
<van-icon name="chat-o" dot />
<van-icon name="chat-o" badge="9" />
<van-icon name="chat-o" badge="99+" />
```

图标颜色
通过 color 属性来设置图标的颜色。

```js
<van-icon name="cart-o" color="#1989fa" />
<van-icon name="fire-o" color="#ee0a24" />
```

图标大小  
通过 size 属性来设置图标的尺寸大小，可以指定任意 CSS 单位。

```js
<!-- 不指定单位，默认使用 px -->
<van-icon name="chat-o" size="40" />
<!-- 指定使用 rem 单位 -->
<van-icon name="chat-o" size="3rem" />
```

自定义图标  
如果需要在现有 Icon 的基础上使用更多图标，可以引入第三方 iconfont 对应的字体文件和 CSS 文件，之后就可以在 Icon 组件中直接使用。

```js
/* 引入第三方或自定义的字体图标样式 */
@font-face {
  font-family: 'my-icon';
  src: url('./my-icon.ttf') format('truetype');
}

.my-icon {
  font-family: 'my-icon';
}

.my-icon-extra::before {
  content: '\e626';
}
<!-- 通过 class-prefix 指定类名为 my-icon -->
<van-icon class-prefix="my-icon" name="extra" />
```

## Image 图片

基础用法  
基础用法与原生 img 标签一致，可以设置 src、width、height、alt 等原生属性。

```js
<van-image
  width="100"
  height="100"
  src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
/>
```

填充模式  
通过 fit 属性可以设置图片填充模式，等同于原生的 object-fit 属性，可选值见下方表格。

```js
<van-image
  width="10rem"
  height="10rem"
  fit="contain"
  src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
/>
```

图片位置  
通过 position 属性可以设置图片位置，结合 fit 属性使用，等同于原生的 object-position 属性。
```js
<van-image
  width="10rem"
  height="10rem"
  fit="cover"
  position="left"
  src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
/>
```

圆形图片  
通过 round 属性可以设置图片变圆

图片懒加载  
设置 lazy-load 属性来开启图片懒加载，需要搭配 Lazyload 组件使用  

加载中提示  
Image 组件提供了默认的加载中提示，支持通过 loading 插槽自定义内容。

```js
<van-image src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg">
  <template v-slot:loading>
    <van-loading type="spinner" size="20" />
  </template>
</van-image>
```

加载失败提示  
Image 组件提供了默认的加载失败提示，支持通过 error 插槽自定义内容。

```js
<van-image src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg">
  <template v-slot:error>加载失败</template>
</van-image>
```

## Layout 布局

引入  
通过以下方式来全局注册组件，更多注册方式请参考组件注册。

```js
import { createApp } from 'vue';
import { Col, Row } from 'vant';

const app = createApp();
app.use(Col);
app.use(Row);
```

基础用法  
Layout 组件提供了 24列栅格，通过在 Col 上添加 span 属性设置列所占的宽度百分比。此外，添加 offset 属性可以设置列的偏移宽度，计算方式与 span 相同。

```js
<van-row>
  <van-col span="8">span: 8</van-col>
  <van-col span="8">span: 8</van-col>
  <van-col span="8">span: 8</van-col>
</van-row>

<van-row>
  <van-col span="4">span: 4</van-col>
  <van-col span="10" offset="4">offset: 4, span: 10</van-col>
</van-row>

<van-row>
  <van-col offset="12" span="12">offset: 12, span: 12</van-col>
</van-row>
```

设置列元素间距  
通过 gutter 属性可以设置列元素之间的间距，默认间距为 0。

```js
<van-row gutter="20">
  <van-col span="8">span: 8</van-col>
  <van-col span="8">span: 8</van-col>
  <van-col span="8">span: 8</van-col>
</van-row>
```

对齐方式  
通过 justify 属性可以设置主轴上内容的对齐方式，等价于 flex 布局中的 justify-content 属性。
```js
<!-- 居中 -->
<van-row justify="center">
  <van-col span="6">span: 6</van-col>
  <van-col span="6">span: 6</van-col>
  <van-col span="6">span: 6</van-col>
</van-row>

<!-- 右对齐 -->
<van-row justify="end">
  <van-col span="6">span: 6</van-col>
  <van-col span="6">span: 6</van-col>
  <van-col span="6">span: 6</van-col>
</van-row>

<!-- 两端对齐 -->
<van-row justify="space-between">
  <van-col span="6">span: 6</van-col>
  <van-col span="6">span: 6</van-col>
  <van-col span="6">span: 6</van-col>
</van-row>

<!-- 每个元素的两侧间隔相等 -->
<van-row justify="space-around">
  <van-col span="6">span: 6</van-col>
  <van-col span="6">span: 6</van-col>
  <van-col span="6">span: 6</van-col>
</van-row>
```

## Popup 弹出层
弹出层容器，用于展示弹窗、信息提示等内容，支持多个弹出层叠加展示。

**引入**  
通过以下方式来全局注册组件，更多注册方式请参考组件注册。

```js
import { createApp } from 'vue';
import { Popup } from 'vant';

const app = createApp();
app.use(Popup);
```

**基础用法**  
通过 v-model:show 控制弹出层是否展示。

```js
<van-cell is-link @click="showPopup">展示弹出层</van-cell>
<van-popup v-model:show="show" :style="{ padding: '64px' }">内容</van-popup>
import { ref } from 'vue';

export default {
  setup() {
    const show = ref(false);
    const showPopup = () => {
      show.value = true;
    };
    return {
      show,
      showPopup,
    };
  },
};
```

**弹出位置**  
通过 position 属性设置弹窗的弹出位置，默认为居中弹出，可以设置为 top、bottom、left、right。

当弹窗从顶部或底部弹出时，默认宽度与屏幕宽度保持一致，弹窗高度取决于内容的高度。
当弹窗从左侧或右侧弹出时，默认不设置宽度和高度，弹窗的宽高取决于内容的宽高。

```js
<!-- 顶部弹出 -->
<van-popup v-model:show="showTop" position="top" :style="{ height: '30%' }" />

<!-- 底部弹出 -->
<van-popup
  v-model:show="showBottom"
  position="bottom"
  :style="{ height: '30%' }"
/>

<!-- 左侧弹出 -->
<van-popup
  v-model:show="showLeft"
  position="left"
  :style="{ width: '30%', height: '100%' }"
/>

<!-- 右侧弹出 -->
<van-popup
  v-model:show="showRight"
  position="right"
  :style="{ width: '30%', height: '100%' }"
/>
```

关闭图标  
设置 closeable 属性后，会在弹出层的右上角显示关闭图标，并且可以通过 close-icon 属性自定义图标，使用 close-icon-position 属性可以自定义图标位置。

圆角弹窗  
设置 round 属性后，弹窗会根据弹出位置添加不同的圆角样式。

监听点击事件  
Popup 支持以下点击事件：

click: 点击弹出层时触发。
click-overlay: 点击遮罩层时触发。
click-close-icon: 点击关闭图标时触发。

监听显示事件  
当 Popup 被打开或关闭时，会触发以下事件：

open: 打开弹出层时立即触发。
opened: 打开弹出层且动画结束后触发。
close: 关闭弹出层时立即触发。
closed: 关闭弹出层且动画结束后触发。

## Space 间距

设置元素之间的间距
基础用法  
Space 组件会在各个子组件之间设置一定的间距，默认间距为 8px。

```js
<van-space>
  <van-button type="primary">按钮</van-button>
  <van-button type="primary">按钮</van-button>
  <van-button type="primary">按钮</van-button>
  <van-button type="primary">按钮</van-button>
</van-space>
```

垂直排列  

将 direction 属性设置为 vertical，可以设置垂直方向排列的间距。

自定义间距  
通过调整 size 的值来控制间距的大小。传入 number 类型时，会默认使用 px 单位；也可以传入 string 类型，比如 2rem 或 5vw 等带有单位的值。

对齐方式  
通过调整 align 的值来设置子元素的对齐方式, 可选值为 start, center ,end ,baseline，在水平模式下的默认值为 center。

自动换行  
在水平模式下, 通过 wrap 属性来控制子元素是否自动换行。

## 内置样式

Vant 中默认包含了一些常用样式，可以直接通过 className 的方式使用。

文字省略
当文本内容长度超过容器最大宽度时，自动省略多余的文本。

```js
<!-- 最多显示一行 -->
<div class="van-ellipsis">这是一段最多显示一行的文字，多余的内容会被省略</div>

<!-- 最多显示两行 -->
<div class="van-multi-ellipsis--l2">
  这是一段最多显示两行的文字，多余的内容会被省略
</div>

<!-- 最多显示三行 -->
<div class="van-multi-ellipsis--l3">
  这是一段最多显示三行的文字，多余的内容会被省略
</div>
```

1px 边框  
为元素添加 Retina 屏幕下的 1px 边框（即 hairline），基于伪类 transform 实现。

```js
<!-- 上边框 -->
<div class="van-hairline--top"></div>

<!-- 下边框 -->
<div class="van-hairline--bottom"></div>

<!-- 左边框 -->
<div class="van-hairline--left"></div>

<!-- 右边框 -->
<div class="van-hairline--right"></div>

<!-- 上下边框 -->
<div class="van-hairline--top-bottom"></div>

<!-- 全边框 -->
<div class="van-hairline--surround"></div>
```

安全区  
为元素添加安全区适配。
```js
<!-- 顶部安全区 -->
<div class="van-safe-area-top"></div>

<!-- 底部安全区 -->
<div class="van-safe-area-bottom"></div>
```

动画  
可以通过 transition 组件使用内置的动画类。

```js
<!-- 淡入 -->
<transition name="van-fade">
  <div v-show="visible">Fade</div>
</transition>

<!-- 上滑进入 -->
<transition name="van-slide-up">
  <div v-show="visible">Slide Up</div>
</transition>

<!-- 下滑进入 -->
<transition name="van-slide-down">
  <div v-show="visible">Slide Down</div>
</transition>

<!-- 左滑进入 -->
<transition name="van-slide-left">
  <div v-show="visible">Slide Left</div>
</transition>

<!-- 右滑进入 -->
<transition name="van-slide-right">
  <div v-show="visible">Slide Right</div>
</transition>
```

## Toast 轻提示

在页面中间弹出黑色半透明提示，用于消息通知、加载提示、操作结果提示等场景。

文字提示

```js
import { showToast } from 'vant';

showToast('提示内容');
```

加载提示
使用 showLoadingToast 方法展示加载提示，通过 forbidClick 选项可以禁用背景点击。

```js
import { showLoadingToast } from 'vant';

showLoadingToast({
  message: '加载中...',
  forbidClick: true,
});
```

成功/失败提示   
使用 showSuccessToast 方法展示成功提示，使用 showFailToast 方法展示失败提示。

```js
import { showSuccessToast, showFailToast } from 'vant';

showSuccessToast('成功文案');
showFailToast('失败文案');
```

自定义图标  
通过 icon 选项可以自定义图标，支持传入图标名称或图片链接，等同于 Icon 组件的 name 属性。

```js
import { showToast } from 'vant';

showToast({
  message: '自定义图标',
  icon: 'like-o',
});

showToast({
  message: '自定义图片',
  icon: 'https://fastly.jsdelivr.net/npm/@vant/assets/logo.png',
});
通过loadingType 属性可以自定义加载图标类型。

import { showLoadingToast } from 'vant';

showLoadingToast({
  message: '加载中...',
  forbidClick: true,
  loadingType: 'spinner',
});
```

自定义位置
Toast 默认渲染在屏幕正中位置，通过 position 属性可以控制 Toast 展示的位置。

```js
import { showToast } from 'vant';

showToast({
  message: '顶部展示',
  position: 'top',
});

showToast({
  message: '底部展示',
  position: 'bottom',
});
文字换行方式
通过 wordBreak 选择可以控制 Toast 中的文字过长时的截断方式，默认值为 break-all，可选值为 break-word 和 normal。

import { showToast } from 'vant';

// 换行时截断单词
showToast({
  message: 'This message will contain a incomprehensibilities long word.',
  wordBreak: 'break-all',
});

// 换行时不截断单词
showToast({
  message: 'This message will contain a incomprehensibilities long word.',
  wordBreak: 'break-word',
});
```
动态更新提示
执行 Toast 方法时会返回对应的 Toast 实例，通过修改实例上的 message 属性可以实现动态更新提示的效果。

```js
import { showLoadingToast, closeToast } from 'vant';

const toast = showLoadingToast({
  duration: 0,
  forbidClick: true,
  message: '倒计时 3 秒',
});

let second = 3;
const timer = setInterval(() => {
  second--;
  if (second) {
    toast.message = `倒计时 ${second} 秒`;
  } else {
    clearInterval(timer);
    closeToast();
  }
}, 1000);
```

单例模式
Toast 默认采用单例模式，即同一时间只会存在一个 Toast，如果需要在同一时间弹出多个 Toast，可以参考下面的示例：

```js
import { showToast, showSuccessToast, allowMultipleToast } from 'vant';

allowMultipleToast();

const toast1 = showToast('第一个 Toast');
const toast2 = showSuccessToast('第二个 Toast');

toast1.close();
toast2.close();
```

修改默认配置
通过 setToastDefaultOptions 函数可以全局修改 showToast 等方法的默认配置。

```js
import { setToastDefaultOptions, resetToastDefaultOptions } from 'vant';

setToastDefaultOptions({ duration: 2000 });

setToastDefaultOptions('loading', { forbidClick: true });

resetToastDefaultOptions();

resetToastDefaultOptions('loading');
```

使用 Toast 组件
如果需要在 Toast 内嵌入组件或其他自定义内容，可以直接使用 Toast 组件，并使用 message 插槽进行定制。使用前需要通过 app.use 等方式注册组件。

```js
<van-toast v-model:show="show" style="padding: 0">
  <template #message>
    <van-image :src="image" width="200" height="140" style="display: block" />
  </template>
</van-toast>
import { ref } from 'vue';

export default {
  setup() {
    const show = ref(false);
    return { show };
  },
};
```

# 表单组件

## Calendar 日历

## Cascader 级联选择

基础用法
级联选择组件可以搭配 Field 和 Popup 组件使用，示例如下：

```js
<van-field
  v-model="fieldValue"
  is-link
  readonly
  label="地区"
  placeholder="请选择所在地区"
  @click="show = true"
/>
<van-popup v-model:show="show" round position="bottom">
  <van-cascader
    v-model="cascaderValue"
    title="请选择所在地区"
    :options="options"
    @close="show = false"
    @finish="onFinish"
  />
</van-popup>
```

## Checkbox 复选框

基础用法
通过 v-model 绑定复选框的勾选状态。

```js
<van-checkbox v-model="checked">复选框</van-checkbox>
import { ref } from 'vue';

export default {
  setup() {
    const checked = ref(true);
    return { checked };
  },
};
```

## DatePicker 日期选择

格式化选项
通过传入 formatter 函数，可以对选项文字进行格式化处理。

```js
<van-date-picker
  v-model="currentDate"
  title="选择年月"
  :min-date="minDate"
  :max-date="maxDate"
  :formatter="formatter"
  :columns-type="columnsType"
/>
```

```js
import { ref } from 'vue';

export default {
  setup() {
    const currentDate = ref(['2021', '01']);
    const columnsType = ['year', 'month'];

    const formatter = (type, option) => {
      if (type === 'year') {
        option.text += '年';
      }
      if (type === 'month') {
        option.text += '月';
      }
      return option;
    };

    return {
      minDate: new Date(2020, 0, 1),
      maxDate: new Date(2025, 5, 1),
      formatter,
      currentDate,
      columnsType,
    };
  },
};
```

## Field 输入框

引入  
通过以下方式来全局注册组件，更多注册方式请参考组件注册。

```js
import { createApp } from 'vue';
import { Field, CellGroup } from 'vant';

const app = createApp();
app.use(Field);
app.use(CellGroup);
```

自定义类型
根据 type 属性定义不同类型的输入框，默认值为 text。

```js
<van-cell-group inset>
  <!-- 输入任意文本 -->
  <van-field v-model="text" label="文本" />
  <!-- 输入手机号，调起手机号键盘 -->
  <van-field v-model="tel" type="tel" label="手机号" />
  <!-- 允许输入正整数，调起纯数字键盘 -->
  <van-field v-model="digit" type="digit" label="整数" />
  <!-- 允许输入数字，调起带符号的纯数字键盘 -->
  <van-field v-model="number" type="number" label="数字" />
  <!-- 输入密码 -->
  <van-field v-model="password" type="password" label="密码" />
</van-cell-group>
import { ref } from 'vue';

export default {
  setup() {
    const tel = ref('');
    const text = ref('');
    const digit = ref('');
    const number = ref('');
    const password = ref('');

    return { tel, text, digit, number, password };
  },
};
```

## Form 表单

引入  
通过以下方式来全局注册组件，更多注册方式请参考组件注册。
```js
import { createApp } from 'vue';
import { Form, Field, CellGroup } from 'vant';

const app = createApp();
app.use(Form);
app.use(Field);
app.use(CellGroup);
```
代码演示  
基础用法  
在表单中，每个 Field 组件 代表一个表单项，使用 Field 的 rules 属性定义校验规则。

```js
<van-form @submit="onSubmit">
  <van-cell-group inset>
    <van-field
      v-model="username"
      name="用户名"
      label="用户名"
      placeholder="用户名"
      :rules="[{ required: true, message: '请填写用户名' }]"
    />
    <van-field
      v-model="password"
      type="password"
      name="密码"
      label="密码"
      placeholder="密码"
      :rules="[{ required: true, message: '请填写密码' }]"
    />
  </van-cell-group>
  <div style="margin: 16px;">
    <van-button round block type="primary" native-type="submit">
      提交
    </van-button>
  </div>
</van-form>
import { ref } from 'vue';

export default {
  setup() {
    const username = ref('');
    const password = ref('');
    const onSubmit = (values) => {
      console.log('submit', values);
    };

    return {
      username,
      password,
      onSubmit,
    };
  },
};
```

校验规则  
通过 rules 定义表单校验规则，所有可用字段见下方表格。

```js
<van-form @failed="onFailed">
  <van-cell-group inset>
    <!-- 通过 pattern 进行正则校验 -->
    <van-field
      v-model="value1"
      name="pattern"
      placeholder="正则校验"
      :rules="[{ pattern, message: '请输入正确内容' }]"
    />
    <!-- 通过 validator 进行函数校验 -->
    <van-field
      v-model="value2"
      name="validator"
      placeholder="函数校验"
      :rules="[{ validator, message: '请输入正确内容' }]"
    />
    <!-- 通过 validator 返回错误提示 -->
    <van-field
      v-model="value3"
      name="validatorMessage"
      placeholder="校验函数返回错误提示"
      :rules="[{ validator: validatorMessage }]"
    />
    <!-- 通过 validator 进行异步函数校验 -->
    <van-field
      v-model="value4"
      name="asyncValidator"
      placeholder="异步函数校验"
      :rules="[{ validator: asyncValidator, message: '请输入正确内容' }]"
    />
  </van-cell-group>
  <div style="margin: 16px;">
    <van-button round block type="primary" native-type="submit">
      提交
    </van-button>
  </div>
</van-form>
import { ref } from 'vue';
import { closeToast, showLoadingToast } from 'vant';

export default {
  setup() {
    const value1 = ref('');
    const value2 = ref('');
    const value3 = ref('abc');
    const value4 = ref('');
    const pattern = /\d{6}/;

    // 校验函数返回 true 表示校验通过，false 表示不通过
    const validator = (val) => /1\d{10}/.test(val);

    // 校验函数可以直接返回一段错误提示
    const validatorMessage = (val) => `${val} 不合法，请重新输入`;

    // 校验函数可以返回 Promise，实现异步校验
    const asyncValidator = (val) =>
      new Promise((resolve) => {
        showLoadingToast('验证中...');

        setTimeout(() => {
          closeToast();
          resolve(val === '1234');
        }, 1000);
      });

    const onFailed = (errorInfo) => {
      console.log('failed', errorInfo);
    };

    return {
      value1,
      value2,
      value3,
      value4,
      pattern,
      onFailed,
      validator,
      asyncValidator,
    };
  },
};
```

## NumberKeyboard 数字键盘

虚拟数字键盘，可以配合密码输入框组件或自定义的输入框组件使用。

## PasswordInput 密码输入框
带网格的输入框组件，可以用于输入密码、短信验证码等场景，通常与数字键盘组件配合使用。

## Picker 选择器
提供多个选项集合供用户选择，支持单列选择、多列选择和级联选择，通常与弹出层组件配合使用。  
基础用法
选项配置    
Picker 组件通过 columns 属性配置选项数据，columns 是一个包含字符串或对象的数组。

顶部栏  
顶部栏包含标题、确认按钮和取消按钮，点击确认按钮触发 confirm 事件，点击取消按钮触发 cancel 事件。
```js
<van-picker
  title="标题"
  :columns="columns"
  @confirm="onConfirm"
  @cancel="onCancel"
  @change="onChange"
/>
import { showToast } from 'vant';

export default {
  setup() {
    const columns = [
      { text: '杭州', value: 'Hangzhou' },
      { text: '宁波', value: 'Ningbo' },
      { text: '温州', value: 'Wenzhou' },
      { text: '绍兴', value: 'Shaoxing' },
      { text: '湖州', value: 'Huzhou' },
    ];
    const onConfirm = ({ selectedValues }) => {
      showToast(`当前值: ${selectedValues.join(',')}`);
    };
    const onChange = ({ selectedValues }) => {
      showToast(`当前值: ${selectedValues.join(',')}`);
    };
    const onCancel = () => showToast('取消');

    return {
      columns,
      onChange,
      onCancel,
      onConfirm,
    };
  },
};
```

## SwipeCell 滑动单元格

可以左右滑动来展示操作按钮的单元格组件

基础用法
SwipeCell 组件提供了 left 和 right 两个插槽，用于定义两侧滑动区域的内容。

```js
<van-swipe-cell>
  <template #left>
    <van-button square type="primary" text="选择" />
  </template>
  <van-cell :border="false" title="单元格" value="内容" />
  <template #right>
    <van-button square type="danger" text="删除" />
    <van-button square type="primary" text="收藏" />
  </template>
</van-swipe-cell>
```
自定义内容
SwipeCell 可以嵌套任意内容，比如嵌套一个商品卡片。
```js
<van-swipe-cell>
  <van-card
    num="2"
    price="2.00"
    desc="描述信息"
    title="商品标题"
    class="goods-card"
    thumb="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
  />
  <template #right>
    <van-button square text="删除" type="danger" class="delete-button" />
  </template>
</van-swipe-cell>

<style>
  .goods-card {
    margin: 0;
    background-color: @white;
  }

  .delete-button {
    height: 100%;
  }
</style>
```

## SubmitBar 提交订单栏

用于展示订单金额与提交订单。

基础用法
```js
<van-submit-bar :price="3050" button-text="提交订单" @submit="onSubmit" />
import { showToast } from 'vant';

export default {
  setup() {
    const onSubmit = () => showToast('点击按钮');
    return {
      onSubmit,
    };
  },
};
```

## Stepper 步进器

步进器由增加按钮、减少按钮和输入框组成，用于在一定范围内输入、调整数字。

基础用法  
通过 v-model 绑定输入值，可以通过 change 事件监听到输入值的变化。

```js
<van-stepper v-model="value" />
```

```js
import { ref } from 'vue';

export default {
  setup() {
    const value = ref(1);
    return { value };
  },
};
```

步长设置  

通过 step 属性设置每次点击增加或减少按钮时变化的值，默认为 1。

```js
<van-stepper v-model="value" step="2" />
```

限制输入范围  
通过 min 和 max 属性限制输入值的范围，默认超出范围后会自动校正最大值或最小值，通过 auto-fixed 可以关闭自动校正。

```js
<van-stepper v-model="value" min="5" max="8" />
```

限制输入整数  
设置 integer 属性后，输入框将限制只能输入整数。

```js
<van-stepper v-model="value" integer />
```
## Tab 标签页

选项卡组件，用于在不同的内容区域之间进行切换。
基础用法  
通过 v-model:active 绑定当前激活标签对应的索引值，默认情况下启用第一个标签。

```js
<van-tabs v-model:active="active">
  <van-tab title="标签 1">内容 1</van-tab>
  <van-tab title="标签 2">内容 2</van-tab>
  <van-tab title="标签 3">内容 3</van-tab>
  <van-tab title="标签 4">内容 4</van-tab>
</van-tabs>
```

```js
import { ref } from 'vue';

export default {
  setup() {
    const active = ref(0);
    return { active };
  },
};
```

通过名称匹配  
在标签指定 name 属性的情况下，v-model:active 的值为当前标签的 name（此时无法通过索引值来匹配标签）。

```js
<van-tabs v-model:active="activeName">
  <van-tab title="标签 1" name="a">内容 1</van-tab>
  <van-tab title="标签 2" name="b">内容 2</van-tab>
  <van-tab title="标签 3" name="c">内容 3</van-tab>
</van-tabs>
```

```js
import { ref } from 'vue';

export default {
  setup() {
    const activeName = ref('a');
    return { activeName };
  },
};
```

## PullRefresh 下拉刷新

用于提供下拉刷新的交互操作。

下拉刷新时会触发 refresh 事件，在事件的回调函数中可以进行同步或异步操作，操作完成后将 v-model 设置为 false，表示加载完成。
```js
<van-pull-refresh v-model="loading" @refresh="onRefresh">
  <p>刷新次数: {{ count }}</p>
</van-pull-refresh>
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
  setup() {
    const count = ref(0);
    const loading = ref(false);
    const onRefresh = () => {
      setTimeout(() => {
        showToast('刷新成功');
        loading.value = false;
        count.value++;
      }, 1000);
    };

    return {
      count,
      loading,
      onRefresh,
    };
  },
};
```