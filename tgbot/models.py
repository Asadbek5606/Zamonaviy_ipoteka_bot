from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    verify = models.CharField(max_length=20, null=True)
    verify_counter = models.IntegerField(default=0)
    lang_id = models.IntegerField(null=True)
    chat_id = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'user'
        managed = True
        verbose_name = 'Mijoz'
        verbose_name_plural = 'Mijozlar'


class Category(models.Model):
    name_uz = models.CharField(max_length=150)
    name_ru = models.CharField(max_length=150)
    parent = models.ForeignKey("Category", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name_uz}'

    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Product(models.Model):
    name_uz = models.CharField(max_length=150)
    name_ru = models.CharField(max_length=150)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    description_uz = models.TextField(null=False, blank=False)
    description_ru = models.TextField(null=False, blank=False)
    price = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.name_uz}'

    class Meta:
        db_table = 'product'
        managed = True
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'


class About(models.Model):
    text_uz = models.TextField()
    text_ru = models.TextField()

    def __str__(self):
        return f'{self.text_uz}'

    class Meta:
        db_table = 'about_us'
        managed = True
        verbose_name = 'Biz haqimizda'
        verbose_name_plural = 'Biz haqimizda'


class Comment(models.Model):
    user_id = models.IntegerField()
    comment_text = models.TextField()
    username = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.username}'

    class Meta:
        db_table = 'comment'
        managed = True
        verbose_name = 'Kommentariya'
        verbose_name_plural = 'Kommentariyalar'


class New(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    heading_uz = models.CharField(max_length=500)
    heading_ru = models.CharField(max_length=500)
    text_uz = models.TextField()
    text_ru = models.TextField()

    def __str__(self):
        return f'{self.heading_uz}'

    class Meta:
        managed = True
        verbose_name: "Yangiliklar"
        verbose_name_plural: "Yangiliklar"