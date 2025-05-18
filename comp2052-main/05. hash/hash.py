from werkzeug.security import generate_password_hash, check_password_hash

print()

# Crear un hash
hashed_password = generate_password_hash("secreto")
print('Password Hashed')
print(hashed_password)

# Verificar un hash
is_valid = check_password_hash(hashed_password, "Secreto")
print('Password Validation')
print(is_valid) # True