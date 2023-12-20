import tenseal as ts
import utils

context = ts.context_from(utils.read_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/keys/public.txt"))

#calculations with encrypted-plain vectors
salary_proto = utils.read_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/outputs/salary_encrypted.txt")
salary_encrypted = ts.lazy_ckks_vector_from(salary_proto)
salary_encrypted.link_context(context)

#wage increas 20% -> 1.2
wage_increase_rate_plain = ts.plain_tensor([1.2])

#bonus 600 kr
bonus_increase_rate_plain = ts.plain_tensor([600])

salary_new_encrypted = (salary_encrypted * wage_increase_rate_plain) + bonus_increase_rate_plain

utils.write_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/outputs/salary_encrypted_new_with_plain_calculations.txt", salary_new_encrypted.serialize())

#calculations with encrypted-encrypted vectors
# w_proto = utils.read_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/outputs/wage_weight.txt")
# w = ts.lazy_ckks_vector_from(w_proto)
# w.link_context(context)

# b_proto = utils.read_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/outputs/bonus_weight.txt")
# b = ts.lazy_ckks_vector_from(w_proto)
# b.link_context(context)

# salary_encrypted_new_v2 = (salary_encrypted * w) + b
# utils.write_data("/Users/jespervestin/Documents/GitHub/Federated-Learning/FL/outputs/salary_encrypted_new_with_enctypted_vectors.txt")