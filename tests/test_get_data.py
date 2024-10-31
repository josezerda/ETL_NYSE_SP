import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Importar la función o el módulo que estás probando
from dags.src.get_data import url, output_file, api_key, simbol  # Asegúrate de importar correctamente las variables necesarias

class TestGetData(unittest.TestCase):

    @patch('src.get_data.requests.get')
    def test_api_request_success(self, mock_get):
        # Configurar el mock para simular una respuesta exitosa
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': [{'v': 1000, 'vw': 100.0, 'o': 90.0, 'c': 110.0, 'h': 120.0, 'l': 80.0, 't': 1633036800000, 'n': 10}]}
        mock_get.return_value = mock_response
        
        # Ejecutar la función que realiza la solicitud (que en este caso es el script completo)
        from src.get_data import main  # Asegúrate de que tu archivo tenga una función main para ejecutar el código

        # Verificar que el DataFrame se crea correctamente
        df = pd.DataFrame(mock_response.json()['results'])
        df['Fecha'] = pd.to_datetime(df['t'], unit='ms')
        
        self.assertEqual(len(df), 1)  # Asegúrate de que se creó una fila
        self.assertEqual(df['volumen'][0], 1000)  # Verifica un campo específico

    def test_url_construction(self):
        expected_url = 'https://api.polygon.io/v2/aggs/ticker/X:XYZ/range/1/day/2023-01-01/2024-01-01?sort=asc&apiKey=YOUR_API_KEY'
        # Cambia 'XYZ' y 'YOUR_API_KEY' por los valores adecuados según tu entorno
        self.assertEqual(url, expected_url)

if __name__ == '__main__':
    unittest.main()