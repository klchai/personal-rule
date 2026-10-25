# CDN

用于直连分流的补充规则集，合并手动规则、异常流量清单中缺少的域名规则及 Feishu 上游规则。包含业务接口、推送、广告及统计域名，名称 CDN 不表示所有条目都是内容分发服务。

## 来源

- 手动提供的 7 条 `DOMAIN-SUFFIX`：`aliapp.org`、`futunn.com`、`larkoffice.com`、`miaozhen.com`、`adukwai.com`、`tanhuoo.com`、`ctobsnssdk.com`。
- 日志清单中缺少域名覆盖的 8 个主机，以精确 `DOMAIN` 规则补充：`tags.tiqcdn.com`、`sis.jpush.io`、`p66-ad.adkwai.com`、`qzs.gdtimg.com`、`df.tanx.com`、`ef-dongfeng.tanx.com`、`px.effirst.com`、`av1.xdrig.com`。只覆盖列出的主机，不扩展到整个主域。
- [MetaCubeX Feishu Classical YAML](https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/classical/feishu.yaml)：完整合并飞书域名规则，由仓库每周同步流程跟踪上游增删，快照见 `sync/upstream/metacubex-feishu.txt`。

## 使用

Clash / OpenSurge 以 `behavior: classical`、`format: yaml` 加载 `CDN.yaml`；Loon 使用 `CDN.list`。策略在引用时指定，规则文件中不附带 `DIRECT`。

```text
RULE-SET,CDN,DIRECT
```

放在需要覆盖的代理规则及 Final / MATCH 之前。若需要继续拦截广告或统计请求，将相应拦截规则放在 CDN 之前。飞书已合并到此组，可用此组替代单独的 Feishu 订阅。

本组未纳入已有 Apple、Google 策略覆盖的域名，也未纳入被 Claude 的 `sentry` 关键词匹配的 `app-sentry.taou.com`；这些域名的策略需单独处理。
