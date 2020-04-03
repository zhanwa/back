# Generated by Django 2.2.1 on 2020-04-02 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapi', '0005_lottery'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votetheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_name', models.CharField(blank=True, max_length=255, null=True)),
                ('theme_id', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('vote_time', models.DateTimeField(auto_now_add=True)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapi.Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='Voteuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('answer', models.CharField(blank=True, max_length=32, null=True)),
                ('votetheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapi.Votetheme', to_field='theme_id')),
            ],
        ),
        migrations.CreateModel(
            name='Voteoption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(blank=True, max_length=255, null=True)),
                ('result', models.CharField(blank=True, max_length=32, null=True)),
                ('votetheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapi.Votetheme', to_field='theme_id')),
            ],
        ),
    ]
