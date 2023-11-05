# 笔记

## 安装

 1. 问题：无法将“conda”项识别为 cmdlet  
   解决： 增加以下三个环境变量就可以了：D:\ProgramData\Anaconda3，D:\ProgramData\Anaconda3\Scripts， D:\ProgramData\Anaconda3\Library\bin, D:\ProgramData\anaconda3\Library\mingw-w64\bin, D:\ProgramData\anaconda3\Library\usr\bin
 2. 问题: CondaSSLError: OpenSSL appears to be unavailable on this machine.
   解决： libcrypto-1_1-x64.dll，libssl-1_1-x64.dll 两个文件从D:\ProgramData\Anaconda3\Library\bin拷贝到D:\ProgramData\Anaconda3\DLLs

## 命令

1. activate
activate 能将我们引入anaconda设定的虚拟环境中, 如果你后面什么参数都不加那么会进入anaconda自带的base环境
2.   创建自己的虚拟环境

3. conda env list
   去查看所有的环境  
   conda env reomove 环境名  删除  
   conda create --prefix=D:/ProgramData/anaconda3/envs/appium_env python=3

   问题：Conda环境无法激活conda activate myenv usage: conda-script.py [-h] [--no-plugins] [-V]  
    解决方法： 管理员执行conda init
4. conda install -n 环境名 安装第三方包
5. conda remove 卸载第三方包
6. 要查看当前环境中所有安装了的包可以用
conda list 
7. 导入导出环境
如果想要导出当前环境的包信息可以用
conda env export > environment.yaml
将包信息存入yaml文件中.
8. 当需要重新创建一个相同的虚拟环境时可以用
conda env create -f environment.yaml
9. 安装特定版本的 第三方包,然后conda search 第三方包=版本
10. 镜像管理  
查看：conda config --show channels  
删除：conda config --remove-key channels  
添加镜像：  
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main  
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r  
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2 
conda config --set show_channel_urls yes 是用于设置搜索时显示镜像源地址


conda create -n learn python=3


### 1. 问题 PackagesNotFoundError: The following packages are not available from current channels

  解决方法: conda config --append channels conda-forge 告诉conda在搜索软件包时也要在conda-forge channel上查看
