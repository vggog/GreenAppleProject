from src.core.config.models import ProjectSetUp


def load_project_set_up() -> ProjectSetUp:
    return ProjectSetUp(
        password_length=8
    )
