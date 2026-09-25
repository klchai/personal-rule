# Personal Rule

个人使用的 Clash 和 Loon 分流规则。

| 规则 | 内容 | Clash | Loon |
| --- | --- | --- | --- |
| US_Bank | 美国银行及个人金融服务 | [YAML](US_Bank/US_Bank.yaml) | [List](US_Bank/US_Bank.list) |
| HK_Bank | 香港银行 | [YAML](HK_Bank/HK_Bank.yaml) | [List](HK_Bank/HK_Bank.list) |
| PikPak | PikPak 相关域名 | [YAML](PikPak/pikpak.yaml) | [List](PikPak/pikpak.list) |
| Apple_AI | Apple AI、Siri 及相关服务域名 | [YAML](Apple_AI/Apple_AI.yaml) | [List](Apple_AI/Apple_AI.list) |
| X | X（Twitter）、X Money、xAI 及 Grok | [YAML](X/X.yaml) | [List](X/X.list) |

## 使用

- Clash：使用 `.yaml` 文件作为规则提供器，设置 `type: http`、`behavior: classical` 和 `format: yaml`，通过 `RULE-SET` 指定策略。
- Loon：使用 `.list` 文件作为订阅规则，并选择对应策略。
- 在线订阅需使用文件的 Raw 链接；私有仓库的文件无法通过公开 Raw 链接直接订阅。

同一套规则的两种格式保持一致，更新时请同步修改。

### 香港银行

将 `HK_Bank` 绑定到香港节点或策略组，并放在 `ChinaMax` 等中国直连规则以及最终兜底规则之前。更新文件后需刷新客户端的规则订阅。

`hsbc.com.hk` 和 `bochk.com` 的后缀规则已覆盖其子域名。根据访问实测补充了 `welab.bank`，以及工银亚洲的 `icbc-asia.icbc.com.cn`、`mobilehk.icbc.com.cn`。未将整个 `icbc.com.cn` 纳入香港规则，以免影响中国内地工行服务；其他配套接口需确认具体域名后再添加。华侨银行（香港）的网站已从 `ocbcwhhk.com` 迁到 `ocbc.com.hk`，两个域名均保留。

### X

`X` 涵盖 X（Twitter）、X Money、xAI 和 Grok。X Money 的 `money.x.com`、XChat 的 `chat.x.com` 以及 X 内置 Grok 的 `grok.x.com` 已由 `x.com` 的后缀规则覆盖，`x.ai` 的后缀规则覆盖 xAI 的 API、控制台和账户等子域名。

IP 规则均带 `no-resolve`，只匹配直接以 IP 发起的连接，不会为域名请求额外触发 DNS 解析。Grok 客户端还会请求 Statsig 的 `featureassets.org`，这是多个应用共用的域名，为避免影响其他应用未予收录。

## 自动同步上游

[sync-upstream](.github/workflows/sync-upstream.yml) 每周一 10:00（北京时间）运行一次，也可以在 Actions 页面手动触发。它把每个上游来源与 `sync/upstream/` 中的快照对比，只把上游的增删应用到对应规则，并开一个 PR 供审核；个人补充的条目不受影响。

在 [scripts/sync_upstream.py](scripts/sync_upstream.py) 的 `exclude` 中列出的条目（如 `eastwest.com`、Zelle 关键词）不会被重新加回；已被现有规则覆盖的新增条目会跳过，并在 PR 说明中列出。

## 来源

`US_Bank` 合并个人规则与 [Accademia/Additional_Rule_For_Clash 的 BankUS.yaml](https://github.com/Accademia/Additional_Rule_For_Clash/blob/main/Bank/BankUS.yaml)，并去除完全重复项。上游的 `eastwest.com` 实为度假酒店管理公司 East West Hospitality 的域名，已更正为 East West Bank 的 `eastwestbank.com`；另补充 Dave 和 BNY 现用的 `dave.com`、`bny.com`。删除了上游的 Zelle 关键词规则（会误匹配 `gazelle.com` 等无关域名）和无法确认归属的 `gobankrewards.com`。

`HK_Bank` 来源于 [Accademia/Additional_Rule_For_Clash 的 BankHK.yaml](https://github.com/Accademia/Additional_Rule_For_Clash/blob/main/Bank/BankHK.yaml)，将 `DOMAIN-SUFFIX,.hk.hsbc.com` 规范为 `DOMAIN-SUFFIX,hk.hsbc.com`，并结合个人访问实测补充域名。

`X` 基于 [blackmatrix7/ios_rule_script 的 Twitter.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Loon/Twitter/Twitter.list)，补充 xAI 和 Grok 的 `x.ai`、`grokipedia.com`、`grokusercontent.com`，以及 [Accademia/Additional_Rule_For_Clash 的 Grok 规则](https://github.com/Accademia/Additional_Rule_For_Clash/tree/main/Grok)中的 `xai.chronosphere.io`；IP 段在上游基础上补充了 X 的自治系统 AS13414 当前宣告的 IPv4 和 IPv6 前缀。

`PikPak` 参照 [v2fly/domain-list-community 的 pikpak 列表](https://github.com/v2fly/domain-list-community/blob/master/data/pikpak)补充了 `pikpak.me` 和 `pikpakdrive.com`。

其余规则由个人提供。
