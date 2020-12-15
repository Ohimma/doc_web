## 1.1 创建编译环境
vscode + go + 外网

#### 下载安装 go
根据系统下载指定类型 https://studygolang.com/dl

https://studygolang.com/dl/golang/go1.14.4.windows-amd64.msi
目前我用的windows
我安装到了D盘下

设置环境变量，参考 https://jingyan.baidu.com/article/00a07f3876cd0582d128dc55.html

具体细节我就不说了


#### 下载安装 vscode
https://code.visualstudio.com/Download

#### 配置 vscode
```
1. 安装插件后重启软件  Go + code runner

2. 右下角弹出的需要安装服务，点击 install all

3. 新建文件测试运行，正常输出则ok
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}

```
