# MINECRAFT.NET-TRANSLATIONS

寄存在 GitHub 上的官网博文翻译参考目录。



目前，你可以直接在 GitHub 仓库中浏览以下分类的表格：

* [内部资讯 INSIDER](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E5%86%85%E9%83%A8%E8%B5%84%E8%AE%AF.md)
* [社区文化 CULTURE](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E7%A4%BE%E5%8C%BA%E6%96%87%E5%8C%96.md)
* [每周方块 INSIDER: Block of the Week](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E6%AF%8F%E5%91%A8%E6%96%B9%E5%9D%97.md)
* [遇见生物 INSIDER: Meet the Mob](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E9%81%87%E8%A7%81%E7%94%9F%E7%89%A9.md)
* [背包盘点 INSIDER: Taking Inventory](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E8%83%8C%E5%8C%85%E7%9B%98%E7%82%B9.md)
* [与之建造 CULTURE: Build With It](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E4%B8%8E%E4%B9%8B%E5%BB%BA%E9%80%A0.md)



## 文件

- `rawtable.csv`：存放所有 culture 与 insider 分类的博文及翻译。
- `mcContent.py`：使用 `python mcContents.py` 运行后会将官网上的新博文同步到上述两个表格中。

* `config.json`：指示博文分类的对应名称。
* `uid.json`：存放uid与昵称的对应关系，每月更新一次。
* 其它`.md`文件：对应分类博文的目录。

## 使用与编辑

请在命令行中运行`mcContent.py`。可用的参数有：

* `pull`：将`rawtable.csv`更新到最新状态。
* `render`：根据分类输出不同的`.csv`文件。
* <s>`bbcode`：按分类切分并输出bbcode表格，bbcode存放在`bbcode.txt`中。</s> 该功能暂未实现。

示例：

```python
python mcContent.py pull render
```

将把表格更新到最新，并输出分类过的表格。



如果你想在`rawtable.csv`中添加或编辑译文信息，推荐使用 VSCode 的 [janisdd.vscode-edit-csv](http://marketplace.visualstudio.com/items?itemName=janisdd.vscode-edit-csv) 插件。

除非你知道自己在做什么，**不要**使用 Excel 等软件，这将导致包括乱码在内的问题。

## 说明

[MCBBS 的官方博文录](https://www.mcbbs.net/thread-675773-1-1.html) 于近期调整了收录标准，剔除了很多不合格的博文。本目录主要是为了方便对历史已存在译文、最新博文译文的查询参考，

**本目录仅供译文参考，不保证所收录译文的质量。**

本目录不收录MERCH（周边产品）和NEWS（新闻资讯）分类（除非官网分错类别），周边产品请到MCBBS博文录寻找，新闻资讯请到MCBBS新闻资讯版寻找。

部分不属于文章的视频链接类官网内容（点击后跳转到Youtube）可能不会被包含在本目录中。



## 收录与替换

在 MCBBS 【翻译 & Wiki】 板块使用官网博文分类发帖，如果帖子符合基本标准（标题、正文链接、非机翻等），则本目录会将其收录。

出现同一博文的不同翻译版本，质量差异不大时收录最早发布的版本，质量存在明显差异时取更优的版本。

如果某版本得到绿宝石奖励的认证，则没有得到绿宝石的版本会被替换掉。

如果收录的文章因机翻要素等原因在 MCBBS 被锁定，同时出现了新的翻译时，则会将其从目录中替换。



## 实用链接

- 在线博文转换器：https://spgoding.com
- MCBBS官方博文录：https://www.mcbbs.net/thread-675773-1-1.html  
![](https://attachment.mcbbs.net/forum/201909/14/001453yfroxnbheoot0nfm.png)
