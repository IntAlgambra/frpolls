# Generated by Django 2.2.10 on 2021-04-18 09:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(null=True)),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='PollsUser',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('question_type', models.IntegerField()),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='polls.Poll')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='polls.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='polls.PollsUser')),
            ],
        ),
    ]