import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'routing-logic'))

from routing_engine import RoutingEngine

class Orchestrator:
    def __init__(self):
        self.router = RoutingEngine()

    def parse_issue(self, issue_text):
        """
        Mock classification logic.
        """
        issue_text = issue_text.lower()
        if "security" in issue_text or "vulnerability" in issue_text:
            return "security", 8
        elif "bug" in issue_text or "fix" in issue_text:
            return "bug", 4
        elif "docs" in issue_text or "readme" in issue_text:
            return "docs", 2
        else:
            return "feature", 9

    def process_issue(self, title, body):
        print(f"--- Orchestrator received issue ---")
        print(f"Title: {title}")
        category, complexity = self.parse_issue(title + " " + body)
        print(f"Classified as: {category.upper()} (Complexity: {complexity})")
        
        agent = self.router.route_issue(category, complexity)
        print(f"Routing to Agent: {agent['name']} ({agent['id']}) - Cost: ${agent['cost_per_token']}/token")
        print(f"Security Clearance: {agent['security_clearance'].upper()}")
        print("---")

if __name__ == "__main__":
    orchestrator = Orchestrator()
    
    # Test cases
    orchestrator.process_issue("Security vulnerability in login", "We found a leaked token in the API.")
    orchestrator.process_issue("Add new payment gateway", "Integrate Stripe API for the new checkout flow. Needs extensive testing.")
    orchestrator.process_issue("Fix typo in README", "Just a small typo in the install instructions.")
