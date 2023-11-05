# axios笔记📝

## 简介

axios 是一个基于Promise 用于浏览器和 nodejs 的 HTTP 客户端，它本身具有以下特征：

* 🚀从浏览器中创建 XMLHttpRequest  
* 🚀从 node.js 发出 http 请求  
* 🚀支持 Promise API  
* 🚀拦截请求和响应  
* 🚀转换请求和响应数据  
* 🚀取消请求  
* 🚀自动转换JSON数据  

## 执行get请求

```js
// 向具有指定ID的用户发出请求
axios.get('/user?ID=12345')
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
// 也可以通过 params 对象传递参数
axios.get('/user', {
    params: {
      ID: 12345
    }
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
```

## 执行post请求

```js
axios.post('/user', {
    firstName: 'Fred',
    lastName: 'Flintstone'
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
```

## 执行多个并发请求

```js
function getUserAccount() {
  return axios.get('/user/12345');
}
function getUserPermissions() {
  return axios.get('/user/12345/permissions');
}
axios.all([getUserAccount(), getUserPermissions()])
  .then(axios.spread(function (acct, perms) {
    //两个请求现已完成
  }));
```

## axios api

可以通过将相关配置传递给axios来进行请求

1. axios(config)

   ```js
    // 发送一个 POST 请求
    axios({
    method: 'post',
    url: '/user/12345',
    data: {
        firstName: 'Fred',
        lastName: 'Flintstone'
    }
    });
   ```

2. axios(url[, config])

   ```js
   // 发送一个 GET 请求 (GET请求是默认请求模式)
    axios('/user/12345');
   ```

3. 请求方法别名
axios.request（config）  
axios.get（url [，config]）  
axios.delete（url [，config]）  
axios.head（url [，config]）  
axios.post（url [，data [，config]]）  
axios.put（url [，data [，config]]）  
注意：当使用别名方法时，不需要在config中指定url，method和data属性。

4. 并发
帮助函数处理并发请求。  
axios.all（iterable）  
axios.spread（callback）

5. 创建实例
   您可以使用自定义配置创建axios的新实例。  

    ```js
    axios.create（[config]）

    var instance = axios.create({
      baseURL: 'https://some-domain.com/api/',
      timeout: 1000,
      headers: {'X-Custom-Header': 'foobar'}
    });
    ```

6. 实例方法
可用的实例方法如下所示。 指定的配置将与实例配置合并。  
axios＃request（config）  
axios＃get（url [，config]）  
axios＃delete（url [，config]）  
axios＃head（url [，config]）  
axios＃post（url [，data [，config]]）  
axios＃put（url [，data [，config]]）  
axios＃patch（url [，data [，config]]）  

