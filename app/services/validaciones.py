def valida_cedula(cedula: str) -> bool:
    """
    Valida una cédula dominicana usando el algoritmo oficial.
    Acepta formato con o sin guiones: 001-0012345-6 o 00100123456
    """
    vc_cedula = cedula.replace("-", "").replace(" ", "")

    if len(vc_cedula) != 11:
        return False

    if not vc_cedula.isdigit():
        return False

    digito_mult = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    vn_total = 0

    for i in range(11):
        v_calculo = int(vc_cedula[i]) * digito_mult[i]
        if v_calculo < 10:
            vn_total += v_calculo
        else:
            vn_total += int(str(v_calculo)[0]) + int(str(v_calculo)[1])

    return vn_total % 10 == 0


def valida_rnc(rnc: str) -> bool:
    """
    Valida un RNC dominicano usando el algoritmo oficial.
    Acepta formato con o sin guiones: 1-31-00124-0 o 131000124
    """
    vc_rnc = rnc.replace("-", "").replace(" ", "")

    if len(vc_rnc) != 9:
        return False

    if not vc_rnc.isdigit():
        return False

    # El primer dígito debe ser 1, 4 o 5
    if vc_rnc[0] not in ("1", "4", "5"):
        return False

    digito_mult = [7, 9, 8, 6, 5, 4, 3, 2]
    v_digito = vc_rnc[8]
    vn_total = 0

    for i in range(8):
        v_calculo = int(vc_rnc[i]) * digito_mult[i]
        vn_total += v_calculo

    residuo = vn_total % 11

    if (residuo == 0 and v_digito == "1") or \
       (residuo == 1 and v_digito == "1") or \
       (str(11 - residuo) == v_digito):
        return True

    return False


def valida_cedula_o_rnc(valor: str) -> tuple[bool, str]:
    """
    Determina si el valor es una cédula o RNC válido.
    Retorna (es_valido, tipo) donde tipo es 'CEDULA', 'RNC' o 'INVALIDO'
    """
    limpio = valor.replace("-", "").replace(" ", "")

    if len(limpio) == 11 and valida_cedula(valor):
        return True, "CEDULA"
    elif len(limpio) == 9 and valida_rnc(valor):
        return True, "RNC"
    else:
        return False, "INVALIDO"
