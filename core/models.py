from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Q
    # need to figure out what this is
from django.utils import timezone
from datetime import date


def get_hashtags(text):
    """
    Split a string by spaces, then strip off punctuation, returning only the words
    that start with a pound sign.
    """
    tags = set([
        item.strip("#.,-\"\'&*^!")
            # strip out punctuation (this is done last) 
        for item in text.split() 
            # splits text by spaces
        if item.startswith("#")
            # only return words that start with '#'
        ])
    return tags

# Create your models here.
# class User(AbstractUser):
#     pass

#### Review QuerySet ####
class TaskQuerySet(models.QuerySet):

    # def with_hashid(self, hashid):
    #     ids = hashids.decode(hashid)
    #     # TODO add check -- if len is 0, hashid is invalid, should raise exception
    #     if len(ids) == 1:
    #         return self.get(pk=ids[0])
    #     return self.filter(pk__in=ids)

    def incomplete(self):
        return self.filter(completed_at__isnull=True)

    def complete(self):
        return self.filter(completed_at__isnull=False).order_by('completed_at')

    def current(self):
        return self.incomplete().filter(
            Q(show_on__isnull=True) | Q(show_on__lte=date.today()))

    def future(self):
        return self.incomplete().filter(
            show_on__isnull=False, show_on__gt=date.today())
#### Review QuerySet ####

class Task(models.Model):

    class Meta:
        base_manager_name = 'objects'

    objects = TaskQuerySet.as_manager()
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

    # @property # don't treat this like a method, but treat like an attribute to avoid paranthesis to call it...the function definition can't take any arguments
    # def hashid(self):
    #     return hashids.encode(self.pk)
            # https://hashids.org/

    def is_complete(self):
        return self.completed_at is not None

    def is_current(self):
        return not self.is_complete and (self.show_on is None or self.show_on <= date.today())

    def is_future(self):
        return not self.is_complete() and (self.show_on is not None and self.show_on > date.today())

    def mark_complete(self, save=True):
        """
        Mark task as completed at current time.
        Saves completion to DB until 'save' is set to False.
        """
        self.completed_at = timezone.now()
        if save:
            self.save()
        return self

    def save(self, *args, **kwargs): 
        # when you override a built-in function and you don't know what argument it takes, you pass it along with the super() statement below
        super().save(*args, **kwargs)
            # Task object needs to be saved first before parse_tags() can be called due to M2M relationship
        self.parse_tags()

    def parse_tags(self):
        """
        Read through the description of the task and pull out any tags.
        Create Tag model objects for these and associate them.
        """
        tags = []
        text_tags = get_hashtags(self.description)
        for tag_text in text_tags:
            tag, _ = Tag.objects.get_or_create(text=tag_text)
                # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#get-or-create
            tags.append(tag)
        self.tags.set(tags)
            # https://docs.djangoproject.com/en/2.2/topics/db/examples/many_to_many/
            # relation sets can be set...'set(<a list>)'


class Note(models.Model):
    task = models.ForeignKey(to=Task, related_name='notes', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(null=True, auto_now_add=True)
        # updated_at = models.DateTimeField(null=True, auto_now=True)

class Tag(models.Model):
    """
    Represents a tag or hashtag -- a free-form category that we can add to tasks.

    - Tags should be case-insensitive
    """

    # This should be enforced to be unique in a case-insenstive fashion
    # but we are leaving it for now
    text = models.CharField(max_length=100, unique=True, help_text='Tag text (must be lowercase)')
    tasks = models.ManyToManyField(to=Task, related_name='tags')

    def __str__(self):
        """String for representing the Tag object."""
        return self.text


