from app.models import User


def check_rights_and_noneless(user, id_, item):
    return (
        user.is_authenticated and
        user.id in (id_, 1) and
        item is not None
    )


def check_users_exists(users_ids):
    return all(User.query.get(user_id) is not None for user_id in users_ids)
