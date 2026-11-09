
import os
import hmac
import hashlib
import requests

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# -----------------------------------------
# 1. Load Environment Variables
# -----------------------------------------

load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

if not API_KEY or not WEBHOOK_SECRET:
    raise ValueError("API_KEY or WEBHOOK_SECRET missing in .env file")


# -----------------------------------------
# 2. Create Requests Session with Retry
# -----------------------------------------

def create_session() -> requests.Session:

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


# -----------------------------------------
# 3. Fetch Users from REST API
# -----------------------------------------

def get_users(session: requests.Session) -> list:

    url = "https://jsonplaceholder.typicode.com/users"

    response = session.get(url, timeout=30)

    response.raise_for_status()

    return response.json()


# -----------------------------------------
# 4. Print First Five Users
# -----------------------------------------

def print_users(users: list) -> None:

    print("\nFirst 5 Users:")

    for user in users[:5]:

        print(
            f"{user.get('id')} - "
            f"{user.get('name')} - "
            f"{user.get('email')}"
        )


# -----------------------------------------
# 5. Extract First User Details
# -----------------------------------------

def print_first_user_details(users: list) -> None:

    if not users:
        print("No users available")
        return

    first_user = users[0]

    address = first_user.get("address", {})
    geo = address.get("geo", {})
    company = first_user.get("company", {})

    city = address.get("city", "Not Available")
    latitude = geo.get("lat", "Not Available")
    zip_code = address.get("zip", "Not Available")
    company_name = company.get("name", "Not Available")

    print("\nFirst User Details:")

    print(f"City: {city}")
    print(f"Latitude: {latitude}")
    print(f"Zip: {zip_code}")
    print(f"Company: {company_name}")


# -----------------------------------------
# 6. Generate HMAC Signature
# -----------------------------------------

def generate_signature(payload: str, secret: str) -> str:

    signature = hmac.new(
        secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return signature


# -----------------------------------------
# 7. Verify Webhook Signature
# -----------------------------------------

def verify_signature(
    payload: str,
    signature: str,
    secret: str
) -> bool:

    expected_signature = generate_signature(
        payload,
        secret
    )

    return hmac.compare_digest(
        expected_signature,
        signature
    )


# -----------------------------------------
# 8. Test Webhook Security
# -----------------------------------------

def test_webhook_security(secret: str) -> None:

    payload = '{"event": "employee_created", "id": 101}'

    # Generate valid signature
    valid_signature = generate_signature(
        payload,
        secret
    )

    # Tampered payload
    tampered_payload = '{"event": "employee_deleted", "id": 101}'

    # Generate signature using wrong secret
    wrong_signature = generate_signature(
        payload,
        "wrong_secret"
    )

    valid = verify_signature(
        payload,
        valid_signature,
        secret
    )

    tampered = verify_signature(
        tampered_payload,
        valid_signature,
        secret
    )

    wrong_secret = verify_signature(
        payload,
        wrong_signature,
        secret
    )

    print("\nWebhook Security Results:")

    print(
        f"Valid: {valid} | "
        f"Tampered: {tampered} | "
        f"Wrong secret: {wrong_secret}"
    )


# -----------------------------------------
# 9. Main Function
# -----------------------------------------

def main() -> None:

    session = create_session()

    try:

        users = get_users(session)

        print_users(users)

        print_first_user_details(users)

        test_webhook_security(WEBHOOK_SECRET)

    except requests.RequestException as error:

        print(f"API Request Error: {error}")

    finally:

        session.close()


# -----------------------------------------
# 10. Program Entry Point
# -----------------------------------------

if __name__ == "__main__":
    main()
