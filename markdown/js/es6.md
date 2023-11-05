# es6学习笔记

## ES6 let 与 const

### let命令

1. 基本用法  
声明变量，用法类似于var 但是声明的变量只在let命令所在的代码块内有效

   * 不存在变量提升， 跟var比较，var命令发生变量提升，即变量可以在声明之前使用，值为undefined.let命令改变了语法行为，所声明的变量一定要在声明后使用，否则报错
   * 暂时性死区 在声明之前使用变量都是不可用的，运行时就会抛出一个ReferenceError
   * 不允许重复声明

2. 块级作用域

   * 没有块级作用域，内层变量可能会覆盖外层变量
   * 用来计数的循环变量泄露为全局变量

### const命令

const声明一个只读的常量。一旦声明，常量的值就不能改变。本质 const实际上保证的，并不是变量的值不得改动，而是变量指向的那个内存地址所保存的数据不得改动。对于简单类型的数据（数值、字符串、布尔值），值就保存在变量指向的那个内存地址，因此等同于常量。但对于复合类型的数据（主要是对象和数组），变量指向的内存地址，保存的只是一个指向实际数据的指针，const只能保证这个指针是固定的（即总是指向另一个固定的地址），至于它指向的数据结构是不是可变的，就完全不能控制了。因此，将一个对象声明为常量必须非常小心.真的想将对象冻结，应该使用Object.freeze方法

### 顶层对象的属性

顶层对象在浏览器环境指的是window对象，在node指的是global对象，es5中，顶层对象的属性与全局变量是等价的。es6中全局变量a由var命令声明，所以它是顶层对象的属性；全局变量b由let命令声明，所以它不是顶层对象的属性，返回undefined。

### globalThis对象

## 解构赋值

1. 数组的解构赋值

   * 基本用法
  
   ```js
   let [a, b, c] = [1, 2, 3];
   ```

   ES6 允许按照一定模式，从数组和对象中提取值，对变量进行赋值，这被称为解构（Destructuring）。本质上，这种写法属于“模式匹配”，只要等号两边的模式相同，左边的变量就会被赋予对应的值。  
   另一种情况是不完全解构，即等号左边的模式，只匹配一部分的等号右边的数组。这种情况下，解构依然可以成功。

   ```js
   let [a, [b], d] = [1, [2, 3], 4];
    a // 1
    b // 2
    d // 4
   ```

    * 默认值

   解构赋值允许指定默认值。注意，es6内部使用严格相等运算符（===），判断一个位置是否有值。所以只有当一个数组成员严格等于undefined，默认值才会生效

   ```js
    let [x = 1, y = x] = [];     // x=1; y=1
    let [x = 1, y = x] = [2];    // x=2; y=2
    let [x = 1, y = x] = [1, 2]; // x=1; y=2
    let [x = y, y = 1] = [];     // ReferenceError: y is not defined
   ```

2. 对象的解构赋值

    * 基本用法
  
    对象的属性没有次序，变量必须与属性同名，才能取到正确的值

    ```js
    let { bar, foo } = { foo: 'aaa', bar: 'bbb' };
    foo // "aaa"
    bar // "bbb"
    let { baz } = { foo: 'aaa', bar: 'bbb' };
    baz // undefined

    // 例一
    let { log, sin, cos } = Math;
    // 例二
    const { log } = console;
    log('hello') // hello
    ```

    如果变量名与属性名不一致，必须写成下面这样。

    ```js
    let { foo: baz } = { foo: 'aaa', bar: 'bbb' };
    baz // "aaa"
    let obj = { first: 'hello', last: 'world' };
    let { first: f, last: l } = obj;
    f // 'hello'
    l // 'world'
    ```

    这实际上说明，对象的解构赋值是下面形式的简写（参见《对象的扩展》一章）。也就是说，对象的解构赋值的内部机制，是先找到同名属性，然后再赋给对应的变量。真正被赋值的是后者，而不是前者。

    解构也可以用于嵌套结构的对象。

    ```js
    let obj = {
        p: [
            'Hello',
            { y: 'World' }
        ]
    };
    let { p, p: [x, { y }] } = obj;
    x // "Hello"
    y // "World"
    p // ["Hello", {y: "World"}]

    let obj = {};
    let arr = [];
    ({ foo: obj.prop, bar: arr[0] } = { foo: 123, bar: true });
    obj // {prop:123}
    arr // [true]
    ```

    注意，对象的解构赋值可以取到继承的属性。

    ```js
    const obj1 = {};
    const obj2 = { foo: 'bar' };
    Object.setPrototypeOf(obj1, obj2);
    const { foo } = obj1;
    foo // "bar"
    ```

    上面代码中，对象obj1的原型对象是obj2。foo属性不是obj1自身的属性，而是继承自obj2的属性，解构赋值可以取到这个属性。

    * 默认值

    对象的解构也可以指定默认值。

    ```js
    var {x = 3} = {};
    x // 3
    var {x, y = 5} = {x: 1};
    x // 1
    y // 5
    var {x: y = 3} = {};
    y // 3
    var {x: y = 3} = {x: 5};
    y // 5
    var { message: msg = 'Something went wrong' } = {};
    msg // "Something went wrong"
    ```

    默认值生效的条件对象的属性值严格等于undefined  
    **注意点**

    * 要将一个已经声明的变量用于解构赋值，必须非常小心。
  
    ```js
     // 错误的写法
    let x;
    {x} = {x: 1};
    // SyntaxError: syntax error
    ```

    上面代码的写法会报错，因为 JavaScript 引擎会将{x}理解成一个代码块，从而发生语法错误。只有不将大括号写在行首，避免 JavaScript 将其解释为代码块，才能解决这个问题。

    ```js
    // 正确的写法
    let x;
    ({x} = {x: 1});
    ```

    上面代码将整个解构赋值语句，放在一个圆括号里面，就可以正确执行。关于圆括号与解构赋值的关系，参见下文。

    * 由于数组本质是特殊的对象，因此可以对数组进行对象属性的解构。
  
    ```js
    let arr = [1, 2, 3];
    let {0 : first, [arr.length - 1] : last} = arr;
    first // 1
    last // 3
    ```

    上面代码对数组进行对象解构。数组arr的0键对应的值是1，[arr.length - 1]就是2键，对应的值是3。方括号这种写法，属于“属性名表达式”（参见《对象的扩展》一章）。

3. 字符串的解构赋值

   ```js
    const [a, b, c, d, e] = 'hello';
    a // "h"
    b // "e"
    c // "l"
    d // "l"
    e // "o"

    let {length : len} = 'hello';
    len // 5
   ```

4. 数值和布尔值的解构赋值

5. 函数参数的解构赋值

   函数的参数也可以使用解构赋值。

   ```js
   function add([x, y]){
    return x + y;
    }
    add([1, 2]); // 3
   ```

   函数参数的解构也可以使用默认值。

   ```js
   function move({x = 0, y = 0} = {}) {
    return [x, y];
    }
    move({x: 3, y: 8}); // [3, 8]
    move({x: 3}); // [3, 0]
    move({}); // [0, 0]
    move(); // [0, 0]
   ```

6. 用途

    * 交换变量的值
  
    ```js
    let x = 1;
    let y = 2;
    [x, y] = [y, x];
    ```

    * 从函数返回多个值

    函数只能返回一个值，如果要返回多个值，只能将它们放在数组或对象里返回。有了解构赋值，取出这些值就非常方便。

    ```js
    // 返回一个数组
    function example() {
    return [1, 2, 3];
    }
    let [a, b, c] = example();
    // 返回一个对象
    function example() {
    return {
        foo: 1,
        bar: 2
    };
    }
    let { foo, bar } = example();
    ```

    * 函数参数的定义

    解构赋值可以方便地将一组参数与变量名对应起来。

    ```js
    // 参数是一组有次序的值
    function f([x, y, z]) { ... }
    f([1, 2, 3]);
    // 参数是一组无次序的值
    function f({x, y, z}) { ... }
    f({z: 3, y: 2, x: 1});
    ```

    * 提取 JSON 数据
  
    解构赋值对提取 JSON对象中的数据，尤其有用。

    ```js
    let jsonData = {
    id: 42,
    status: "OK",
    data: [867, 5309]
    };
    let { id, status, data: number } = jsonData;
    console.log(id, status, number);
    // 42, "OK", [867, 5309]
    ```

    * 函数参数的默认值

    ```js
    jQuery.ajax = function (url, {
    async = true,
    beforeSend = function () {},
    cache = true,
    complete = function () {},
    crossDomain = false,
    global = true,
    // ... more config
    } = {}) {
    // ... do stuff
    };
    ```

    * 遍历 Map 结构
  
    ```js
    const map = new Map();
    map.set('first', 'hello');
    map.set('second', 'world');
    for (let [key, value] of map) {
    console.log(key + " is " + value);
    }
    // first is hello
    // second is world
        // 获取键名
    for (let [key] of map) {
    // ...
    }
    // 获取键值
    for (let [,value] of map) {
    // ...
    }
    ```

    * 输入模块的指定方法

    ```js
    const { SourceMapConsumer, SourceNode } = require("source-map");
    ```

