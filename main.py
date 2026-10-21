import json
import logging
import random
import string
import time
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class TemporaMailClient:
    def __init__(
        self,
        domain: str = "temporamail.uk",
        email_length: int = 10,
        base_url: str = "https://temporamail.uk",
    ):
        self.domain = domain
        self.email_length = email_length
        self.base_url = base_url
        self.logger = logging.getLogger(self.__class__.__name__)
        self.email_address = self._generate_random_email()

    def _generate_random_email(self) -> str:
        letters = string.ascii_lowercase + string.digits
        random_string = "".join(
            random.choice(letters) for _ in range(self.email_length)
        )
        return f"{random_string}@{self.domain}"

    def get_email_address(self) -> str:
        return self.email_address

    def check_inbox(self) -> list:
        url = f"{self.base_url}/emails/{self.email_address}"
        params = {"limit": 20, "offset": 0}

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("result", [])
            self.logger.warning(f"Failed to fetch inbox. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error while checking inbox: {e}")

        return []

    def get_email_content(self, email_id: str) -> dict:
        url = f"{self.base_url}/inbox/{email_id}"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("result", {})
            self.logger.warning(f"Failed to fetch email ID {email_id}. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error while fetching email ID {email_id}: {e}")

        return {}

    def wait_for_email(self, timeout_seconds: int = 70, poll_interval: int = 5) -> list:
        self.logger.info(f"Target email address: {self.email_address}")
        self.logger.info(f"Waiting up to {timeout_seconds} seconds for incoming mail...")

        start_time = time.time()

        while time.time() - start_time < timeout_seconds:
            messages = self.check_inbox()
            if messages:
                self.logger.info(f"Found {len(messages)} new message(s). Fetching details...")

                detailed_messages = []
                for msg in messages:
                    email_id = msg.get("id")
                    content = self.get_email_content(email_id)
                    if content:
                        detailed_messages.append(content)

                return detailed_messages

            time.sleep(poll_interval)

        self.logger.warning(f"Timed out after {timeout_seconds} seconds. No emails received.")
        return []


if __name__ == "__main__":
    mail_client = TemporaMailClient()
    received_emails = mail_client.wait_for_email(timeout_seconds=70, poll_interval=5)

    if received_emails:
        logging.info("--- Received Email Details ---")
        for email_detail in received_emails:
            print(json.dumps(email_detail, indent=4))
    else:
        logging.info("No messages processed.")
