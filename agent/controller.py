from tools.log_analyzer import analyze_uipath_logs
from datetime import datetime


class RPABotFailureAgent:
    def __init__(self, log_path: str):
        self.log_path = log_path
        self.decision_log = []

    def plan(self):
        return "Analyze logs, identify root cause, decide next action"

    def observe(self):
        return analyze_uipath_logs(self.log_path)

    def decide(self, analysis: dict) -> dict:
        root = analysis.get("root_cause", {})
        failure_type = root.get("failure_type")
        severity = root.get("severity")
        confidence = root.get("confidence", 0)

        # --- POLICY RULES ---
        if confidence < 0.6:
            return self.escalate("Low confidence in diagnosis")

        if failure_type == "business_exception":
            return self.escalate(root["recommended_action"])

        if failure_type == "technical_exception":
            if severity == "low":
                return self.retry()
            return self.create_ticket(root)

        return self.no_action()

    def act(self, decision: dict):
        self.decision_log.append(decision)
        return decision

    # ---------- ACTIONS ----------
    def retry(self):
        return {
            "action": "retry_bot",
            "reason": "Low severity technical issue",
            "timestamp": self._now()
        }

    def escalate(self, reason: str):
        return {
            "action": "escalate_to_business",
            "reason": reason,
            "timestamp": self._now()
        }

    def create_ticket(self, root):
        return {
            "action": "create_ticket",
            "ticket_payload": {
                "summary": f"RPA Bot Failure: {root['subcategory']}",
                "severity": root["severity"],
                "details": root["recommended_action"]
            },
            "timestamp": self._now()
        }

    def no_action(self):
        return {
            "action": "no_action",
            "reason": "No critical failure detected",
            "timestamp": self._now()
        }

    def run(self):
        plan = self.plan()
        observation = self.observe()
        decision = self.decide(observation)
        result = self.act(decision)

        return {
            "plan": plan,
            "analysis": observation,
            "decision": result
        }

    def _now(self):
        return datetime.utcnow().isoformat()