## ES6 字符串的扩展

1. 字符的 Unicode 表示法

    ES6 加强了对 Unicode 的支持，允许采用 \uxxxx 形式表示一个字符，其中 xxxx 表示字符的 Unicode 码点。但是，这种表示法只限于码点在 \u0000 ~ \uFFFF 之间的字符。超出这个范围的字符，必须用两个双字节的形式表示。ES6 对这一点做出了改进，只要将码点放入大括号，就能正确解读该字符。

    ```js
    "\u{20BB7}"
    // "????"
    "\u{41}\u{42}\u{43}"
    // "ABC"
    let hello = 123;
    hell\u{6F} // 123
    '\u{1F680}' === '\uD83D\uDE80'
    // true
    ```

2. 字符串的遍历器接口

   ES6 为字符串添加了遍历器接口（详见《Iterator》一章），使得字符串可以被 for...of 循环遍历。

3. 模版字符串

    板字符串（template string）是增强版的字符串，用反引号`` 标识。它可以当作普通字符串使用，也可以用来定义多行字符串，或者在字符串中嵌入变量。

    ```js
    // 普通字符串
    `In JavaScript '\n' is a line-feed.`
    // 多行字符串
    `In JavaScript this is
    not legal.`
    console.log(`string text line 1
    string text line 2`);
    // 字符串中嵌入变量
    var name = "Bob", time = "today";
    `Hello ${name}, how are you ${time}?
    ```

    模板字符串中嵌入变量，需要将变量名写在 ${} 之中。模板字符串之中还能调用函数。${fn()}

4. 标签模版

   紧跟在一个函数后面，该函数将被用来处理这个模版字符串

   ```js
   alert`123`
    // 等同于
    alert(123)
   ```

## ES6 正则的扩展

1. RegExp 构造函数

    egExp 构造函数的参数有两种情况。  
    第一种情况是，参数是字符串，这时第二个参数表示正则表达式的修饰符（flag）。  
    第二种情况是，参数是一个正则表示式，这时会返回一个原有正则表达式的拷贝。

2. 字符串的正则方法

    字符串对象共有 4 个方法，可以使用正则表达式： match() 、 replace() 、 search() 和 split() 。

3. u 修饰符 unicode模式
4. y 修饰符

    ES6 还为正则表达式添加了 y 修饰符，叫做“粘连”（sticky）修饰符 y 修饰符确保匹配必须从剩余的第一个位置开始，这也就是“粘连”的涵义。

## 数值的扩展

1. 二进制和八进制表示法 提供了二进制和八进制数值的新的写法，分别用前缀 0b （或 0B ）和 0o （或 0O ）表示。
2. Number.isFinite(), Number.isNaN()
3. Number.parseInt(), Number.parseFloat()
4. Number.isInteger()
5. Number.EPSILON ES6 在 Number 对象上面，新增一个极小的常量Number.EPSILON。根据规格，它表示 1 与大于 1 的最小浮点数之间的差。Number.EPSILON 可以用来设置“能够接受的误差范围”。比如，误差范围设为 2 的-50 次方（即 Number.EPSILON * Math.pow(2, 2) ），即如果两个浮点数的差小于这个值，我们就认为这两个浮点数相等。

## ES6 函数的扩展

1. 基本用法

   * 函数参数指定默认值，参数默认值是惰性求值的。

2. rest参数  
    ES6 引入rest 参数（形式为 ...变量名 ），用于获取函数的多余参数，这样就不需要使用 arguments 对象了。rest 参数搭配的变量是一个数组，该变量将多余的参数放入数组中。

    ```js
    function add(...values) {
    let sum = 0;
    for (var val of values) {
        sum += val;
    }
    return sum;
    }
    add(2, 5, 3) // 10
    ```

    rest参数就是一个真正的数组，数组特有的方法都可以使用

3. 严格模式

   ES2016做了一点修改，规定只要函数参数使用了默认值、解构赋值、或者扩展运算符，那么函数内部就不能显式设定为严格模式，否则会报错。
   两种方法可以规避这种限制。第一种是设定全局性的严格模式，这是合法的。

   ```js
   'use strict';
    function doSomething(a, b = a) {
    // code
    }
   ```

   第二种是把函数包在一个无参数的立即执行函数里面。

   ```js
   const doSomething = (function () {
    'use strict';
        return function(value = 42) {
            return value;
        };
    }());
   ```

4. name属性
5. 箭头函数

    ES6允许使用“箭头”（ => ）定义函数。
    箭头函数有几个使用注意点。

    （1）函数体内的 this对象，就是定义时所在的对象，而不是使用时所在的对象。

    ```js
    function Timer() {
    this.s1 = 0;
    this.s2 = 0;
    // 箭头函数
    setInterval(() => this.s1++, 1000);
    // 普通函数
    setInterval(function () {
        this.s2++;
    }, 1000);
    }
    var timer = new Timer();
    setTimeout(() => console.log('s1: ', timer.s1), 3100);
    setTimeout(() => console.log('s2: ', timer.s2), 3100);
    // s1: 3
    // s2: 0
    ```

    （2）不可以当作构造函数，也就是说，不可以使用 new 命令，否则会抛出一个错误。

    （3）不可以使用arguments对象，该对象在函数体内不存在。如果要用，可以用 rest 参数代替。

    （4）不可以使用 yield命令，因此箭头函数不能用作 Generator 函数。

    **不适用的场合**    
    第一个场合是定义对象的方法，且该方法内部包括this。  

    ```js
    const cat = {
    lives: 9,
    jumps: () => {
        this.lives--;
    }
    }
    ```

    cat.jumps() 方法是一个箭头函数，这是错误的。调用 cat.jumps() 时，如果是普通函数，该方法内部的 this 指向 cat ；如果写成上面那样的箭头函数，使得 this 指向全局对象，因此不会得到预期结果。这是因为对象不构成单独的作用域，导致 jumps 箭头函数定义时的作用域就是全局作用域。

    第二个场合是需要动态 this 的时候，也不应使用箭头函数。

    ```js
    var button = document.getElementById('press');
    button.addEventListener('click', () => {
    this.classList.toggle('on');
    });
    ```

    上面代码运行时，点击按钮会报错，因为 button 的监听函数是一个箭头函数，导致里面的 this 就是全局对象。如果改成普通函数， this 就会动态指向被点击的按钮对象。

6. 微调用优化

    尾调用（Tail Call）是函数式编程的一个重要概念，本身非常简单，一句话就能说清楚，就是指某个函数的最后一步是调用另一个函数。调用之所以与其他调用不同，就在于它的特殊的调用位置。

    我们知道，函数调用会在内存形成一个“调用记录”，又称“调用帧”（call frame），保存调用位置和内部变量等信息。如果在函数 A 的内部调用函数 B ，那么在 A 的调用帧上方，还会形成一个 B 的调用帧。等到 B 运行结束，将结果返回到 A ， B 的调用帧才会消失。如果函数 B 内部还调用函数 C ，那就还有一个 C 的调用帧，以此类推。所有的调用帧，就形成一个“调用栈”（call stack）。

    尾调用由于是函数的最后一步操作，所以不需要保留外层函数的调用帧，因为调用位置、内部变量等信息都不会再用到了，只要直接用内层函数的调用帧，取代外层函数的调用帧就可以了。注意，只有不再用到外层函数的内部变量，内层函数的调用帧才会取代外层函数的调用帧，否则就无法进行“尾调用优化”。

7. 尾递归

    函数调用自身，称为递归。如果尾调用自身，就称为尾递归。
    递归非常耗费内存，因为需要同时保存成千上百个调用帧，很容易发生“栈溢出”错误（stack overflow）。但对于尾递归来说，由于只存在一个调用帧，所以永远不会发生“栈溢出”错误。

    ES6 的尾调用优化只在严格模式下开启，正常模式是无效的。

    **尾递归优化的实现**

    蹦床函数（trampoline）可以将递归执行转为循环执行。

    ```js
    function trampoline(f) {
        while (f && f instanceof Function) {
            f = f();
        }
        return f;
    }
    ```

    上面就是蹦床函数的一个实现，它接受一个函数 f 作为参数。只要 f 执行后返回一个函数，就继续执行。注意，这里是返回一个函数，然后执行该函数，而不是函数里面调用函数，这样就避免了递归执行，从而就消除了调用栈过大的问题。

    然后，要做的就是将原来的递归函数，改写为每一步返回另一个函数。

    ```js
    function sum(x, y) {
    if (y > 0) {
        return sum.bind(null, x + 1, y - 1);
    } else {
        return x;
    }
    }
    ```
    上面代码中， sum 函数的每次执行，都会返回自身的另一个版本。

    现在，使用蹦床函数执行 sum ，就不会发生调用栈溢出。

## 数组的扩展

1. 扩展运算符（spread）  
   是三个点（ ... ）。它好比 rest 参数的逆运算，将一个数组转为用逗号分隔的参数序列。
   可以替代函数的 apply 方法

   ```js
   // ES5 的写法
   function f(x, y, z) {
     // ...
   }
   var args = [0, 1, 2];
   f.apply(null, args);
   // ES6的写法
   function f(x, y, z) {
     // ...
   }
   let args = [0, 1, 2];
   f(...args);
   ```

   扩展运算符的应用  
   (1). 复制数组

   ES5 只能用变通方法来复制数组。

   ```js
   const a1 = [1, 2];
   const a2 = a1.concat();
   a2[0] = 2;
   a1 // [1, 2]
   ```

   上面代码中， a1 会返回原数组的克隆，再修改 a2 就不会对 a1 产生影响。
   es6:

   ```js
   const a1 = [1, 2];
   // 写法一
   const a2 = [...a1];
   // 写法二
   const [...a2] = a1;
   ```

   (2). 合并数组

   扩展运算符提供了数组合并的新写法。

   ```js
   const arr1 = ['a', 'b'];
   const arr2 = ['c'];
   const arr3 = ['d', 'e'];
   // ES5 的合并数组
   arr1.concat(arr2, arr3);
   // [ 'a', 'b', 'c', 'd', 'e' ]
   // ES6 的合并数组
   [...arr1, ...arr2, ...arr3]
   // [ 'a', 'b', 'c', 'd', 'e' ]
   ```

   不过，这两种方法都是浅拷贝，使用的时候需要注意。

   ```js
   const a1 = [{ foo: 1 }];
   const a2 = [{ bar: 2 }];
   const a3 = a1.concat(a2);
   const a4 = [...a1, ...a2];
   a3[0] === a1[0] // true
   a4[0] === a1[0] // true
   ```

   上面代码中， a3 和 a4 是用两种不同方法合并而成的新数组，但是它们的成员都是对原数组成员的引用，这就是浅拷贝。如果修改了引用指向的值，会同步反映到新数组

2. Array.from()  
   Array.from 方法用于将两类对象转为真正的数组：类似数组的对象（array-like object）和可遍历（iterable）的对象（包括 ES6 新增的数据结构 Set 和 Map）。
3. Array.of() 方法用于将一组值，转换为数组。

## ES6 对象的扩展

1. 属性的简洁表示法 ES6 允许在大括号里面，直接写入变量和函数，作为对象的属性和方法。这样的书写更加简洁。
2. 属性名表达式 方法一是直接用标识符作为属性名，方法二是用表达式作为属性名，这时要将表达式放在方括号之内。
3. 方法的name属性  
    函数的name属性，返回函数名。对象方法也是函数，因此也有 name 属性。
    方法的 name 属性返回函数名（即方法名）。    
    如果对象的方法使用了取值函数（ getter ）和存值函数（ setter ），则 name 属性不是在该方法上面，而是该方法的属性的描述对象的 get 和 set 属性上面，返回值是方法名前加上 get 和 set 。  
    有两种特殊情况： bind 方法创造的函数， name 属性返回 bound 加上原函数的名字； Function 构造函数创造的函数， name 属性返回 anonymous 。
4. 属性的可枚举性和遍历
   对象的每个属性都有一个描述对象（Descriptor），用来控制该属性的行为。 Object.getOwnPropertyDescriptor方法可以获取该属性的描述对象。
5. super 关键字
   this关键字总是指向函数所在的当前对象，ES6 又新增了另一个类似的关键字 super ，指向当前对象的原型对象。

   ```js
   const proto = {
    foo: 'hello'
    };
    const obj = {
    foo: 'world',
    find() {
        return super.foo;
    }
    };
    Object.setPrototypeOf(obj, proto);
    obj.find() // "hello"
   ```

   注意❗， super 关键字表示原型对象时，只能用在对象的方法之中，用在其他地方都会报错。

6. 对象的扩展运算符

    **解构赋值**  
    对象的解构赋值用于从一个对象取值，相当于将目标对象自身的所有可遍历的（enumerable）、但尚未被读取的属性，分配到指定的对象上面。所有的键和它们的值，都会拷贝到新对象上面.解构赋值必须是最后一个参数，否则会报错。

    **注意**❗，解构赋值的拷贝是浅拷贝，即如果一个键的值是复合类型的值（数组、对象、函数）、那么解构赋值拷贝的是这个值的引用，而不是这个值的副本。

7. 链判断运算符
    这样的层层判断非常麻烦，因此 ES2020 引入了“链判断运算符”（optional chaining operator） ?. ，简化上面的写法。

    ```js
    const firstName = message?.body?.user?.firstName || 'default';
    const fooValue = myForm.querySelector('input[name=foo]')?.value
    ```

    上面代码使用了 ?. 运算符，直接在链式调用的时候判断，左侧的对象是否为 null 或 undefined 。如果是的，就不再往下运算，而是返回 undefined 。

## ES6 Symbol

ES5的对象属性名都是字符串，这容易造成属性名的冲突。比如，你使用了一个他人提供的对象，但又想为这个对象添加新的方法（mixin 模式），新方法的名字就有可能与现有方法产生冲突。如果有一种机制，保证每个属性的名字都是独一无二的就好了，这样就从根本上防止属性名的冲突。这就是 ES6 引入 Symbol 的原因

1. 作为属性名的 Symbol
   由于每一个 Symbol 值都是不相等的，这意味着 Symbol 值可以作为标识符，用于对象的属性名，就能保证不会出现同名的属性。这对于一个对象由多个模块构成的情况非常有用，能防止某一个键被不小心改写或覆盖。

   ```js
   let mySymbol = Symbol();
    // 第一种写法
    let a = {};
    a[mySymbol] = 'Hello!';
    // 第二种写法
    let a = {
    [mySymbol]: 'Hello!'
    };
    // 第三种写法
    let a = {};
    Object.defineProperty(a, mySymbol, { value: 'Hello!' });
    // 以上写法都得到同样结果
    a[mySymbol] // "Hello!"
   ```

   使用 Symbol 值定义属性时，Symbol 值必须放在方括号之中。

2. Symbol.for()，Symbol.keyFor()  
   Symbol.for()方法可以做到这一点。它接受一个字符串作为参数，然后搜索有没有以该参数作为名称的 Symbol 值。如果有，就返回这个 Symbol 值，否则就新建一个以该字符串为名称的 Symbol 值，并将其注册到全局。  
   Symbol.keyFor() 方法返回一个已登记的 Symbol 类型值的 key 。

3. 模块的 Singleton 模式
    把实例放到顶层对象 global 

    ```js
    // mod.js
    const FOO_KEY = Symbol.for('foo');
    function A() {
    this.foo = 'hello';
    }
    if (!global[FOO_KEY]) {
    global[FOO_KEY] = new A();
    }
    module.exports = global[FOO_KEY];
    ```

    如果键名使用 Symbol 方法生成，那么外部将无法引用这个值，当然也就无法改写。

## ES6 Set 与 Map 数据结构

### Set

1. 基本用法  
   类似于数组，但是成员的值都是唯一的，没有重复的值

2. Set 实例的属性和方法
   Set 结构的实例有以下属性。

    Set.prototype.constructor ：构造函数，默认就是 Set 函数。  
    Set.prototype.size ：返回 Set 实例的成员总数。  
    Set 实例的方法分为两大类：操作方法（用于操作数据）和遍历方法（用于遍历成员）。下面先介绍四个操作方法。
    Set.prototype.add(value) ：添加某个值，返回 Set 结构本身。  
    Set.prototype.delete(value) ：删除某个值，返回一个布尔值，表示删除是否成功。  
    Set.prototype.has(value) ：返回一个布尔值，表示该值是否为 Set 的成员。  
    Set.prototype.clear() ：清除所有成员，没有返回值。  
3. 遍历操作
   Set 结构的实例有四个遍历方法，可以用于遍历成员。

    Set.prototype.keys() ：返回键名的遍历器  
    Set.prototype.values() ：返回键值的遍历器  
    Set.prototype.entries() ：返回键值对的遍历器  
    Set.prototype.forEach() ：使用回调函数遍历每个成员  

4. WeakSet  
   首先，WeakSet 的成员只能是对象，而不能是其他类型的值。  
   其次，WeakSet 中的对象都是弱引用，即垃圾回收机制不考虑 WeakSet 对该对象的引用，也就是说，如果其他对象都不再引用该对象，那么垃圾回收机制会自动回收该对象所占用的内存，不考虑该对象还存在于 WeakSet 之中。由于上面这个特点，WeakSet 的成员是不适合引用的，因为它会随时消失。另外，由于 WeakSet 内部有多少个成员，取决于垃圾回收机制有没有运行，运行前后很可能成员个数是不一样的，而垃圾回收机制何时运行是不可预测的，因此 ES6 规定 WeakSet 不可遍历。

### Map

1. 基本用法
键值对的集合（Hash 结构），但是传统上只能用字符串当作键。这给它的使用带来了很大的限制。ES6 提供了 Map 数据结构。它类似于对象，也是键值对的集合，但是“键”的范围不限于字符串，各种类型的值（包括对象）都可以当作键。也就是说，Object 结构提供了“字符串—值”的对应，Map 结构提供了“值—值”的对应，是一种更完善的 Hash 结构实现。如果你需要“键值对”的数据结构，Map 比 Object 更合适。

    ```js
    const m = new Map();
    const o = {p: 'Hello World'};
    m.set(o, 'content')
    m.get(o) // "content"
    m.has(o) // true
    m.delete(o) // true
    m.has(o) // false
    ```

2. 实例的属性和操作方法
3. 遍历方法
4. map的转换

## ES6 Proxy

Proxy用于修改某些操作的默认行为，等同于在语言层面做出修改，所以属于一种“元编程”（meta programming），即对编程语言进行编程。

```js
var obj = new Proxy({}, {
  get: function (target, propKey, receiver) {
    console.log(`getting ${propKey}!`);
    return Reflect.get(target, propKey, receiver);
  },
  set: function (target, propKey, value, receiver) {
    console.log(`setting ${propKey}!`);
    return Reflect.set(target, propKey, value, receiver);
  }
});

