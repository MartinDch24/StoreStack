from django.db import models


class StatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SINGLE_PRODUCT = 'single-product', 'Single Product'
    PAID = 'paid', 'Paid'
    SHIPPED = 'shipped', 'Shipped'
    OUT_FOR_DELIVERY = 'out_for_delivery', 'Out For Delivery'
    COMPLETED = 'completed', 'Completed'
    CANCELED = 'canceled', 'Canceled'
