from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def veify_password(plain_password, hashed_password):
    # Проверка полученного хэша с существующим
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    # Получение хэша строки
    return pwd_context.hash(password)
