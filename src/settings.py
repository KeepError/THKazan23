from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    serve_port: int = 22512

    postgres_connection_string: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/bluebox_core_iam"
    )

    class_index_to_class_path: str = "data/class_index2class_name.json"
    log_type_to_class_index_path: str = "data/log_type2class_index.json"

    telegram_jwt_rsa_public_key: str = "public_key"
    web_jwt_key: str = "secret_key"

    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 465
    mail_login: str = "zakupokzakupkovic@gmail.com"
    mail_password: str = "phlo pdqt jrzj bkil"


settings = Settings()
