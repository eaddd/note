```mermaid
sequenceDiagram
    participant 老板A
    participant 员工A

    老板A ->> + 员工A : “在这里我们都是兄弟！”
    老板A -x + 员工A : 画个饼
    员工A -->> - 老板A : 鼓掌
```

>消息语句格式为：<参与者> <箭头> <参与者> : <描述文本>。
>其中 <箭头>的写法有：
> ->> 显示为实线箭头（主动发出消息）
> -->>显示为虚线箭头（响应）
> -x显示为末尾带「X」的实线箭头（异步消息）


```mermaid
sequenceDiagram
    老板B ->> + 员工B : “你们要669！”
    员工B -->> - 老板B : 鼓掌
    
    老板B ->> + 员工B : “悔创本司！”
    员工B -->> - 老板B : 鼓掌
```

```mermaid
sequenceDiagram
    Note left of 老板A : 对脸不感兴趣
    Note right of 老板B : 对钱不感兴趣
    Note over 老板A,老板B : 对996感兴趣
```

```mermaid
sequenceDiagram
    网友 ->> + X宝 : 网购钟意的商品
    X宝 -->> - 网友 : 下单成功
    
    loop 一天七次
        网友 ->> + X宝 : 查看配送进度
        X宝 -->> - 网友 : 配送中
    end
```

```mermaid
sequenceDiagram    
    土豪 ->> 取款机 : 查询余额
    取款机 -->> 土豪 : 余额
    
    alt 余额 > 5000
        土豪 ->> 取款机 : 取上限值 5000 块
    else 5000 < 余额 < 100
        土豪 ->> 取款机 : 有多少取多少
    else 余额 < 100
        土豪 ->> 取款机 : 退卡
    end
    
    取款机 -->> 土豪 : 退卡
```

```mermaid
sequenceDiagram
    老板C ->> 员工C : 开始实行996
    
    opt 永不可能
        员工C -->> 老板C : 拒绝
    end
```

```mermaid
sequenceDiagram
    老板C ->> 员工C : 开始实行996
    
    par 并行
        员工C ->> 员工C : 刷微博
    and
        员工C ->> 员工C : 工作
    and
        员工C ->> 员工C : 刷朋友圈
    end
    
    员工C -->> 老板C : 9点下班
```

[链接文字](http://www.kancloud.cn)

看云是一个文档写作[^write]和托管平台[^platform]。
[^write]: 写作格式采用Markdown格式，支持版本和多人写作。

[^platform]: 发布的文档可以直接在平台阅读、分享和私有存储，并支持付费阅读。

单行代码 `define('APP_DEBUG',      false);`






多行代码：
```
// 系统常量定义
defined('THINK_PATH')   or define('THINK_PATH',     __DIR__.'/');
defined('APP_PATH')     or define('APP_PATH',       dirname($_SERVER['SCRIPT_FILENAME']).'/');
defined('APP_STATUS')   or define('APP_STATUS',     ''); // 应用状态 加载对应的配置文件
defined('APP_DEBUG')    or define('APP_DEBUG',      false); // 是否调试模式
```

> 这是一段引用内容文字  
> 这是第二行引用内容文字  
> 这是第三行引用内容文字 

>[info] 这里是**提示信息**
>通常用于一些提醒事项

>[warning] 这里是**警告信息**
>通常用于一些警告事项

>[danger] 这里是**危险信息**
>需要引起特别的注意

| 编号 | 产品 | 描述 |
|---|---|---|
| 1 | ThinkPHP  | 开源WEB应用框架  | 
| 2 | OneThink  | 开源内容管理框架   | 
| 3 | 看云  | 文档托管平台   |

```mermaid
graph LR;
A --> B
B --> C
A --> C
```
