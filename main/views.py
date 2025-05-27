from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import News, NewsCategory, Partner, JobApplication, ContactMessage
from .forms import JobApplicationForm, ContactForm

def main_view(request):
    """Главная страница"""
    # Последние новости для главной
    latest_news = News.objects.filter(is_published=True)[:3]
    # Главная новость
    featured_news = News.objects.filter(is_published=True, is_featured=True).first()
    # Партнеры для отображения
    partners = Partner.objects.filter(is_active=True)[:5]
    
    context = {
        'latest_news': latest_news,
        'featured_news': featured_news,
        'partners': partners,
    }
    return render(request, 'main.html', context)

def about_view(request):
    """Страница О нас"""
    return render(request, 'about.html')

def services_view(request):
    """Страница Услуги"""
    return render(request, 'services.html')

def news_list_view(request):
    """Список новостей"""
    category_filter = request.GET.get('category', 'all')
    
    news_list = News.objects.filter(is_published=True)
    
    if category_filter != 'all':
        news_list = news_list.filter(category__slug=category_filter)
    
    # Главная новость (отдельно)
    featured_news = News.objects.filter(is_published=True, is_featured=True).first()
    
    # Остальные новости
    regular_news = news_list.exclude(is_featured=True)
    
    # Пагинация
    paginator = Paginator(regular_news, 6)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    # Категории для фильтра
    categories = NewsCategory.objects.all()
    
    context = {
        'featured_news': featured_news,
        'news': news,
        'categories': categories,
        'current_category': category_filter,
    }
    return render(request, 'news.html', context)

def news_detail_view(request, slug):
    """Детальная страница новости"""
    news_item = get_object_or_404(News, slug=slug, is_published=True)
    
    # Похожие новости из той же категории
    related_news = News.objects.filter(
        category=news_item.category,
        is_published=True
    ).exclude(id=news_item.id)[:3]
    
    context = {
        'news_item': news_item,
        'related_news': related_news,
    }
    return render(request, 'news_detail.html', context)

def partners_view(request):
    """Страница партнеров"""
    category_filter = request.GET.get('category', 'all')
    
    partners_list = Partner.objects.filter(is_active=True)
    
    if category_filter != 'all':
        partners_list = partners_list.filter(category=category_filter)
    
    context = {
        'partners': partners_list,
        'current_category': category_filter,
    }
    return render(request, 'partners.html', context)

def contacts_view(request):
    """Страница контактов"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Сообщение отправлено!'})
            messages.success(request, 'Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.')
            return redirect('contacts')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contacts.html', context)

def work_view(request):
    """Страница работы с нами"""
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Заявка отправлена!'})
            messages.success(request, 'Спасибо за заявку! Мы свяжемся с вами в течение 24 часов.')
            return redirect('work')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = JobApplicationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'work.html', context)

def search_view(request):
    """Поиск по сайту"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Поиск в новостях
        news_results = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        )
        
        # Поиск в партнерах
        partner_results = Partner.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        )
        
        results = {
            'news': news_results,
            'partners': partner_results,
            'query': query,
        }
    
    return render(request, 'search_results.html', results)