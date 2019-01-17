from django.test import TestCase
from django.urls import reverse
from .factory import ProductFactory, CategoryFactory, LikeFactory, CommentFactory, UserFactory
from .forms import CommentForm
from .models import Like, Product
from django.utils import timezone
import unittest.mock


class CategoryPageViewTest(TestCase):

    def setUp(self):
        self.category = CategoryFactory()
        self.url = reverse('category_page', args=(self.category.slug, ))

    def create_products(self, n):
        ProductFactory.create_batch(n, category=self.category)

    def test_empty_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Empty')
        self.assertQuerysetEqual(response.context['filter'].qs, [])

    def test_product_list(self):
        self.create_products(3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['filter'].qs, ['<Product: product0>', '<Product: product1>',\
                                                                 '<Product: product2>'], ordered=False)


class ProductDescriptionViewTest(TestCase):

    def setUp(self):
        self.product = ProductFactory(name='test_description')
        self.user = UserFactory()
        self.url = reverse('product_details', args=(self.product.category.slug, self.product.slug,))

    def test_product_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h3>test_description</h3>')

    def test_comment_form(self):
        data = {'text': 'text_for_form'}
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_list_comment(self):
        CommentFactory.create_batch(2, product=self.product)
        time = timezone.now() - timezone.timedelta(days=28)
        with unittest.mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = time
            CommentFactory.create(product=self.product)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['comments'].count(), 2)


class MainViewTest(TestCase):

    def setUp(self):
        self.category = CategoryFactory()
        self.user = UserFactory()
        self.url = reverse('main_page')

    def create_likes_of_the_week(self):
        product = ProductFactory()
        for day in range(1, 8):
            time_7 = timezone.now() - timezone.timedelta(days=day, hours=3)
            with unittest.mock.patch('django.utils.timezone.now') as mock_now:
                mock_now.return_value = time_7
                CommentFactory.create_batch(day+10, product=product)

    def create_product_for_popular_item(self):
        self.product_10_likes = ProductFactory(category=self.category)
        LikeFactory.create_batch(10, product=self.product_10_likes)
        self.product_15_likes = ProductFactory(category=self.category, static_out_top_list=True)
        LikeFactory.create_batch(15, product=self.product_15_likes)
        self.product_5_likes = ProductFactory(category=self.category)
        LikeFactory.create_batch(5, product=self.product_5_likes)
        self.product_3_likes = ProductFactory(category=self.category)
        LikeFactory.create_batch(3, product=self.product_3_likes)
        self.product_20_likes = ProductFactory(category=self.category)
        LikeFactory.create_batch(20, product=self.product_20_likes)
        self.product_30_likes = ProductFactory(category=self.category)
        LikeFactory.create_batch(30, product=self.product_30_likes)
        self.product_1_likes = ProductFactory(category=self.category)
        LikeFactory(product=self.product_3_likes)
        ProductFactory.create_batch(5, in_top_list=True)

    def create_product_for_choice_of_the_week(self):
        # base
        self.product_base_20_likes = ProductFactory(category=self.category, grade='B')
        LikeFactory.create_batch(20, product=self.product_base_20_likes)
        self.product_base_5_likes = ProductFactory(category=self.category, grade='B')
        LikeFactory.create_batch(5, product=self.product_base_5_likes)
        self.product_base_2_likes = ProductFactory(category=self.category, grade='B')
        LikeFactory.create_batch(1, product=self.product_base_2_likes)

        # standard
        self.product_standard_20_likes = ProductFactory(category=self.category, grade='S')
        LikeFactory.create_batch(20, product=self.product_standard_20_likes)
        self.product_standard_5_likes = ProductFactory(category=self.category, grade='S')
        LikeFactory.create_batch(5, product=self.product_standard_5_likes)
        self.product_standard_2_likes = ProductFactory(category=self.category, grade='S')
        LikeFactory.create_batch(2, product=self.product_standard_2_likes)

        # premium
        self.product_premium_1 = ProductFactory(category=self.category, grade='P')
        self.product_premium_2 = ProductFactory(category=self.category, grade='P')
        self.product_premium_3 = ProductFactory(category=self.category, grade='P')

    def test_maim_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_choice_week(self):
        self.create_product_for_choice_of_the_week()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        grade_list = {'base': 1, 'standard': 2, 'premium': 3}
        self.assertEqual(grade_list, response.context['choice_week'])

    def test_popular_items(self):
        self.create_product_for_popular_item()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(Product.objects.get(static_out_top_list=True), response.context['popular_products'])
        self.assertNotIn(self.product_1_likes, response.context['popular_products'])
        in_top = Product.objects.filter(in_top_list=True)
        for product in in_top:
            self.assertIn(product, response.context['popular_products'])
        self.assertIn(self.product_3_likes, response.context['popular_products'])
        self.assertNotIn(self.product_1_likes, response.context['popular_products'])


class CategoryListViewTest(TestCase):

    def setUp(self):
        self.url = reverse('category_list')

    def test_empty_list_category(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Empty')
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_categories_page(self):
        CategoryFactory.create_batch(2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['categories'], ['<Category: category0>', '<Category: category1>'],\
                                 ordered=False)


class LikeViewTest(TestCase):

    def setUp(self):
        self.product = ProductFactory(name='test_description')
        self.user = UserFactory()
        self.url = reverse('product_details', args=(self.product.category.slug, self.product.slug,))

    def test_create_like(self):
        like_count_before = Like.objects.filter(product=self.product).count()
        response = self.client.post(reverse('like', args=(self.product.category.slug, self.product.slug,)))
        self.assertEqual(response.status_code, 200)
        like_count_after = Like.objects.filter(product=self.product).count()
        self.assertEqual(like_count_before + 1, like_count_after)
