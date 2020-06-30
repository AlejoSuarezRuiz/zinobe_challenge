## Python challenge to Zinobe

Este proyecto está desarrollado bajo la tecnología de contenedores docker.
Para correrlo se tiene como requerimentos docker y docker-compose. Una vez se tenga, se debe correr los comandos:

```
    docker-compose build
    docker-compose up
```

Para visualizar gráficamente los resultados se debe ingresar en la url `http://localhos:5000`.
Esta vista está desarrollada sobre Flask. Se envía un template que mediante Javascript realiza la petición a los endpoints necesarios.

El código como tal se encuentra en `challenge.py` y `challenge_parallel.py`. Básicamente la estructura des olución es la misma, se diferencian en que el segundo archivo corre en paralelo los llamados al API externo, significando una mejora en los tiempos totales de cálculo.

Mediante la interfáz, con los botones de refrescar y refrescar en paralelo se puede recargar los datos.