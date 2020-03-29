# MINECRAFT.NET-TRANSLATIONS

![pull & sync](https://github.com/RicoloveFeng/minecraft.net-translations/workflows/Pull%20%26%20Sync/badge.svg)
![render](https://github.com/RicoloveFeng/minecraft.net-translations/workflows/Render/badge.svg)

寄存在 GitHub 上的官网博文翻译参考目录。从 2020 年 3 月 18 日起，本仓库将收录全部分类的官网博文。

**本目录仅供译文参考，不保证所收录译文的质量。**

部分不属于文章的视频链接类官网内容（点击后跳转到Youtube）可能不会被包含在本目录中。



## 重要提示（临时）

鉴于官网于 2020 年 3 月更新了博文分类策略，本仓库将收录全部分类的博文。

以下更新内容需要您注意：

* 与以往不同，现在一个博文可能会出现在多个子目录中。
* 本目录将会收录从 2020 年 3 月 18 日起的 NEWS 和 MERCH 分类的博文，过往博文暂时不考虑追加。



## 子目录

### 官网博文分类

|  分类名称 | 分类原名  |
| ---- | ---- |
| [内部资讯](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E5%86%85%E9%83%A8%E8%B5%84%E8%AE%AF.md) | INSIDER |
| [社区文化](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E7%A4%BE%E5%8C%BA%E6%96%87%E5%8C%96.md) | CULTURE |
| [建筑展示](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E5%BB%BA%E7%AD%91%E5%B1%95%E7%A4%BA.md) | MINECRAFT BUILDS |
| [市场消息](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E5%B8%82%E5%9C%BA%E6%B6%88%E6%81%AF.md) | MARKETPLACE |
| [块海拾贝](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E5%9D%97%E6%B5%B7%E6%8B%BE%E8%B4%9D.md) | DEEP DIVES |
| 教程指导（暂无文章） | GUIDES |
| 大事件（暂无文章） | EVENTS |
| 周边产品（暂无文章） | MERCH |
| [新闻资讯](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E6%96%B0%E9%97%BB%E8%B5%84%E8%AE%AF.md) | NEWS |



### 专栏文章与视频系列

| 专栏或视频名称                 | 原名称                                |
| ------------------------------ | ------------------------------------- |
| [每周方块](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E6%AF%8F%E5%91%A8%E6%96%B9%E5%9D%97.md)                       | Block of the Week                     |
| [遇见生物](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E9%81%87%E8%A7%81%E7%94%9F%E7%89%A9.md)                       | Meet the ...                          |
| [背包盘点](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E8%83%8C%E5%8C%85%E7%9B%98%E7%82%B9.md)                       | Taking Inventory                      |
| [与之建造](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E4%B8%8E%E4%B9%8B%E5%BB%BA%E9%80%A0.md) | Build with it                         |
| :film_strip:[《Minecraft：地下城》开发日志](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E5%9C%B0%E4%B8%8B%E5%9F%8E%E6%97%A5%E5%BF%97.md) | Dungeon Diary                         |
| :film_strip: [十件你或许不知道的事情](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E5%8D%81%E6%88%96%E4%B8%8D%E7%9F%A5.md)        | 10 Things You Don't Know About ...    |
| [版本资讯](https://github.com/RicoloveFeng/minecraft.net-translations/blob/master/%E7%89%88%E6%9C%AC%E8%B5%84%E8%AE%AF.md)                       | （无，收录 Minecraft 新版本发布博文） |



### 表格认证项说明

对于除新闻资讯类的博文，认证一栏的屏障代表尚未被收录或未达到收录标准，绿宝石代表已经被收录。

对于发表在新闻资讯板块下帖子，由于其一般不参与绿宝石发放和博文收录，有译文的时候默认为收录。

图片素材版权归 Mojang 所有。



## 文件

* `rawtable.csv`：存放所有博文及翻译。
* `mcContent.py`：使用 `python mcContents.py` 运行后会将官网上的新博文同步到上述表格中。
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



## 同步 MCBBS 官方博文录

我们提供了一个能够将 [MCBBS 官方博文录](https://www.mcbbs.net/thread-823054-1-1.html)中的内容同步到 `rawtable.csv` 文件的脚本 `sync.js`。

运行 JavaScript 脚本需要下载并安装 [Node.js](https://nodejs.org/zh-cn/download/)。长期支持版（LTS）是受到推荐的。

该脚本没有任何参数，直接使用命令行工具执行即可。

示例：

```bash
node sync
```

你可以后续执行命令块 `python mcContent.py render` 将相关改动渲染到 `*.md` 文档之中。



## 收录与替换

在 MCBBS 【翻译 & Wiki】 板块使用官网博文分类发帖，如果帖子符合基本标准（标题、正文链接、非机翻等），则本目录会将其收录。

对于新闻资讯板块下的帖子，直接将其收录。

出现同一博文的不同翻译版本，质量差异不大时收录最早发布的版本，质量存在明显差异时取更优的版本。

如果某版本得到绿宝石奖励的认证，则没有得到绿宝石的版本会被替换掉。

如果收录的文章因机翻要素等原因在 MCBBS 被锁定，同时出现了新的翻译时，则会将其从目录中替换。

在添加译文信息时，请在`tr_title`, `tr_link`字段添加译文标题，译文链接。如果链接正确，原本为空的 UID 会在执行 `render` 命令时自动填写。当译文被收录后，请将`emeralded`字段改为`1`；执行`node sync`可以自动完成这一步。



## 实用链接

- 在线博文转换器 SPX：https://spgoding.com
- 在线博文转换器 BCC：https://bcc.wd-ljt.com
- MCBBS官方博文录：https://www.mcbbs.net/thread-823054-1-1.html  
![](https://attachment.mcbbs.net/forum/201909/14/001453yfroxnbheoot0nfm.png)
