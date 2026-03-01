# 易数 (Yì Shù) Agent --- Standardized Scoring & Analysis Specification

Generated on: 2026-02-28 17:05:17

------------------------------------------------------------------------

## 1. Purpose

This document defines the **deterministic scoring logic and output
standard** for the 易数 number analysis agent (Phone & Car Plate).

It is designed for: - RAG reference - File search retrieval - Backend
implementation consistency - 100% standardized response generation

All interpretations are for reference only.

* Response shall be in Chinese as default, unless the query is using english.

------------------------------------------------------------------------

# 2. Deterministic Parsing Rules

## 2.1 Normalize Input

1.  Convert to uppercase
2.  Convert letters A--Z → 1--26 (concatenate digits)
3.  Keep digits only

Example: AB12 → 11212

------------------------------------------------------------------------

## 2.2 Handle 0 and 5

-   Remove all 0 and 5 before pairing
-   5 = Amplifier (显)
-   0 = Hidden influence (隐)

Maintain: - digits_full → original digits including 0/5 - digits_clean →
digits after removing 0/5

------------------------------------------------------------------------

## 2.3 Build Energy Pairs

Use consecutive two-digit pairs from digits_clean.

Example: 13876 → 13 / 38 / 87 / 76

If fewer than 2 digits → insufficient data.

------------------------------------------------------------------------

# 3. Energy Mapping

  Energy   Pairs
  -------- -------------------------
  天医     13,31,68,86,49,94,27,72
  延年     19,91,78,87,43,34,26,62
  生气     14,41,76,67,93,39,28,82
  伏位     11,22,33,44,66,77,88,99
  绝命     12,21,69,96,48,84,37,73
  祸害     17,71,89,98,46,64,32,23
  六煞     16,61,74,47,38,83,92,29
  五鬼     18,81,79,97,36,63,42,24

Ignore unmapped pairs.

------------------------------------------------------------------------

# 4. Scoring Model

## 4.1 Frequency Score

count\[e\] = number of mapped pairs\
N = total mapped pairs\
share\[e\] = count\[e\] / N

------------------------------------------------------------------------

## 4.2 显 / 隐 Modifier (Optional)

Detect in digits_full:

If digit = 5: - Amplify nearest left & right non-0/5 digits pair

If digit = 0: - Mark hidden influence on nearest pair

Modifier formula:

score\[e\] =\
count\[e\]\
+ 0.25 × amplify_count\[e\]\
+ 0.10 × hidden_count\[e\]

score_share\[e\] = score\[e\] / total_score

------------------------------------------------------------------------

# 5. Ranking Rules

Sort by: 1. score_share (descending) 2. count (descending) 3. Fixed tie
order:

天医 \> 延年 \> 生气 \> 伏位 \> 绝命 \> 祸害 \> 六煞 \> 五鬼

Only display Top 3 energies.

Percent format: - Round to nearest integer

------------------------------------------------------------------------

# 6. Ending Warning Rule

If last pair belongs to:

  Energy   Warning
  -------- ---------------------------------
  绝命     冲动破财（投资/消费需控）
  五鬼     意外破财（避免随手决策）
  六煞     情绪破财（人情/冲动消费）
  祸害     口舌破财（争执带来损耗）
  伏位     保守漏财（错失机会/资金效率低）

Only show ONE warning sentence.

------------------------------------------------------------------------

# 7. Meaning Keywords

  Energy   Keywords
  -------- --------------------
  天医     贵人 / 财富 / 顺
  延年     领导 / 责任 / 压力
  生气     好运 / 人缘 / 贵人
  伏位     稳定 / 保守 / 耐力
  绝命     冲劲 / 风险 / 决断
  祸害     口才 / 争执 / 口舌
  六煞     情绪 / 桃花 / 敏感
  五鬼     变化 / 偏财 / 谋略

------------------------------------------------------------------------

# 8. Summary Template Rules

Template A: {TOP1}为主（{KW1}），整体倾向稳定发展。

Template B: {TOP1}为主（{KW1}），搭配{TOP2}（{KW2}），需注意平衡。

If combination exists in predefined mapping, use mapped sentence.
Otherwise use default Template B.

Only 1--2 short sentences allowed.

------------------------------------------------------------------------

# 9. Suggestion Rules

## Phone Number

If top1: - 天医 / 生气 → 适合长期使用；把握贵人资源。 - 延年 →
适合带团队；注意压力管理。 - 伏位 → 适合稳健路线；避免保守。 - 绝命 /
五鬼 → 适合冲刺阶段；做好风控。 - 祸害 / 六煞 → 适合沟通场景；控制情绪。

------------------------------------------------------------------------

## Car Plate

If top3 includes 祸害 / 绝命 / 五鬼: 驾驶需稳健，避免情绪驾驶。

Else: 整体偏稳，可日常使用。

------------------------------------------------------------------------

# 10. Final Output Structure

Must follow exactly:

### 🔢 数字分析：XXXX

The analysis shall be present in table format.
磁场   |    数字
-------------------
天医   |    13，31
五鬼   |    18，81
延年   |    19，91

[主导磁场]： - Energy (pair)
[能量比例]： - Energy XX%
[综合简评]： Short sentence.
[财务提醒]： (if applicable)
[适用建议]： Short sentence.

⚠ 仅供参考。

------------------------------------------------------------------------

# 11. Implementation Notes

Recommended approach: 1. Generate structured JSON internally 2. Render
standardized text from structured data 3. Do not allow LLM free-form
description 4. Enforce maximum 8--12 lines

This ensures: - Deterministic output - No storytelling - Clean
formatting - RAG-friendly structure
