# pytest笔记

## 安装

```sh
pip install -U pytest
```

## 使用规则：

设计测试用例时候注意点（必须遵循的规则，否者不识别）：

1. .py测试文件必须以test（test_xxx）开头（或者以_test结尾）
2. 测试类必须以Test开头，并且不能有init方法-----测试类Test开头
3. 测试方法必须以test_开头
4. 断言必须使用assert

### pytest函数级别

函数级别的测试用例必须test_开头：如下test_tc01，test_tc02两个测试用例

```python
import pytest
    def test_tc01():　　　　#定义函数类型测试用例　　
        assert 1+1==2  　　#断言
    def test_tc02():
        assert 1+1==3  　　#断言
 
    if __name__ == '__main__':
        pytest.main(["test_func01.py"])        #我主动运行我的pytest框架(自动调用所有的test测试函数，按照顺序依次运行，test开头的用例自动识别）
```

### pytest类级别（工作一般以类位单元，一个模块一个类，登录类，订单类，购物类）

类级别的测试l类必须以Test开头，并且类李不能有init方法，类里面的函数都是test_开头
封装好函数和类就行，其他的交给框架，设置好，框架帮你自动组织怎么运行
封装为了分层，后面更好维护，代码结构整洁

```python
import pytest
 
class Test_login():  　　　　　　　　　　　　#登录模块的测试类
　　def test_login01(self):
    print("---test_login01----")
    assert 1 + 1 == 2
　　def test_login02(self):
    print("---test_login02----")
    assert 1 + 1 == 3
if __name__ == '__main__':
　　pytest.main(["test_func01.py","-s"])  #框架自己调用函数　　需要打印对应的信息，需要在列表里面加-s
```

## 自动化测试里面的环境初始化与清除

### pytest前置和后置条件

pyets种有四种级别的setup和teardown

1. setup_module和teardown_module,在整个测试用例所在的文件中所在的文件中所有的方法运行前和运行后运行，只运行一次---模块的
2. setup_class和teardown_class,在整个测试文件中的一个class中所有的用例的签后运行 ----class类
3. setup_method和teardown_method,在class内的每个方法运行前后运行 ---------方法的
4. setup_function和teardown_function,在非class下属的每个测试方法的前后运行 ----函数的分层分级（不同级别有不同方法）

### pytest里面的数据初始化装饰器fixture参数说明

@pytest.fixture(scope=xxx,params=xxx,autouse=xxx)

fiixture装饰器可以传单三个参数

1. scope参数：初始化清除定义级别
2. params:参数
3. autouse：是否自动化执行

```python
import pytest

#函数级别的@pytest.fixture()初始化操作

@pytest.fixture()   　　　　#标记函数是个初始化操作，标记后需要传给每个函数statr_func这个函数名才会执行初始化操作（函数级别的）
def statr1_func():

#这不是测试函数，一个普通函数,pytest执行用例只能识别test开头的方法和函数，所以pytest.main不会执行(不参加pytest用例)

print("------初始化操作1------")

@pytest.fixture()
def statr2_func():

    print("------初始化操作2------")

#fixture:有哪些操作（可以多个初始化可以一起调，需要两个初始化，需要连接，需要登录）

#这种写法很方便，函数需要statr_func1函数做一个初始化操作可以调用statr_func1这个函数，---def test_001(statr1_func):

# 需要其他初始化方法可以选择性调用其他初始化函数，传递函数名就行（灵活选择）----def test_002(statr2_func):

#函数初始化操作需要传递几个函数也可以多个函数名传递--def test_003(statr2_func,statr1_func):

#方便灵活

def test_001(statr1_func):
    print("-----test01------")

def test_002(statr2_func):
    print("-----test02 ------")

def test_003(statr2_func,statr1_func):
    print("-----test03 ------")

if __name__ == '__main__':
    pytest.main(["test_pytest.py","-s"])
```

### 类级别的初始化class，可以使用setup做初始化，也可以使用fixture做初始化

类级别初始化fixture，虽然test_001和test_002都调用了statr1_func这个类级别的初始化函数，但是执行类测试用例的时候只执行statr1_func初始函数一次. 多个类都可以调用statr1_func这个类级别的初始化方法,调用的时候最好放在类里的第一个函数，后面的函数可以不传(因为对应的是类级别的初始化)

