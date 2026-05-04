import plotly.express as px
import pandas as pd
import numpy as np

# 1. SETUP THE FRAMEWORK STRUCTURE
focus_areas = ['Culture', 'Functional Governance', 'Security', 'Unified Platform', 'Observability']
care_structure = {
    'Consistent': ['Strategic', 'Viable', 'Resilient'],
    'Accurate': ['Valid', 'Unbiased', 'Explainable', 'Integrated'],
    'Reliable': ['Observable', 'Transparent', 'Accountable', 'Interoperable'],
    'Effective': ['Desirable', 'Secure', 'Context-Aware', 'Safe']
}

sub_caps = []
for trait, caps in care_structure.items():
    prefix = trait[0]
    for cap in caps:
        sub_caps.append(f"{prefix}: {cap}")

# 2. GENERATE "LONG FORMAT" DATA
# To make a density map meaningful, we simulate 5 different assessors 
# scoring the same 75 cells. This creates "density" of scores.
all_observations = []

for assessor in range(1): # 5 different people scoring
    for focus in focus_areas:
        for trait in care_structure:
            for sub_cap in care_structure[trait]:

                # Simulate a score with some variance around a mean
                score = np.random.randint(1, 11) 
                all_observations.append({
                    'Focus Area': focus,
                    'Sub-capability':  sub_cap,
                    'Trait': trait,
                    'Score': score
                })

df_long = pd.DataFrame(all_observations)

for obs in all_observations:
    print(f"observations: {obs}")

print(len(all_observations))
# 3. CREATE THE DENSITY HEATMAP
'''fig = px.density_heatmap(
    df_long, 
    # Pass the hierarchy here: Trait first, then Sub-cap
    x= "Sub-capability", 
    y="Focus Area", 
    z="Score", 
    #facet_col = "Focus Area", facet_row = "Trait",
    text_auto = True,
    color_continuous_scale='oranges',
    template='plotly_dark',
    title="Trustably Density Heatmap: CARE Traits Grouped"
)
'''
fig = px.treemap(df_long, 
                path = ["Focus Area", "Trait", "Sub-capability"], 
                color = "Score", 
                color_continuous_scale = "viridis", 
                template='plotly_dark',
                custom_data=["Score"],
                title="Trustably Density Heatmap: CARE Traits Grouped")

# 4. THE CRITICAL STYLING FIX


fig.update_layout(
    font_family="Inter, Arial, sans-serif",
    width=1400, # Increased width to accommodate the groups
    height=600,
    margin=dict(b=100) # Give space for the two-level labels
)


fig.update_traces(
    marker=dict(cornerradius=5),
    texttemplate="<b>%{label}</b><br>Score: %{customdata[0]}",
    textinfo="label+text",
    hovertemplate='<b>%{label}</b><br>Maturity Score: %{customdata[0]}<extra></extra>'
)

fig.write_image("/Users/ayanguha/projects/trustably-app/static/chart.png")
