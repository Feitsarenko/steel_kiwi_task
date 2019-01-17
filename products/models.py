from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, max_length=20, unique=True)
    description = models.TextField()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_list', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_GRADE = (
        ('B', 'Base'),
        ('S', 'Standard'),
        ('P', 'Premium')
    )
    grade = models.CharField(max_length=1, choices=PRODUCT_GRADE, default='S')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    image = models.ImageField(default=None, blank=True, upload_to='media/', null=True)
    slug = models.SlugField(blank=True, max_length=20, unique=True)
    description = models.TextField(max_length=600)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    in_top_list = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    static_out_top_list = models.BooleanField(default=False)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_list', kwargs={'product_slug': self.slug, 'category_slug': self.category.slug})

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Product)
def model_pre_save(instance, sender, **kwargs):
    if not instance.slug:
        slug = slugify(instance.name)  # change the attibute to the field that would be used as a slug
        new_slug = slug
        count = 0
        while sender.objects.filter(slug=new_slug).exclude(id=instance.id).count() > 0:
            count += 1
            new_slug = '{slug}-{count}'.format(slug=slug, count=count)

        instance.slug = new_slug
    if sender == Product and instance.in_top_list and instance.static_out_top_list:
        instance.static_out_top_list = False


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('product', 'user'), ('product', 'user_ip'))

    def __str__(self):
        return '{} from {}'.format(self.product, self.user or self.user_ip)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return '{}'.format(self.product)


class PageLoadsLogbook(models.Model):
    url = models.URLField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} from {} at {}'.format(self.url, self.user or self.user_ip, self.created_at)
