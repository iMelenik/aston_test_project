# Generated by Django 4.1.7 on 2023-02-27 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('commission', models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=15, null=True)),
                ('status', models.CharField(choices=[('P', 'PAID'), ('F', 'FAILED')], default='FAILED', max_length=6)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trans_receiver', to='wallets.wallet')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trans_sender', to='wallets.wallet')),
            ],
        ),
    ]
