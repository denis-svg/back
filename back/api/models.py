from django.db import models


from django.db import models


class AvgEvents(models.Model):
    event = models.OneToOneField('Events', models.DO_NOTHING, primary_key=True)
    hour = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'avgEvents'


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    person = models.ForeignKey('Persons', models.DO_NOTHING)
    event_name = models.TextField()
    clicked_date = models.TextField()
    url = models.TextField(db_column='urL') 

    class Meta:
        managed = False
        db_table = 'events'


class Persons(models.Model):
    person_id = models.IntegerField(primary_key=True)
    master_id = models.IntegerField(null=True)
    locale = models.TextField()
    device = models.TextField()

    class Meta:
        managed = False
        db_table = 'persons'


class PersonsMetric(models.Model):
    person = models.OneToOneField(Persons, models.DO_NOTHING, primary_key=True)
    clicksToConvert = models.IntegerField(db_column='clicksToConvert', null=True)  
    clicksToShare = models.IntegerField(db_column='clicksToShare', null=True)  
    timeToConvert = models.IntegerField(db_column='timeToConvert', null=True)  
    timeToShare = models.IntegerField(db_column='timeToShare', null=True)  

    class Meta:
        managed = False
        db_table = 'persons_metric'


class UrlsMetric(models.Model):
    url = models.TextField()
    unique_clicks = models.IntegerField()
    total_clicks = models.IntegerField()
    timeonpage = models.IntegerField(db_column='timeOnPage', null=True) 
    timeonpage_filtered = models.IntegerField(db_column='timeOnPage_filtered', null=True) 
    pageBeforeConversion = models.IntegerField(db_column='pageBeforeConversion', null=True) 
    pageBeforeShare = models.IntegerField(db_column='pageBeforeShare', null=True) 
    device = models.TextField(null=True)
    locale = models.TextField(null=True)
    ratio_clicks = models.DecimalField(db_column='ratio_clicks', max_digits=100, decimal_places=10)
    ratio_time = models.DecimalField(db_column='ratio_time', max_digits=100, decimal_places=10)
    class Meta:
        managed = False
        db_table = 'urls_metric'

