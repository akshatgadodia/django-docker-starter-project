from django.db.models import Manager

from common.db.querysets import BaseQueryset


class SoftDeletionManager(Manager.from_queryset(BaseQueryset)):
    """
    Custom manager class for models with soft deletion support.
    This manager extends the default Django Manager by using a custom queryset (BaseQueryset) that includes
    support for soft deletion. Soft deletion involves marking objects as deleted instead of physically removing
    them from the database.
    """

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


class BaseManager(SoftDeletionManager):
    """
    Base manager class for models with soft deletion support.
    This class inherits from SoftDeletionManager, providing common functionality for managing models
    with soft deletion, which involves marking objects as deleted instead of physically removing them
    from the database.
    """
    pass


class ActiveManager(BaseManager):
    def get_active(self):
        return super().get_queryset().filter(active=True)
