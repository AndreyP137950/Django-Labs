"""
Модульные тесты приложения designer

Команда запуска тестов:
python manage.py test designer

Примеры тестов для проверки корректности вычисления функций
и работы API endpoints
"""

import math
from django.test import TestCase, Client
from django.urls import reverse
from .models import FunctionChain

class FunctionChainModelTests(TestCase):
    """
    Тесты для модели FunctionChain
    Проверяют корректность вычисления функций и обработку ошибок
    """
    
    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.chain = FunctionChain(
            function_f1='sqrt',
            function_f2='reciprocal',
            function_f3='exp'
        )
    
    def test_sqrt_function_valid(self):
        """Тест sqrt с допустимым значением"""
        result, error = FunctionChain.apply_function('sqrt', 4)
        self.assertEqual(result, 2.0)
        self.assertIsNone(error)
    
    def test_sqrt_function_invalid(self):
        """Тест sqrt с отрицательным значением (ошибка)"""
        result, error = FunctionChain.apply_function('sqrt', -1)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn('отрицательным', error)
    
    def test_reciprocal_function_valid(self):
        """Тест 1/x с допустимым значением"""
        result, error = FunctionChain.apply_function('reciprocal', 2)
        self.assertEqual(result, 0.5)
        self.assertIsNone(error)
    
    def test_reciprocal_function_invalid(self):
        """Тест 1/x с нулем (ошибка деления на 0)"""
        result, error = FunctionChain.apply_function('reciprocal', 0)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn('ноль', error)
    
    def test_exp_function_valid(self):
        """Тест e^x с допустимым значением"""
        result, error = FunctionChain.apply_function('exp', 1)
        self.assertAlmostEqual(result, math.e, places=5)
        self.assertIsNone(error)
    
    def test_calculate_chain_valid(self):
        """Тест вычисления полной цепочки с корректными значениями"""
        result_data = self.chain.calculate(0.5)
        
        self.assertIsNone(result_data['error'])
        self.assertIsNotNone(result_data['result'])
        self.assertTrue(len(result_data['steps']) > 0)
    
    def test_calculate_chain_with_error(self):
        """Тест цепочки с ошибкой на первом шаге"""
        chain = FunctionChain(
            function_f1='sqrt',
            function_f2='sqrt',
            function_f3='sqrt'
        )
        
        result_data = chain.calculate(-1)
        
        self.assertIsNone(result_data['result'])
        self.assertIsNotNone(result_data['error'])
    
    def test_vba_code_generation(self):
        """Тест генерирования VBA кода"""
        vba_code = self.chain.generate_vba_code()
        
        # Проверяем наличие ключевых функций
        self.assertIn('Function CalculateChain', vba_code)
        self.assertIn('sqrt_func', vba_code)
        self.assertIn('reciprocal_func', vba_code)
        self.assertIn('exp_func', vba_code)
        
        # Проверяем наличие проверок ошибок
        self.assertIn('If x < 0', vba_code)
        self.assertIn('If x = 0', vba_code)
        self.assertIn('MsgBox', vba_code)


class FunctionChainViewTests(TestCase):
    """
    Тесты для представлений (views) приложения
    Проверяют работу HTTP endpoints
    """
    
    def setUp(self):
        """Подготовка клиента для тестирования"""
        self.client = Client()
    
    def test_index_page_loads(self):
        """Тест загрузки главной страницы"""
        response = self.client.get(reverse('designer:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('designer/index.html'.encode(), response.content)
    
    def test_calculate_api_valid_request(self):
        """Тест API endpoint для вычисления с корректными параметрами"""
        response = self.client.post(
            reverse('designer:calculate'),
            {
                'x_value': '2',
                'f1': 'sqrt',
                'f2': 'reciprocal',
                'f3': 'exp'
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIsNone(data['error'])
        self.assertIsNotNone(data['result'])
    
    def test_calculate_api_invalid_input(self):
        """Тест API endpoint с некорректным числовым вводом"""
        response = self.client.post(
            reverse('designer:calculate'),
            {
                'x_value': 'not_a_number',
                'f1': 'sqrt',
                'f2': 'reciprocal',
                'f3': 'exp'
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIsNotNone(data['error'])
    
    def test_generate_vba_api(self):
        """Тест API endpoint для генерирования VBA кода"""
        response = self.client.post(
            reverse('designer:generate_vba'),
            {
                'f1': 'sqrt',
                'f2': 'reciprocal',
                'f3': 'exp'
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('Function CalculateChain', data['vba_code'])
    
    def test_save_chain_api(self):
        """Тест API endpoint для сохранения конфигурации"""
        response = self.client.post(
            reverse('designer:save_chain'),
            {
                'f1': 'sqrt',
                'f2': 'reciprocal',
                'f3': 'exp',
                'description': 'Test configuration'
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['chain_id'])
        
        # Проверяем что цепочка действительно сохранена в БД
        chain = FunctionChain.objects.get(id=data['chain_id'])
        self.assertEqual(chain.function_f1, 'sqrt')
        self.assertEqual(chain.function_f2, 'reciprocal')
        self.assertEqual(chain.function_f3, 'exp')
        self.assertEqual(chain.description, 'Test configuration')
    
    def test_download_vba_file(self):
        """Тест скачивания VBA файла"""
        response = self.client.post(
            reverse('designer:download_vba'),
            {
                'f1': 'sqrt',
                'f2': 'reciprocal',
                'f3': 'exp'
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Проверяем что это файл с правильным MIME типом
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn('attachment', response['Content-Disposition'])
        self.assertIn('case_functions.bas', response['Content-Disposition'])


class EdgeCaseTests(TestCase):
    """
    Тесты граничных случаев и особых ситуаций
    """
    
    def test_very_large_number(self):
        """Тест с очень большим числом"""
        chain = FunctionChain(
            function_f1='sqrt',
            function_f2='reciprocal',
            function_f3='sqrt'
        )
        result_data = chain.calculate(1e10)
        
        # Должен быть результат (может быть ошибка при делении на очень маленькое число)
        self.assertIsNotNone(result_data['result'] or result_data['error'])
    
    def test_very_small_positive_number(self):
        """Тест с очень маленьким положительным числом"""
        chain = FunctionChain(
            function_f1='sqrt',
            function_f2='reciprocal',
            function_f3='sqrt'
        )
        result_data = chain.calculate(0.0001)
        
        self.assertIsNone(result_data['error'])
        self.assertIsNotNone(result_data['result'])
    
    def test_zero_input(self):
        """Тест с нулевым входом"""
        chain = FunctionChain(
            function_f1='sqrt',
            function_f2='reciprocal',
            function_f3='exp'
        )
        result_data = chain.calculate(0)
        
        # e^0 = 1, 1/1 = 1, sqrt(1) = 1
        # Должно работать
        self.assertIsNone(result_data['error'])
        self.assertAlmostEqual(result_data['result'], 1.0, places=5)
