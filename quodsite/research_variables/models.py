from django.db import models


# Data storage models

class Variable(models.Model):
    # Contains the information about the variables
    version = models.PositiveIntegerField()
    category = models.PositiveIntegerField()
    section = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()


class Session(models.Model):
    user = models.CharField(max_length=45)
    session = models.PositiveIntegerField()
    version = models.CharField(max_length=45)
    timestamp = models.CharField(max_length=45)
    variables = models.ManyToManyField(Variable)
    name = models.CharField(max_length=45)
    saves = models.PositiveIntegerField()
    archived = models.BooleanField()


# Dynamic page models
class DictionaryStructure(models.Model):
    # Stores the rendering structure of variable dictionary
    DictionaryCategory = models.CharField(max_length=45)
    DictionarySection = models.CharField(max_length=45)
    DictionaryVersion = models.CharField(max_length=45)


class Category(models.Model):
    name = models.CharField(max_length=255)


class Section(models.Model):
    level = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
