import tenseal as ts
from utils import write_data, read_data

#params = [1000, 2000, 5000, 10000]

#generate keys
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8912,
    coeff_mod_bit_sizes = [60, 40, 40, 60]
)
context.generate_galois_keys()
context.global_scale = 2**40

secret_context = context.serialize(save_secret_key = True)
write_data("./keys/secret.txt", secret_context)

context.make_context_public()
public_context = context.serialize()
write_data("./keys/public.txt", public_context)

#encrypt
context = ts.context_from(read_data("./keys/secret.txt"))
salary = [10000]
salary_encrypted = ts.ckks_vector(context, salary)
write_data("./outputs/salary_encrypted.txt", salary_encrypted.serialize())

#decryption
m_proto = read_data("./outputs/salary_encrypted_new_with_plain_calculations.txt")
m = ts.lazy_ckks_vector_from(m_proto)
m.link_context(context)

round(m.decrypt()[0], 2)

# def encryption(params):
#     context = ts.Context()
#     context.generate_galois_keys()
    
#     # Encrypt each parameter using a TenSEAL CKKS encoder
#     encrypted_params = [ts.ckks_vector(context, p.tolist()) for p in params]
    
#     # Serialize encrypted parameters
#     encrypted_params_serialized = [ep.serialize() for ep in encrypted_params]
    
#     return encrypted_params_serialized

# def decryption(encrypted_params_serialized):
#     # Initialize TenSEAL context and keys
#     context = ts.Context()
#     context.generate_galois_keys()
    
#     # Deserialize encrypted parameters
#     encrypted_params = [ts.ckks_vector_from(context, ep) for ep in encrypted_params_serialized]
    
#     # Decrypt each parameter using a TenSEAL CKKS encoder
#     decrypted_params = [ep.decrypt() for ep in encrypted_params]
    
#     return decrypted_params