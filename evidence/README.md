# Reading the historical evidence

These seven PNGs and two text companions are preserved byte-for-byte from the submitted repository. They record October 26, 2026 Athena observations. Existing AWS account/session-banner masks remain; technical results were not redrawn or changed.

| Evidence | What to inspect |
|---|---|
| [Customer landing](customer_landing.png) | Raw customer sample and consent fields |
| [Accelerometer landing](accelerometer_landing.png) | Phone user, time, and x/y/z sample |
| [Step-trainer landing](step_trainer_landing.png) | Device serial, time, and distance sample |
| [Customer trusted](customer_trusted.png) | Sample from actual `erica_customer_trusted` |
| [Missing consent](landing-missing-consent.png) | Landing records selected with `IS NULL` |
| [Counts and consent](rubric-counts-and-consent.png) | Full-table count/consent query |
| [Complementary count view](rubric-counts-results.png) | Rows obscured by the sticky footer in the other view |
| [Count query record](rubric-counts-and-consent.txt) | Historical query reference and values |
| [Missing-consent record](landing-missing-consent.txt) | Historical query reference and samples |

Open images at original size for detail. Samples illustrate records; count queries support totals. Neither proves a new cloud run or substitutes for an evaluator report.

[Interpret results](../docs/VALIDATION.md) · [Project home](../README.md)
