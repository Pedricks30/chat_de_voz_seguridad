def calcular_horas_reales(dias_mes, horas_dia, trabajadores, meses_anio, nv, np, n_be):
    """Calcula las horas realmente trabajadas"""
    horas_totales = dias_mes * horas_dia * trabajadores * meses_anio
    return horas_totales - nv - np - n_be

def calcular_jornadas_perdidas(muertes, brazos, piernas, j2_directo=None):
    """Calcula las jornadas perdidas totales"""
    if j2_directo is not None:
        return j2_directo
    return (muertes * 6000) + (brazos * 4500) + (piernas * 3000)

def calcular_indice_frecuencia(accidentes, nr):
    """Calcula el índice de frecuencia"""
    return (accidentes * 1000000) / nr if nr > 0 else 0

def calcular_indice_gravedad(jornadas_perdidas, nr):
    """Calcula el índice de gravedad"""
    return (jornadas_perdidas * 1000000) / nr if nr > 0 else 0

def calcular_indice_incidencia(accidentes, trabajadores):
    """Calcula el índice de incidencia"""
    return (accidentes * 1000) / trabajadores if trabajadores > 0 else 0

def interpretar_if(if_valor):
    """Interpreta el índice de frecuencia"""
    if if_valor < 5:
        return "Excelente desempeño en seguridad"
    elif 5 <= if_valor < 15:
        return "Buen desempeño, oportunidades de mejora"
    elif 15 <= if_valor < 25:
        return "Requiere atención prioritaria"
    else:
        return "Situación crítica, revisión inmediata"

def interpretar_ig(ig_valor):
    """Interpreta el índice de gravedad"""
    if ig_valor < 100:
        return "Accidentes con baja severidad"
    elif 100 <= ig_valor < 500:
        return "Severidad moderada"
    else:
        return "Alta severidad, revisar protocolos"