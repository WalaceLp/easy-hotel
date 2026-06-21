def limpar_cpf(cpf: str) -> str:
    return "".join(char for char in cpf if char.isdigit())


def cpf_valido(cpf: str) -> bool:
    cpf_limpo = limpar_cpf(cpf)
    if len(cpf_limpo) != 11 or cpf_limpo == cpf_limpo[0] * 11:
        return False

    for tamanho in (9, 10):
        soma = sum(int(cpf_limpo[indice]) * (tamanho + 1 - indice) for indice in range(tamanho))
        digito = (soma * 10) % 11
        digito = 0 if digito == 10 else digito
        if digito != int(cpf_limpo[tamanho]):
            return False

    return True
