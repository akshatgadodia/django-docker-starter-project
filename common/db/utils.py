from datetime import datetime
from django.db import transaction

from common.logging import LogInfo


def set_delete_attributes(obj, user):
    """
    Helper function to set delete attributes for an object.
    Args:
        obj: The object to be marked as deleted.
        user: The user initiating the deletion.
    Returns:
        None
    """
    obj.is_deleted = True
    obj.deleted_at = datetime.utcnow()
    obj.deleted_by = user
    obj.save()


def manage_delete_dependency(collector, user=None):
    """
    Main function to manage the deletion of objects and their dependencies.
    Args:
        collector: An object collector containing fast_deletes and data.
        user: The user initiating the deletion (optional).
    Note:
        The collector parameter is assumed to have the following structure:
        - collector.fast_deletes: A list of sets, each containing objects for fast deletion.
        - collector.data: A dictionary where keys are model classes and values are lists of objects to be deleted.
    """
    try:
        with transaction.atomic():
            # Fast deletes: Efficiently mark objects for deletion
            # Fast deletes are usually used for cases where you can bypass certain Django signals and optimizations,
            # making the deletion process faster.
            for fast_deletes_set in collector.fast_deletes:
                if len(fast_deletes_set):
                    for delete_obj in fast_deletes_set:
                        set_delete_attributes(delete_obj, user)

            # Standard deletes: Mark objects for deletion that couldn't be handled with fast deletes
            for model, data_objects in collector.data.items():
                for obj in data_objects:
                    set_delete_attributes(obj, user)
    except Exception as e:
        LogInfo.exception(e)