```python
import pytest
 
@pytest.fixture(scope="class")   　　　　　　　　#类级别的初始化函数  scope="class" 就是把这个初始化定义成类级别的
def statr1_func():
    print("------初始化操作1------")

class Test_00:　#需要执行 Test_00测试类，需要做初始化(可以setup_class)
    # def setup_class(self):
    #     print("类内部的初始化,")  #只对类有用,类级别的，类里只做一次(几个类的初始化操作一样这种不适合，需要重复写)
                                    　　     #fixture初始化类就是避免重复代码
    def test_001(self,statr1_func):
        print("-----test01------")

    def test_002(self,statr1_func):
        print("-----test02 ------")


if __name__ == '__main__':
    pytest.main(["test_pytest01.py","-s"])
```

### 模块级别的初始化mudule

模块（module）级别的初始化，（整个模块所有的类所有的东西要做一步操作，可以使用module这个模式）只在模块运行前面只做一次，后面不做了，哪怕多调用也没用，一个模块里面有test_003函数测试用例，
也有classTest_00类级别的测试用例，定义一个模块级别的初始化函数statr1_func
函数里面调用初始化方法def test_003(statr1_func):和类里面的方法调用初始化方法test_001(self,statr1_func):，test_001(self,statr1_func):
整个模块执行的时候初始化函数都只执行一次（不管你这个模块里面调用多少次）

```python
import pytest
@pytest.fixture(scope="module")   　　　　　　#模块级别的初始化函数
def statr1_func():
    print("------初始化操作1------")
    
　　　　　　　　　　　　　　　　　　　　　　　　　　#一个模块里面有函数用例也有类的用例怎么做：（class级别的初始化只对类有用，对函数没用）
def test_003(statr1_func):  　　　　　　　　  #测试函数,
    print("-----test03------")

class Test_00:                        　　#需要执行test00测试类，需要做初始化(可以setup_class)
    # def setup_class(self):
    #     print("类内部的初始化,")  　　　　#只对类有用,类级别的，类里只做一次(几个类的初始化操作一样这种不适合，需要重复写)
    #                               　　　　#fixture初始化类就是避免重复代码

    def test_001(self,statr1_func):
        print("-----test01------")

    def test_001(self,statr1_func):
        print("-----test02 ------")

if __name__ == '__main__':
    pytest.main(["test_pytest01.py","-s"])
```

### 两种调用初始化和清除函数的方式

```python
import pytest
@pytest.fixture()
def befor_func():
    print('xxxxxxxxxxxxx测试用例的初始化xxxxxxxxxxxxxxxx')
    yield 10
    print('zzzzzzzzzzzzzzzzzz测试用例的清除zzzzzzzzzzzzzz')
 
def test_001(befor_func):　　　　　　　　　　　　　　　　#调用初始化和清除方式一：直接在测试用例里传递初始化清除函数的函数名来调用
    print("测试用例001")
    res=befor_func　　　　　　　　　　　　　　　　　　　　#如果初始化清除函数有返回值，可以直接这样接收参数来使用
    print(res)
 
@pytest.mark.usefixtures('befor_func')　　　　　　　　#调用初始化和清除方式二：使用usefixtures放在测试用例前面直接调用初始化清除函数
def test_002():
    print("测试用例002")
 
if __name__ == '__main__':
    pytest.main(["test1.py",'-s'])
```

### fixture函数的返回值

1. 使用yield关键字来是实现　　推荐使用这种，因为yield关键字能返回函数的值
2. 使用finc()函数来实现

```python 
import pytest
@pytest.fixture()
def befor_func():
    print('xxxxxxxxxxxxx测试用例的初始化xxxxxxxxxxxxxxxx')
    yield 10　　　　　　　　　　　　　　　　　　　　　　　　　　　　#yield后面跟的是测试用例的后置条件，支持用例执行后就执行yield里的内容
    print('zzzzzzzzzzzzzzzzzz测试用例的清除zzzzzzzzzzzzzz')
 
def test_001(befor_func):
    print("测试用例001")
    res=befor_func
    print(res)
 
if __name__ == '__main__':
    pytest.main(["test1.py",'-s'])

```

### 参数化

@pytest.mark.parametrize("a",[1,2,3])：　　　　　　　　参数化传一组参数　　

@pytest.mark.parametrize("a,b", [(1,2),(3,4),(5,6)]) 　　   参数化传多组参数