7. 请求配置  
   这些是用于发出请求的可用配置选项。 只有url是必需的。 如果未指定方法，请求将默认为GET。

  ```js
  {
    // `url`是将用于请求的服务器URL
    url: '/user',

    // `method`是发出请求时使用的请求方法

    // `baseURL`将被添加到`url`前面，除非`url`是绝对的。
    // 可以方便地为 axios 的实例设置`baseURL`，以便将相对 URL 传递给该实例的方法。
    baseURL: 'https://some-domain.com/api/',

    // `transformRequest`允许在请求数据发送到服务器之前对其进行更改
    // 这只适用于请求方法'PUT'，'POST'和'PATCH'

    transformRequest: [function (data) {
      // 做任何你想要的数据转换
      return data;
    }],

    // `transformResponse`允许在 then / catch之前对响应数据进行更改
    transformResponse: [function (data) {
      // Do whatever you want to transform the data
      return data;
    }],

    // `headers`是要发送的自定义 headers
    headers: {'X-Requested-With': 'XMLHttpRequest'},

    // `params`是要与请求一起发送的URL参数
    // 必须是纯对象或URLSearchParams对象
    params: {
      ID: 12345

    // `paramsSerializer`是一个可选的函数，负责序列化`params`
    // (e.g. https://www.npmjs.com/package/qs, http://api.jquery.com/jquery.param/)
    paramsSerializer: function(params) {
      return Qs.stringify(params, {arrayFormat: 'brackets'})
    },

    // `data`是要作为请求主体发送的数据
    // 仅适用于请求方法“PUT”，“POST”和“PATCH”
    // 当没有设置`transformRequest`时，必须是以下类型之一：
    // - string, plain object, ArrayBuffer, ArrayBufferView, URLSearchParams
    // - Browser only: FormData, File, Blob
    // - Node only: Stream
    data: {
      firstName: 'Fred'
    },

    // `timeout`指定请求超时之前的毫秒数。
    // 如果请求的时间超过'timeout'，请求将被中止。
    timeout: 1000,

    // `withCredentials`指示是否跨站点访问控制请求
    // should be made using credentials
    withCredentials: false, // default

    // `adapter'允许自定义处理请求，这使得测试更容易。
    // 返回一个promise并提供一个有效的响应（参见[response docs]（＃response-api））
    adapter: function (config) {
      /* ... */
    },

    // `auth'表示应该使用 HTTP 基本认证，并提供凭据。
    // 这将设置一个`Authorization'头，覆盖任何现有的`Authorization'自定义头，使用`headers`设置。
    auth: {
      username: 'janedoe',
      password: 's00pers3cret'
    },

    // “responseType”表示服务器将响应的数据类型
    // 包括 'arraybuffer', 'blob', 'document', 'json', 'text', 'stream'
    responseType: 'json', // default

    //`xsrfCookieName`是要用作 xsrf 令牌的值的cookie的名称
    xsrfCookieName: 'XSRF-TOKEN', // default

    // `xsrfHeaderName`是携带xsrf令牌值的http头的名称
    xsrfHeaderName: 'X-XSRF-TOKEN', // default

    // `onUploadProgress`允许处理上传的进度事件
    onUploadProgress: function (progressEvent) {
      // 使用本地 progress 事件做任何你想要做的
    },

    // `onDownloadProgress`允许处理下载的进度事件
    onDownloadProgress: function (progressEvent) {
      // Do whatever you want with the native progress event
    },

    // `maxContentLength`定义允许的http响应内容的最大大小
    maxContentLength: 2000,

    // `validateStatus`定义是否解析或拒绝给定的promise
    // HTTP响应状态码。如果`validateStatus`返回`true`（或被设置为`null` promise将被解析;否则，promise将被
    // 拒绝。
    validateStatus: function (status) {
      return status >= 200 && status < 300; // default
    },

    // `maxRedirects`定义在node.js中要遵循的重定向的最大数量。
    // 如果设置为0，则不会遵循重定向。
    maxRedirects: 5, // 默认

    // `httpAgent`和`httpsAgent`用于定义在node.js中分别执行http和https请求时使用的自定义代理。
    // 允许配置类似`keepAlive`的选项，
    // 默认情况下不启用。
    httpAgent: new http.Agent({ keepAlive: true }),
    httpsAgent: new https.Agent({ keepAlive: true }),

    // 'proxy'定义代理服务器的主机名和端口
    // `auth`表示HTTP Basic auth应该用于连接到代理，并提供credentials。
    // 这将设置一个`Proxy-Authorization` header，覆盖任何使用`headers`设置的现有的`Proxy-Authorization` 自定义 headers。
    proxy: {
      host: '127.0.0.1',
      port: 9000,
      auth: : {
        username: 'mikeymike',
        password: 'rapunz3l'
      }
    },

    // “cancelToken”指定可用于取消请求的取消令牌
    // (see Cancellation section below for details)
    cancelToken: new CancelToken(function (cancel) {
    })
  }
  ```

## 配置默认值

可以指定将应用于每个请求的配置默认值

1. 全局axios默认值  

    ```js
      axios.defaults.baseURL = 'https://api.example.com';
      axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
      axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'; 
    ```

2. 自定义实例默认值

   ```js
      //在创建实例时设置配置默认值
    var instance = axios.create（{
      baseURL：'https://api.example.com'
    }）;

    //在实例创建后改变默认值
    instance.defaults.headers.common ['Authorization'] = AUTH_TOKEN;
   ```

3. 配置优先级顺序

   ```js
        //使用库提供的配置默认值创建实例
    //此时，超时配置值为`0`，这是库的默认值
    var instance = axios.create（）;

    //覆盖库的超时默认值
    //现在所有请求将在超时前等待2.5秒
    instance.defaults.timeout = 2500;

    //覆盖此请求的超时，因为它知道需要很长时间
    instance.get（'/ longRequest'，{
      timeout：5000
    }）;
   ```

## 拦截器

你可以截取请求或响应在被 then 或者 catch 处理之前

  ```js
  //添加请求拦截器
  axios.interceptors.request.use（function（config）{
      //在发送请求之前做某事
      return config;
    }，function（error）{
      //请求错误时做些事
      return Promise.reject（error）;
    }）;

  //添加响应拦截器
  axios.interceptors.response.use（function（response）{
      //对响应数据做些事
        return response;
    }，function（error）{
      //请求错误时做些事
      return Promise.reject（error）;
    }）;
  ```

如果你以后可能需要删除拦截器。

```js
var myInterceptor = axios.interceptors.request.use(function () {/*...*/});
axios.interceptors.request.eject(myInterceptor);
 ```

你可以将拦截器添加到axios的自定义实例。

```js
var instance = axios.create();
instance.interceptors.request.use(function () {/*...*/});
```

1. 处理错误

      ```js
    axios.get（'/ user / 12345'）
      .catch（function（error）{
        if（error.response）{
          //请求已发出，但服务器使用状态代码进行响应
          //落在2xx的范围之外
          console.log（error.response.data）;
          console.log（error.response.status）;
          console.log（error.response.headers）;
        } else {
          //在设置触发错误的请求时发生了错误
          console.log（'Error'，error.message）;
        }}
        console.log（error.config）;
      }）;
    ```

您可以使用validateStatus配置选项定义自定义HTTP状态码错误范围。

```js
axios.get（'/ user / 12345'，{
   validateStatus：function（status）{
     return status < 500; //仅当状态代码大于或等于500时拒绝
   }}
}）
 ```

1. 消除
您可以使用取消令牌取消请求。

axios cancel token API基于可取消的promise提议，目前处于阶段1。

您可以使用CancelToken.source工厂创建一个取消令牌，如下所示：

```js
var CancelToken = axios.CancelToken;
var source = CancelToken.source（）;
axios.get('/user/12345', {
  cancelToken: source.token
}).catch(function(thrown) {
  if (axios.isCancel(thrown)) {
    console.log('Request canceled', thrown.message);
  } else {
    // 处理错误
  }
});
//取消请求（消息参数是可选的）
source.cancel（'操作被用户取消。'）;
```

您还可以通过将执行器函数传递给CancelToken构造函数来创建取消令牌：

```js
var CancelToken = axios.CancelToken;
var cancel;

