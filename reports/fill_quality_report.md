# Industry Fill Quality Report

## Executive Summary

The original portfolio contains **50,441 policy records**.

Industry information was originally missing for **17,631 records**, representing **34.95%** of the portfolio.

A deterministic same-client history strategy recovered **16,159 of the 17,631 missing industry values**, representing a **91.65% recovery rate**.

After the recovery process, **1,472 records** remain classified as `Unknown`, representing **2.92%** of the portfolio.

The final portfolio classification coverage is **97.08%**.

Rather than forcing a 100% fill rate, unresolved cases were preserved as `Unknown` when the available data did not provide sufficient evidence for a reliable assignment.

---

## Fill Strategy

The industry completion process followed a conservative hierarchical approach:

1. Preserve all original industry values.
2. Recover missing values from the same `ClientId` when that client has another policy with a known industry.
3. Evaluate supervised machine-learning models using policy-level characteristics.
4. Evaluate client-name text classification.
5. Evaluate high-precision semantic keyword rules.
6. Assess the feasibility of external enrichment.
7. Preserve unresolved cases explicitly as `Unknown`.

Only methods supported by sufficiently reliable evidence were used for automatic assignment.

The objective was not simply to maximize the fill rate, but to improve portfolio coverage while preserving **data integrity and traceability**.

---

## Results

| Fill Method | Records |
|---|---:|
| Original industry | 32,810 |
| Same-client history | 16,159 |
| Unknown | 1,472 |
| **Total** | **50,441** |

### Key Metrics

- **Original missing industries:** 17,631
- **Missing-value recovery rate:** 91.65%
- **Final classified portfolio coverage:** 97.08%
- **Residual unknown rate:** 2.92%

---

## Deterministic Client-History Recovery

Industry consistency was evaluated using clients with at least one known industry value.

Among these clients, no `ClientId` was associated with more than one distinct known industry label.

This consistency supported the use of `ClientId` as a deterministic recovery key.

For records with missing industry information, the industry was recovered when another policy belonging to the same `ClientId` contained a known industry value.

Using this method, **16,159 of the 17,631 originally missing industry values** were recovered.

This approach was prioritized because it relies on direct evidence from the client's own history rather than on a probabilistic prediction based on indirect characteristics.

---

## Alternative Methods Evaluated

### Policy-Level Machine Learning

Supervised classification models using policy-level characteristics were evaluated.

Training and validation data were separated at the **client level** rather than at the individual policy-record level.

This was done to prevent **data leakage** caused by policies belonging to the same client appearing in both the training and validation sets.

The models showed weak predictive performance and did not provide sufficient evidence for reliable automatic industry assignment.

For this reason, policy-level machine learning was not used to fill the remaining missing values.

---

### Client-Name Classification

Client names were evaluated as a potential source of industry information.

A **TF-IDF** text representation combined with **Logistic Regression** achieved:

- **Accuracy:** 6.65%
- **Macro F1:** 6.23%

These results indicate that client names contain limited information for predicting the industry labels used in this portfolio.

In addition, high predicted probabilities did not consistently correspond to correct predictions. Therefore, model probability was not considered sufficient evidence for automatic assignment.

The model was retained as an exploratory analysis but was not used in the final fill process.

---

### Semantic Keyword Rules

Client-name keywords were evaluated at the client level to determine whether specific business terms could provide high-confidence industry signals.

A candidate rule required:

- At least **10 distinct clients**.
- At least **90% industry purity**.

No evaluated keyword satisfied both criteria.

Even semantically suggestive business terms showed low empirical industry purity:

| Keyword | Industry Purity |
|---|---:|
| `inmobiliaria` | 14.1% |
| `constructora` | 14.3% |
| `tecnologias` | 13.7% |
| `agroindustrias` | 16.9% |

These results indicate that, within this dataset, apparently industry-related terms do not reliably identify the target industry classification.

Therefore, semantic keyword rules were rejected for automatic assignment.

---

### External Enrichment

External enrichment was considered for the residual unresolved clients.

However, client names appear synthetic, anonymized, or only weakly related to the actual industry labels.

In addition, the dataset does not provide a reliable external identifier, such as a tax ID, legal entity identifier, or verified company domain, that could be used to confidently match clients with real-world companies.

Under these conditions, external matching could introduce incorrect information rather than improve data quality.

External enrichment was therefore considered too ambiguous for automatic industry assignment and was not used in the final dataset.

---

## Quality Controls

The completed dataset was validated to ensure that the recovery process did not alter the integrity of the original portfolio.

The following controls were applied:

- The final row count remained unchanged at **50,441 records**.
- Original non-null industry values were preserved and never overwritten.
- Same-client assignments were only made when a known industry existed for the corresponding `ClientId`.
- No conflicting known industry labels were observed within the same `ClientId`.
- Each recovered record retains its corresponding `fill_method`.
- Records without sufficient evidence for classification remain explicitly labeled as `Unknown`.

These controls provide **record-level traceability** and make the completion process reproducible and auditable.

---

## Uncertainty Handling

Residual cases that could not be classified with sufficient evidence were explicitly assigned `Unknown`.

After applying the deterministic recovery strategy, **1,472 records** remained unresolved, representing **2.92%** of the complete portfolio.

Alternative methods were explored for these records, including supervised machine learning, client-name classification, semantic keyword rules, and external enrichment.

None provided sufficient reliability to justify automatic assignment.

For this reason, the remaining `Unknown` values were intentionally preserved.

This decision prioritizes **data integrity and transparency** over achieving an artificial 100% fill rate.

The `fill_method` field preserves record-level traceability and distinguishes original values, deterministic recoveries, and unresolved cases.

---

## Conclusion

The industry completion process increased portfolio classification coverage from **65.05% to 97.08%**, while preserving the original industry information and avoiding unsupported predictions.

The strongest recovery signal came from **same-client history**, which allowed **91.65% of the originally missing industry values** to be recovered deterministically.

Additional predictive and semantic approaches were evaluated but were not incorporated into the final fill process because their performance did not provide sufficient evidence for reliable classification.

The final result balances **coverage, reliability, and transparency**:

- **48,969 of 50,441 policy records** have an industry classification.
- **1,472 records** remain explicitly identified as `Unknown`.
