# 日程助手 · 洛克王国世界免费云端图鉴索引

本仓库为「日程助手」提供**纯 JSON 图鉴索引**：只包含编号、名称、属性、种族值、蛋组与在线立绘文件链接，**不存储和分发游戏图片文件**。

## 免费访问

- [云端 JSON（无需启用 Pages）](https://raw.githubusercontent.com/qaqdeyan/Rczs/main/site/pokedex.json)
- [GitHub Actions 自动同步状态](https://github.com/qaqdeyan/Rczs/actions)
- 启用 GitHub Pages 后，也可使用 `https://qaqdeyan.github.io/Rczs/pokedex.json`

## 数据来源与更新

上游来自 [洛克王国世界 BWIKI 镜像数据](https://github.com/JayeGT002/rocom-wiki-data)，每日自动检查一次（具体更新以 GitHub Actions 记录为准），上游数据未更新时不会凭空增加宠物。原始 WIKI：[精灵列表](https://wiki.biligame.com/nrc/精灵列表)。

此项目不提供官方数据保证。素材属于其各自权利人，游戏图片版权归权利人所有。所用社区数据资料遵循上游所标注的 **CC BY-NC-SA 4.0** 非商业署名相同方式共享条款；如需商业用途请核验授权。严禁将此索引视为游戏官方 API。

## 客户端建议

Android APP 只读云端 JSON，在线加载当前可见的立绘；不把图片打包进 APK，不预下载图片。不稳定时回退上一次成功读取的 JSON。WIKI 图片重定向可能受网络、防盗链及授权政策影响：失败时显示「暂无立绘」，不要用其他宠物图片冒充。

## 索引结构

`site/pokedex.json` 字段：`schema_version`、`updated_at`、`record_count`、`records`，单条数据包含 `id/number/name/types/form/stage/egg_group/stats/avatar_url/portrait_url/source_url` 等。
