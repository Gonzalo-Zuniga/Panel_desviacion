# modelo/scoring.py

import sys
import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

# -------------------------------------------------------------------
# 1. Validar argumentos
# -------------------------------------------------------------------
if len(sys.argv) < 2:
    print(json.dumps({"error": "No se recibió la ruta del archivo CSV"}))
    sys.exit(1)

ruta_csv = sys.argv[1]

if not os.path.exists(ruta_csv):
    print(json.dumps({"error": "El archivo CSV no existe en el servidor"}))
    sys.exit(1)

# -------------------------------------------------------------------
# 2. Carga de datos crudos
# -------------------------------------------------------------------
try:
    df = pd.read_csv(ruta_csv)
except Exception as e:
    print(json.dumps({"error": f"No se pudo leer el CSV: {str(e)}"}))
    sys.exit(1)

# Verificación mínima de columnas originales
cols_minimas = [
    "ID", "rule_name", "FECHA_CREACION", "HORA_CREACION",
    "TIPO", "token_rut"
]
faltan = [c for c in cols_minimas if c not in df.columns]
if faltan:
    print(json.dumps({"error": f"Faltan columnas básicas en el CSV: {faltan}"}))
    sys.exit(1)

# -------------------------------------------------------------------
# 3. Limpieza de textos (Celda 3)
# -------------------------------------------------------------------
cols_texto = ['rule_name', 'ID', 'token_rut', 'TIPO']
for c in cols_texto:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.upper()

# Diccionario de normalización de nombres de reglas (RULE_NORM)
map_rulename = {
    'OS_WPP_WEB RECAUDA.3ROS HITES': 'OS_WPP_WEB_RECAUDA.3ROS_HITES',
    'OS_WEBPAY_WEB LIDER.CL':        'OS_WEBPAY_WEB_LIDER.CL',
    'OS_WEBPAY HITES':               'OS_WEBPAY_HITES',
    'OS_WEBPAY WEB PAGADOOR':        'OS_WEBPAY_WEB_PAGADOOR',
    'OS_WEBPAY PRONTO PAGA':         'OS_WEBPAY_PRONTO_PAGA',
    'ALERT GOOGLE':                  'ALERT_GOOGLE',
    'ALERTA BILLETERA BE PAY':       'ALERTA_BILLETERA_BE_PAY',
    'CC S.ALERTA BILLETERA DATE TOKEN': 'CC_S.ALERTA_BILLETERA_DATE_TOKEN',
    'CC BLOQ TARJETA FUERZA BRUTA':  'CC_BLOQ_TARJETA_FUERZA_BRUTA',
    'OS_WEBPAY_WEB LIDER ONE CLICK': 'OS_WEBPAY_WEB_LIDER_ONE_CLICK',
    'OS_WEBPAY LIDER ONE CLICK':     'OS_WEBPAY_WEB_LIDER_ONE_CLICK',
    'CC CCIO PRUEBA BANDA':          'CC_CCIO_PRUEBA_BANDA',
    'CC ECOMMERCE SCORE ALTO':       'CC_ECOMMERCE_SCORE_ALTO',
    'CC FACEBOOK 2.0':               'CC_FACEBOOK_2.0',
    'CC LC ALERT POR MONTO':         'CC_LC_ALERT_POR_MONTO',
    'CC VALIDA PRIM. TRX MP WALLET': 'CC_VALIDA_PRIM._TRX_MP_WALLET',
    'CC SUPLANTACION 3DS':           'CC_SUPLANTACION_3DS',
    'CC TX CONSECUTIVA ECOMMERCE':   'CC_TX_CONSECUTIVA_ECOMMERCE',
    'CC TX PARALELAS NAC INT':       'CC_TX_PARALELAS_NAC_INT',
    'OS WEB MONEYGRAM PAYMENT':      'OS_WEB_MONEYGRAM_PAYMENT',
    'OS WEB PK COMERCIOS EN LINEA':  'OS_WEB_PK_COMERCIOS_EN_LINEA',
    'OS WEBPAY AFEX':                'OS_WEBPAY_AFEX',
    'CC PILOTO SCORE VAAI':          'CC_PILOTO_SCORE_VAAI',
    'OS WEBPAY ALPS Y NUVEI':        'OS_WEBPAY_ALPS_Y_NUVEI'
}

df['RULE_NORM'] = df['rule_name'].map(map_rulename).fillna(df['rule_name'])
df['RULE_NORM'] = (
    df['RULE_NORM']
    .str.replace(" ", "_", regex=False)
    .str.replace("__+", "_", regex=True)
)

# -------------------------------------------------------------------
# 4. Construcción de ALERTA (Celda 3)
# -------------------------------------------------------------------
id_str = df['ID'].astype(str).str.strip()
mask_num = id_str.str.fullmatch(r"\d+")
prefijo_id = id_str.str.extract(r"^([^-\s]+-[^-]+)", expand=False)

df['ALERTA'] = np.where(mask_num, df['RULE_NORM'], prefijo_id.fillna(df['RULE_NORM']))
df['ALERTA'] = (
    df['ALERTA']
    .str.replace(" ", "_", regex=False)
    .str.replace("__+", "_", regex=True)
)

