# CDN

用于直连分流的补充规则集，合并手动规则、异常流量清单中缺少的域名规则及 Feishu 上游规则。包含业务接口、推送、广告及统计域名，名称 CDN 不表示所有条目都是内容分发服务。

## 来源

- 手动及日志补充的 44 条规则（含 42 条 `DOMAIN-SUFFIX` 及 2 条本地化 `DOMAIN`）：`bvmlt.top`、`kuaishouzt.com`、`tiqcdn.com`、`puata.info`、`linkedin.com`、`jddebug.com`、`51.la`、`mob.com`、`uyunad.com`、`id6.me`、`aliapp.org`、`futunn.com`、`larkoffice.com`、`miaozhen.com`、`adukwai.com`、`tanhuoo.com`、`ctobsnssdk.com`、`zimenur.com`、`jpush.io`、`adkwai.com`、`gdtimg.com`、`tanx.com`、`effirst.com`、`xdrig.com`、`mmstat.com`、`alicdn.com`、`ixigua.com`、`weibo.cn`、`xiaohongshu.com`、`fengkongcloud.com`、`cmpassport.com`、`futustatic.com`、`moomoo.com`、`xiaoyuzhoufm.com`、`zhuanzhuan.com`、`cup.com.cn`、`snssdk.com`、`isnssdk.com`、`xhscdn.com`、`xhscdn.net`、`apple.cn`、`weatherkit.apple.com`、`bag.itunes.apple.com`、`icbcasia.com`。
- [MetaCubeX Feishu Classical YAML](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/classical/feishu.yaml)：完整合并飞书域名规则，由仓库每周同步流程跟踪上游增删，快照见 `sync/upstream/metacubex-feishu.txt`。

## 使用

Clash / OpenSurge 以 `behavior: classical`、`format: yaml` 加载 `CDN.yaml`；Loon 使用 `CDN.list`。策略在引用时指定，规则文件中不附带 `DIRECT`。

```text
RULE-SET,CDN,DIRECT
```

放在需要覆盖的代理规则及 Final / MATCH 之前。若需要继续拦截广告或统计请求，将相应拦截规则放在 CDN 之前。飞书已合并到此组，可用此组替代单独的 Feishu 订阅。

本组已补充 Apple 国内基础及天气服务（`apple.cn`、`weatherkit.apple.com`、`bag.itunes.apple.com`）以保证直连，其余 Apple、Google 策略仍由对应规则集覆盖；Claude 规则集已移除泛匹配 `DOMAIN-KEYWORD,sentry`，保留 `DOMAIN-SUFFIX,sentry.io`。
