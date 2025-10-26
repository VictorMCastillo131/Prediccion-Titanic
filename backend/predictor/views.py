from django.conf import settings
import os
import joblib
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

# 1. Cargar el modelo
MODEL_PATH = os.path.join(settings.BASE_DIR, 'predictor/titanic_model.joblib')
model = joblib.load(MODEL_PATH)

# 2. Valores por defecto
DEFAULT_AGE = 29.69911764705882

# 3. Tarifas por clase
FARE_MAP = {
    1: 84.15,
    2: 20.66,
    3: 13.68
}


class PredictView(APIView):
    """
    Vista de API que recibe: pclass, sex, age, embarked
    y devuelve: survival_percentage
    """

    # ✅ Permitir GET para que no salga el error 405
    def get(self, request, *args, **kwargs):
        return Response({
            "message": "Usa POST para enviar datos y obtener la predicción.",
            "ejemplo": {
                "pclass": 3,
                "sex": "male",
                "age": 22,
                "embarked": "S"
            }
        })

    # ✅ Método principal para predicciones
    def post(self, request, *args, **kwargs):
        try:
            data = request.data

            # Validar campos
            pclass = data.get('pclass')
            sex_str = data.get('sex')
            age_str = data.get('age')
            embarked = data.get('embarked')

            if not all([pclass, sex_str, embarked]):
                return Response({'error': 'Faltan campos requeridos'}, status=400)

            # Convertir tipos
            pclass = int(pclass)
            sex_encoded = 1 if sex_str.lower() == 'female' else 0
            age = float(age_str) if age_str else DEFAULT_AGE
            fare = FARE_MAP.get(pclass, 13.68)

            # One-hot encoding para el puerto
            embarked_c = 1 if embarked == 'C' else 0
            embarked_q = 1 if embarked == 'Q' else 0
            embarked_s = 1 if embarked == 'S' else 0

            # Vector de características
            features = np.array([[
                pclass, sex_encoded, age, fare, embarked_c, embarked_q, embarked_s
            ]])

            # Predicción
            probability = model.predict_proba(features)[0][1]
            survival_percentage = round(probability * 100, 2)

            return Response({'survival_percentage': survival_percentage})

        except Exception as e:
            return Response({'error': str(e)}, status=400)


def home(request):
    html = """
    <html>
    <head>
        <title>Bienvenido a Proyecto Titanic</title>
        <style>
            body {
                background: #111;
                color: #e0f7fa;
                font-family: 'Segoe UI', Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 80px auto;
                background: rgba(30, 60, 120, 0.85);
                border-radius: 16px;
                box-shadow: 0 8px 32px 0 rgba(0,0,0,0.3);
                padding: 40px;
                text-align: center;
            }
            h1 {
                color: #2196f3;
                margin-bottom: 24px;
            }
            a {
                color: #64b5f6;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                color: #bbdefb;
            }
            .api-form {
                margin-top: 32px;
                background: #222;
                border-radius: 12px;
                padding: 24px;
                box-shadow: 0 4px 16px 0 rgba(0,0,0,0.2);
            }
            label {
                color: #90caf9;
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
            }
            input, select {
                width: 80%;
                padding: 8px;
                margin-bottom: 16px;
                border-radius: 6px;
                border: none;
                background: #1e2a38;
                color: #e0f7fa;
            }
            button {
                background: #2196f3;
                color: #fff;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 1em;
                cursor: pointer;
                transition: background 0.2s;
            }
            button:hover {
                background: #1565c0;
            }
            .result {
                margin-top: 24px;
                color: #64b5f6;
                font-size: 1.2em;
            }
        </style>
        <script>
        async function predict(event) {
            event.preventDefault();
            const pclass = document.getElementById('pclass').value;
            const sex = document.getElementById('sex').value;
            const age = document.getElementById('age').value;
            const embarked = document.getElementById('embarked').value;
            const response = await fetch('/predict/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({pclass, sex, age, embarked})
            });
            const data = await response.json();
            document.getElementById('result').innerHTML =
                'Probabilidad de supervivencia: <b>' + 
                (data.survival_percentage ? data.survival_percentage + '%' : 'Error') + '</b>';
        }
        </script>
    </head>
    <body>
        <div class='container'>
            <h1>Bienvenido a Proyecto Titanic</h1>
            
            <form class='api-form' onsubmit='predict(event)'>
                <label for='pclass'>Clase (1, 2, 3):</label>
                <select id='pclass' required>
                    <option value='1'>1ra Clase</option>
                    <option value='2'>2da Clase</option>
                    <option value='3'>3ra Clase</option>
                </select>
                
                <label for='sex'>Sexo:</label>
                <select id='sex' required>
                    <option value='male'>Masculino</option>
                    <option value='female'>Femenino</option>
                </select>
                
                <label for='age'>Edad:</label>
                <input type='number' id='age' min='0' max='100' required />
                
                <label for='embarked'>Puerto de embarque:</label>
                <select id='embarked' required>
                    <option value='S' selected>S (Southampton)</option>
                    <option value='C'>C (Cherbourg)</option>
                    <option value='Q'>Q (Queenstown)</option>
                </select>
                
                <button type='submit'>Predecir</button>
            </form>
            
            <div id='result' class='result'></div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
