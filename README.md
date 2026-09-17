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

### 香港银行

将 `Bank_HK` 绑定到香港节点或策略组，并放在 `ChinaMax` 等中国直连规则以及最终兜底规则之前。更新文件后需刷新客户端的规则订阅。

`hsbc.com.hk` 和 `bochk.com` 的后缀规则已覆盖其子域名。根据访问实测补充了 `welab.bank`，以及工银亚洲的 `icbc-asia.icbc.com.cn`、`mobilehk.icbc.com.cn`。未将整个 `icbc.com.cn` 纳入香港规则，以免影响中国内地工行服务；其他配套接口需确认具体域名后再添加。

## 来源

`US_Bank` 合并个人规则与 [Accademia/Additional_Rule_For_Clash 的 BankUS.yaml](https://github.com/Accademia/Additional_Rule_For_Clash/blob/main/Bank/BankUS.yaml)，并去除完全重复项。

`Bank_HK` 来源于 [Accademia/Additional_Rule_For_Clash 的 BankHK.yaml](https://github.com/Accademia/Additional_Rule_For_Clash/blob/main/Bank/BankHK.yaml)，将 `DOMAIN-SUFFIX,.hk.hsbc.com` 规范为 `DOMAIN-SUFFIX,hk.hsbc.com`，并结合个人访问实测补充域名。

其余规则由个人提供。
