from app.models.user import UserRole


USER_ROLE_LABELS = {
    UserRole.admin.value: "Администратор",
    UserRole.staff.value: "Менеджер",
    UserRole.customer.value: "Клиент",
}


WEB_USER_ROLES = tuple(USER_ROLE_LABELS.keys())