# Identificador numérico de cliente
df['CLIENTE_ID'] = df['token_rut'].astype('category').cat.codes.astype('int64')

# Construcción de FECHA_ALERTA
df['FECHA_ALERTA'] = pd.to_datetime(
    df['FECHA_CREACION'].astype(str) + " " + df['HORA_CREACION'].astype(str),
    format="%d-%m-%Y %H:%M:%S",
    errors='coerce'
)

# Codificación numérica de tipo de alerta
df['TIPO_N'] = df['TIPO'].map({'MANUAL': 1, 'AUTOMATICA': 2}).astype('int64')

# FECHA_ALERTA solo fecha
df['FECHA_ALERTA'] = pd.to_datetime(df['FECHA_ALERTA']).dt.date
df['FECHA_ALERTA'] = pd.to_datetime(df['FECHA_ALERTA'])
df = df.dropna(subset=['FECHA_ALERTA'])

# -------------------------------------------------------------------
# 5. Agrupación diaria df_diario (cant_diaria, rut_unicos_diarios)
# -------------------------------------------------------------------
df_diario = (
    df.groupby(['FECHA_ALERTA', 'ALERTA'], as_index=False)
      .agg(
          cant_diaria=('ID', 'count'),
          rut_unicos_diarios=('CLIENTE_ID', 'nunique')
      )
)

# Variables de calendario
df_diario['anio'] = df_diario['FECHA_ALERTA'].dt.year
df_diario['mes'] = df_diario['FECHA_ALERTA'].dt.month
df_diario['semana'] = df_diario['FECHA_ALERTA'].dt.isocalendar().week.astype(int)
df_diario['dia_mes'] = df_diario['FECHA_ALERTA'].dt.day

# -------------------------------------------------------------------
# 6. Cantidades semanales/mensuales y RUTs (Celdas 4 y 5)
# -------------------------------------------------------------------
# Cantidad semanal por ALERTA
df_diario['cant_semana'] = df_diario.groupby(
    ['ALERTA', 'anio', 'semana']
)['cant_diaria'].transform('sum')

# Cantidad mensual por ALERTA
df_diario['cant_mes'] = df_diario.groupby(
    ['ALERTA', 'anio', 'mes']
)['cant_diaria'].transform('sum')

# RUTs únicos por semana
df_diario['rut_semana'] = df_diario.groupby(
    ['ALERTA', 'anio', 'semana']
)['rut_unicos_diarios'].transform('sum')

# RUTs únicos por mes
df_diario['rut_mes'] = df_diario.groupby(
    ['ALERTA', 'anio', 'mes']
)['rut_unicos_diarios'].transform('sum')

