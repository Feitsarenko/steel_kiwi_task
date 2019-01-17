from django.core.management.base import BaseCommand, CommandError
from products.models import Product
from django.db.models import Count, Q
import csv
from sys import stdout


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-l',
            '--like',
            action='store_true',
            default=False,
            help="don't add products without likes"
        )
        parser.add_argument(
            '-c',
            '--comment',
            action='store_true',
            default=False,
            help="don't add products without comment"
        )

    def handle(self, *args, **options):
        if options['like'] and options['comment']:
            qs = Product.objects.exclude(Q(like__isnull=True) | Q(comment__isnull=True)). \
                annotate(likes=Count('like'), comments=Count('comment'))
        elif options['comment']:
            qs = Product.objects.exclude(comment__isnull=True).\
                annotate(likes=Count('like'), comments=Count('comment'))
        elif options['like']:
            qs = Product.objects.exclude(like__isnull=True).annotate(likes=Count('like'), comments=Count('comment'))
        else:
            qs = Product.objects.annotate(likes=Count('like'), comments=Count('comment'))
        writer = csv.writer(stdout, quoting=csv.QUOTE_ALL)
        writer.writerow(['Title', 'ID',  'Number of Likes', 'Number of Comments'])
        for product in qs:
            row = [product.name, product.id, product.likes, product.comments]
            writer.writerow(row)