axios.get（'/ user / 12345'，{
   cancelToken：new CancelToken（function executor（c）{
     //一个执行器函数接收一个取消函数作为参数
     cancel = c;
   }）
}）;

// 取消请求
clear();
```

注意：您可以使用相同的取消令牌取消几个请求。  

使用application / x-www-form-urlencoded格式
默认情况下，axios将JavaScript对象序列化为JSON。 要以应用程序/ x-www-form-urlencoded格式发送数据，您可以使用以下选项之一。

(1) 浏览器
在浏览器中，您可以使用URLSearchParams API，如下所示：

var params = new URLSearchParams();
params.append('param1', 'value1');
params.append('param2', 'value2');
axios.post('/foo', params);

请注意，所有浏览器都不支持URLSearchParams，但是有一个polyfill可用（确保polyfill全局环境）。

或者，您可以使用qs库对数据进行编码：

var qs = require('qs');
axios.post('/foo', qs.stringify({ 'bar': 123 });

(2) Node.js
在node.js中，可以使用querystring模块，如下所示：

var querystring = require('querystring');
axios.post('http://something.com/', querystring.stringify({ foo: 'bar' });

你也可以使用qs库。

1.  Promise
axios 依赖本机要支持ES6 Promise实现。 如果您的环境不支持ES6 Promises，您可以使用polyfill。

1.  TypeScript
axios包括TypeScript定义。

import axios from 'axios';
axios.get('/user?ID=12345');

axios在很大程度上受到Angular提供的http-like服务。