obj.count = 1
//  setting count!
++obj.count
//  getting count!
//  setting count!
//  2
```

ES6 原生提供 Proxy 构造函数，用来生成 Proxy 实例。

```js
var proxy = new Proxy(target, handler);
```

下面是 Proxy 支持的拦截操作一览，一共 13 种。

get(target, propKey, receiver)：拦截对象属性的读取，比如 proxy.foo 和 proxy['foo'] 。  
set(target, propKey, value, receiver)：拦截对象属性的设置，比如 proxy.foo = v 或 proxy['foo'] = v ，返回一个布尔值。  
has(target, propKey)：拦截 propKey in proxy 的操作，返回一个布尔值。
deleteProperty(target, propKey)：拦截 delete proxy[propKey] 的操作，返回一个布尔值。  
ownKeys(target)：拦截 Object.getOwnPropertyNames(proxy) 、 Object.getOwnPropertySymbols(proxy) 、 Object.keys(proxy) 、 for...in 循环，返回一个数组。该方法返回目标对象所有自身的属性的属性名，而 Object.keys() 的返回结果仅包括目标对象自身的可遍历属性。  
getOwnPropertyDescriptor(target, propKey)：拦截 Object.  getOwnPropertyDescriptor(proxy, propKey) ，返回属性的描述对象。  
defineProperty(target, propKey, propDesc)：拦截 Object.  defineProperty(proxy, propKey, propDesc） 、 Object.defineProperties(proxy, propDescs) ，返回一个布尔值。  
preventExtensions(target)：拦截 Object.preventExtensions(proxy) ，返回一个布尔值。  
getPrototypeOf(target)：拦截 Object.getPrototypeOf(proxy) ，返回一个对象。  
isExtensible(target)：拦截 Object.isExtensible(proxy) ，返回一个布尔值。  
setPrototypeOf(target, proto)：拦截 Object.setPrototypeOf(proxy, proto) ，返回一个布尔值。如果目标对象是函数，那么还有两种额外操作可以拦截。  
apply(target, object, args)：拦截 Proxy 实例作为函数调用的操作，比如 proxy(...args) 、 proxy.call(object, ...args) 、 proxy.apply(...) 。  
construct(target, args)：拦截 Proxy 实例作为构造函数调用的操作，比如 new proxy(...args) 。

## ES6 Reflect

Reflect 对象与Proxy 对象一样，也是 ES6 为了操作对象而提供的新 API。 Reflect 对象的设计目的有这样几个。

（1） 将 Object 对象的一些明显属于语言内部的方法（比如 Object.defineProperty ），放到 Reflect 对象上。现阶段，某些方法同时在 Object 和 Reflect 对象上部署，未来的新方法将只部署在 Reflect 对象上。也就是说，从 Reflect 对象上可以拿到语言内部的方法。

（2） 修改某些 Object 方法的返回结果，让其变得更合理。比如， Object.defineProperty(obj, name, desc) 在无法定义属性时，会抛出一个错误，而 Reflect.defineProperty(obj, name, desc) 则会返回 false 。

```js
// 老写法
try {
  Object.defineProperty(target, property, attributes);
  // success
} catch (e) {
  // failure
}
// 新写法
if (Reflect.defineProperty(target, property, attributes)) {
  // success
} else {
  // failure
}
```

（3） 让 Object 操作都变成函数行为。某些 Object 操作是命令式，比如 name in obj 和 delete obj[name] ，而 Reflect.has(obj, name) 和 Reflect.deleteProperty(obj, name) 让它们变成了函数行为。

（4） Reflect对象的方法与 Proxy对象的方法一一对应，只要是 Proxy 对象的方法，就能在 Reflect 对象上找到对应的方法。这就让 Proxy 对象可以方便地调用对应的 Reflect 方法，完成默认行为，作为修改行为的基础。也就是说，不管 Proxy 怎么修改默认行为，你总可以在 Reflect 上获取默认行为。

1. 静态方法

Reflect对象一共有13个静态方法。

Reflect.apply(target, thisArg, args)  
Reflect.construct(target, args)  
Reflect.get(target, name, receiver)  
Reflect.set(target, name, value, receiver)  
Reflect.defineProperty(target, name, desc)  
Reflect.deleteProperty(target, name)  
Reflect.has(target, name)  
Reflect.ownKeys(target)  
Reflect.isExtensible(target)  
Reflect.preventExtensions(target)  
Reflect.getOwnPropertyDescriptor(target, name)  
Reflect.getPrototypeOf(target)  
Reflect.setPrototypeOf(target, prototype)  


## ES6 Promise 对象

所谓 Promise ，简单说就是一个容器，里面保存着某个未来才会结束的事件（通常是一个异步操作）的结果。从语法上说，Promise 是一个对象，从它可以获取异步操作的消息。Promise 提供统一的 API，各种异步操作都可以用同样的方法进行处理。

Promise 对象有以下两个特点。

（1）对象的状态不受外界影响。 Promise 对象代表一个异步操作，有三种状态：pending（进行中）、fulfilled（已成功）和rejected（已失败）。只有异步操作的结果，可以决定当前是哪一种状态，任何其他操作都无法改变这个状态。这也是 Promise 这个名字的由来，它的英语意思就是“承诺”，表示其他手段无法改变。

（2）一旦状态改变，就不会再变，任何时候都可以得到这个结果。 Promise 对象的状态改变，只有两种可能：从 pending 变为 fulfilled 和从 pending 变为 rejected 。只要这两种情况发生，状态就凝固了，不会再变了，会一直保持这个结果，这时就称为 resolved（已定型）。如果改变已经发生了，你再对 Promise 对象添加回调函数，也会立即得到这个结果。这与事件（Event）完全不同，事件的特点是，如果你错过了它，再去监听，是得不到结果的。

Promise 也有一些缺点。首先，无法取消 Promise ，一旦新建它就会立即执行，无法中途取消。其次，如果不设置回调函数， Promise 内部抛出的错误，不会反应到外部。第三，当处于 pending 状态时，无法得知目前进展到哪一个阶段（刚刚开始还是即将完成）。

如果某些事件不断地反复发生，一般来说，使用 Stream 模式是比部署 Promise 更好的选择。

1. 基本用法  
   Promise 对象是一个构造函数，用来生成Promise 实例。

   ```js
   const promise = new Promise(function(resolve, reject) {
    // ... some code
    if (/* 异步操作成功 */){
        resolve(value);
    } else {
        reject(error);
    }
    });
   ```

   Promise 构造函数接受一个函数作为参数，该函数的两个参数分别是resolve 和reject 。它们是两个函数，由 JavaScript 引擎提供，不用自己部署。

    resolve 函数的作用是，将 Promise对象的状态从“未完成”变为“成功”（即从 pending 变为 resolved），在异步操作成功时调用，并将异步操作的结果，作为参数传递出去；reject函数的作用是，将 Promise对象的状态从“未完成”变为“失败”（即从 pending 变为 rejected），在异步操作失败时调用，并将异步操作报出的错误，作为参数传递出去。

    Promise 实例生成以后，可以用 then方法分别指定resolved状态和 rejected状态的回调函数。

## ES6 Iterator 与 for...of 循环

1. Iterator（遍历器）的概念
   遍历器（Iterator）就是这样一种机制。它是一种接口，为各种不同的数据结构提供统一的访问机制。任何数据结构只要部署 Iterator 接口，就可以完成遍历操作（即依次处理该数据结构的所有成员）。

    Iterator 的作用有三个：一是为各种数据结构，提供一个统一的、简便的访问接口；二是使得数据结构的成员能够按某种次序排列；三是 ES6 创造了一种新的遍历命令 for...of 循环，Iterator 接口主要供 for...of 消费。

    Iterator 的遍历过程是这样的。

    （1）创建一个指针对象，指向当前数据结构的起始位置。也就是说，遍历器对象本质上，就是一个指针对象。

    （2）第一次调用指针对象的 next 方法，可以将指针指向数据结构的第一个成员。

    （3）第二次调用指针对象的 next 方法，指针就指向数据结构的第二个成员。

    （4）不断调用指针对象的 next 方法，直到它指向数据结构的结束位置。  
    每一次调用 next 方法，都会返回数据结构的当前成员的信息。具体来说，就是返回一个包含 value 和 done 两个属性的对象。其中， value 属性是当前成员的值， done 属性是一个布尔值，表示遍历是否结束。

    下面是一个模拟 next 方法返回值的例子。

    ```js
    var it = makeIterator(['a', 'b']);
    it.next() // { value: "a", done: false }
    it.next() // { value: "b", done: false }
    it.next() // { value: undefined, done: true }
    function makeIterator(array) {
    var nextIndex = 0;
    return {
        next: function() {
        return nextIndex < array.length ?
            {value: array[nextIndex++], done: false} :
            {value: undefined, done: true};
        }
    };
    }
    ```

2. 默认 Iterator 接口  
   ES6 规定，默认的 Iterator 接口部署在数据结构的 Symbol.iterator 属性，或者说，一个数据结构只要具有 Symbol.iterator 属性，就可以认为是“可遍历的”（iterable）。 Symbol.iterator 属性本身是一个函数，就是当前数据结构默认的遍历器生成函数。执行这个函数，就会返回一个遍历器。至于属性名 Symbol.iterator ，它是一个表达式，返回 Symbol 对象的 iterator 属性，这是一个预定义好的、类型为 Symbol 的特殊值，所以要放在方括号内（参见《Symbol》一章）。

   ```js
   const obj = {
    [Symbol.iterator] : function () {
        return {
        next: function () {
            return {
            value: 1,
            done: true
            };
        }
        };
    }
    };
   ```

   一个对象如果要具备可被 for...of 循环调用的 Iterator 接口，就必须在 Symbol.iterator 的属性上部署遍历器生成方法（原型链上的对象具有该方法也可）。

   ```js
   class RangeIterator {
    constructor(start, stop) {
        this.value = start;
        this.stop = stop;
    }
    [Symbol.iterator]() { return this; }
    next() {
        var value = this.value;
        if (value < this.stop) {
            this.value++;
            return {done: false, value: value};
        }
        return {done: true, value: undefined};
        }
    }
    function range(start, stop) {
        return new RangeIterator(start, stop);
    }
    for (var value of range(0, 3)) {
    console.log(value); // 0, 1, 2
    }
   ```

   上面代码是一个类部署 Iterator 接口的写法。 Symbol.iterator 属性对应一个函数，执行后返回当前对象的遍历器对象。

    下面是通过遍历器实现指针结构的例子。

    ```js
    function Obj(value) {
        this.value = value;
        this.next = null;
    }
    Obj.prototype[Symbol.iterator] = function() {
    var iterator = { next: next };
    var current = this;
    function next() {
            if (current) {
                var value = current.value;
                current = current.next;
                return { done: false, value: value };
            } else {
                return { done: true };
            }
        }
        return iterator;
    }
    var one = new Obj(1);
    var two = new Obj(2);
    var three = new Obj(3);
    one.next = two;
    two.next = three;
    for (var i of one){
        console.log(i); // 1, 2, 3
    }
    ```

    上面代码首先在构造函数的原型链上部署 Symbol.iterator 方法，调用该方法会返回遍历器对象 iterator ，调用该对象的 next 方法，在返回一个值的同时，自动将内部指针移到下一个实例。

    下面是另一个为对象添加 Iterator 接口的例子。

    ```js
    let obj = {
        data: [ 'hello', 'world' ],
        [Symbol.iterator]() {
            const self = this;
            let index = 0;
            return {
            next() {
                if (index < self.data.length) {
                return {
                    value: self.data[index++],
                    done: false
                };
                } else {
                return { value: undefined, done: true };
                }
            }
            };
        }
    };
    ```

3. 调用 Iterator 接口的场合
   由于数组的遍历会调用遍历器接口，所以任何接受数组作为参数的场合，其实都调用了遍历器接口。下面是一些例子。

    for...of  
    Array.from()  
    Map(),   Set(),   WeakMap(), WeakSet()（比如 new Map([['a',1],['b',2]]) ）  
    Promise.all()  
    Promise.race()
4. 字符串的 Iterator 接口
5. Iterator 接口与 Generator 函数

   ```js
   let myIterable = {
    [Symbol.iterator]: function* () {
        yield 1;
        yield 2;
        yield 3;
    }
    }
    [...myIterable] // [1, 2, 3]
    // 或者采用下面的简洁写法
    let obj = {
    * [Symbol.iterator]() {
        yield 'hello';
        yield 'world';
    }
    };
    for (let x of obj) {
        console.log(x);
    }
    // "hello"
    // "world"
   ```
   
   上面代码中， Symbol.iterator 方法几乎不用部署任何代码，只要用 yield 命令给出每一步的返回值即可。

6. for...of 循环  
   对于普通的对象， for...of 结构不能直接使用，会报错，必须部署了 Iterator 接口后才能使用。但是，这样情况下， for...in 循环依然可以用来遍历键名。上面代码表示，对于普通的对象， for...in 循环可以遍历键名， for...of 循环会报错。

    一种解决方法是，使用 Object.keys 方法将对象的键名生成一个数组，然后遍历这个数组。另一个方法是使用 Generator 函数将对象重新包装一下。

## ES6 Generator函数的语法

1. 基本概念  
    Generator 函数有多种理解角度。语法上，首先可以把它理解成，Generator 函数是一个状态机，封装了多个内部状态。

    执行 Generator 函数会返回一个遍历器对象，也就是说，Generator 函数除了状态机，还是一个遍历器对象生成函数。返回的遍历器对象，可以依次遍历 Generator 函数内部的每一个状态。

    形式上，Generator函数是一个普通函数，但是有两个特征。一是， function 关键字与函数名之间有一个星号；二是，函数体内部使用 yield 表达式，定义不同的内部状态（ yield 在英语里的意思就是“产出”）。

    ```js
    function* helloWorldGenerator() {
        yield 'hello';
        yield 'world';
        return 'ending';
    }
    var hw = helloWorldGenerator();
    ```

    必须调用遍历器对象的 next 方法，使得指针移向下一个状态。也就是说，每次调用 next 方法，内部指针就从函数头部或上一次停下来的地方开始执行，直到遇到下一个 yield 表达式（或 return 语句）为止。换言之，Generator 函数是分段执行的， yield 表达式是暂停执行的标记，而 next 方法可以恢复执行。

    ES6 没有规定， function 关键字与函数名之间的星号，写在哪个位置。这导致下面的写法都能通过。

    ```js
    function * foo(x, y) { ··· }
    function *foo(x, y) { ··· }
    function* foo(x, y) { ··· }
    function*foo(x, y) { ··· }
    ```

    由于 Generator 函数仍然是普通函数，所以一般的写法是上面的第三种，即星号紧跟在 function 关键字后面。本书也采用这种写法。

2. yield 表达式

    由于 Generator 函数返回的遍历器对象，只有调用 next 方法才会遍历下一个内部状态，所以其实提供了一种可以暂停执行的函数。yield表达式就是暂停标志。

    遍历器对象的 next 方法的运行逻辑如下。

    （1）遇到 yield 表达式，就暂停执行后面的操作，并将紧跟在 yield 后面的那个表达式的值，作为返回的对象的 value 属性值。

    （2）下一次调用 next 方法时，再继续往下执行，直到遇到下一个 yield 表达式。

    （3）如果没有再遇到新的 yield 表达式，就一直运行到函数结束，直到 return 语句为止，并将 return 语句后面的表达式的值，作为返回的对象的 value 属性值。

    （4）如果该函数没有 return 语句，则返回的对象的 value 属性值为 undefined 。

    需要注意的是， yield 表达式后面的表达式，只有当调用 next 方法、内部指针指向该语句时才会执行，因此等于为 JavaScript 提供了手动的“惰性求值”（Lazy Evaluation）的语法功能。

3. next 方法的参数  
   yield表达式本身没有返回值，或者说总是返回 undefined 。 next 方法可以带一个参数，该参数就会被当作上一个 yield 表达式的返回值。

   ```js
   function* f() {
        for(var i = 0; true; i++) {
            var reset = yield i;
            if(reset) { i = -1; }
        }
    }
    var g = f();
    g.next() // { value: 0, done: false }
    g.next() // { value: 1, done: false }
    g.next(true) // { value: 0, done: false }
   ```

4. Generator.prototype.throw()  
   Generator函数返回的遍历器对象，都有一个 throw方法，可以在函数体外抛出错误，然后在 Generator 函数体内捕获。

   ```js
    var g = function* () {
    try {
        yield;
    } catch (e) {
        console.log('内部捕获', e);
    }
    };
    var i = g();
    i.next();
    try {
    i.throw('a');
    i.throw('b');
    } catch (e) {
    console.log('外部捕获', e);
    }
    // 内部捕获 a
    // 外部捕获 b
   ```

   上面代码中，遍历器对象 i 连续抛出两个错误。第一个错误被 Generator 函数体内的 catch 语句捕获。 i 第二次抛出错误，由于 Generator 函数内部的 catch 语句已经执行过了，不会再捕捉到这个错误了，所以这个错误就被抛出了 Generator 函数体，被函数体外的 catch 语句捕获。throw 方法抛出的错误要被内部捕获，前提是必须至少执行过一次 next 方法。
5. Generator.prototype.return()  
   Generator函数返回的遍历器对象，还有一个 return方法，可以返回给定的值，并且终结遍历 Generator 函数。
6. yield* 表达式  
   ES6 提供了 yield* 表达式，作为解决办法，用来在一个 Generator 函数里面执行另一个 Generator 函数。

   ```js
   function* bar() {
    yield 'x';
    yield* foo();
    yield 'y';
    }
    // 等同于
    function* bar() {
    yield 'x';
    yield 'a';
    yield 'b';
    yield 'y';
    }
    // 等同于
    function* bar() {
    yield 'x';
    for (let v of foo()) {
        yield v;
    }
    yield 'y';
    }
    for (let v of bar()){
    console.log(v);
    }
    // "x"
    // "a"
    // "b"
    // "y"
   ```
7. 作为对象属性的 Generator 函数
   如果一个对象的属性是 Generator 函数，可以简写成下面的形式。

    ```js
    let obj = {
        * myGeneratorMethod() {
        ···
    }
    };
    ```
8. Generator 与协程  
   协程（coroutine）是一种程序运行的方式，可以理解成“协作的线程”或“协作的函数”。协程既可以用单线程实现，也可以用多线程实现。前者是一种特殊的子例程，后者是一种特殊的线程。

    （1）协程与子例程的差异

    传统的“子例程”（subroutine）采用堆栈式“后进先出”的执行方式，只有当调用的子函数完全执行完毕，才会结束执行父函数。协程与其不同，多个线程（单线程情况下，即多个函数）可以并行执行，但是只有一个线程（或函数）处于正在运行的状态，其他线程（或函数）都处于暂停态（suspended），线程（或函数）之间可以交换执行权。也就是说，一个线程（或函数）执行到一半，可以暂停执行，将执行权交给另一个线程（或函数），等到稍后收回执行权的时候，再恢复执行。这种可以并行执行、交换执行权的线程（或函数），就称为协程。

    从实现上看，在内存中，子例程只使用一个栈（stack），而协程是同时存在多个栈，但只有一个栈是在运行状态，也就是说，协程是以多占用内存为代价，实现多任务的并行。

    （2）协程与普通线程的差异

    不难看出，协程适合用于多任务运行的环境。在这个意义上，它与普通的线程很相似，都有自己的执行上下文、可以分享全局变量。它们的不同之处在于，同一时间可以有多个线程处于运行状态，但是运行的协程只能有一个，其他协程都处于暂停状态。此外，普通的线程是抢先式的，到底哪个线程优先得到资源，必须由运行环境决定，但是协程是合作式的，执行权由协程自己分配。

    由于 JavaScript 是单线程语言，只能保持一个调用栈。引入协程以后，每个任务可以保持自己的调用栈。这样做的最大好处，就是抛出错误的时候，可以找到原始的调用栈。不至于像异步操作的回调函数那样，一旦出错，原始的调用栈早就结束。

    Generator 函数是 ES6 对协程的实现，但属于不完全实现。Generator 函数被称为“半协程”（semi-coroutine），意思是只有 Generator 函数的调用者，才能将程序的执行权还给 Generator 函数。如果是完全执行的协程，任何函数都可以让暂停的协程继续执行。

    如果将 Generator 函数当作协程，完全可以将多个需要互相协作的任务写成 Generator 函数，它们之间使用 yield 表达式交换控制权。
9.  应用  
    （1）. 异步操作的同步化表达  
    Generator 函数的暂停执行的效果，意味着可以把异步操作写在yield表达式里面，等到调用 next 方法时再往后执行。这实际上等同于不需要写回调函数了，因为异步操作的后续操作可以放在 yield 表达式下面，反正要等到调用 next 方法时再执行。所以，Generator 函数的一个重要实际意义就是用来处理异步操作，改写回调函数。

    ```js
    function* loadUI() {
    showLoadingScreen();
    yield loadUIDataAsynchronously();
    hideLoadingScreen();
    }
    var loader = loadUI();
    // 加载UI
    loader.next()
    // 卸载UI
    loader.next()
    ```

    （2）控制流管理  
    Generator 函数可以进一步改善代码运行流程。

    ```js
    function* longRunningTask(value1) {
    try {
        var value2 = yield step1(value1);
        var value3 = yield step2(value2);
        var value4 = yield step3(value3);
        var value5 = yield step4(value4);
        // Do something with value4
    } catch (e) {
        // Handle any error from step1 through step4
    }
    }
    ```

## ES6 Generator函数的异步应用

1. 基本概念
   所谓"异步"，简单说就是一个任务不是连续完成的，可以理解成该任务被人为分成两段，先执行第一段，然后转而执行其他任务，等做好了准备，再回过头执行第二段。

2. 协程
   传统的编程语言，早有异步编程的解决方案（其实是多任务的解决方案）。其中有一种叫做"协程"（coroutine），意思是多个线程互相协作，完成异步任务。

    协程有点像函数，又有点像线程。它的运行流程大致如下。

    第一步，协程 A 开始执行。
    第二步，协程 A 执行到一半，进入暂停，执行权转移到协程 B 。
    第三步，（一段时间后）协程 B 交还执行权。
    第四步，协程 A 恢复执行。
    上面流程的协程 A ，就是异步任务，因为它分成两段（或多段）执行。

    举例来说，读取文件的协程写法如下。

    ```js
    function* asyncJob() {
    // ...其他代码
    var f = yield readFile(fileA);
    // ...其他代码
    }
    ```

    上面代码的函数 asyncJob 是一个协程，它的奥妙就在其中的 yield 命令。它表示执行到此处，执行权将交给其他协程。也就是说， yield 命令是异步两个阶段的分界线。

    协程遇到 yield 命令就暂停，等到执行权返回，再从暂停的地方继续往后执行。它的最大优点，就是代码的写法非常像同步操作，如果去除 yield 命令，简直一模一样。

    **协程的 Generator 函数实现**  

    Generator 函数是协程在 ES6 的实现，最大特点就是可以交出函数的执行权（即暂停执行）。

    整个Generator 函数就是一个封装的异步任务，或者说是异步任务的容器。异步操作需要暂停的地方，都用 yield 语句注明。Generator 函数的执行方法如下。

    ```js
    function* gen(x) {
    var y = yield x + 2;
    return y;
    }
    var g = gen(1);
    g.next() // { value: 3, done: false }
    g.next() // { value: undefined, done: true }
    ```

    **Generator 函数的数据交换和错误处理**

    Generator 函数可以暂停执行和恢复执行，这是它能封装异步任务的根本原因。除此之外，它还有两个特性，使它可以作为异步编程的完整解决方案：函数体内外的数据交换和错误处理机制。

    next 返回值的 value 属性，是 Generator 函数向外输出数据； next 方法还可以接受参数，向 Generator 函数体内输入数据

    ```js
    function* gen(x){
        var y = yield x + 2;
        return y;
    }
    var g = gen(1);
    g.next() // { value: 3, done: false }
    g.next(2) // { value: 2, done: true }
    ```

    上面代码中，第一个 next 方法的 value 属性，返回表达式 x + 2 的值 3 。第二个 next 方法带有参数 2 ，这个参数可以传入 Generator 函数，作为上个阶段异步任务的返回结果，被函数体内的变量 y 接收。因此，这一步的 value 属性，返回的就是 2 （变量 y 的值）。

    Generator 函数内部还可以部署错误处理代码，捕获函数体外抛出的错误。

    ```js
    function* gen(x){
    try {
        var y = yield x + 2;
    } catch (e){
        console.log(e);
    }
    return y;
    }
    var g = gen(1);
    g.next();
    g.throw('出错了');
    // 出错了
    ```

    上面代码的最后一行，Generator 函数体外，使用指针对象的 throw 方法抛出的错误，可以被函数体内的 try...catch 代码块捕获。这意味着，出错的代码与处理错误的代码，实现了时间和空间上的分离，这对于异步编程无疑是很重要的。

3. JavaScript 语言的 Thunk 函数
    任何函数，只要参数有回调函数，就能写成 Thunk 函数的形式。下面是一个简单的 Thunk 函数转换器。  
    **Thunkify 模块**  
    建议使用 Thunkify 模块。安装：npm install thunkify

    ```js
    var thunkify = require('thunkify');
    var fs = require('fs');
    var read = thunkify(fs.readFile);
    read('package.json')(function(err, str){
    // ...
    });
    ```

    **Generator 函数的流程管理**  

    ```js
    var fs = require('fs');
    var thunkify = require('thunkify');
    var readFileThunk = thunkify(fs.readFile);
    var gen = function* (){
    var r1 = yield readFileThunk('/etc/fstab');
    console.log(r1.toString());
    var r2 = yield readFileThunk('/etc/shells');
    console.log(r2.toString());
    ```

    yield 命令用于将程序的执行权移出 Generator 函数，那么就需要一种方法，将执行权再交还给 Generator 函数。

    这种方法就是 Thunk 函数，因为它可以在回调函数里，将执行权交还给 Generator 函数。为了便于理解，我们先看如何手动执行上面这个 Generator 函数。

    ```js
    var g = gen();
    var r1 = g.next();
    r1.value(function (err, data) {
    if (err) throw err;
    var r2 = g.next(data);
    r2.value(function (err, data) {
        if (err) throw err;
        g.next(data);
    });
    });
    ```

    **Thunk 函数的自动流程管理**  
    Thunk 函数真正的威力，在于可以自动执行 Generator 函数。下面就是一个基于 Thunk 函数的 Generator 执行器。

    function run(fn) {
    var gen = fn();
    function next(err, data) {
        var result = gen.next(data);
        if (result.done) return;
        result.value(next);
    }
    next();
    }
    function* g() {
    // ...
    }
    run(g);
    上面代码的 run 函数，就是一个 Generator 函数的自动执行器。内部的 next 函数就是 Thunk 的回调函数。 next 函数先将指针移到 Generator 函数的下一步（ gen.next 方法），然后判断 Generator 函数是否结束（ result.done 属性），如果没结束，就将 next 函数再传入 Thunk 函数（ result.value 属性），否则就直接退出。

    有了这个执行器，执行 Generator 函数方便多了。不管内部有多少个异步操作，直接把 Generator 函数传入 run 函数即可。当然，前提是每一个异步操作，都要是 Thunk 函数，也就是说，跟在 yield 命令后面的必须是 Thunk 函数。

    var g = function* (){
    var f1 = yield readFileThunk('fileA');
    var f2 = yield readFileThunk('fileB');
    // ...
    var fn = yield readFileThunk('fileN');
    };
    run(g);
    上面代码中，函数 g 封装了 n 个异步的读取文件操作，只要执行 run 函数，这些操作就会自动完成。这样一来，异步操作不仅可以写得像同步操作，而且一行代码就可以执行。

    Thunk 函数并不是 Generator 函数自动执行的唯一方案。因为自动执行的关键是，必须有一种机制，自动控制 Generator 函数的流程，接收和交还程序的执行权。回调函数可以做到这一点，Promise 对象也可以做到这一点。

4. co 模块
   co 模块是著名程序员 TJ Holowaychuk 于 2013 年 6 月发布的一个小工具，用于 Generator 函数的自动执行。

    下面是一个 Generator 函数，用于依次读取两个文件。

    ```js
    var gen = function* () {
    var f1 = yield readFile('/etc/fstab');
    var f2 = yield readFile('/etc/shells');
    console.log(f1.toString());
    console.log(f2.toString());
    };
    ```

    co 模块可以让你不用编写 Generator 函数的执行器。

    ```js
    var co = require('co');
    co(gen);
    ```

    上面代码中，Generator 函数只要传入 co 函数，就会自动执行。

    co 函数返回一个 Promise 对象，因此可以用 then 方法添加回调函数。

    ```js
    co(gen).then(function (){
        console.log('Generator 函数执行完成');
    });
    ```
    上面代码中，等到 Generator 函数执行结束，就会输出一行提示。

    **co 模块的原理**  
    为什么 co 可以自动执行 Generator 函数？

    前面说过，Generator 就是一个异步操作的容器。它的自动执行需要一种机制，当异步操作有了结果，能够自动交回执行权。

    两种方法可以做到这一点。

    （1）回调函数。将异步操作包装成 Thunk 函数，在回调函数里面交回执行权。

    （2）Promise 对象。将异步操作包装成 Promise 对象，用 then 方法交回执行权。

    co 模块其实就是将两种自动执行器（Thunk 函数和 Promise 对象），包装成一个模块。使用 co 的前提条件是，Generator 函数的 yield 命令后面，只能是 Thunk 函数或 Promise 对象。如果数组或对象的成员，全部都是 Promise 对象，也可以使用 co，详见后文的例子。

    上一节已经介绍了基于 Thunk 函数的自动执行器。下面来看，基于 Promise 对象的自动执行器。这是理解 co 模块必须的。

## ES6 async 函数

ES2017 标准引入了async 函数，使得异步操作变得更加方便。

async 函数是什么？一句话，它就是 Generator 函数的语法糖。

```js
const asyncReadFile = async function () {
  const f1 = await readFile('/etc/fstab');
  const f2 = await readFile('/etc/shells');
  console.log(f1.toString());
  console.log(f2.toString());
};
```
一比较就会发现， async 函数就是将 Generator 函数的星号（ * ）替换成 async ，将 yield 替换成 await ，仅此而已。
async 函数对 Generator 函数的改进，体现在以下四点。

（1）内置执行器。

Generator 函数的执行必须靠执行器，所以才有了 co 模块，而 async 函数自带执行器。也就是说， async 函数的执行，与普通函数一模一样，只要一行。

asyncReadFile();
上面的代码调用了 asyncReadFile 函数，然后它就会自动执行，输出最后结果。这完全不像 Generator 函数，需要调用 next 方法，或者用 co 模块，才能真正执行，得到最后结果。

（2）更好的语义。

async 和 await ，比起星号和 yield ，语义更清楚了。 async 表示函数里有异步操作， await 表示紧跟在后面的表达式需要等待结果。

（3）更广的适用性。

co 模块约定， yield 命令后面只能是 Thunk 函数或 Promise 对象，而 async 函数的 await 命令后面，可以是 Promise 对象和原始类型的值（数值、字符串和布尔值，但这时会自动转成立即 resolved 的 Promise 对象）。

（4）返回值是 Promise。

async 函数的返回值是 Promise 对象，这比 Generator 函数的返回值是 Iterator 对象方便多了。你可以用 then 方法指定下一步的操作。

进一步说， async 函数完全可以看作多个异步操作，包装成的一个 Promise 对象，而 await 命令就是内部 then 命令的语法糖。

1. 基本用法  
   async 函数有多种使用形式。

   ```js
   // 函数声明
    async function foo() {}
    // 函数表达式
    const foo = async function () {};
    // 对象的方法
    let obj = { async foo() {} };
    obj.foo().then(...)
    // Class 的方法
    class Storage {
    constructor() {
        this.cachePromise = caches.open('avatars');
    }
    async getAvatar(name) {
        const cache = await this.cachePromise;
        return cache.match(`/avatars/${name}.jpg`);
    }
    }
    const storage = new Storage();
    storage.getAvatar('jake').then(…);
    // 箭头函数
    const foo = async () => {};
   ```

2. await 命令
   await 命令后面是一个Promise对象，返回该对象的结果。如果不是 Promise 对象，就直接返回对应的值  
   另一种情况是， await 命令后面是一个 thenable 对象（即定义了 then 方法的对象），那么 await 会将其等同于 Promise 对象。await 命令后面是一个 Sleep 对象的实例。这个实例不是 Promise 对象，但是因为定义了 then 方法， await 会将其视为 Promise 处理。
3. 错误处理  
   await 后面的异步操作出错，那么等同于 async 函数返回的 Promise 对象被 reject 。
   下面的例子使用 try...catch 结构，实现多次重复尝试。
    ```js
    const superagent = require('superagent');
    const NUM_RETRIES = 3;
    async function test() {
    let i;
    for (i = 0; i < NUM_RETRIES; ++i) {
        try {
        await superagent.get('http://google.com/this-throws-an-error');
        break;
        } catch(err) {}
    }
    console.log(i); // 3
    }
    test();
    ```

4. 使用注意点  
   第一点，前面已经说过， await 命令后面的 Promise 对象，运行结果可能是 rejected ，所以最好把 await 命令放在 try...catch 代码块中。  
   第二点，多个 await 命令后面的异步操作，如果不存在继发关系，最好让它们同时触发。

   ```js
   // 写法一
    let [foo, bar] = await Promise.all([getFoo(), getBar()]);
    // 写法二
    let fooPromise = getFoo();
    let barPromise = getBar();
    let foo = await fooPromise;
    let bar = await barPromise;
   ```

   上面两种写法， getFoo 和 getBar 都是同时触发，这样就会缩短程序的执行时间。

    第三点， await 命令只能用在 async 函数之中，如果用在普通函数，就会报错。

5. 实例：按顺序完成异步操作

    ```js
    async function logInOrder(urls) {
    // 并发读取远程URL
    const textPromises = urls.map(async url => {
        const response = await fetch(url);
        return response.text();
    });
    // 按次序输出
    for (const textPromise of textPromises) {
        console.log(await textPromise);
    }
    }
    ```

    虽然 map 方法的参数是 async 函数，但它是并发执行的，因为只有 async 函数内部是继发执行，外部不受影响。后面的 for..of 循环内部使用了 await ，因此实现了按顺序输出。

## ES6 Class 的基本语法

S6 提供了更接近传统语言的写法，引入了 Class（类）这个概念，作为对象的模板。通过 class 关键字，可以定义类。

```js
class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
  toString() {
    return '(' + this.x + ', ' + this.y + ')';
  }
}
```

1. constructor 方法  
   constructor 方法是类的默认方法，通过 new 命令生成对象实例时，自动调用该方法。一个类必须有 constructor 方法，如果没有显式定义，一个空的 constructor 方法会被默认添加。

2. 取值函数（getter）和存值函数（setter）
   在“类”的内部可以使用 get和 set关键字，对某个属性设置存值函数和取值函数，拦截该属性的存取行为。

   ```js
    class CustomHTMLElement {
        constructor(element) {
            this.element = element;
        }
        get html() {
            return this.element.innerHTML;
        }
        set html(value) {
            this.element.innerHTML = value;
        }
    }
    var descriptor = Object.getOwnPropertyDescriptor(
    CustomHTMLElement.prototype, "html"
    );
    "get" in descriptor  // true
    "set" in descriptor  // true
   ```
3. 属性表达式

4. 静态方法
   类相当于实例的原型，所有在类中定义的方法，都会被实例继承。如果在一个方法前，加上 static 关键字，就表示该方法不会被实例继承，而是直接通过类来调用，这就称为“静态方法”。

5. 静态属性
   静态属性指的是Class本身的属性，即 Class.propName，而不是定义在实例对象（ this ）上的属性。

    ```js
    class Foo {
    }
    Foo.prop = 1;
    Foo.prop // 1
    ```
6. 私有方法和私有属性
   私有方法和私有属性，是只能在类的内部访问的方法和属性，外部不能访问
   一种做法是在命名上加以区别。  方法前面的下划线，表示这是一个只限于内部使用的私有方法  
   另一种方法就是索性将私有方法移出模块，因为模块内部的所有方法都是对外可见的。

   ```js
    class Widget {
    foo (baz) {
        bar.call(this, baz);
    }
    // ...
    }
    function bar(baz) {
    return this.snaf = baz;
    }
    ```
    还有一种方法是利用Symbol值的唯一性，将私有方法的名字命名为一个 Symbol 值。

    ```js
    ```
    const bar = Symbol('bar');
    const snaf = Symbol('snaf');
    export default class myClass{
    // 公有方法
    foo(baz) {
        this[bar](baz);
    }
    // 私有方法
    [bar](baz) {
        return this[snaf] = baz;
    }
    // ...
    };
7. new.target 属性
   new是从构造函数生成实例对象的命令。ES6 为 new 命令引入了一个 new.target 属性，该属性一般用在构造函数之中，返回 new 命令作用于的那个构造函数。如果构造函数不是通过 new 命令或 Reflect.construct() 调用的， new.target 会返回 undefined ，因此这个属性可以用来确定构造函数是怎么调用的。

   ```js
    function Person(name) {
        if (new.target !== undefined) {
            this.name = name;
        } else {
            throw new Error('必须使用 new 命令生成实例');
        }
    }
    // 另一种写法
    function Person(name) {
        if (new.target === Person) {
            this.name = name;
        } else {
            throw new Error('必须使用 new 命令生成实例');
        }
    }
    var person = new Person('张三'); // 正确
    var notAPerson = Person.call(person, '张三');  // 报错
   ```

## ES6 Class 的继承

Class 可以通过extends关键字实现继承，这比 ES5 的通过修改原型链实现继承，要清晰和方便很多。子类必须在 constructor 方法中调用 super 方法，否则新建实例时会报错。这是因为子类自己的 this 对象，必须先通过父类的构造函数完成塑造，得到与父类同样的实例属性和方法，然后再对其进行加工，加上子类自己的实例属性和方法。如果不调用 super 方法，子类就得不到 this 对象。

```js
class Point { /* ... */ }
class ColorPoint extends Point {
  constructor() {
  }
}
let cp = new ColorPoint(); // ReferenceError
```
上面代码中， ColorPoint 继承了父类 Point ，但是它的构造函数没有调用 super 方法，导致新建实例时报错。ES6 的继承机制完全不同，实质是先将父类实例对象的属性和方法，加到 this 上面（所以必须先调用 super 方法），然后再用子类的构造函数修改 this .另一个需要注意的地方是，在子类的构造函数中，只有调用 super 之后，才可以使用 this 关键字，否则会报错。这是因为子类实例的构建，基于父类实例，只有 super 方法才能调用父类实例。最后，父类的静态方法，也会被子类继承。

## ES6 Module 的语法

1. 基本用法
    ES6 模块不是对象，而是通过 export 命令显式指定输出的代码，再通过 import 命令输入。

    // ES6模块
    import { stat, exists, readFile } from 'fs';
    上面代码的实质是从 fs 模块加载 3 个方法，其他方法不加载。这种加载称为“编译时加载”或者静态加载，即 ES6 可以在编译时就完成模块加载，效率要比 CommonJS 模块的加载方式高。当然，这也导致了没法引用 ES6 模块本身，因为它不是对象

2. 严格模式
   ES6 的模块自动采用严格模式，不管你有没有在模块头部加上 "use strict"; 。

    严格模式主要有以下限制。

    变量必须声明后再使用  
    函数的参数不能有同名属性，否则报错  
    不能使用 with 语句  
    不能对只读属性赋值，否则报错  
    不能使用前缀 0 表示八进制数，否则报错  
    不能删除不可删除的属性，否则报错  
    不能删除变量 delete prop ，会报错，只能删除属性 delete global[prop]  
    eval 不会在它的外层作用域引入变量  
    eval 和 arguments 不能被重新赋值  
    arguments 不会自动反映函数参数的变化  
    不能使用 arguments.callee  
    不能使用 arguments.caller  
    禁止 this 指向全局对象  
    不能使用 fn.caller 和 fn.arguments 获取函数调用的堆栈  
    增加了保留字（比如 protected 、 static 和 interface ）  
    上面这些限制，模块都必须遵守。由于严格模式是 ES5 引入的，不属于 ES6，所以请参阅相关  ES5 书籍，本书不再详细介绍了。  

    其中，尤其需要注意 this 的限制。ES6 模块之中，顶层的 this 指向 undefined ，即不应该在顶层代码使用 this 。  
3. export 命令

4. import 命令 import 命令输入的变量都是只读的，因为它的本质是输入接口。也就是说，不允许在加载模块的脚本里面，改写接口。

5. 模块的整体加载

6. export default 命令 export default 命令，为模块指定默认输出。

    ```js
    // export-default.js
    export default function () {
    console.log('foo');
    }
    ```

    上面代码是一个模块文件 export-default.js ，它的默认输出是一个函数。

    其他模块加载该模块时， import 命令可以为该匿名函数指定任意名字。

    ```js
    // import-default.js
    import customName from './export-default';
    customName(); // 'foo'
    ```

    下面比较一下默认输出和正常输出。

    ```js
    // 第一组
    export default function crc32() { // 输出
    // ...
    }
    import crc32 from 'crc32'; // 输入
    // 第二组
    export function crc32() { // 输出
    // ...
    };
    import {crc32} from 'crc32'; // 输入
    ```

    上面代码的两组写法，第一组是使用 export default 时，对应的 import 语句不需要使用大括号；第二组是不使用 export default 时，对应的 import 语句需要使用大括号。

    export default 命令用于指定模块的默认输出。显然，一个模块只能有一个默认输出，因此 export default 命令只能使用一次。所以，import命令后面才不用加大括号，因为只可能唯一对应 export default 命令。

    本质上， export default 就是输出一个叫做 default 的变量或方法，然后系统允许你为它取任意名字。所以，下面的写法是有效的。

    ```js
    // modules.js
    function add(x, y) {
    return x * y;
    }
    export {add as default};
    // 等同于
    // export default add;
    // app.js
    import { default as foo } from 'modules';
    // 等同于
    // import foo from 'modules';
    ```

    正是因为 export default 命令其实只是输出一个叫做 default 的变量，所以它后面不能跟变量声明语句。

    有了 export default 命令，输入模块时就非常直观了，以输入 lodash 模块为例。

    import _ from 'lodash';
    如果想在一条 import 语句中，同时输入默认方法和其他接口，可以写成下面这样。

    import _, { each, forEach } from 'lodash';

7. 模块的继承