```python
    import pytest
    #[(1,2),(3,4),(5,6)]   [1,2,3]
    class Test_login():  
        def setup_class(self):
            print("执行测试类之前，我需要执行操作")
 
        @pytest.mark.parametrize("a",[1,2,3])            #("变量名",[1,2,3]),数据需要封装成一个列表，多个数据需要封装成列表嵌套元组   ----数据驱动
        def test_login01(self,a):                  #数据驱动，一定要把变量名a引入引来，不然无法参数化
```

```python
print("---test_login01----")
            assert 1 + 1 == a
 
        @pytest.mark.parametrize("a,b", [(1,2),(3,4),(5,6)])    #数据驱动传多组参数
        def test_login02(self,a,b):
             print("---test_login02----")
             assert a + 1 == b
 
        def teardown_class(self):
            print("------该测试类的环境清除-----")
 
    if __name__ == '__main__':
        pytest.main(["test_func01.py","-s"])  
```

初始化函数before_test也能参数化

```python
import pytest
#假设启动被测app的时候需要去填写配置项信息，每个的端口号不同，多终端需要两个appim server
#这时候setup_module和teardown_module不能传参，搞不定，需要换一种方法做测试用例的初始化和清除，

　　　　　　　　　　　　　　　　#setup_module以模块为作用域，不写module以测试用例（测试函数）为作用域
# def setup_module(): 　　 #测试用例之前执行，原始的setup和teardown有个缺陷，里面不能传参数，
#             　　　　　　   #默认test级别，每个测试用例执行的时候都会执行一次，希望当前某个模块执行的时候只执行一次（不管里面用例执行多少次）
#             　　　　　　   #setup初始化和tear_down升个级，升级成module模块级别的
#     print("启动被测app")
#     print('连接appium服务')
#
# def teardown_module():
#     print('关闭被测app')
#     print('断开appium服务')

#定义个函数，名字随便取　　使用@pytest.fixture装饰器把这个函数装饰成初始化清除函数
@pytest.fixture(scope='module')    #作用域默认test，初始化，加装饰器，初始化清除函数,autouse=True（自动执行）这种方法不建议使用                               #
def before_test():                   #初始化函数升级作用域到module模块级别
    print("启动被测app")
    print('连接appium服务')
    yield   #后面写清除动作，
    after_test()

#清除函数，清除函数并不会直接被初始化函数使用，我们必须放在初始化函数yiled后面才能回被调用
def after_test():
    print('关闭被测app')
    print('断开appium服务')
#目前一共有两个port，需要测试两个手机，两个多终端,before_test需要装饰器标记

#测试用例的参数化
@pytest.mark.usefixtures('before_test')                        #这表示调用某个自定义的初始化函数，括号里面的字符串写被调用函数的名字
@pytest.mark.parametrize('psw',['boss123','boss456'])
def test_app(psw):                        #测试用例，可能涉及到其他参数,比如需要一些配置信息,测试用例涉及到参数，
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　#多组参数需要使用装饰器pytest.mark.parametrize(数据驱动)，psw传参和形参名字对应的
    print('测试boss app')
    print(f'登录测试账号{psw}')

if __name__ == '__main__':
    pytest.main(['pytest_ywt.py','-s'])
```

## pytest的用例定制化执行　　mark标签

> mark标记呢，需要先在配置文件中注册自定义标记。如果不做这一步，会有warning提示。

在根目录或测试的文件夹中可以新建配置文件，这里我们使用pytest.ini

```ini
[pytest]
markers= 
    do:do
    undo:undo
```

```python
# content of test_demo09.py
import pytest

@pytest.mark.do
def test01():
    print("test01")
    
@pytest.mark.undo
def test02():
    print("test02")

```

接着使用命令pytest -svm do test_demo09.py

@pytest.mark.skip("跳过test_lesson_add")　　　　　　　　无条件跳过

@pytest.mark.skipif(1==1,reason="条件需要前面完成某一个步骤--前面条件为真的时候则跳过函数，不为真执行函数")　　　　有条件的跳过


### 配置文件

>。Pytest框架中，有4个配置文件，分别是 pytest.ini ， pyproject.toml ， tox.ini 和 setup.cfg 文件

- addopts
addopts是添加指定的命令行参数，比如pytest.ini中内容如下：

    ```ini
    [pytest]
    addopts = -sv
    ```

- norecursedirs  设置在递归查找用例时，不进入哪些文件夹中收集用例。

### 依赖

> Pytest有一个专门的依赖插件pytest-dependency直接使用 pip3 install pytest-dependency 进行安装