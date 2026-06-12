
def format_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, str(cnpj)))

    if len(cnpj) != 14:
        return cnpj

    return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
