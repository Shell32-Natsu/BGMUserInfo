# BGMUserInfo

抓取[Bangumi](http://bgm.tv/)上标记看过的动画, 并抓取相关信息, 生成Excel表格. 使用时编辑Line 7的`user_id`为要抓取的ID. 生成文件为main.xls

抓取的字段有:
* Bangumi条目URL
* 中文名称
* 全名
* 评分
* 监督
* 制作公司


使用到的库:

* BeautifulSoup
* xlwt
