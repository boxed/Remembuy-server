from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)

    def as_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            createdAt=self.created_at.isoformat(),
            user=self.user.username,
            completed=self.completed,
            completedAt=self.completed_at.timestamp() if self.completed_at else None,
        )
