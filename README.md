# Personal Rule

个人使用的 Clash 和 Loon 分流规则。

| 规则 | 内容 | Clash | Loon | 上游来源 |
| --- | --- | --- | --- | --- |
| US_Bank | 美国银行及个人金融服务 | [YAML](US_Bank/US_Bank.yaml) | [List](US_Bank/US_Bank.list) | [Accademia BankUS](https://github.com/Accademia/Additional_Rule_For_Clash/blob/main/Bank/BankUS.yaml) |
| HK_Bank | 香港银行 | [YAML](HK_Bank/HK_Bank.yaml) | [List](HK_Bank/HK_Bank.list) | [Accademia BankHK](https://github.com/Accademia/Additional_Rule_For_Clash/blob/main/Bank/BankHK.yaml) |
| PikPak | PikPak 相关域名 | [YAML](PikPak/pikpak.yaml) | [List](PikPak/pikpak.list) | [v2fly pikpak](https://github.com/v2fly/domain-list-community/blob/master/data/pikpak) |
| Apple_AI | Apple AI、Siri 及相关服务 | [YAML](Apple_AI/Apple_AI.yaml) | [List](Apple_AI/Apple_AI.list) | [Accademia AppleAI](https://github.com/Accademia/Additional_Rule_For_Clash/tree/main/AppleAI)、[v2fly apple-intelligence](https://github.com/v2fly/domain-list-community/blob/master/data/apple-intelligence) |
| X | X（Twitter）、X Money、xAI 及 Grok | [YAML](X/X.yaml) | [List](X/X.list) | [blackmatrix7 Twitter](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Loon/Twitter/Twitter.list)、[v2fly xai](https://github.com/v2fly/domain-list-community/blob/master/data/xai)、[Accademia Grok](https://github.com/Accademia/Additional_Rule_For_Clash/tree/main/Grok)、AS13414 |

各规则在上游基础上结合个人实测做了增删。

## 使用

- Clash：以 `.yaml` 作为规则提供器（`type: http`、`behavior: classical`、`format: yaml`），通过 `RULE-SET` 指定策略。
- Loon：以 `.list` 作为订阅规则。
- 订阅需使用 Raw 链接，私有仓库无法直接订阅。
- 将 `HK_Bank` 绑定到香港节点，并放在 `ChinaMax` 等直连规则和兜底规则之前。
- `X` 的 IP 规则带 `no-resolve`，不会为域名请求触发 DNS 解析；X Money（`money.x.com`）、XChat 等已由 `x.com` 覆盖。

两种格式内容保持一致，修改时需同步。

## 自动同步

[sync-upstream](.github/workflows/sync-upstream.yml) 每周一 10:00（北京时间）运行，也可手动触发。它将上游与 `sync/upstream/` 中的快照对比，只同步上游的增删，并开 PR 供审核。不想被加回的条目写入 [sync_upstream.py](scripts/sync_upstream.py) 的 `exclude`。
