import json
from actions import plan_actions, execute_actions

# Load intent classifier output
with open("sample_input.json") as f:
    intent_data = json.load(f)

# Convert intent into browser actions
actions = plan_actions(intent_data)

# Execute the actions automatically
execute_actions(actions)
