from django.db import models
from django.conf import settings

class Source(models.Model):

    name = models.CharField(max_length=1024)

class Text(models.Model):

    class Meta:

        constraints = [
            # models.constraints.UniqueConstraint(
            #     fields=['contents', 'user'],
            #     name='unique_contents_per_user'
            # )
        ]

    contents = models.TextField()
    source = models.ForeignKey(Source,
                               on_delete=models.SET_NULL,
                               null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

class Word(models.Model):

    reading = models.CharField(max_length=1024)
    definition = models.ForeignKey(Text,
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    constraints = [
        models.constraints.UniqueConstraint(
            fields=['reading', 'definition', 'user'],
            name='unique_reading_and_definition_per_user'
           )
        ]

class WordRelation(models.Model):

    constraints = [
        models.constraints.UniqueConstraint(
            fields=['text', 'word'],
            name='unique_word_per_text'
           )
        ]

    text = models.ForeignKey(Text,
                             on_delete=models.CASCADE)
    word = models.ForeignKey(Word,
                             on_delete=models.CASCADE)
    begin = models.PositiveIntegerField()
    end = models.PositiveIntegerField()

