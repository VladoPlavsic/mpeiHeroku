from app.db.repositories.parsers import string_or_null

def create_payment_request_query(user_fk: int, offer_fk: int, payment_id: str, level: int, confirmation_token: str):
    return \
        f"SELECT subscriptions.create_subscription_pending({user_fk}, {offer_fk}, {string_or_null(payment_id)}, {level}, {string_or_null(confirmation_token)})"

def check_payment_request_query(user_fk: int, offer_fk: int, level: int):
    return \
        f"SELECT subscriptions.check_subscription_pending({user_fk}, {offer_fk}, {level}) AS payment_id"

def get_payment_request_query(payment_id: str):
    return \
        f"SELECT (subscriptions.get_subscription_pending({string_or_null(payment_id)})).*"

def get_offer_details_query(level: int, offer_fk: int):
    return \
        f"SELECT (subscriptions.get_offer_details({level}, {offer_fk})).*"

def get_plan_details_query(level: int, plan_fk: int) -> str:
    return \
        f"SELECT (subscriptions.get_plan_details({level}, {plan_fk})).*"

def delete_expired_subscriptions_query() -> str:
    return \
        f"SELECT users.delete_expired_subscriptions()"

def delete_pending_subscripiton_query(payment_id: str) -> str:
    return \
        f"SELECT subscriptions.delete_subscription_pending({string_or_null(payment_id)})"