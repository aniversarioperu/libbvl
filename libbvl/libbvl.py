#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Libreria libbvl para obtener datos y ratios de la Bolsa de Valores de
   Lima

"""

from obtener_data import obtener_data_bolsa
from funciones_csv import generar_csv
from config import TRIMESTRE_INICIAL, TRIMESTRE_FINAL, DICT_EMPRESAS

def ratios_empresa(codigo_empresa, anho_ini, trim_ini, anho_fin, trim_fin):
    """Regresa una lista de diccionarios, donde cada diccionario son los
    ratios de un trimestre"""

    datos_anhos = []

    # Se iteran los años
    for anho in range (anho_ini, anho_fin+1):
        # Los trimestres inicial y final tienes los valores por defecto (1 y 4)
        # a menos que sean del año inicial y final, en cuyo caso tienen los
        # valores ingresados como parámetros para el rango de fechas
        trimestre_ini = TRIMESTRE_INICIAL
        trimestre_fin = TRIMESTRE_FINAL
        if anho == anho_ini:
            trimestre_ini = trim_ini
        if anho == anho_fin:
            trimestre_fin = trim_fin

        # Se iteran los trimestres por cada año
        for trimestre in range(trimestre_ini, trimestre_fin+1):
            # Se obtienen los ratios de la función generar_ratios
            ratios = generar_ratios(obtener_data_bolsa(codigo_empresa,
                                            str(trimestre), str(anho)))
            # Si no existe el url debido a que aún se ha llegado al trimestre
            # solicitado ratios es False y se cierra el bucle
            if ratios:
                datos_anhos.append(ratios)
            else:
                break

    return datos_anhos

def datos_empresa(codigo_empresa, anho_ini, trim_ini, anho_fin, trim_fin):
    """Regresa una lista de diccionarios, donde cada diccionario son los datos
    de un trimestre"""

    datos_anhos = []

    # Se iteran los años
    for anho in range (anho_ini, anho_fin+1):
        # Los trimestres inicial y final tienes los valores por defecto (1 y 4)
        # a menos que sean del año inicial y final, en cuyo caso tienen los
        # valores ingresados como parámetros para el rango de fechas
        trimestre_ini = TRIMESTRE_INICIAL
        trimestre_fin = TRIMESTRE_FINAL
        if anho == anho_ini:
            trimestre_ini = trim_ini
        if anho == anho_fin:
            trimestre_fin = trim_fin

        # Se iteran los trimestres por cada año
        for trimestre in range(trimestre_ini, trimestre_fin+1):
            # Se obtienen los ratios de la función generar_ratios
            datos = obtener_data_bolsa(codigo_empresa, str(trimestre),
                                                             str(anho))
            datos_anhos.append(datos)

            # Luego de los trimestres se agregan los reportes anuales auditados
            if trimestre == trimestre_fin:
                datos = obtener_data_bolsa(codigo_empresa, 'A', str(anho))
                datos_anhos.append(datos)

    return datos_anhos


def datos_empresa_csv(codigo_empresa, anho_ini, trim_ini, anho_fin, trim_fin, \
                                             nombre_archivo='', directorio='.'):
    """Graba en un archivo csv el resultado de obtener los datos de la
    empresa"""

    datos = datos_empresa(codigo_empresa, anho_ini, trim_ini, anho_fin,
                                                               trim_fin)
    try:
        generar_csv(datos, DICT_EMPRESAS[codigo_empresa], nombre_archivo,
                                                              directorio)
    except IOError:
        return False

    return True


def ratios_empresa_csv(codigo_empresa, anho_ini, trim_ini, anho_fin, trim_fin,
                                             nombre_archivo='', directorio='.'):
    """Graba en un archivo csv el resultado de obtener los ratios de la
    empresa"""

    ratios = ratios_empresa(codigo_empresa, anho_ini, trim_ini, anho_fin,
                                                                   trim_fin)
    try:
        generar_csv(ratios, DICT_EMPRESAS[codigo_empresa], nombre_archivo, directorio)
    except IOError:
        return False


def generar_ratios(data):
    """Se utilizan los datos obtenidos de los reportes financieros para generar
    ratios"""

    #Se identifica si la data es valida
    if (data):

        variables = {}

        variables['periodo'] = data['periodo']

        variables['roa'] = round(data['ing_act_ord']/data['activos'], 3)
        variables['roe'] = round(data['ing_act_ord']/data['valor_libros'], 3)
        variables['roa_fc'] = round(data['flujo_efectivo']/data['activos'], 3)

        #Si no hay utilidades,el ratio es cero
        if data['utilidades']:
            variables['ratio_dividendos_utilidades'] = round(
                      data['dividendos']/data['utilidades'], 3)
        else:
            variables['ratio_dividendos_utilidades'] = 0

        #Si los ingresos son mayores que el flujo de efectivo hay ajustes
        if data['ing_act_ord'] > data['flujo_efectivo']:
            variables['ajustes']  = 1
        else:
            variables['ajustes']  = 0

        variables['liquidez'] = \
        round(data['act_circulante']/data['deuda_corto_plazo'], 3)
        variables['ratio_deuda_largo_plazo'] = \
        round(data['deuda_largo_plazo']/data['activos'], 3)
        variables['emision_acciones'] = int(data['emision_acciones'])
        variables['utilidades'] = round(data['utilidades'], 3)

        return variables
    else:
        return False




