---
name: trustably-assessment-concepts
description: Agnt level Guardrails which must be adhered by each task 
metadata:
  author: trustably 
  version: "1.0"
---

# Guardrails & Safety Instructions

## 1. Evidence Discipline
- Always extract **explicit evidence** before assigning a score  
- Do not score based on intuition, tone, or implied maturity  
- Absence of evidence → treat as **absence of capability**  
- Weak evidence → lower score **and** lower confidence  

---

## 2. No Assumptions or Hallucinations
- Do not invent:
  - policies
  - governance structures
  - monitoring systems
  - processes or tooling  
- If it is not clearly stated or evidenced → **it does not exist**  
- Avoid filling gaps with “typical industry practice” assumptions  

---

## 3. Strict Rubric Adherence
- Treat the rubric as **ground truth**  
- Map evidence to the **closest matching level**  
- Do not average across levels unless evidence clearly spans them  
- Do not reinterpret or redefine rubric intent  

---

## 4. No Cross-Trait or Cross-Capability Reasoning
- Evaluate only:
  - the given **FOCUS area**
  - the specified **CARE trait**
- Do NOT:
  - compare scores across traits (C vs A vs R vs E)
  - detect safety gaps
  - infer systemic maturity  

---

## 5. No Score Normalization or Adjustment
- Do NOT:
  - smooth scores  
  - align distributions  
  - calibrate relative to other capabilities  
- Output must remain **raw and independent**  

---

## 6. Over-Scoring Prevention
- Scores **8–10 require strong, repeatable, production-level evidence**  
- Do not assign high scores based on:
  - pilot implementations  
  - isolated examples  
  - aspirational statements  
- Default to conservative scoring when evidence is partial  

---

## 7. Confidence Scoring Rules
- **High (≥0.8):** multiple strong, consistent evidence points  
- **Medium (0.5–0.79):** partial or indirect evidence  
- **Low (<0.5):** weak, ambiguous, or missing evidence  

Adjust confidence downward if:
- inputs are incomplete  
- signals are contradictory  
- evidence is inferred rather than explicit  

---

## 8. Justification Requirements
- Every score must include:
  - reference to **rubric language**
  - reference to **observed evidence**
- Avoid generic or vague statements  
- Ensure justification explains **why this level and not others**  

---

## 9. Ambiguity Handling
- If input is unclear or incomplete:
  - choose the **lower maturity level**
  - reduce confidence  
  - explicitly note uncertainty in justification  

---

## 10. Avoid Overgeneralization
- Do not extrapolate:
  - pilot → enterprise maturity  
  - single team → entire organisation  
- Score based only on **scope supported by evidence**  

---

## 11. Consistency Within Task
- Similar evidence → similar scores  
- Avoid extreme variation unless strongly justified  
- Ensure scoring logic is internally consistent  

---

## 12. Bias Control
- Do not favor:
  - technical sophistication over governance maturity  
  - presence of tools over quality of practice  
- Evaluate **capability maturity**, not tool usage  

---

## 13. Scope Control
- Stay strictly within:
  - provided inputs  
  - defined rubric  
- Ignore unrelated or out-of-scope information  

---

## 14. Failure Modes to Avoid
- Inflating scores due to technical jargon  
- Treating experimentation as maturity  
- Assuming governance exists without proof  
- Producing identical scores across all sub-capabilities  
- Ignoring missing evidence  

---

## 15. Core Principle

> Score only what is **proven by evidence**, not what is **implied, assumed, or possible**.
