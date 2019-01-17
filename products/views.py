from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import FormMixin
from .models import Category, Product, Like, Comment, PageLoadsLogbook
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from ipware.ip import get_ip
from django.shortcuts import reverse
from django.utils import timezone
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt
from .filters import ProductFilter
from django.core.paginator import Paginator


class MainView(TemplateView):
    template_name = 'product/main_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choice_week'] = Product.objects\
            .annotate(count_likes=Count('like', Q(like__created_at__gt=timezone.now()-timezone.timedelta(days=7))))\
            .filter(Q(count_likes__gte=10) & Q(grade='B') | Q(count_likes__gte=5) & Q(grade='S') | Q(grade='P'))\
            .aggregate(
                base=Count('pk', filter=Q(grade='B')),
                standard=Count('pk', filter=Q(grade='S')),
                premium=Count('pk', filter=Q(grade='P')))
        context['popular_products'] = Product.objects.annotate(count_likes=Count('like'))\
            .filter(static_out_top_list=False).order_by('-in_top_list', '-count_likes')[:10]
        context['count_visit_on_day'] = PageLoadsLogbook.objects\
            .exclude(created_at__gt=timezone.now().replace(hour=0, minute=0, second=0))\
            .filter(created_at__gt=timezone.now().date()-timezone.timedelta(days=7))\
            .aggregate(
                sunrday=Count('pk', filter=Q(created_at__week_day=1)),
                monday=Count('pk', filter=Q(created_at__week_day=2)),
                tuesday=Count('pk', filter=Q(created_at__week_day=3)),
                wednesday=Count('pk', filter=Q(created_at__week_day=4)),
                thursday=Count('pk', filter=Q(created_at__week_day=5)),
                friday=Count('pk', filter=Q(created_at__week_day=6)),
                saturday=Count('pk', filter=Q(created_at__week_day=7)),
            )
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'product/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = Category.objects.all().annotate(count_products=Count('product'))
        return queryset


class CategoryPageView(TemplateView):
    template_name = 'product/category_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context['filter'] = ProductFilter(self.request.GET, queryset=Product.objects.filter(category=category)\
                                          .annotate(count_likes=Count('like')))
        paginator = Paginator(context['filter'].qs.order_by('name'), 10)
        page = self.request.GET.get('page')
        context['contacts'] = paginator.get_page(page)

        return context


class ProductDetailsView(FormMixin, DetailView):
    model = Product
    template_name = 'product/product_details.html'
    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('product_details', kwargs={'product_slug': self.object.slug,
                                                  'category_slug': self.object.category.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        context['comments'] = Comment.objects.filter(product=product,\
                                                     created_at__gte=timezone.now()-timezone.timedelta(hours=24),\
                                                     created_at__lte=timezone.now())
        context['form'] = self.get_form()
        context['like_count'] = Like.objects.filter(product=product).count()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        form.instance.product = self.object
        if request.user.is_authenticated:
            form.instance.user = request.user
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LikeView(View):
    http_method_names = ('post', )

    def dispatch(self, request, *args, **kwargs):
        product_slug = kwargs['product_slug']
        try:
            self.product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                Like.objects.get(product=self.product, user=request.user)
            else:
                Like.objects.get(product=self.product, user_ip=get_ip(request))
        except Like.DoesNotExist:
            if request.user.is_authenticated:
                like = Like.objects.create(product=self.product, user=request.user)
            else:
                like = Like.objects.create(product=self.product, user_ip=get_ip(request))
            like.save()
            result = True
            count = Like.objects.filter(product=self.product).count()
            return JsonResponse({
                'result': result,
                'count': count,
                }
            )


class ProductChooseWeekView(ListView):
    model = Product
    template_name = 'product/choose_week.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects\
            .annotate(count_likes=Count('like', Q(like__created_at__gt=timezone.now()-timezone.timedelta(days=7))))\
            .filter(Q(count_likes__gt=10) & Q(grade='B') | Q(count_likes__gt=5) & Q(grade='S') | Q(grade='P'))
        return queryset




