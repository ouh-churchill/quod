from django.db import models


# Data storage models

class NewVariable(models.Model):
    # Contains the information about the variables
    version = models.PositiveIntegerField()
    category = models.PositiveIntegerField()
    section = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()


class NewSession(models.Model):
    user = models.CharField(max_length=45)
    session = models.PositiveIntegerField()
    version = models.CharField(max_length=45)
    timestamp = models.CharField(max_length=45)
    variables = models.ManyToManyField(NewVariable)
    name = models.CharField(max_length=45)
    saves = models.PositiveIntegerField()
    archived = models.BooleanField()


# Dynamic page models
class DictionaryStructure(models.Model):
    # Stores the rendering structure of variable dictionary
    DictionaryCategory = models.CharField(max_length=45)
    DictionarySection = models.CharField(max_length=45)
    DictionaryVersion = models.CharField(max_length=45)


class NewCategory(models.Model):
    name = models.CharField(max_length=255)


class NewSection(models.Model):
    level = models.PositiveIntegerField()
    category = models.ForeignKey(NewCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
