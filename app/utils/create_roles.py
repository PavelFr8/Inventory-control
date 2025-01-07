from app import db, logger
from app.models import Role


def create_roles():
    """
    Создаёт в БД роли пользователей
    """
    roles = ['user', 'admin']

    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            role = Role(name=role_name)
            db.session.add(role)

    db.session.commit()
    logger.info("Rolls successfully added.")
