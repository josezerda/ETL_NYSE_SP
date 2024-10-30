import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Asegúrate de importar el módulo que estás probando
from dags.src.insert_data import insert_data_function  # Cambia esto según la estructura de tu código

class TestInsertData(unittest.TestCase):

    @patch('dags.src.insert_data.pd.read_csv')
    @patch('dags.src.insert_data.redshift_connector.connect')
    @patch('dags.src.insert_data.wr.redshift.to_sql')
    def test_data_insertion(self, mock_to_sql, mock_connect, mock_read_csv):
        # Simular un DataFrame que se leería desde un archivo CSV
        mock_df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['A', 'B', 'C']
        })
        mock_read_csv.return_value = mock_df
        
        # Simular la conexión a Redshift
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Llamar a la función de inserción (asegúrate de que sea una función separada en tu código)
        insert_data_function('mock_path.csv')  # Cambia esto según tu implementación

        # Verificar que se haya llamado a to_sql
        mock_to_sql.assert_called_once_with(
            df=mock_df,
            con=mock_conn,
            table=os.getenv('redshift_table'),
            schema=os.getenv('redshift_schema'),
            mode='overwrite',
            use_column_names=True,
            lock=True,
            index=False
        )

    def test_invalid_csv_path(self):
        with self.assertRaises(SystemExit):
            sys.argv = ['insert_data.py', 'invalid_path.csv']
            from dags.src.insert_data import main  # Asegúrate de que el código tenga una función main
            main()  # Esto debería levantar una excepción debido a un archivo CSV inválido

if __name__ == '__main__':
    unittest.main()