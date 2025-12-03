# Command Grammar for Maturion Foreman

## How Johan speaks to Maturion
Commands begin with:

“Maturion Foreman, …”

### Examples:
- “Maturion Foreman, begin Threat module architecture review.”
- “Maturion Foreman, generate QA for the PIT integration.”
- “Maturion Foreman, inspect builder output for WRAC.”
- “Maturion Foreman, show me missing architecture requirements.”
- “Maturion Foreman, sequence the Course Crafter build plan.”

## How Maturion speaks to Builder Agents
Builder tasks follow:

“@agent_name:task { … }”

### Examples:
- “@ui-builder:generate_component_map { module: ‘Threat’ }”
- “@api-builder:scaffold_endpoints { module: ‘Vulnerability’ }”
- “@schema-builder:update_schema { module: ‘ERM’ }”
- “@qa-builder:run_tests { module: ‘RA’ }”

## How Builders respond
Builders must:
- produce PRs  
- attach QA reports  
- reference architecture sections  
