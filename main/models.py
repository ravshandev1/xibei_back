from django.db import models


class Branch(models.Model):
    address = models.CharField(max_length=250, null=True, blank=True)
    address_uz = models.CharField(max_length=250, verbose_name="Manzil nomi", null=True, blank=True)
    address_cn = models.CharField(max_length=250, verbose_name="Адрес китайский", null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.address


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(verbose_name="Ism", max_length=100)
    username = models.CharField(verbose_name="Telegram username", max_length=100, null=True)
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID', unique=True, default=1)

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.full_name


class Rate(models.Model):
    user = models.CharField(max_length=250)
    comment = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.user


class Category(models.Model):
    title = models.CharField(verbose_name="Имя категория", max_length=150)
    title_uz = models.CharField(verbose_name="Kategoriya nomi", max_length=150)
    title_cn = models.CharField(verbose_name="Имя китайский", max_length=150)

    class Meta:
        db_table = "categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name="Kategoriya", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Имя субкатегория", max_length=150)
    title_uz = models.CharField(verbose_name="Subkategoriya nomi", max_length=150)
    title_cn = models.CharField(verbose_name="Имя китайский", max_length=150)

    class Meta:
        db_table = "subcategories"
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.title


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, verbose_name="Subkategoriya", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Имя продукт", max_length=150)
    title_uz = models.CharField(verbose_name="Maxsulot nomi", max_length=150)
    title_cn = models.CharField(verbose_name="Имя китайский", max_length=150)
    price = models.PositiveIntegerField(verbose_name="Narxi")
    structure = models.TextField(verbose_name="Tarkibi", null=True, blank=True)
    image = models.ImageField(verbose_name="Rasm", null=True, blank=True)

    class Meta:
        db_table = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(Users, verbose_name="Foydalanuvchi", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Mahsulot", on_delete=models.CASCADE)
    count = models.CharField(verbose_name="Maxsulot soni", max_length=10)
    price = models.PositiveIntegerField(verbose_name="Narxi", null=True, blank=True)

    class Meta:
        db_table = "cart"

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        self.price = self.product.price * int(self.count)
        return super(Cart, self).save(*args, **kwargs)


class Order(models.Model):
    class Meta:
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    STATUS_CHOICE = (
        ('new', 'new'),
        ('processing', 'processing'),
        ('finished', 'finished'),
        ('cancel', 'cancel')
    )
    user = models.ForeignKey(Users, verbose_name="Foydalanuvchi", on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICE, max_length=255, default='new')
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    name = models.CharField(max_length=150, verbose_name="Ismi")
    total = models.PositiveIntegerField(null=True, blank=True, verbose_name="Jami")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Vaqti")

    def __str__(self):
        return str(self.phone_number)


class OrderProduct(models.Model):
    class Meta:
        ordering = ('-id',)

    order = models.ForeignKey(Order, verbose_name="Buyurtma", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Maxsulot", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, verbose_name="Soni")

    def __str__(self):
        return self.product.title
