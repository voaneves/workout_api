from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe para gerenciar as configurações da aplicação.
    Ela lê as variáveis de um arquivo .env.
    """
    model_config = SettingsConfigDict(
        env_file='.env',   # Especifica o nome do arquivo de onde ler as variáveis
        extra='ignore'     # Ignora variáveis extras que não foram definidas aqui
    )

    DATABASE_URL: str  # Define que a variável DATABASE_URL é esperada e deve ser uma string
    API_SECRET_KEY: str
    API_ALGORITHM: str


# Cria uma instância única das configurações para ser usada em todo o projeto
settings = Settings()
