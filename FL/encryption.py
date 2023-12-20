import tenseal as ts
import utils

#generate keys
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes = [60, 40, 40, 60]
)
context.generate_galois_keys()
context.global_scale = 2**40

secret_context = context.serialize(save_secret_key = True)
utils.write_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/keys/secret.txt", secret_context)

context.make_context_public()
public_context = context.serialize()
utils.write_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/keys/public.txt", public_context)

#encrypt
context = ts.context_from(utils.read_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/keys/secret.txt"))
salary = [10000]
salary_encrypted = ts.ckks_vector(context, salary)
utils.write_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/outputs/salary_encrypted.txt", salary_encrypted.serialize())

#encrypt increase
#wage_weight = [1.2]
#bonus_weight = [600]
#wage_weight_encrypted = ts.ckks_vector(context, wage_weight)
#bonus_weight_encrypted = ts.ckks_vector(context, bonus_weight)
#write_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/outputs/wage_weight_encrypted", wage_weight_encrypted.serialize())
#write_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/outputs/bonus_weight_encrypted", bonus_weight_encrypted.serialize())

#decryption from encrypted-plain vector
m_proto = utils.read_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/outputs/salary_encrypted_new_with_plain_calculations.txt")
m = ts.lazy_ckks_vector_from(m_proto)
m.link_context(context)

#decryption from encrypted-enctypted vector
# m2_proto = utils.read_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/outputs/salary_encrypted_new_with_encrypted_vectors.txt")
# m2 = ts.lazy_ckks_vector_from(m2_proto)
# m2.link_context(context)

printout = round(m.decrypt()[0], 2)
print(printout)





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