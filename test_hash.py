
from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash('test_password', method='sha256')
print(hashed_password)