# -------------------------------------------------------------------
# 7. Semana del mes e inicio de mes (Celda 6)
# -------------------------------------------------------------------
df_diario['semana_mes'] = ((df_diario['dia_mes'] - 1) // 7) + 1
df_diario['es_inicio_mes'] = (df_diario['dia_mes'] <= 7).astype(int)

# -------------------------------------------------------------------
# 8. Cambio semana a semana (Celda 7)
# -------------------------------------------------------------------
df_sem = df_diario[['ALERTA', 'anio', 'semana', 'cant_semana']].drop_duplicates()
df_sem = df_sem.sort_values(by=['ALERTA', 'anio', 'semana'])
df_sem['cant_semana_prev'] = df_sem.groupby('ALERTA')['cant_semana'].shift(1)

df_sem['pct_cambio_semana'] = (
    (df_sem['cant_semana'] - df_sem['cant_semana_prev']) /
    df_sem['cant_semana_prev']
)
df_sem['pct_cambio_semana'] = df_sem['pct_cambio_semana'] \
    .replace([np.inf, -np.inf], np.nan).fillna(0)

df_diario = df_diario.merge(
    df_sem[['ALERTA', 'anio', 'semana', 'cant_semana_prev', 'pct_cambio_semana']],
    on=['ALERTA', 'anio', 'semana'],
    how='left'
)

# -------------------------------------------------------------------
# 9. Cambio mes a mes (Celda 8)
# -------------------------------------------------------------------
df_mes = df_diario[['ALERTA', 'anio', 'mes', 'cant_mes']].drop_duplicates()
df_mes = df_mes.sort_values(by=['ALERTA', 'anio', 'mes'])
df_mes['cant_mes_prev'] = df_mes.groupby('ALERTA')['cant_mes'].shift(1)

df_mes['pct_cambio_mes'] = (
    (df_mes['cant_mes'] - df_mes['cant_mes_prev']) /
    df_mes['cant_mes_prev']
)
df_mes['pct_cambio_mes'] = df_mes['pct_cambio_mes'] \
    .replace([np.inf, -np.inf], np.nan).fillna(0)

df_diario = df_diario.merge(
    df_mes[['ALERTA', 'anio', 'mes', 'cant_mes_prev', 'pct_cambio_mes']],
    on=['ALERTA', 'anio', 'mes'],
    how='left'
)

# -------------------------------------------------------------------
# 10. Acumulado mensual (Celda 9)
# -------------------------------------------------------------------
df_diario = df_diario.sort_values(by=['ALERTA', 'anio', 'mes', 'FECHA_ALERTA'])
df_diario['cant_mes_acum'] = df_diario.groupby(
    ['ALERTA', 'anio', 'mes']
)['cant_diaria'].cumsum()

# -------------------------------------------------------------------
# 11. Scores y categorías (Celda 13)
# -------------------------------------------------------------------
# Mediana diaria por ALERTA
df_diario['mediana_dia'] = df_diario.groupby('ALERTA')['cant_diaria'].transform('median')
df_diario['mediana_dia'] = df_diario['mediana_dia'].replace(0, 1)
df_diario['score_volumen_dia'] = df_diario['cant_diaria'] / df_diario['mediana_dia']

# Ratio alertas/cliente
df_diario['ratio_alertas_cliente'] = df_diario['cant_diaria'] / df_diario['rut_unicos_diarios'].replace(0, 1)
df_diario['mediana_ratio'] = df_diario.groupby('ALERTA')['ratio_alertas_cliente'].transform('median')
df_diario['mediana_ratio'] = df_diario['mediana_ratio'].replace(0, 1)
df_diario['score_clientes'] = df_diario['ratio_alertas_cliente'] / df_diario['mediana_ratio']

# Score mensual
df_diario['pct_mes'] = df_diario['dia_mes'] / 30
df_diario['mediana_mensual'] = df_diario.groupby('ALERTA')['cant_mes'].transform('median')
df_diario['mediana_mensual'] = df_diario['mediana_mensual'].replace(0, 1)
df_diario['esperado_mes'] = (df_diario['mediana_mensual'] * df_diario['pct_mes']).replace(0, 1)
df_diario['score_mes'] = df_diario['cant_mes'] / df_diario['esperado_mes']

# Score total
df_diario['score_total'] = (
    0.4 * df_diario['score_volumen_dia'] +
    0.4 * df_diario['score_clientes'] +
    0.2 * df_diario['score_mes']
)

def categoria(x):
    if x < 1.5:
        return 'NORMAL'
    elif x < 3:
        return 'MEDIA'
    else:
        return 'CRITICA'

df_diario['categoria'] = df_diario['score_total'].apply(categoria)

# -------------------------------------------------------------------
# 12. Filtro temporal df_final (como en el notebook)
# -------------------------------------------------------------------
df_final = df_diario[df_diario['FECHA_ALERTA'] >= "2025-06-01"].copy()
if df_final.empty:
    # Si no hay registros después de esa fecha, usamos todo lo disponible
    df_final = df_diario.copy()

# -------------------------------------------------------------------
# 13. Carga del modelo Random Forest y predicción
# -------------------------------------------------------------------
features = [
    "cant_diaria",
    "rut_unicos_diarios",
    "cant_semana",
    "cant_mes",
    "cant_mes_acum",
    "score_volumen_dia",
    "score_clientes",
    "score_mes",
    "score_total",
]

faltan_feat = [c for c in features if c not in df_final.columns]
if faltan_feat:
    print(json.dumps({"error": f"Faltan columnas para el modelo: {faltan_feat}"}))
    sys.exit(1)

ruta_modelo = os.path.join(os.path.dirname(__file__), "modelo_rf.pkl")
if not os.path.exists(ruta_modelo):
    print(json.dumps({"error": "No se encontró el archivo modelo_rf.pkl"}))
    sys.exit(1)

try:
    modelo = joblib.load(ruta_modelo)
except Exception as e:
    print(json.dumps({"error": f"No se pudo cargar el modelo: {str(e)}"}))
    sys.exit(1)

X = df_final[features]

try:
    pred = modelo.predict(X)
except Exception as e:
    print(json.dumps({"error": f"Error al predecir con el modelo: {str(e)}"}))
    sys.exit(1)

df_final['anomalia_pred'] = pred

# -------------------------------------------------------------------
# 14. Resumen para la fecha más reciente
# -------------------------------------------------------------------
fecha_max = df_final['FECHA_ALERTA'].max()
df_dia = df_final[df_final['FECHA_ALERTA'] == fecha_max].copy()

total_anomalias = int((df_dia['anomalia_pred'] == 1).sum())
total_normales  = int((df_dia['anomalia_pred'] == 0).sum())

resumen = {
    "fecha": fecha_max.strftime("%Y-%m-%d"),
    "total_registros": int(len(df_dia)),
    "total_anomalias": total_anomalias,
    "total_normales": total_normales,
    "detalle": df_dia[[
        "FECHA_ALERTA",
        "ALERTA",
        "cant_diaria",
        "rut_unicos_diarios",
        "score_total",
        "anomalia_pred"
    ]].assign(
        FECHA_ALERTA=lambda x: x["FECHA_ALERTA"].dt.strftime("%Y-%m-%d")
    ).to_dict(orient="records")
}

print(json.dumps(resumen, ensure_ascii=False))
