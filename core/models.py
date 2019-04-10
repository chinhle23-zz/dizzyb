from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
# class User(AbstractUser):
#     pass

# class TaskQuerySet(models.QuerySet):
#     pass

class Task(models.Model):

    class Meta:
        base_manager_name = 'objects'

    # objects = TaskQuerySet.as_manager()
        # what is this?
    description = models.CharField('Task', max_length=512)
        # https://docs.djangoproject.com/en/2.2/ref/models/fields/#charfield
        # 'Task' is the verbose_name?
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    show_on = models.DateField('hide until', null=True, blank=True)
        # https://docs.djangoproject.com/en/2.2/ref/models/fields/#datefield
        # 'hide until' is the verbose_name?

    # @property
    # def hashid(self):
    #     return hashids.encode(self.pk)

    def is_complete(self):
        return self.completed_at is not None

    def is_current(self):
        return not self.is_complete and (self.show_on is None or self.show_on <= date.today())

    def is_future(self):
        return not self.is_complet() and (self.show_on is not None and self.show_on > date.today())

    def mark_complete(self, save=True):
        """
        Mark task as completed at current time.
        Saves completion to DB until 'save' is set to False.
        """
        self.completed_at = timezone.now()
        if save:
            self.save()
        return self

    # def save(self, *args, **kwargs): 
    #     super().save(*args, **kwargs)
    #     self.parse_tags()


class Note(models.Model):
    task = models.ForeignKey(to=Task, related_name='notes', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(null=True, auto_now_add=True)
        # updated_at = models.DateTimeField(null=True, auto_now=True)
