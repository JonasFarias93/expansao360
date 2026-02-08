from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cadastro", "0009_loja_loja_hist_idx_loja_loja_uf_idx"),
    ]

    operations = [
        migrations.CreateModel(
            name="CodeSequence",
            fields=[
                ("prefix", models.CharField(max_length=8, primary_key=True, serialize=False)),
                ("last_value", models.PositiveIntegerField(default=0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
