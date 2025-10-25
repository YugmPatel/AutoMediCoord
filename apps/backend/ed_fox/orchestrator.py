"""
Template orchestrator module. Add your uAgents Agent here with:

- REST: POST /ems (accept InboundCase)
- REST: GET /cases (return list[CaseStatus])
- fan-out messages to agents (cath, lab, pharmacy, bed, notify)
"""