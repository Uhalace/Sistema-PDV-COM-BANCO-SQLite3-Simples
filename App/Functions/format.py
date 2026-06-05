def format_reais(cents):
    return f"R$ {cents / 100:.2f}".replace('.', ',')