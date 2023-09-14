

## Documentation

### `SoftDeletableModel`

#### Overview

`SoftDeletableModel` is an abstract base class that provides functionality for soft-deleting objects. Instead of removing records from the database, objects are marked as "deleted" by setting a `deleted_at` timestamp. This allows for potential restoration of objects and ensures data integrity.

#### Fields

- `deleted_at`: A `DateTimeField` that is set when an object is soft-deleted. If this field is `NULL`, the object is considered active.

#### Methods

- `soft_delete()`: Marks the object as deleted by setting the current timestamp to the `deleted_at` field.

- `restore()`: Restores a soft-deleted object by setting the `deleted_at` field to `NULL`.

#### Usage

To use `SoftDeletableModel`, simply inherit from it in your model:

```python
from utils.models import SoftDeletableModel

class YourModel(SoftDeletableModel):
    ...
```

---

### `TimestampedModel`

#### Overview

`TimestampedModel` is an abstract base class that provides automatic timestamping for objects. It includes fields to track when an object is created and when it's last updated.

#### Fields

- `created_at`: A `DateTimeField` that is set when an object is created. It's also indexed for faster query performance.

- `updated_at`: A `DateTimeField` that is updated every time an object is saved.

#### Usage

To use `TimestampedModel`, inherit from it in your model:

```python
from utils.models import TimestampedModel

class YourModel(TimestampedModel):
    ...
```

For models that also need soft delete functionality, use multiple inheritance:

```python
from utils.models import SoftDeletableModel, TimestampedModel

class YourModel(SoftDeletableModel, TimestampedModel):
    ...
```

---

### Best Practices

1. **Consistency**: Ensure that all models that require timestamping or soft delete functionality inherit from the appropriate base models.

2. **Avoid Hard Deletes**: When using `SoftDeletableModel`, avoid using the `delete()` method directly on objects or querysets. Instead, use the `soft_delete()` method to ensure data integrity.

3. **Database Queries**: When querying for active objects, use the custom manager method `active()` to filter out soft-deleted objects.

4. **Documentation Updates**: As the project evolves, ensure that any modifications or extensions to these base models are documented to keep the team informed.

---

This documentation provides a clear overview of the functionalities and usage of the `SoftDeletableModel` and `TimestampedModel`. It's essential to keep documentation updated and accessible to ensure consistent and correct usage across the project.