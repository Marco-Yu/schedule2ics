# schedule2ics
通过Python把BNU教务系统导出的课表转换成.ics日历文件

## 声明
作者不是主修计算机专业的学生，编写此程序主要是出于兴趣（闲的），还请多指教！

除了参考了所使用的库的官方文档以外，还参考了以下内容：  
RFC 5545: https://www.rfc-editor.org/rfc/rfc5545  
ICS To Calendar: https://www.routinehub.co/shortcut/7005/

## 编写环境（俺也不知道这么说是否准确，但……）
- python 3.9.13
- icalendar 4.0.7
- pandas 1.4.4

## 使用方法

### 0. 配置环境
因为作者也刚刚入门Python，怎么配置环境其实还没太整明白，所以这部分需要自己解决一下……

### 1. 下载代码
安装好python和相关的包后，下载本项目中的 schedule2ics.py 或 schedule2ics.ipynb（建议单独放在一个文件夹里）

### 2. 从教务系统导出课表
教务系统 → “网上选课” → “我的课表” → 在“学年学期”中选择学期 → 选择“按列表方式显示” → 点击“检索” → 检查是否为所需学期，点击“导出”

把下载的.xls文件和上一步中下载的代码放在同一个文件夹里（如果你尝试打开这个xls，Excel会弹出一个警告，不用管它）

### 3. 运行schedule2ics代码
在JupyterLab/Notebook里运行.ipynb，或者在python里运行.py

## 输出
（按理说）运行代码后文件夹里会出现两个文件：20xx-20xx学年x季学期.ics 和 Apple.txt

### .ics文件
日历文件，Windows和安卓可以直接打开并导入日历，但苹果设备好像不行（至少iPhone不行，iPad和Mac我不确定）

### Apple.txt
由于iPhone没办法直接打开ics文件，这个txt文件是为了简化导入日历的操作，以下是（我认为）最简单的方法：  
1. 把 Apple.txt 发到自己的手机上；
2. 在手机上打开 Apple.txt；
3. 复制文件中的所有内容；
4. 打开Safari浏览器，将复制的内容粘贴到地址栏中并访问
5. 按“导入全部”

## 没了嘻嘻
