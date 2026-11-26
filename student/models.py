from django.db import models

# Create your models here.
from api.models import User,Problem
# Create your models here.


class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

   
    college = models.CharField(
        max_length=150,
        blank=True
    )

    qualification = models.CharField(
        max_length=100,
        blank=True
    )

    github_url = models.URLField(
        blank=True
    )

    linkedin_url = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


from django.db.models.signals import post_save


def create_student_profile(sender,instance,created,**kwargs):

    if created and not instance.is_superuser:

        StudentProfile.objects.create(user=instance)


post_save.connect(create_student_profile,User)



class Submission(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("evaluated", "Evaluated"),
        ("failed", "Evaluation Failed"),
    ]

    answer = models.TextField()

    submitted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions"
    )



    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    score = models.PositiveIntegerField(
        default=0
    )

    remarks = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )



    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["submitted_by", "problem"],
                name="unique_student_problem_submission"
            )
        ]

    def __str__(self):
        return f"{self.submitted_by.username} - {self.problem.title}"