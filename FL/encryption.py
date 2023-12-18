import tenseal as ts

params = [1000, 2000, 5000, 10000]

def encryption(params):
    context = ts.Context()
    context.generate_galois_keys()
    
    # Encrypt each parameter using a TenSEAL CKKS encoder
    encrypted_params = [ts.ckks_vector(context, p.tolist()) for p in params]
    
    # Serialize encrypted parameters
    encrypted_params_serialized = [ep.serialize() for ep in encrypted_params]
    
    return encrypted_params_serialized

def decryption(encrypted_params_serialized):
    # Initialize TenSEAL context and keys
    context = ts.Context()
    context.generate_galois_keys()
    
    # Deserialize encrypted parameters
    encrypted_params = [ts.ckks_vector_from(context, ep) for ep in encrypted_params_serialized]
    
    # Decrypt each parameter using a TenSEAL CKKS encoder
    decrypted_params = [ep.decrypt() for ep in encrypted_params]
    
    return decrypted_params