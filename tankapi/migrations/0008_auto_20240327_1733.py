from django.db import migrations
import json


def load_data(apps, schema_editor):
    Tank = apps.get_model('tankapi', 'Tank')
    TankVolume = apps.get_model('tankapi', 'TankVolume')
    DailyTankSales = apps.get_model('tankapi', 'DailyTankSales')

    with open('tanks_data.json') as file:
        data = json.load(file)

        for item in data:
            if item['model'] == 'tankapi.tank':
                Tank.objects.create(pk=item['pk'], name=item['fields']['name'])
            elif item['model'] == 'tankapi.tankvolume':
                tank_id = item['fields']['tank_id']
                tank = Tank.objects.get(pk=tank_id)
                TankVolume.objects.create(
                    pk=item['pk'],
                    tank_id=tank,
                    volume=item['fields']['volume'],
                    created_at=item['fields']['created_at']
                )
            elif item['model'] == 'tankapi.dailytanksales':
                tank_id = item['fields']['tank_id']
                tank = Tank.objects.get(pk=tank_id)
                DailyTankSales.objects.create(
                    pk=item['pk'],
                    tank_id=tank,
                    date=item['fields']['date'],
                    sales=item['fields']['sales']
                )




class Migration(migrations.Migration):

    dependencies = [
        ('tankapi', '0007_remove_dailytanksales_volume_id'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
