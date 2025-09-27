from playwright.sync_api import sync_playwright
import time

def plan_actions(intent_data):
    intent = intent_data["intent"]
    entities = intent_data.get("entities", {})

    if intent == "search_product":
        return [
            {"action": "open_page", "url": "https://www.amazon.in"},
            {"action": "type", "selector": "#twotabsearchtextbox", "text": entities.get("product")},
            {"action": "click", "selector": "input.nav-input[type='submit']"},
            {"action": "click_first_product"}
        ]
    else:
        return [{"action": "log", "message": f"Unknown intent: {intent}"}]

def execute_actions(actions):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for act in actions:
            if act["action"] == "open_page":
                page.goto(act["url"])
                time.sleep(3)
            elif act["action"] == "type":
                page.fill(act["selector"], act["text"])
                time.sleep(1)
            elif act["action"] == "click":
                page.click(act["selector"])
                time.sleep(3)
            elif act["action"] == "click_first_product":
                # Click first product from search results
                page.click("div.s-main-slot div[data-component-type='s-search-result'] h2 a")
                time.sleep(3)
            elif act["action"] == "log":
                print(act["message"])

        print("Task Completed ✅")
        browser.close()
