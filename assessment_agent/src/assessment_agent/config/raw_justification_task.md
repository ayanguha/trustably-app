You are generating a justification for a pre-assigned maturity score.

    ---
    ## INPUT (DO NOT MODIFY)

    - Focus Area: {context[focus_area]}
    - Trait: {context[trait]}

    You will receive 4 scored items. Each will have following information 
    - Sub-capability:  {context[N]['sub_capability']}
    - Score:  {context[N]['score']}
    - justification:  {context[N]['justification']}
    - evidence: List {context[N]['evidence']}


    ---
    ## YOUR TASK

    Explain WHY the assigned score is correct.

    You MUST:

    1. Align the evidence to the selected rubric level
    2. Explain why this level fits better than:
       - the level below
       - the level above
    3. Highlight any uncertainty due to missing or weak evidence

    ---
    ## HARD CONSTRAINTS (NON-NEGOTIABLE)

    - Score is LOCKED → DO NOT change it
    - Do NOT introduce new evidence
    - Do NOT infer capabilities not present in evidence
    - Do NOT re-evaluate maturity
    - You must loop through variable to get all sub-capabilities and produce justification for each one of the sub-capabilities. 

    You are explaining a decision, not making one.

    ---
    ## OUTPUT FORMAT (MARKDOWN ONLY)

     ## Focus Area: {context[focus_area]} 
     # Trait: {context[trait]}

    ### Sub-Capability: {context[0]['sub_capability']} 
    ### Score: {context[0]['score'])

    **Rubric Alignment**  
    <Why this level fits>

    **Evidence**  
    - ...
    - ...

    **Boundary Analysis**  
    - Not lower: ...
    - Not higher: ...

    **Confidence**  
    <confidence note>

    ---
    (Repeat for all 4 sub-capabilities)


