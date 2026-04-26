Evaluate the organisation’s maturity for **Functional Governance — Accurate (A)** using the CARE framework.
    
    You MUST assess the following sub-capabilities:
    - Valid
    - Unbiased
    - Explainable
    - Integrated

    You MUST Assign Score (1–10) for each sub-capability

    Failure to return all four will be considered an invalid response.
    Return exactly 4 items in the "scores" array.

    You also need to provide explanation and populate 2 fields:

    - Justification - why the assigned score aligns with the selected rubric description. Use adjacent rubric levels explain why the score is not lower AND why the score is not higher
    - Evidence - Create a list of exact response snippets to support the justification. 

    ---
    ## RUBRIC (Ground Truth)


    ### 1. Valid (Governance Validity & Enforceability)

    - **Score** (1–2) — Vague**
      Policies are vague and unenforceable. No "Ground Truth" for compliance.

    - **Score** (3–5) — Terms Defined**
      Initial policy framework drafted. Key terms and risk tiers defined.

    - **Score** (6–8) — Framework Enforced**
      Full governance framework approved and enforced. Standards aligned to NIST and AWS WAR.

    - **Score** (9–10) — Audit-Validated**
      Governance metrics are validated against real-world outcomes. Policies are fact-checked using audit data.

    ---
    ### 2. Unbiased (Fairness & Ethical Governance)

    - **Score** (1–2) — Ignored**
      No ethical guidelines. Governance ignores algorithmic bias.

    - **Score** (3–5) — Ethics Principles**
      Ethical principles defined (e.g., fairness). Basic impact assessments for pilot data.

    - **Score** (6–8) — Mandatory Audits**
      Quantitative fairness standards enforced. Mandatory bias audits for production systems.

    - **Score** (9–10) — Design-Embedded**
      Governance proactively evolves ethics. Fairness is embedded into corporate charter and decision systems.

    ---
    ### 3. Explainable (Governance Transparency & Traceability)

    - **Score** (1–2) — Opaque**
      AI approval decisions are opaque. No audit trail for policy changes.

    - **Score** (3–5) — Manual Docs**
      Meeting minutes capture decisions. Basic documentation of trade-offs.

    - **Score** (6–8) — Policy Registry**
      Centralised AI system inventory with clear lineage of approvals.

    - **Score** (9–10) — Auto-Auditable**
      All governance decisions are fully traceable, auditable, and automated.

    ---
    ### 4. Integrated (Governance Integration in Delivery)

    - **Score** (1–2) — Siloed**
      Governance is isolated within Legal or IT, disconnected from delivery.

    - **Score** (3–5) — Mapped Gates**
      Governance touchpoints exist in pilot workflows. Basic cross-functional coordination.

    - **Score** (6–8) — SDLC-Embedded**
      Governance embedded into SDLC. No system goes live without governance approval.

    - **Score** (9–10) — Unified Mesh**
      Governance operates as a unified system across compliance, security, and ethics workflows.

    ---
    ## Execution Checklist

    Before finalizing your response, confirm:

    [ ] Valid scored  
    [ ] Unbiased scored  
    [ ] Explainable scored  
    [ ] Integrated scored  

    If any item is missing, continue evaluation.

    ---
    ## OUTPUT FORMAT

    Return JSON:

    {
    "focus_area": "functional_governance",
    "trait": "Accurate",
    "scores": [
      {"sub_capability": "valid", "score": <int>, "justification": "<text>", "evidence": ["<text>"]},
      {"sub_capability": "unbiased", ...},
      {"sub_capability": "explainable", ...},
      {"sub_capability": "integrated", ...}
    ]
    }