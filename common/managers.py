from django.db.models import Manager

from common.querysets import SoftDeletionQuerySet


class SoftDeletionManager(Manager.from_queryset(SoftDeletionQuerySet)):
    def __init__(self, *args, non_deleted_only=True, **kwargs):
        """
        Custom manager for soft deletion.

        Args:
            non_deleted_only (bool): If True, the manager will filter out deleted objects by default.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.non_deleted_only = non_deleted_only
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """
        Returns the queryset with optional non-deleted filtering.

        Returns:
            SoftDeletionQuerySet: The queryset, potentially filtered for non-deleted objects.
        """
        queryset = super().get_queryset()

        # Ensure a default ordering for predictable results
        if not queryset.query.order_by:
            queryset = queryset.order_by('id')

        # Optionally filter for non-deleted objects
        if self.non_deleted_only:
            return queryset.non_deleted()

        return queryset

    def hard_delete(self):
        """
        Performs a hard delete on the queryset.

        Returns:
            int: The number of objects deleted.
        """
        return self.get_queryset().hard_delete()
