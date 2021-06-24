from django.db import models
from django.utils import timezone

class Examples(models.Model):

    is_deleted = models.BooleanField(default=False)
    priority_user = models.ForeignKey("PriorityUser", on_delete=models.CASCADE)
    affirmation = models.CharField(max_length=200)
    created_on = models.DateTimeField(default=timezone.now)
    ended_on = models.DateTimeField(null=True)
    goal_date = models.DateField()
    how = models.IntegerField()

    creator = models.ForeignKey("PriorityUser", related_name="creator", on_delete=models.CASCADE)
    subscriber = models.ForeignKey("PriorityUser", related_name="subscriber", on_delete=models.CASCADE)

    parts = models.ManyToManyField("Part", through="CompanyPart", related_name="companies")
    vendor = models.ManyToManyField("Vendor", related_name="companies")


    @property
    def is_author(self):
        return self.__is_author

    @is_author.setter
    def is_author(self, value):
        self.__is_author = value