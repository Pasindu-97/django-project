# Generated by Django 4.2.5 on 2023-09-18 07:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.models.collections


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('taggit', '0005_auto_20220424_2025'),
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='item', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='item',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='item', to='wagtailimages.image', verbose_name='Images'),
        ),
        migrations.AddField(
            model_name='customrendition',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renditions', to='customers.customimage'),
        ),
        migrations.AddField(
            model_name='customimage',
            name='collection',
            field=models.ForeignKey(default=wagtail.models.collections.get_root_collection_id, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.collection', verbose_name='collection'),
        ),
        migrations.AddField(
            model_name='customimage',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags'),
        ),
        migrations.AddField(
            model_name='customimage',
            name='uploaded_by_user',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user'),
        ),
        migrations.AddField(
            model_name='customerorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order', to='customers.customer', verbose_name='Customer'),
        ),
        migrations.AddField(
            model_name='category',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='category', to='auth.group', verbose_name='Group'),
        ),
        migrations.AlterUniqueTogether(
            name='customrendition',
            unique_together={('image', 'filter_spec', 'focal_point_key')},
        ),
    ]