# **Pipeline ETL de Inteligencia Financiera (End-to-End)**

Este proyecto es una arquitectura de datos automatizada diseñada para monitorear y analizar el impacto del tipo de cambio (USD/MXN/EUR) en los costos operativos de una empresa. El pipeline extrae datos vivos de internet, los cruza con reportes financieros locales y centraliza la información en un Data Warehouse para la toma de decisiones directivas.

## **Arquitectura y Tecnologías (Stack Técnico)**

El proyecto implementa una arquitectura modular con separación de dominios:

* **Extracción (Extract):** Python \+ Requests (Frankfurter API \- Banco Central Europeo)  
* **Transformación (Transform):** Python \+ Pandas (Limpieza, cruce de datos y cálculo de divisas)  
* **Carga (Load):** PostgreSQL \+ psycopg2 (Data Warehouse local aislado)  
* **Orquestación:** Librerías nativas (os, subprocess, sys, logging)  
* **Capa Semántica (BI):** Power BI (Dashboard analítico para C-Level)

## &nbsp;**Flujo de Trabajo (Pipeline)**

1. **api\_divisas.py:** Se conecta a la API de Frankfurter para extraer el histórico de 30 días del tipo de cambio base (USD).  
2. **costos\_operativos.csv:** Simula el reporte diario de un ERP (ej. SAP) con los gastos departamentales en dólares.  
3. **transformacion.py:** Realiza un *Left Join* entre la tabla de costos y el tipo de cambio del día exacto, calculando el impacto financiero real en MXN y EUR.  
4. **carga\_db.py:** Inyecta de forma masiva los datos enriquecidos en una tabla relacional de PostgreSQL.  
5. **main\_pipeline.py:** Actúa como orquestador maestro, ejecutando las fases en cascada y abortando el proceso de forma segura si detecta un fallo en la red o en los datos.

## **Estructura del Repositorio**

&nbsp;ETL\_Inteligencia\_Financiera  
&nbsp;┣  1\_Extract y logs/  
&nbsp;┃ ┣  api\_divisas.py          \# Script de conexión a la API  
&nbsp;┃ ┣  costos\_operativos.csv   \# Mock de datos del ERP  
&nbsp;┃ ┣ tasas\_crudas.csv        \# Archivo temporal extraído  
&nbsp;┃ ┗  pipeline\_financiero.log \# Bitácora de auditoría  
&nbsp;┣ transformacion.py         \# Script de cruce de datos y Pandas  
&nbsp;┣ master\_costos\_divisas.csv \# Data Mart temporal resultante  
&nbsp;┣ carga\_db.py               \# Script de inyección a BD  
&nbsp;┣  main\_pipeline.py          \# ORQUESTADOR PRINCIPAL  
&nbsp;┣ .gitignore                \# Reglas de exclusión de Git  
&nbsp;┗  README.md                 \# Documentación del proyecto

## &nbsp;**Instalación y Ejecución local**

Para reproducir este pipeline en un entorno local:

1. Clonar el repositorio:  
   git clone https://github.com/TuUsuario/ETL\_Inteligencia\_Financiera.git

2. Crear y activar un entorno virtual:  
   python \-m venv .venv  
   source .venv/Scripts/activate  \# En Windows

3. Instalar dependencias necesarias:  
   pip install pandas requests psycopg2

4. Configurar PostgreSQL: Crear una base de datos llamada finanzas\_corp y actualizar las credenciales en carga\_db.py.  
5. Ejecutar el orquestador:  
   python main\_pipeline.py

## &nbsp;**Capa Analítica (Power BI)**

La base de datos resultante alimenta un Dashboard Directivo que permite a la gerencia:

* Visualizar el gasto total operativo en pesos mexicanos (MXN) frente al presupuesto original en USD.  
* Analizar la tendencia diaria de gasto cruzada con la volatilidad del tipo de cambio.  
* Filtrar por departamento (Logística, Operaciones, Mantenimiento) para detectar desviaciones presupuestales.