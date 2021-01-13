# Generated by Django 3.1 on 2020-11-24 12:42

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('starting_bid', models.DecimalField(decimal_places=3, max_digits=10)),
                ('image_url', models.CharField(max_length=100)),
                ('description', models.TextField(default='')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(default='')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commet_owner', to=settings.AUTH_USER_MODEL)),
                ('on_auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_on_auction', to='auctions.auction')),
            ],
        ),
        migrations.CreateModel(
            name='bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_value', models.IntegerField(default='')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_suggestion', to=settings.AUTH_USER_MODEL)),
                ('on_auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_on_auction', to='auctions.auction')),
            ],
        ),
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.category'),
        ),
        migrations.AddField(
            model_name='auction',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='activelisting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.ManyToManyField(blank=True, related_name='watchlist', to='auctions.auction')),
                ('watcher', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='listing', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
