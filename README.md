# Personal Rule

个人使用的 Clash 和 Loon 分流规则。

| 规则 | 内容 | Clash | Loon |
| --- | --- | --- | --- |
| US_Bank | 美国银行及个人金融服务 | [YAML](US_Bank/US_Bank.yaml) | [List](US_Bank/US_Bank.list) |
| Bank_HK | 香港银行 | [YAML](Bank_HK/Bank_HK.yaml) | [List](Bank_HK/Bank_HK.list) |
| PikPak | PikPak 相关域名 | [YAML](PikPak/pikpak.yaml) | [List](PikPak/pikpak.list) |
| Apple_AI | Apple AI、Siri 及相关服务域名 | [YAML](Apple_AI/Apple_AI.yaml) | [List](Apple_AI/Apple_AI.list) |

## 使用

- Clash：使用 `.yaml` 文件作为规则提供器，设置 `type: http`、`behavior: classical` 和 `format: yaml`，通过 `RULE-SET` 指定策略。
- Loon：使用 `.list` 文件作为订阅规则，并选择对应策略。
- 在线订阅需使用文件的 Raw 链接；私有仓库的文件无法通过公开 Raw 链接直接订阅。

同一套规则的两种格式保持一致，更新时请同步修改。

## 来源

`US_Bank` 合并个人规则与 [Accademia/Additional_Rule_For_Clash 的 BankUS.yaml](https://github.com/Accademia/Additional_Rule_For_Clash/blob/main/Bank/BankUS.yaml)，并去除完全重复项。

`Bank_HK` 来源于 [Accademia/Additional_Rule_For_Clash 的 BankHK.yaml](https://github.com/Accademia/Additional_Rule_For_Clash/blob/main/Bank/BankHK.yaml)，将 `DOMAIN-SUFFIX,.hk.hsbc.com` 规范为 `DOMAIN-SUFFIX,hk.hsbc.com`。

其余规则由个人提供。
