# twoTimesSql
作者最近正在研究代码审计，作为初学者，看到很多大牛都在发表二次注入的相关漏洞，头脑发热，也就自己尝试着去做二次注入的代码审计。然而在实际的过程中，却发现二次注入的漏洞相比于传统注入漏洞，审计难度非常大。虽然名字叫做二次注入，但是整个过程却是应该有三次数据库的操作：

1.插入或者更新数据表table1

2.从table1中取出一条数据data1

3.使用data1中的某一个字段值column1再进行数据库操作

为了简化人工审计的复杂度，作者使用python脚本编写了二次注入的探测工具，仅作为测试使用。

工具能做的事情只是帮我们定位到关键点，至于究竟是不是二次注入，还需要我们手工进行判断
