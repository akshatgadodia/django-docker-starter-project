from django.db import models
from users.models import User


# Base model for adding timestamp fields (created_at, updated_at) to other models
class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when an object is created
    updated_at = models.DateTimeField(auto_now=True)      # Automatically set whenever an object is updated

    class Meta:
        abstract = True


# Base model for adding created_by, updated_by field to other models
class CreatedByUpdatedBy(models.Model):

    # User who created the object
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated', null=True,
                                   blank=True)  # User who last updated the object

    class Meta:
        abstract = True


# Base model for implementing soft delete functionality
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)             # Flag indicating whether the object is deleted or not
    deleted_at = models.DateTimeField(null=True, blank=True)    # Timestamp when the object was deleted
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_deleted', null=True,
                                   blank=True)  # User who deleted the object

    class Meta:
        abstract = True
