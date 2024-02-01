from datetime import datetime
from django.db.models import QuerySet
from django.db.models.deletion import Collector

from common.utils import manage_delete_dependency


class SoftDeletionQuerySet(QuerySet):
    """
    Custom Queryset to handle Soft Delete
    """
    def delete(self, user=None):
        """
        Soft deletes objects in the queryset and manages dependencies.
        Args:
            user: The user initiating the deletion (optional).
        Returns:
            int: The number of objects updated (soft deleted).
        """
        # Create a query for deletion
        del_query = self._chain()
        del_query._for_write = True

        # Disable non-supported fields for deletion
        del_query.query.select_for_update = False
        del_query.query.select_related = False
        del_query.query.clear_ordering()

        # Use a collector to gather related objects for deletion
        collector = Collector(using='default')
        collector.collect(del_query)

        # Manage dependencies and mark objects for deletion
        manage_delete_dependency(collector, user)

        # Set 'deleted_at' attribute to mark soft deletion
        update = {'deleted_at': datetime.utcnow()}
        return super(SoftDeletionQuerySet, self).update(**update)

    def hard_delete(self):
        """
        Hard deletes (permanently removes) objects in the queryset.
        Returns:
            int: The number of objects deleted.
        """
        return super(SoftDeletionQuerySet, self).delete()

    def non_deleted(self):
        """
        Returns a queryset containing non-deleted objects.
        Returns:
            SoftDeletionQuerySet: A queryset of non-deleted objects.
        """
        return self.filter(deleted_at=None)

    def deleted(self):
        """
        Returns a queryset containing deleted objects.
        Returns:
            SoftDeletionQuerySet: A queryset of deleted objects.
        """
        return self.exclude(deleted_at=None)


class BaseQueryset(SoftDeletionQuerySet):
    """
    Custom Queryset which inherits SoftDeletionQuerySet which helps in providing
    the common functionality
    """
    pass
