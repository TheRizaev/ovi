from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class NewsCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL")
    
    class Meta:
        verbose_name = "Категория новостей"
        verbose_name_plural = "Категории новостей"
    
    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL")
    excerpt = models.TextField(max_length=300, verbose_name="Краткое описание")
    content = models.TextField(verbose_name="Полный текст")
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, verbose_name="Категория")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Изображение")
    is_featured = models.BooleanField(default=False, verbose_name="Главная новость")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

class Partner(models.Model):
    PARTNER_TYPES = [
        ('clinics', 'Клиники'),
        ('labs', 'Лаборатории'),
        ('pharmacies', 'Аптеки'),
        ('specialists', 'Специалисты'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    category = models.CharField(max_length=20, choices=PARTNER_TYPES, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")
    services = models.TextField(verbose_name="Услуги", help_text="Каждую услугу с новой строки")
    contact_info = models.TextField(verbose_name="Контактная информация")
    logo = models.ImageField(upload_to='partners/', blank=True, null=True, verbose_name="Логотип")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class JobApplication(models.Model):
    PROFESSION_CHOICES = [
        ('doctor-therapist', 'Врач-терапевт'),
        ('doctor-cardiologist', 'Врач-кардиолог'),
        ('doctor-neurologist', 'Врач-невролог'),
        ('doctor-pediatrician', 'Врач-педиатр'),
        ('doctor-other', 'Врач другой специальности'),
        ('nurse', 'Медсестра'),
        ('clinic', 'Представитель клиники'),
        ('pharmacy', 'Представитель аптеки'),
        ('lab', 'Представитель лаборатории'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('1-3', '1-3 года'),
        ('3-5', '3-5 лет'),
        ('5-10', '5-10 лет'),
        ('10+', 'Более 10 лет'),
    ]
    
    AVAILABILITY_CHOICES = [
        ('fulltime', 'Полный день'),
        ('parttime', 'Неполный день'),
        ('evenings', 'Вечерние часы'),
        ('weekends', 'Выходные дни'),
        ('flexible', 'Гибкий график'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_review', 'На рассмотрении'),
        ('interview', 'Собеседование'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]
    
    full_name = models.CharField(max_length=200, verbose_name="Полное имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    profession = models.CharField(max_length=30, choices=PROFESSION_CHOICES, verbose_name="Специальность")
    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, verbose_name="Опыт работы")
    education = models.CharField(max_length=300, blank=True, verbose_name="Образование")
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, blank=True, verbose_name="Предпочтительное время работы")
    message = models.TextField(blank=True, verbose_name="Дополнительная информация")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи")
    
    class Meta:
        verbose_name = "Заявка на работу"
        verbose_name_plural = "Заявки на работу"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.get_profession_display()}"

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('support', 'Техническая поддержка'),
        ('partnership', 'Партнерство'),
        ('career', 'Вакансии'),
        ('feedback', 'Отзыв или предложение'),
        ('other', 'Другое'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, verbose_name="Тема обращения")
    message = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"