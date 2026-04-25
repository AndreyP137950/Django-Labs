# Модели данных приложения assets
# Определяют структуру таблиц базы данных для хранения информации об основных средствах

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

# Модель "Подразделение" хранит структурные единицы организации.
class Department(models.Model):
    """
    Модель подразделения организации
    
    Атрибуты:
    - code: код подразделения (уникальный, используется в коде внутреннего учета)
    - name: наименование подразделения
    - description: описание подразделения
    - created_at: дата создания записи
    """
    
    # Код подразделения (например "ОФ", "ЦЕХ1", "ОТД2" и т.д.)
    code = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name='Код подразделения',
        help_text='Уникальный код (например: ОФ, ЦЕХ1, ОТД2)'
    )
    
    # Наименование подразделения
    name = models.CharField(
        max_length=200, 
        verbose_name='Наименование подразделения'
    )
    
    # Описание (опциональное поле)
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Описание'
    )
    
    # Дата и время создания записи (автоматически устанавливается)
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания'
    )
    
    class Meta:
        # Понятное имя модели в единственном числе
        verbose_name = 'Подразделение'
        # Понятное имя модели во множественном числе
        verbose_name_plural = 'Подразделения'
        # Сортировка по коду подразделения
        ordering = ['code']
    
    def __str__(self):
        """Представление объекта в виде строки"""
        return f"{self.code} - {self.name}"


# Модель "Основное средство" хранит учетные записи по активам.
class FixedAsset(models.Model):
    """
    Модель основного средства организации
    
    Атрибуты:
    - name: наименование ОС
    - description: описание
    - department: подразделение (место хранения)
    - purchase_date: дата покупки
    - cost: стоимость
    - internal_code: автоматически генерируемый код внутреннего учета
    - sequence_number: порядковый номер ОС в подразделении
    """
    
    # Наименование основного средства (например "Компьютер HP", "Стол офисный" и т.д.)
    name = models.CharField(
        max_length=300, 
        verbose_name='Наименование основного средства'
    )
    
    # Подробное описание
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Описание'
    )
    
    # Связь с моделью Department (место хранения ОС)
    # Если подразделение удалится, удалится и все его ОС
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        verbose_name='Подразделение (место хранения)',
        related_name='assets'
    )
    
    # Дата покупки основного средства
    purchase_date = models.DateField(
        verbose_name='Дата покупки'
    )
    
    # Первоначальная стоимость в рублях
    cost = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name='Первоначальная стоимость',
        help_text='В рублях'
    )
    
    # Процент износа (от 0 до 100%)
    depreciation_percent = models.IntegerField(
        default=0, 
        verbose_name='Процент износа (%)',
        help_text='От 0 до 100%'
    )
    
    # Порядковый номер основного средства в подразделении.
    # Автоматически генерируется при создании нового ОС
    sequence_number = models.IntegerField(
        verbose_name='Порядковый номер в подразделении',
        default=0
    )
    
    # КОД ВНУТРЕННЕГО УЧЕТА (новый реквизит согласно заданию)
    # Формируется по правилу: код_подразделения + порядковый_номер
    # Пример: ОФ_1, ЦЕХ1_2, ОТД2_1 и т.д.
    internal_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Код внутреннего учета',
        help_text='Автоматически генерируется (КодПодразд_ПорядковыйНомер)',
        blank=True
    )
    
    # Дата и время создания записи
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания'
    )
    
    # Дата и время последнего редактирования
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Дата изменения'
    )
    
    class Meta:
        verbose_name = 'Основное средство'
        verbose_name_plural = 'Основные средства'
        # Сортировка по подразделению и внутреннему коду
        ordering = ['department', 'internal_code']
    
    def __str__(self):
        """Представление объекта в виде строки"""
        return f"{self.internal_code} - {self.name}"

    @property
    def residual_cost(self):
        """Остаточная стоимость с учетом процента износа."""
        depreciation_ratio = Decimal(self.depreciation_percent) / Decimal('100')
        return self.cost * (Decimal('1') - depreciation_ratio)
    
    # Метод для автоматического присвоения внутреннего кода
    def generate_internal_code(self):
        """
        Генерирует код внутреннего учета по правилу:
        КодПодразделения_НовыйПорядковыйНомер
        
        Пример: ОФ_1, ОФ_2, ЦЕХ1_1, ЦЕХ1_2
        """
        
        # Получаем максимальный порядковый номер для текущего подразделения
        max_sequence = FixedAsset.objects.filter(
            department=self.department
        ).aggregate(models.Max('sequence_number'))['sequence_number__max']
        
        # Если нет ОС в подразделении, начинаем с 1
        if max_sequence is None:
            self.sequence_number = 1
        else:
            self.sequence_number = max_sequence + 1
        
        # Формируем код внутреннего учета
        self.internal_code = f"{self.department.code}_{self.sequence_number}"
    
    def clean(self):
        """Валидация данных перед сохранением"""
        # Проверка, что стоимость положительная
        if self.cost <= 0:
            raise ValidationError('Стоимость должна быть больше 0')
        
        # Проверка процента износа (от 0 до 100)
        if not (0 <= self.depreciation_percent <= 100):
            raise ValidationError('Процент износа должен быть от 0 до 100%')
    
    def save(self, *args, **kwargs):
        """Сохранение объекта в БД"""
        # Если internal_code пустой, генерируем его автоматически
        if not self.internal_code:
            self.generate_internal_code()
        
        # Генерируем более явно для очистки
        self.full_clean()
        super().save(*args, **kwargs)
