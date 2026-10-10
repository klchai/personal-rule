# HK_Bank 香港业务补充记录

从 CN_Bank 上游筛除项中选取香港相关域名；既有条目不重复添加。筛查日期：2026-10-10。

| 上游 | 域名 | 归属 |
| --- | --- | --- |
| BOC | `bocgi.com` | 中银集团投资（香港） |
| BOC | `bocgins.com` | 中银集团保险（香港） |
| BOC | `bochk.com` | 中国银行（香港），原有规则保留 |
| BOC | `bochkonline.com` | 中银香港相关上游域名 |
| BOC | `bocigroup.com` | 中银国际（香港） |
| CCB | `ccbintl.com.hk` | 建银国际（香港） |
| CEB | `ebchinaintl.com` | 光大国际历史域名，香港集团业务 |
| CEB | `everbright.com` | 光大控股，香港总部及跨境业务 |
| CMB | `cmbi.com.hk` | 招银国际（香港） |
| CMB | `cmbwinglungbank.com` | 招商永隆，原有规则保留 |
| ICBC | `icbcasia.com` | 工银亚洲 |
| ICBC | `icbci.com.hk` | 工银国际（香港） |

工银亚洲 `icbc-asia.icbc.com.cn`、`mobilehk.icbc.com.cn` 也归入此组，并从 CN_Bank 移除对应精确规则。HK_Bank 必须放在 CN_Bank 之前，才能优先于大陆规则的 `icbc.com.cn` 后缀匹配。

香港集团的主域名也可能承载大陆或其他地区业务；按用户要求整体归入香港策略。`ebchinaintl.com` 是历史域名，保留上游条目，不代表当前仍正常提供服务。

这些补充项属于个人维护条目，由现有同步逻辑保留；仍在 CN_Bank 排除清单中，防止重复加入大陆规则。

## 核对来源

- [中银集团投资资料](https://www.cbinsights.com/investor/bank-of-china-group-investment)
- [中银集团保险](https://www.bocgins.com/)
- [中银国际香港银行业务](https://www.bocigroup.com/PrivateBank/EN)
- [建银国际联系资料](https://www.ccbintl.com.hk/English/contact.html)
- [光大国际历史报告](https://www.hkexnews.hk/listedco/listconews/sehk/2020/0703/2020070302815.pdf)
- [光大控股联系资料](https://www.everbright.com/public/about/20170915_CorpFactsheet_eng.pdf)
- [招银国际](https://www.cmbi.com.hk/)
- [工行官方工银亚洲说明](https://www.icbc.com.cn/column/1438058343720960553.html)
- [工银国际](https://www.icbci.com.hk/)
- [中行上游规则（含 bochkonline.com）](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Loon/BOC/BOC.list)
