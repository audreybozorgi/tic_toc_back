# Generated by Django 3.2.8 on 2022-02-15 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_alter_game_nextplayer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='nextPlayer',
            field=models.CharField(choices=[(0, 'PLAYER_X'), (1, 'PLAYER_O')], default='PLAYER_X', max_length=20),
        ),
    ]
